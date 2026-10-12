"""Consult one job's oracle on a probe set, with that job's own [oracle] and [prompts] configuration.

The oracle client, retry and abort policy are the pipeline's own (`_build_oracle_manager`, `_run_consultations`),
so a probe call is made exactly like an M_ask call of the same job: same endpoint, model, decoding settings,
developer prompt, response mode and answer parsing. Only the two entity lines differ: they come pre-rendered
(masked) from the probe set, in the layout of `one_level_of_parents_and_synonyms`.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd

import logmap_llm.oracle.consultation as oc
import logmap_llm.oracle.prompts.developer as dp
from logmap_llm.constants import PAIRS_SEPARATOR
from logmap_llm.oracle.prompts.context import PromptContext

from .inputs import Job

SUPPORTED_USER_TEMPLATE = "one_level_of_parents_and_synonyms"
COLUMNS = ["Source", "Target", "Prediction", "Confidence", "InputTokens", "OutputTokens"]


def check_job(job: Job) -> None:
    p, fs = job.cfg.prompts, job.cfg.few_shot
    if p.cls_usr_prompt_template_name != SUPPORTED_USER_TEMPLATE:
        raise ValueError(f"{job.config_path.name}: user template {p.cls_usr_prompt_template_name!r} is not supported; "
                         f"the masked probe renderer reproduces only {SUPPORTED_USER_TEMPLATE!r} "
                         "(mutual-subsumption / other templates need their own renderer)")
    if fs.few_shot_k:
        raise ValueError(f"{job.config_path.name}: few_shot_k={fs.few_shot_k}; probes are zero-shot only")


def build_prompts(job: Job, labels: pd.DataFrame) -> dict[str, str]:
    ctx = PromptContext.from_config(job.cfg)
    tail = f"\nDo they mean the same thing? {ctx.response_instruction}"
    return {f"{r.src}{PAIRS_SEPARATOR}{r.tgt}": "\n".join([ctx.domain_preamble, r.entity_lines, tail])
            for r in labels.itertuples()}


def developer_prompt(job: Job) -> str:
    c = job.cfg
    return dp.get_developer_prompt(name=c.prompts.cls_dev_prompt_template_name, answer_format=c.oracle.answer_format,
                                   response_mode=c.oracle.response_mode)


def _load_done(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=COLUMNS)
    old = pd.read_csv(path)
    return old[old.Prediction.astype(str).isin(["True", "False"])]


def consult(job: Job, probe_set: Path, out_csv: Path, *, limit: int | None = None, dry_run: bool = False,
            max_workers: int | None = None) -> pd.DataFrame | None:
    check_job(job)
    labels = pd.read_csv(probe_set, sep="\t")
    if limit:
        labels = pd.concat([labels[labels.label == 1].head(limit // 2),
                            labels[labels.label == 0].head(limit - limit // 2)])
    prompts = build_prompts(job, labels)
    dev = developer_prompt(job)
    if dry_run:
        print(f"--- {job.label}: developer prompt ({job.cfg.prompts.cls_dev_prompt_template_name}) ---\n{dev}")
        for (k, v), r in list(zip(prompts.items(), labels.itertuples()))[:2]:
            print(f"--- user prompt [label={r.label} kind={r.kind}] ---\n{v}")
        print(f"dry run: {len(prompts)} prompts built, no calls made")
        return None

    done = _load_done(out_csv)
    done_keys = {f"{s}{PAIRS_SEPARATOR}{t}" for s, t in zip(done.Source, done.Target)}
    todo = {k: v for k, v in prompts.items() if k not in done_keys}
    print(f"{job.label} on {probe_set.name}: {len(done_keys)} cached, {len(todo)} to ask "
          f"({job.cfg.oracle.interaction_style} @ {job.cfg.oracle.base_url})")
    rows = []
    if todo:
        mgr = oc._build_oracle_manager(job.cfg.oracle, dev, None)
        mgr.freeze_messages()
        results = oc._run_consultations(
            llm_oracle=mgr, m_ask_prompts=todo, pair_entity_types={}, developer_prompt_map=None,
            max_workers=max_workers or job.cfg.oracle.max_workers,
            failure_tolerance=oc._resolve_failure_tolerance(job.cfg.oracle, len(todo)),
            desc=f"{job.label} probe")
        if results is None:
            raise SystemExit(f"{job.label}: consultation aborted by the failure policy (check the endpoint)")
        for key, (pred, conf, usage) in results.items():
            s, t = key.split(PAIRS_SEPARATOR)[:2]
            rows.append((s, t, pred, conf, getattr(usage, "input_tokens", None), getattr(usage, "output_tokens", None)))
    new = pd.DataFrame(rows, columns=COLUMNS)
    df = pd.concat([done, new], ignore_index=True) if len(done) else new
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    meta = {"job_config": str(job.config_path), "model_name": job.label, "probe_set": str(probe_set),
            "interaction_style": str(job.cfg.oracle.interaction_style), "base_url": job.cfg.oracle.base_url,
            "dev_template": job.cfg.prompts.cls_dev_prompt_template_name,
            "user_template": job.cfg.prompts.cls_usr_prompt_template_name,
            "response_mode": str(job.cfg.oracle.response_mode), "n_pairs": int(len(df)),
            "n_failed": int((~df.Prediction.astype(str).isin(["True", "False"])).sum()),
            "updated": time.strftime("%Y-%m-%dT%H:%M:%S")}
    out_csv.with_suffix(".json").write_text(json.dumps(meta, indent=2))
    print(f"  -> {out_csv}  ({meta['n_failed']} failed)")
    return df

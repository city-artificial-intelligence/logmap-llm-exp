"""Experiment file (probe.toml) and everything it points at.

probe.toml lists, per task, the existing LogMapLLM job configs whose oracles are compared. Everything else is read
from those configs: ontologies, reference alignment, oracle endpoint and settings, prompt templates, and the job's
own M_ask prediction file (the "real" side of the comparison).

    output_root = "runs"                      # relative to this file

    [path_map]                                # optional: rewrite path prefixes found in the job configs
    "/home/jon/data" = "/data/oaei"

    [tasks.anatomy]
    probe_sets = ["pairs/anatomy/v4-100.tsv", "pairs/anatomy/v5-g-150.tsv"]
    logmap_dir = ""                           # optional: folder with <task>-logmap_anchors.tsv etc.
                                              #   (default: logmap-initial-alignment dir of the first job)
    [[tasks.anatomy.jobs]]
    config = "jobs/anatomy/anatomy-qwen3-8b-zero-shot-current-r0-89d6c28b.toml"
    run_root = ""                             # optional: set when the batch harness rooted outputs elsewhere
"""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
from pydantic import ValidationError

from logmap_llm.config.schema import LogMapLLMConfig, validate_config
from logmap_llm.evaluation.io import load_mapping_pairs, load_oracle_predictions
from logmap_llm.pipeline.paths import PipelinePaths

LOGMAP_FILES = {
    "anchors": ("logmap_anchors.tsv", "\t"),
    "hard_discarded": ("logmap_hard_discarded_mappings.txt", "|"),
    "m_ask": ("logmap_mappings_to_ask_oracle_user_llm.txt", "|"),
}


@dataclass
class Job:
    config_path: Path
    cfg: LogMapLLMConfig
    paths: PipelinePaths

    @property
    def label(self) -> str:
        return self.cfg.oracle.model_name

    @property
    def slug(self) -> str:
        return self.label.replace("/", "__")


@dataclass
class Task:
    name: str
    jobs: list[Job]
    probe_sets: list[Path]
    logmap_dir: Path
    output_root: Path
    extra: dict = field(default_factory=dict)

    @property
    def cfg(self) -> LogMapLLMConfig:
        """Any job's config: ontologies, reference and task name are shared by all jobs of a task."""
        return self.jobs[0].cfg

    def out_dir(self, probe_set: Path) -> Path:
        return self.output_root / self.name / probe_set.stem


def _rewrite(value, path_map: dict[str, str]):
    if isinstance(value, str):
        for old, new in path_map.items():
            if value.startswith(old):
                return new + value[len(old):]
        return value
    if isinstance(value, dict):
        return {k: _rewrite(v, path_map) for k, v in value.items()}
    if isinstance(value, list):
        return [_rewrite(v, path_map) for v in value]
    return value


def _validate(raw: dict, config_path: Path) -> LogMapLLMConfig:
    """Validate a job config. Probes are zero-shot, so when a zero-shot job's [few_shot] section is rejected by this
    checkout's schema (e.g. a RAG encoder kind added in a newer local version), that section is reset to defaults
    instead of failing: none of its fields are used here. Any other validation error is raised unchanged."""
    try:
        return validate_config(raw)
    except ValidationError as e:
        bad = {err["loc"][0] for err in e.errors()}
        k = raw.get("few_shot", {}).get("few_shot_k", 0)
        if bad != {"few_shot"} or k:
            raise
        print(f"  note: {config_path.name}: [few_shot] not valid for this checkout's schema "
              f"({'; '.join(err['msg'] for err in e.errors())}); reset to defaults (few_shot_k=0, unused by probes)")
        return validate_config({**raw, "few_shot": {"few_shot_k": 0}})


def load_job(config_path: Path, path_map: dict[str, str], run_root: str | None = None) -> Job:
    with open(config_path, "rb") as fp:
        raw = tomllib.load(fp)
    cfg = _validate(_rewrite(raw, path_map), config_path)
    paths = PipelinePaths.from_config(cfg, run_root=_rewrite(run_root, path_map) if run_root else None)
    return Job(config_path=config_path, cfg=cfg, paths=paths)


def load_experiment(path: str | Path, only_tasks: list[str] | None = None) -> list[Task]:
    path = Path(path).resolve()
    base = path.parent
    with open(path, "rb") as fp:
        spec = tomllib.load(fp)
    path_map = spec.get("path_map", {})
    output_root = (base / spec.get("output_root", "runs")).resolve()
    tasks = []
    for name, t in spec["tasks"].items():
        if only_tasks and name not in only_tasks:
            continue
        jobs = [load_job((base / j["config"]).resolve(), path_map, j.get("run_root") or None) for j in t["jobs"]]
        names = {j.cfg.alignmentTask.task_name for j in jobs}
        if len(names) != 1:
            raise ValueError(f"[{name}] jobs belong to different LogMapLLM tasks: {sorted(names)}")
        logmap_dir = Path(_rewrite(t["logmap_dir"], path_map)) if t.get("logmap_dir") else Path(jobs[0].paths.initial_dir)
        tasks.append(Task(name=name, jobs=jobs, probe_sets=[(base / p).resolve() for p in t.get("probe_sets", [])],
                          logmap_dir=logmap_dir, output_root=output_root,
                          extra={k: v for k, v in t.items() if k not in {"jobs", "probe_sets", "logmap_dir"}}))
    return tasks


def read_pairs(path: Path, sep: str) -> list[tuple[str, str]]:
    """First two columns, order kept, duplicates dropped (same as the chapter scripts)."""
    df = pd.read_csv(path, sep=sep, header=None, usecols=[0, 1], dtype=str).dropna()
    return list(dict.fromkeys(zip(df[0], df[1])))


def logmap_file(task: Task, kind: str) -> Path:
    suffix, _ = LOGMAP_FILES[kind]
    exact = task.logmap_dir / f"{task.cfg.alignmentTask.task_name}-{suffix}"
    if exact.exists():
        return exact
    found = sorted(task.logmap_dir.glob(f"*-{suffix}"))
    if len(found) != 1:
        raise FileNotFoundError(f"[{task.name}] expected one *-{suffix} in {task.logmap_dir}, found {len(found)}")
    return found[0]


def logmap_pairs(task: Task, kind: str) -> list[tuple[str, str]]:
    return read_pairs(logmap_file(task, kind), LOGMAP_FILES[kind][1])


def reference(task: Task) -> set[frozenset]:
    path = task.extra.get("reference") or task.cfg.evaluation.reference_alignment_path
    return {frozenset(p) for p in load_mapping_pairs(Path(path))}


def m_ask_predictions(job: Job) -> pd.DataFrame:
    """The job's own verdicts on M_ask: columns src, tgt, pred (True/False/None = failed)."""
    rows = load_oracle_predictions(job.paths.predictions_csv())
    return pd.DataFrame([(r["source"], r["target"], r["prediction"]) for r in rows], columns=["src", "tgt", "pred"])

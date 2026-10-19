# Anchor probe: running it

This experiment asks each oracle about a small set of pairs whose labels come from LogMap itself, and checks
whether that ranks the oracles the way their real M_ask results do. It reuses the existing
`k0/zero-shot-current` jobs for anatomy and omim-ordo: same configs, same vLLM endpoints, same prompts. It needs no
new LogMap runs.

Everything is in `src/logmap_llm/anchor_probe/` (new module, no existing file changed) and in this folder.

## What is in this folder

| Path | What it is |
|---|---|
| `probe.toml` | the experiment: per task, the probe sets and the job configs to compare |
| `jobs/<task>/*.toml` | the 16 archived zero-shot-current job configs, copied verbatim (8 models × 2 tasks) |
| `pairs/<task>/v4-100.tsv`, `v4-200.tsv` | the v4 probe sets already evaluated (50+50 and 88+112 / 100+100 pairs) |
| `pairs/<task>/v5-g-150.tsv` | **new** v5 set: 50 masked anchors + 100 granularity negatives |
| `pairs/<task>/v5-mix-150.tsv` | **new** v5 set: 50 masked anchors + 50 granularity + 50 v4-style negatives |
| `reference-results/` | earlier v4 runs made over OpenRouter (for comparison only, not read by the code) |
| `runs/` | created by `consult`: one CSV per model per probe set; please commit it back |
| `run_local.sh`, `run_openrouter.sh` | run every local (vLLM) or OpenRouter model on every probe set, both tasks |
| `plot_results.py` | figures from `runs/` into `runs/figures/` |

## Setup

Use the same Python environment as the LogMapLLM runs. The module needs nothing beyond what the pipeline already
imports: pandas, numpy, pydantic, rdflib and owlready2. Run from the repo root with `src` on the path:

```
export PYTHONPATH=src
```

If your local checkout is ahead of this branch, which is likely because the archived configs use
`rag_encoder_kind = "sapbert"` and this branch's schema does not accept it, rebase this branch onto your version.
The module only adds files, so the rebase has no conflicts. It relies on these existing functions:
`config.schema.validate_config`, `pipeline.paths.PipelinePaths.from_config`,
`oracle.consultation._build_oracle_manager`, `_run_consultations` and `_resolve_failure_tolerance`,
`oracle.prompts.context.PromptContext.from_config`, `oracle.prompts.developer.get_developer_prompt`,
`evaluation.io.load_mapping_pairs`, `load_oracle_predictions` and `ontology.access.load_ontologies`.

## Short version

One command per step: `experiments/anchor-probe/run_all.sh` runs the local vLLM models that are up (serve one on the port
of its job config, run, swap, rerun; it resumes), then `run_all.sh openrouter` runs the OpenRouter models (needs
`OPENROUTER_API_KEY`; deepseek and mistral are already in `runs/`, so only gemini-2.5-flash is asked). Each ends with
`report` and the plots. `runs/` already holds deepseek-v4-flash and mistral-small-3.2 on both tasks; commit `runs/` back
when done.

```
python -m logmap_llm.anchor_probe check experiments/anchor-probe/probe.toml   # every job: M_ask predictions ok
experiments/anchor-probe/run_local.sh            # every local model whose vLLM server is up; others are skipped
experiments/anchor-probe/run_openrouter.sh       # the 3 OpenRouter models; needs OPENROUTER_API_KEY
python -m logmap_llm.anchor_probe report experiments/anchor-probe/probe.toml
python -m logmap_llm.anchor_probe budget experiments/anchor-probe/probe.toml
python experiments/anchor-probe/plot_results.py
```

Both run scripts read the models and endpoints from `probe.toml` (after `[path_map]`), take model names as
arguments to run only those, and are resumable. `PROBE_SETS="v5-g-150 v5-mix-150"` restricts the probe sets (the
default is all four) and `LIMIT=6` makes a smoke test. For local models, serve one model on the port of its job
config, run `run_local.sh <model>`, then swap. `plot_results.py` writes `probe_accuracy.png` from the probe answers
alone, `probe_vs_real.png`, `regret.png` and `summary.csv` once `report` has run, and `budget.png` once `budget`
has. The steps below are the same thing one command at a time.

## Steps

**1. Check that every path resolves.** This makes no calls.

```
python -m logmap_llm.anchor_probe check experiments/anchor-probe/probe.toml
```

Each job should show `M_ask predictions ok`, which is the job's own
`*-mappings_to_ask_with_oracle_predictions.csv`. If a batch was run with `--run-root`, add `run_root = "..."` to that
job in `probe.toml`. If files have moved since July, add a prefix rewrite under `[path_map]`. The rewrite also
applies to `base_url`, so a model now served on a different port is one line, for example
`"http://127.0.0.1:18001/v1" = "http://127.0.0.1:8000/v1"`.

**2. Look at the prompts.** This makes no calls.

```
python -m logmap_llm.anchor_probe consult experiments/anchor-probe/probe.toml --task anatomy --model Qwen3-8B --dry-run
```

**3. Serve one model and run it** on the same port as in its job config, exactly as for the batches:

| Model | Port in the configs |
|---|---|
| Qwen3-8B | 18001 |
| Gemma-3-27B | 18004 |
| Llama-3.1-70B-Instruct | 18010 |
| Qwen3.5-122B-A10B | 18011 |
| Qwen3-235B-A22B-Instruct-2507 | 18012 |

```
python -m logmap_llm.anchor_probe consult experiments/anchor-probe/probe.toml --model Qwen3-8B --limit 6   # smoke test
python -m logmap_llm.anchor_probe consult experiments/anchor-probe/probe.toml --model Qwen3-8B             # both tasks, all sets
```

Runs are resumable. Answered pairs are skipped and failed ones are retried on the next run. Each result CSV has a
JSON file next to it recording the endpoint, templates and failure count.

**Priority, if time is short:**

| Priority | What | Calls |
|---|---|---|
| 1 | the 5 local models on `v5-g-150` and `v5-mix-150`, both tasks | 3,000 |
| 2 | Gemma-3-27B and Llama-3.1-70B on `v4-100` and `v4-200`, so v4 and v5 compare on the same panel | 1,200 |
| 3 | the 3 OpenRouter models (DeepSeek, Gemini, Mistral) on the v5 sets; needs `OPENROUTER_API_KEY` | 1,800 |
| 4 | Qwen models on the v4 sets locally (the earlier v4 calls went through OpenRouter, the archive served them locally) | 1,800 |

Restrict with `--probe-set v5-g-150` and similar, and `--task`.

**4. Report.** This makes no calls and can be run at any point.

```
python -m logmap_llm.anchor_probe report experiments/anchor-probe/probe.toml
python -m logmap_llm.anchor_probe negtypes experiments/anchor-probe/probe.toml
python -m logmap_llm.anchor_probe budget experiments/anchor-probe/probe.toml
```

`report` writes `runs/<task>/<probe set>/report.md`. It shows per-model real J on M_ask against probe J, the rank
agreement, the regret of the probe's pick, and references: random pick, 30 or 50 labelled M_ask pairs, Dawid–Skene
and the noise ceiling. `negtypes` types M_ask's false candidates by hierarchy relation to the true match and does
the same for each probe set's negatives. `budget` scores each way of picking the oracle at the same cost, n pairs
answered by every model: n pairs of each probe set (stratified by kind), n unlabelled M_ask pairs ranked by
Dawid–Skene, and n labelled M_ask pairs, for n = 50, 100, ... up to the full size, averaged over 1000 random
subsets. It writes `runs/<task>/budget.csv` (about 1–2 minutes per task).
Both also write `runs/<task>/m_ask_verdicts.csv`: each M_ask pair, its reference label and every model's verdict.
Commit it: on a machine without the jobs' prediction files, `report` and `budget` read the real side from it.

## Not supported

- **Mutual-subsumption (bidirectional) and few-shot configs.** The masked renderer reproduces only the
  `one_level_of_parents_and_synonyms` layout, and `consult` refuses other templates.
- **Building new probe sets** (`build`) needs LogMap's anchors, hard-discarded and to-ask files for the task. Point
  `logmap_dir` in `probe.toml` at them. The shipped sets were built from the collective-anchors alignment-sources
  export. `build --version v4 --seed 42` (100-pair) and `--seed 11` (200-pair) reproduce the shipped v4 files
  byte for byte.

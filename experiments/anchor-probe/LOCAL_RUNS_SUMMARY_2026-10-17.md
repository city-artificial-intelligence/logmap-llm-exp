# Anchor probe: local vLLM runs (17 October 2026)

Summary of the five self-hosted oracles run on the `anchor-probe` branch.

## What was run

| | |
|---|---|
| Models | Qwen3-8B, Gemma-3-27B, Llama-3.1-70B-Instruct, Qwen3.5-122B-A10B, Qwen3-235B-A22B-Instruct-2507 |
| Probe sets | `v4-100`, `v4-200`, `v5-g-150`, `v5-mix-150` on anatomy and omim-ordo |
| Volume | 40 result files, 5,995 answers, 0 failed consultations |
| Code | branch at `f06a4d7`, unmodified; Python from the canonical project venv |
| Command | `experiments/anchor-probe/run_local.sh` per model pair, then `run_all.sh` for check, report and plots |
| Config | `EXP=experiments/anchor-probe/probe.local.toml` |

Each model was served exactly as in the July `zero-shot-current` batches. The arguments were checked against the July vLLM logs: same weights, quantisation, `max_model_len` 8192, `gpu_memory_utilization` 0.90 and `max_num_seqs`.

| Model | Host / GPU | Weights | Quantisation |
|---|---|---|---|
| Qwen3-8B | ngpu / 1 | Qwen3-8B (bf16) | none |
| Gemma-3-27B | ngpu / 2 | Gemma-3-27B-GPTQ-4b-128g | compressed-tensors |
| Llama-3.1-70B-Instruct | xgpu / 1 | Llama-3.1-70B-Instruct-AWQ-INT4 | awq_marlin |
| Qwen3.5-122B-A10B | xgpu / 0 | Qwen3.5-122B-A10B-GPTQ-Int4 | gptq_marlin |
| Qwen3-235B-A22B-Instruct-2507 | xgpu / 0+1, TP=2, `max_num_seqs` 16 | GPTQ-Int4-Int8Mix | gptq_marlin |

### Checks

- **Prompts:** every probe prompt is byte-identical under the branch's `src/` and the canonical July `src/` that produced the M_ask verdicts. That covers 9,592 user prompts and the developer prompt of all 64 model/task/set combinations.
- **Job configs:** all 16 copied configs are byte-identical to the archived `attempts/0001/config.toml`.
- **Real side:** `report` recomputed each job's M_ask Youden's J from its prediction file. Every value matched that job's archived `evaluation_results.json` to within 1e-6 (no warnings). Every job has 0 failed M_ask consultations, so the check ran for all of them.
- **Route:** on the v4 sets, local answers agree with the earlier runs in `reference-results/` (OpenRouter, per the README) on 96–100% of pairs for all three Qwen models, and probe J moves by at most ±0.02 (table below).

## Results

Real J is each model's Youden's J on that task's full M_ask (anatomy 259 pairs, omim-ordo 399). There are 7 models per comparison: the five local models plus DeepSeek-V4-Flash and Mistral-Small-3.2 (OpenRouter, already included). Gemini 2.5 Flash was not run.

### Does the probe rank the oracles like M_ask does?

| Task | Probe set | Spearman (95% CI) | Picks real best? | Regret | Bootstrap mean regret |
|---|---|---|---|---|---|
| anatomy | v4-100 | 0.91 (0.38–0.98) | yes | 0.000 | 0.029 |
| anatomy | v4-200 | 0.89 (0.43–0.96) | yes | 0.000 | 0.014 |
| anatomy | v5-g-150 | 0.88 (0.39–0.96) | tie (DeepSeek = Qwen3.5-122B) | 0.013 | 0.027 |
| anatomy | v5-mix-150 | 0.89 (0.43–0.96) | yes | 0.000 | 0.021 |
| omim-ordo | v4-100 | 0.23 (0.00–0.68) | no | 0.043 | 0.048 |
| omim-ordo | v4-200 | 0.46 (0.04–0.75) | no | 0.043 | 0.047 |
| omim-ordo | v5-g-150 | 0.54 (0.16–0.86) | no | 0.063 | 0.056 |
| omim-ordo | v5-mix-150 | 0.25 (0.00–0.83) | no | 0.053 | 0.050 |

Reference points from `report` (regret is the real J lost by choosing the probe's pick):

| | anatomy | omim-ordo |
|---|---|---|
| random pick, mean regret | 0.104 | 0.103 |
| 30 / 50 labelled M_ask pairs, mean regret | 0.027–0.028 / 0.021–0.022 | 0.028–0.029 / 0.022 |
| Dawid–Skene on M_ask verdicts (no labels): Spearman / regret | 0.82 / 0.000 | 0.89 / 0.000 |
| noise ceiling: real top model stays top under M_ask bootstrap | 0.65–0.67 | 0.92–0.93 |

### Per-model ranks (real rank, then probe rank on each set)

**anatomy:**

| Model | Real J | Rank | v4-100 | v4-200 | v5-g | v5-mix |
|---|---|---|---|---|---|---|
| deepseek-v4-flash | 0.651 | 1 | 1 | 1 | 1 | 1 |
| Qwen3.5-122B-A10B | 0.625 | 2 | 2 | 2 | 1 | 2 |
| mistral-small-3.2-24b | 0.616 | 3 | 4 | 5 | 5 | 5 |
| Qwen3-235B-A22B-2507 | 0.599 | 4 | 2 | 3 | 3 | 3 |
| Llama-3.1-70B-Instruct | 0.597 | 5 | 4 | 4 | 4 | 4 |
| Qwen3-8B | 0.400 | 6 | 6 | 6 | 6 | 6 |
| Gemma-3-27B | 0.339 | 7 | 7 | 7 | 7 | 7 |

**omim-ordo:**

| Model | Real J | Rank | v4-100 | v4-200 | v5-g | v5-mix |
|---|---|---|---|---|---|---|
| Qwen3-235B-A22B-2507 | 0.718 | 1 | 4 | 5 | 2 | 4 |
| mistral-small-3.2-24b | 0.679 | 2 | 6 | 3 | 5 | 6 |
| deepseek-v4-flash | 0.676 | 3 | 1 | 1 | 3 | 1 |
| Llama-3.1-70B-Instruct | 0.671 | 4 | 2 | 4 | 4 | 3 |
| Qwen3.5-122B-A10B | 0.655 | 5 | 3 | 2 | 1 | 1 |
| Qwen3-8B | 0.514 | 6 | 4 | 6 | 6 | 5 |
| Gemma-3-27B | 0.395 | 7 | 7 | 7 | 7 | 7 |

Probe J of the five local models (full tables in `runs/<task>/<set>/report.md`):

| Model | anat v4-100 | anat v4-200 | anat v5-g | anat v5-mix | omim v4-100 | omim v4-200 | omim v5-g | omim v5-mix |
|---|---|---|---|---|---|---|---|---|
| Qwen3-235B-A22B-2507 | 0.840 | 0.826 | 0.860 | 0.870 | 0.620 | 0.640 | 0.770 | 0.700 |
| Qwen3.5-122B-A10B | 0.840 | 0.829 | 0.880 | 0.890 | 0.760 | 0.740 | 0.830 | 0.750 |
| Llama-3.1-70B-Instruct | 0.800 | 0.816 | 0.810 | 0.830 | 0.780 | 0.660 | 0.710 | 0.730 |
| Qwen3-8B | 0.680 | 0.715 | 0.360 | 0.530 | 0.620 | 0.620 | 0.570 | 0.650 |
| Gemma-3-27B | 0.580 | 0.566 | 0.310 | 0.470 | 0.440 | 0.390 | 0.570 | 0.460 |

### Key take-aways

1. **Anatomy: the probe works.** Spearman is 0.88–0.91 on every set, it picks the real best model on three sets and ties for it on the fourth. Its point regret (0.000–0.013) beats 30–50 labelled M_ask pairs (0.021–0.028); its bootstrap mean regret (0.014–0.029) is comparable to them. The top five models' real J spans only 0.597–0.651, and the real top model stays top in only 65–67% of M_ask resamples, so the strong models are not well separated even on the real side.
2. **omim-ordo: the probe does not work.** Spearman is 0.23–0.54 and it never picks Qwen3-235B, the clear real best (stays top in 92–93% of resamples). Its regret (0.043–0.063) is about half a random pick's but worse than 30 labelled M_ask pairs (0.029) on every set. It consistently underrates Qwen3-235B and Mistral, and overrates Qwen3.5-122B (real #5, probe #1–3).
3. **The v5 granularity negatives do not fix omim-ordo.** v5-g has the best Spearman (0.54) but the worst regret (0.063). v5-mix is no better than v4.
4. **The weakest models are separated.** Gemma-3-27B is last on every set, and Qwen3-8B is sixth on six of eight (on omim-ordo it is fourth, tied, on v4-100 and fifth on v5-mix). The probe fails at ordering the strong cluster, where omim-ordo's real J spans 0.655–0.718.
5. **Dawid–Skene beat every probe set:** regret 0.000 on both tasks with no labels. It needs every candidate to answer all of M_ask (259 or 399 calls per model) rather than 100–200 probe pairs, so the comparison is cost against reliability, and worth raising.

### Why omim-ordo fails (diagnostics)

**Probe negatives are easier than M_ask's real false candidates for most models, but not for Qwen3-235B.** On the v4-100 hard-discarded negatives, DeepSeek's TNR is 0.86 against 0.69 on M_ask, and Qwen3.5-122B's is 0.82 against 0.68. Qwen3-235B's is 0.72 against 0.74. The probe removes the edge that makes Qwen3-235B the best model on M_ask (its real TNR of 0.736 is the highest).

**Probe negatives have a different mix from M_ask's.** `negtypes` types false candidates by their relation to the true match. On omim-ordo, per-model TNR on M_ask's *hierarchy* confusions (86 of 227 negatives) tracks real J best (Spearman 0.92). The v4 sets contain few of them (3/50, 11/100). v5-g-150 is mostly hierarchy (79/100) yet still misranks. The five strong models reject its granularity-child negatives at TNR 0.71–0.95 (Qwen3.5-122B highest at 0.95). On M_ask's hierarchy negatives, per-model TNR is 0.21–0.76 (mean 0.59 over the 8 jobs).

**Label noise, measured against the reference for analysis only:**

| Task | Set | Negatives that are true matches | Positives not in reference | Spearman: LogMap labels → reference labels | Regret: LogMap → reference |
|---|---|---|---|---|---|
| anatomy | v4-100 | 2 / 50 | 0 / 50 | 0.91 → 0.86 | 0.000 → 0.000 |
| anatomy | v4-200 | 3 / 112 | 3 / 88 | 0.89 → 0.89 | 0.000 → 0.000 |
| anatomy | v5-g-150 | 0 / 100 | 0 / 50 | 0.88 → 0.88 | 0.013 → 0.013 |
| anatomy | v5-mix-150 | 1 / 100 | 0 / 50 | 0.89 → 0.89 | 0.000 → 0.000 |
| omim-ordo | v4-100 | 3 / 50 | 5 / 50 | 0.23 → 0.23 | 0.043 → 0.063 |
| omim-ordo | v4-200 | 9 / 100 | 13 / 100 | 0.46 → 0.52 | 0.043 → 0.043 |
| omim-ordo | v5-g-150 | 8 / 100 | 5 / 50 | 0.54 → 0.61 | 0.063 → 0.032 |
| omim-ordo | v5-mix-150 | 10 / 100 | 5 / 50 | 0.25 → 0.54 | 0.053 → 0.043 |

LogMap's free labels are noticeably noisier on omim-ordo. Correcting them helps the v5 sets, but no set then picks Qwen3-235B. Label noise is part of the problem; pair selection is the rest. (`negtypes` reports these mislabelled negatives as type `same`, which its docstring does not list.)

### Route robustness (local 4-bit vs the earlier OpenRouter v4 runs)

| Task | Set | Model | Probe J local | Probe J OpenRouter | Verdict agreement |
|---|---|---|---|---|---|
| anatomy | v4-100 | Qwen3-8B | 0.680 | 0.660 | 97.0% |
| anatomy | v4-100 | Qwen3.5-122B | 0.840 | 0.840 | 100% |
| anatomy | v4-100 | Qwen3-235B | 0.840 | 0.840 | 98.0% |
| anatomy | v4-200 | Qwen3-8B | 0.715 | 0.709 | 96.5% |
| anatomy | v4-200 | Qwen3.5-122B | 0.829 | 0.840 | 99.5% |
| anatomy | v4-200 | Qwen3-235B | 0.826 | 0.840 | 98.5% |
| omim-ordo | v4-100 | Qwen3-8B | 0.620 | 0.620 | 96.0% |
| omim-ordo | v4-100 | Qwen3.5-122B | 0.760 | 0.780 | 99.0% |
| omim-ordo | v4-100 | Qwen3-235B | 0.620 | 0.600 | 97.0% |
| omim-ordo | v4-200 | Qwen3-8B | 0.620 | 0.640 | 99.0% |
| omim-ordo | v4-200 | Qwen3.5-122B | 0.740 | 0.730 | 98.5% |
| omim-ordo | v4-200 | Qwen3-235B | 0.640 | 0.640 | 97.0% |

## Potential issues

1. **M_ask prediction paths.** The archived configs point at `.../jobs/<job>/standalone/`, but the batch harness wrote outputs under `.../jobs/<job>/attempts/0001/run-root/`. As shipped, `check` reports every M_ask file MISSING and `report` cannot compare anything. Fixed locally with `probe.local.toml` (gitignored): probe.toml plus a per-job `run_root`, as the README describes. Committing the 16 `run_root` lines would save the next person the step, though they are machine-specific.
2. **Duplicate pair.** `pairs/anatomy/v5-mix-150.tsv` has one pair twice (`MA_0001972` / `NCI_C32957`, once as `granularity_child` and once as `hard_discarded`). It is asked once (149 answers) and counted under both kinds. The DeepSeek run shows the same. It is consistent across models, so it does not affect rankings, but `build` could de-duplicate.
3. **Undocumented `same` type** in `negtypes`.
4. **Gemini 2.5 Flash** (the OpenRouter step) was not run. The reports exclude it automatically (7 of 8 models).

## Where things are

- Raw answers: `runs/<task>/<probe set>/<model>.csv` plus `.json` (endpoint, templates, failure count), for the five local models.
- Reports: `runs/<task>/<probe set>/report.md`, `report_table.csv` and `report_summary.json`. `negtypes` output is in `runs/<task>/m_ask_negative_types.csv`.
- Figures: `runs/figures/` (`probe_accuracy.png`, `probe_vs_real.png`, `regret.png`, `summary.csv`). This folder is gitignored by the branch.
- Local config: `probe.local.toml` (gitignored).

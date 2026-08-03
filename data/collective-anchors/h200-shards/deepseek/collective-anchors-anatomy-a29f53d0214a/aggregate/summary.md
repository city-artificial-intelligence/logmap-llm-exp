# Results: collective-anchors-anatomy

Coverage: **1/8 (12.5%)**

| Status | Jobs |
|---|---:|
| not_run | 7 |
| success | 1 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | ca-k4 | 1 | 1 | 100.0% |
| gemini-2-5-flash-off | ca-k4 | 0 | 1 | 0.0% |
| gemma-3-27b | ca-k4 | 0 | 1 | 0.0% |
| llama-3-1-70b | ca-k4 | 0 | 1 | 0.0% |
| mistral-small-3-2-24b | ca-k4 | 0 | 1 | 0.0% |
| qwen3-235b | ca-k4 | 0 | 1 | 0.0% |
| qwen3-5-122b | ca-k4 | 0 | 1 | 0.0% |
| qwen3-8b | ca-k4 | 0 | 1 | 0.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | ca-k4 | 0.9624 | 0.8437 | 0.8991 | 0.9624 | 0.8437 | 0.8991 | 0.8587 | 0.9576 | 0.9054 | 0.9576 | 0.7234 | 0.6810 |
| gemini-2-5-flash-off | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| mistral-small-3-2-24b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | ca-k4 | Global | 1 | 1 | 1279 | 50 | 237 | 0.9624 | 0.8437 | 0.8991 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| anatomy-gemini-2-5-flash-off-ca-k4-r0-7e7eed14 | not_run |  |
| anatomy-gemma-3-27b-ca-k4-r0-49c4007c | not_run |  |
| anatomy-llama-3-1-70b-ca-k4-r0-68fdc153 | not_run |  |
| anatomy-mistral-small-3-2-24b-ca-k4-r0-2416d977 | not_run |  |
| anatomy-qwen3-235b-ca-k4-r0-610a9ce2 | not_run |  |
| anatomy-qwen3-5-122b-ca-k4-r0-1de4c4f7 | not_run |  |
| anatomy-qwen3-8b-ca-k4-r0-6bf94365 | not_run |  |

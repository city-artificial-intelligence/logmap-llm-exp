# Results: runtime-donor-v1-anatomy

Coverage: **1/8 (12.5%)**

| Status | Jobs |
|---|---:|
| not_run | 7 |
| success | 1 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | rt-k4 | 0 | 1 | 0.0% |
| gemini-2-5-flash-off | rt-k4 | 0 | 1 | 0.0% |
| gemma-3-27b | rt-k4 | 0 | 1 | 0.0% |
| llama-3-1-70b | rt-k4 | 0 | 1 | 0.0% |
| mistral-small-3-2-24b | rt-k4 | 1 | 1 | 100.0% |
| qwen3-235b | rt-k4 | 0 | 1 | 0.0% |
| qwen3-5-122b | rt-k4 | 0 | 1 | 0.0% |
| qwen3-8b | rt-k4 | 0 | 1 | 0.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| mistral-small-3-2-24b | rt-k4 | 0.9510 | 0.8456 | 0.8953 | 0.9510 | 0.8456 | 0.8953 | 0.7931 | 0.9758 | 0.8750 | 0.9758 | 0.5532 | 0.5289 |
| qwen3-235b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| mistral-small-3-2-24b | rt-k4 | Global | 1 | 1 | 1282 | 66 | 234 | 0.9510 | 0.8456 | 0.8953 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| anatomy-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-e7a56102 | not_run |  |
| anatomy-gemini-2-5-flash-off-rt-k4-r0-b85ee179 | not_run |  |
| anatomy-gemma-3-27b-rt-k4-r0-965cea27 | not_run |  |
| anatomy-llama-3-1-70b-rt-k4-r0-e77301a4 | not_run |  |
| anatomy-qwen3-235b-rt-k4-r0-529f67d1 | not_run |  |
| anatomy-qwen3-5-122b-rt-k4-r0-1ff86446 | not_run |  |
| anatomy-qwen3-8b-rt-k4-r0-1eab10c4 | not_run |  |

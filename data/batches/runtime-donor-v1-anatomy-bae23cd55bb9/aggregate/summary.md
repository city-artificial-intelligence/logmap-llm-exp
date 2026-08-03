# Results: runtime-donor-v1-anatomy

Coverage: **5/8 (62.5%)**

| Status | Jobs |
|---|---:|
| not_run | 3 |
| success | 5 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | rt-k4 | 0 | 1 | 0.0% |
| gemini-2-5-flash-off | rt-k4 | 1 | 1 | 100.0% |
| gemma-3-27b | rt-k4 | 1 | 1 | 100.0% |
| llama-3-1-70b | rt-k4 | 1 | 1 | 100.0% |
| mistral-small-3-2-24b | rt-k4 | 0 | 1 | 0.0% |
| qwen3-235b | rt-k4 | 0 | 1 | 0.0% |
| qwen3-5-122b | rt-k4 | 1 | 1 | 100.0% |
| qwen3-8b | rt-k4 | 1 | 1 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | rt-k4 | 0.9560 | 0.8456 | 0.8974 | 0.9560 | 0.8456 | 0.8974 | 0.8214 | 0.9758 | 0.8920 | 0.9758 | 0.6277 | 0.6034 |
| gemma-3-27b | rt-k4 | 0.9474 | 0.8443 | 0.8929 | 0.9474 | 0.8443 | 0.8929 | 0.7718 | 0.9636 | 0.8571 | 0.9636 | 0.5000 | 0.4636 |
| llama-3-1-70b | rt-k4 | 0.9544 | 0.8430 | 0.8953 | 0.9544 | 0.8430 | 0.8953 | 0.8093 | 0.9515 | 0.8747 | 0.9515 | 0.6064 | 0.5579 |
| mistral-small-3-2-24b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | rt-k4 | 0.9595 | 0.8430 | 0.8975 | 0.9595 | 0.8430 | 0.8975 | 0.8396 | 0.9515 | 0.8920 | 0.9515 | 0.6809 | 0.6324 |
| qwen3-8b | rt-k4 | 0.9564 | 0.8397 | 0.8943 | 0.9564 | 0.8397 | 0.8943 | 0.8172 | 0.9212 | 0.8661 | 0.9212 | 0.6383 | 0.5595 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | rt-k4 | Global | 1 | 1 | 1282 | 59 | 234 | 0.9560 | 0.8456 | 0.8974 |
| gemma-3-27b | rt-k4 | Global | 1 | 1 | 1280 | 71 | 236 | 0.9474 | 0.8443 | 0.8929 |
| llama-3-1-70b | rt-k4 | Global | 1 | 1 | 1278 | 61 | 238 | 0.9544 | 0.8430 | 0.8953 |
| qwen3-5-122b | rt-k4 | Global | 1 | 1 | 1278 | 54 | 238 | 0.9595 | 0.8430 | 0.8975 |
| qwen3-8b | rt-k4 | Global | 1 | 1 | 1273 | 58 | 243 | 0.9564 | 0.8397 | 0.8943 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| anatomy-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-e7a56102 | not_run |  |
| anatomy-mistral-small-3-2-24b-rt-k4-r0-3f662728 | not_run |  |
| anatomy-qwen3-235b-rt-k4-r0-529f67d1 | not_run |  |

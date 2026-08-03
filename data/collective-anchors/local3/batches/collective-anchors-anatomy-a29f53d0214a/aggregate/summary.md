# Results: collective-anchors-anatomy

Coverage: **5/8 (62.5%)**

| Status | Jobs |
|---|---:|
| not_run | 3 |
| success | 5 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | ca-k4 | 0 | 1 | 0.0% |
| gemini-2-5-flash-off | ca-k4 | 1 | 1 | 100.0% |
| gemma-3-27b | ca-k4 | 1 | 1 | 100.0% |
| llama-3-1-70b | ca-k4 | 1 | 1 | 100.0% |
| mistral-small-3-2-24b | ca-k4 | 0 | 1 | 0.0% |
| qwen3-235b | ca-k4 | 0 | 1 | 0.0% |
| qwen3-5-122b | ca-k4 | 1 | 1 | 100.0% |
| qwen3-8b | ca-k4 | 1 | 1 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | ca-k4 | 0.9567 | 0.8450 | 0.8974 | 0.9567 | 0.8450 | 0.8974 | 0.8247 | 0.9697 | 0.8914 | 0.9697 | 0.6383 | 0.6080 |
| gemma-3-27b | ca-k4 | 0.9462 | 0.8463 | 0.8935 | 0.9462 | 0.8463 | 0.8935 | 0.7678 | 0.9818 | 0.8617 | 0.9818 | 0.4787 | 0.4605 |
| llama-3-1-70b | ca-k4 | 0.9531 | 0.8450 | 0.8958 | 0.9531 | 0.8450 | 0.8958 | 0.8040 | 0.9697 | 0.8791 | 0.9697 | 0.5851 | 0.5548 |
| mistral-small-3-2-24b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | ca-k4 | 0.9595 | 0.8437 | 0.8979 | 0.9595 | 0.8437 | 0.8979 | 0.8404 | 0.9576 | 0.8952 | 0.9576 | 0.6809 | 0.6384 |
| qwen3-8b | ca-k4 | 0.9543 | 0.8404 | 0.8937 | 0.9543 | 0.8404 | 0.8937 | 0.8053 | 0.9273 | 0.8620 | 0.9273 | 0.6064 | 0.5337 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | ca-k4 | Global | 1 | 1 | 1281 | 58 | 235 | 0.9567 | 0.8450 | 0.8974 |
| gemma-3-27b | ca-k4 | Global | 1 | 1 | 1283 | 73 | 233 | 0.9462 | 0.8463 | 0.8935 |
| llama-3-1-70b | ca-k4 | Global | 1 | 1 | 1281 | 63 | 235 | 0.9531 | 0.8450 | 0.8958 |
| qwen3-5-122b | ca-k4 | Global | 1 | 1 | 1279 | 54 | 237 | 0.9595 | 0.8437 | 0.8979 |
| qwen3-8b | ca-k4 | Global | 1 | 1 | 1274 | 61 | 242 | 0.9543 | 0.8404 | 0.8937 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| anatomy-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-11640eb0 | not_run |  |
| anatomy-mistral-small-3-2-24b-ca-k4-r0-2416d977 | not_run |  |
| anatomy-qwen3-235b-ca-k4-r0-610a9ce2 | not_run |  |

# Results: rag-runtime-anatomy

Coverage: **6/18 (33.3%)**

| Status | Jobs |
|---|---:|
| not_run | 12 |
| success | 6 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-high | runtime-rag-k2 | 0 | 1 | 0.0% |
| deepseek-v4-flash-off | runtime-rag-k2 | 0 | 1 | 0.0% |
| deepseek-v4-flash-off | runtime-rag-k4 | 0 | 1 | 0.0% |
| gemini-2-5-flash-off | runtime-rag-k2 | 0 | 1 | 0.0% |
| gemini-2-5-flash-off | runtime-rag-k4 | 0 | 1 | 0.0% |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2 | 0 | 1 | 0.0% |
| gemma-3-27b | runtime-rag-k2 | 0 | 1 | 0.0% |
| gemma-3-27b | runtime-rag-k4 | 0 | 1 | 0.0% |
| llama-3-1-70b | runtime-rag-k2 | 1 | 1 | 100.0% |
| llama-3-1-70b | runtime-rag-k4 | 1 | 1 | 100.0% |
| mistral-small-3-2-24b | runtime-rag-k2 | 1 | 1 | 100.0% |
| mistral-small-3-2-24b | runtime-rag-k4 | 1 | 1 | 100.0% |
| qwen3-235b | runtime-rag-k2 | 0 | 1 | 0.0% |
| qwen3-235b | runtime-rag-k4 | 0 | 1 | 0.0% |
| qwen3-5-122b | runtime-rag-k2 | 1 | 1 | 100.0% |
| qwen3-5-122b | runtime-rag-k4 | 1 | 1 | 100.0% |
| qwen3-8b | runtime-rag-k2 | 0 | 1 | 0.0% |
| qwen3-8b | runtime-rag-k4 | 0 | 1 | 0.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-high | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-off | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-off | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | runtime-rag-k2 | 0.9558 | 0.8423 | 0.8955 | 0.9558 | 0.8423 | 0.8955 | 0.8168 | 0.9455 | 0.8764 | 0.9455 | 0.6277 | 0.5731 |
| llama-3-1-70b | runtime-rag-k4 | 0.9531 | 0.8443 | 0.8954 | 0.9531 | 0.8443 | 0.8954 | 0.8030 | 0.9636 | 0.8760 | 0.9636 | 0.5851 | 0.5487 |
| mistral-small-3-2-24b | runtime-rag-k2 | 0.9518 | 0.8463 | 0.8959 | 0.9518 | 0.8463 | 0.8959 | 0.7980 | 0.9818 | 0.8804 | 0.9818 | 0.5638 | 0.5456 |
| mistral-small-3-2-24b | runtime-rag-k4 | 0.9497 | 0.8463 | 0.8950 | 0.9497 | 0.8463 | 0.8950 | 0.7864 | 0.9818 | 0.8733 | 0.9818 | 0.5319 | 0.5137 |
| qwen3-235b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | runtime-rag-k2 | 0.9595 | 0.8437 | 0.8979 | 0.9595 | 0.8437 | 0.8979 | 0.8404 | 0.9576 | 0.8952 | 0.9576 | 0.6809 | 0.6384 |
| qwen3-5-122b | runtime-rag-k4 | 0.9588 | 0.8437 | 0.8975 | 0.9588 | 0.8437 | 0.8975 | 0.8360 | 0.9576 | 0.8927 | 0.9576 | 0.6702 | 0.6278 |
| qwen3-8b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| llama-3-1-70b | runtime-rag-k2 | Global | 1 | 1 | 1277 | 59 | 239 | 0.9558 | 0.8423 | 0.8955 |
| llama-3-1-70b | runtime-rag-k4 | Global | 1 | 1 | 1280 | 63 | 236 | 0.9531 | 0.8443 | 0.8954 |
| mistral-small-3-2-24b | runtime-rag-k2 | Global | 1 | 1 | 1283 | 65 | 233 | 0.9518 | 0.8463 | 0.8959 |
| mistral-small-3-2-24b | runtime-rag-k4 | Global | 1 | 1 | 1283 | 68 | 233 | 0.9497 | 0.8463 | 0.8950 |
| qwen3-5-122b | runtime-rag-k2 | Global | 1 | 1 | 1279 | 54 | 237 | 0.9595 | 0.8437 | 0.8979 |
| qwen3-5-122b | runtime-rag-k4 | Global | 1 | 1 | 1279 | 55 | 237 | 0.9588 | 0.8437 | 0.8975 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| anatomy-deepseek-v4-flash-high-runtime-rag-k2-r0-2fac2e7c | not_run |  |
| anatomy-deepseek-v4-flash-off-runtime-rag-k2-r0-cb5f2ece | not_run |  |
| anatomy-deepseek-v4-flash-off-runtime-rag-k4-r0-a6e40c68 | not_run |  |
| anatomy-gemini-2-5-flash-off-runtime-rag-k2-r0-8cd5c8cf | not_run |  |
| anatomy-gemini-2-5-flash-off-runtime-rag-k4-r0-fb1f4d7c | not_run |  |
| anatomy-gemini-2-5-flash-reason-1028-runtime-rag-k2-r0-f0f8400d | not_run |  |
| anatomy-gemma-3-27b-runtime-rag-k2-r0-cc209f8b | not_run |  |
| anatomy-gemma-3-27b-runtime-rag-k4-r0-121dbae7 | not_run |  |
| anatomy-qwen3-235b-runtime-rag-k2-r0-57d65a4a | not_run |  |
| anatomy-qwen3-235b-runtime-rag-k4-r0-e589adf5 | not_run |  |
| anatomy-qwen3-8b-runtime-rag-k2-r0-097ac0e8 | not_run |  |
| anatomy-qwen3-8b-runtime-rag-k4-r0-5bd630b5 | not_run |  |

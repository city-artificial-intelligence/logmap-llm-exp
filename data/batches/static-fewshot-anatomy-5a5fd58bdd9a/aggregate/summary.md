# Results: static-fewshot-anatomy

Coverage: **6/6 (100.0%)**

| Status | Jobs |
|---|---:|
| degraded | 1 |
| success | 5 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| gemini-2-5-flash-off | static-k4 | 1 | 1 | 100.0% |
| gemma-3-27b | static-k4 | 1 | 1 | 100.0% |
| llama-3-1-70b | static-k4 | 1 | 1 | 100.0% |
| mistral-small-3-2-24b | static-k4 | 1 | 1 | 100.0% |
| qwen3-5-122b | static-k4 | 1 | 1 | 100.0% |
| qwen3-8b | static-k4 | 1 | 1 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | static-k4 | 0.9581 | 0.8450 | 0.8980 | 0.9581 | 0.8450 | 0.8980 | 0.8333 | 0.9697 | 0.8964 | 0.9697 | 0.6596 | 0.6293 |
| gemma-3-27b | static-k4 | 0.9503 | 0.8450 | 0.8946 | 0.9503 | 0.8450 | 0.8946 | 0.7882 | 0.9697 | 0.8696 | 0.9697 | 0.5426 | 0.5123 |
| llama-3-1-70b | static-k4 | 0.9559 | 0.8443 | 0.8967 | 0.9559 | 0.8443 | 0.8967 | 0.8196 | 0.9636 | 0.8858 | 0.9636 | 0.6277 | 0.5913 |
| mistral-small-3-2-24b | static-k4 | 0.9537 | 0.8423 | 0.8946 | 0.9537 | 0.8423 | 0.8946 | 0.8041 | 0.9811 | 0.8839 | 0.9811 | 0.5730 | 0.5542 |
| qwen3-5-122b | static-k4 | 0.9609 | 0.8423 | 0.8977 | 0.9609 | 0.8423 | 0.8977 | 0.8478 | 0.9455 | 0.8940 | 0.9455 | 0.7021 | 0.6476 |
| qwen3-8b | static-k4 | 0.9605 | 0.8344 | 0.8930 | 0.9605 | 0.8344 | 0.8930 | 0.8372 | 0.8727 | 0.8546 | 0.8727 | 0.7021 | 0.5749 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | static-k4 | Global | 1 | 1 | 1281 | 56 | 235 | 0.9581 | 0.8450 | 0.8980 |
| gemma-3-27b | static-k4 | Global | 1 | 1 | 1281 | 67 | 235 | 0.9503 | 0.8450 | 0.8946 |
| llama-3-1-70b | static-k4 | Global | 1 | 1 | 1280 | 59 | 236 | 0.9559 | 0.8443 | 0.8967 |
| mistral-small-3-2-24b | static-k4 | Global | 1 | 1 | 1277 | 62 | 239 | 0.9537 | 0.8423 | 0.8946 |
| qwen3-5-122b | static-k4 | Global | 1 | 1 | 1277 | 52 | 239 | 0.9609 | 0.8423 | 0.8977 |
| qwen3-8b | static-k4 | Global | 1 | 1 | 1265 | 52 | 251 | 0.9605 | 0.8344 | 0.8930 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

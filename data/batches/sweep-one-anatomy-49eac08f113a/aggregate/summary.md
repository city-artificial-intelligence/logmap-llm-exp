# Results: sweep-one-anatomy

Coverage: **9/9 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 9 |

## Groups

| model | completed | expected | coverage |
|---|---|---|---|
| deepseek-v4-flash | 1 | 1 | 100.0% |
| gemini-2-5-flash | 1 | 1 | 100.0% |
| gemma-3-27b | 1 | 1 | 100.0% |
| llama-3-1-70b | 1 | 1 | 100.0% |
| mistral-small-3-2-24b | 1 | 1 | 100.0% |
| plain-logmap | 1 | 1 | 100.0% |
| qwen3-235b | 1 | 1 | 100.0% |
| qwen3-5-122b | 1 | 1 | 100.0% |
| qwen3-8b | 1 | 1 | 100.0% |

## Primary metrics

| model | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 0.9588 | 0.8450 | 0.8983 | 0.9588 | 0.8450 | 0.8983 | 0.8421 | 0.9697 | 0.9014 | 0.9697 | 0.6809 | 0.6505 |
| gemini-2-5-flash | 0.9531 | 0.8450 | 0.8958 | 0.9531 | 0.8450 | 0.8958 | 0.8081 | 0.9697 | 0.8815 | 0.9697 | 0.5957 | 0.5654 |
| gemma-3-27b | 0.9372 | 0.8470 | 0.8898 | 0.9372 | 0.8470 | 0.8898 | 0.7277 | 0.9879 | 0.8380 | 0.9879 | 0.3511 | 0.3389 |
| llama-3-1-70b | 0.9553 | 0.8450 | 0.8967 | 0.9553 | 0.8450 | 0.8967 | 0.8205 | 0.9697 | 0.8889 | 0.9697 | 0.6277 | 0.5974 |
| mistral-small-3-2-24b | 0.9561 | 0.8470 | 0.8982 | 0.9561 | 0.8470 | 0.8982 | 0.8274 | 0.9879 | 0.9006 | 0.9879 | 0.6383 | 0.6262 |
| plain-logmap | 0.9153 | 0.8483 | 0.8805 | 0.9153 | 0.8483 | 0.8805 |  |  |  |  |  |  |
| qwen3-235b | 0.9580 | 0.8417 | 0.8961 | 0.9580 | 0.8417 | 0.8961 | 0.8333 | 0.9394 | 0.8832 | 0.9394 | 0.6702 | 0.6096 |
| qwen3-5-122b | 0.9567 | 0.8456 | 0.8978 | 0.9567 | 0.8456 | 0.8978 | 0.8299 | 0.9758 | 0.8969 | 0.9758 | 0.6489 | 0.6247 |
| qwen3-8b | 0.9426 | 0.8443 | 0.8907 | 0.9426 | 0.8443 | 0.8907 | 0.7500 | 0.9636 | 0.8435 | 0.9636 | 0.4362 | 0.3998 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | Global | 1 | 1 | 1281 | 55 | 235 | 0.9588 | 0.8450 | 0.8983 |
| gemini-2-5-flash | Global | 1 | 1 | 1281 | 63 | 235 | 0.9531 | 0.8450 | 0.8958 |
| gemma-3-27b | Global | 1 | 1 | 1284 | 86 | 232 | 0.9372 | 0.8470 | 0.8898 |
| llama-3-1-70b | Global | 1 | 1 | 1281 | 60 | 235 | 0.9553 | 0.8450 | 0.8967 |
| mistral-small-3-2-24b | Global | 1 | 1 | 1284 | 59 | 232 | 0.9561 | 0.8470 | 0.8982 |
| plain-logmap | Global | 1 | 1 | 1286 | 119 | 230 | 0.9153 | 0.8483 | 0.8805 |
| qwen3-235b | Global | 1 | 1 | 1276 | 56 | 240 | 0.9580 | 0.8417 | 0.8961 |
| qwen3-5-122b | Global | 1 | 1 | 1282 | 58 | 234 | 0.9567 | 0.8456 | 0.8978 |
| qwen3-8b | Global | 1 | 1 | 1280 | 78 | 236 | 0.9426 | 0.8443 | 0.8907 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

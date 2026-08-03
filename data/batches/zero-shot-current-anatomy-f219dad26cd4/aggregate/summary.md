# Results: zero-shot-current-anatomy

Coverage: **8/8 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 8 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | zero-shot-current | 1 | 1 | 100.0% |
| gemini-2-5-flash-off | zero-shot-current | 1 | 1 | 100.0% |
| gemma-3-27b | zero-shot-current | 1 | 1 | 100.0% |
| llama-3-1-70b | zero-shot-current | 1 | 1 | 100.0% |
| mistral-small-3-2-24b | zero-shot-current | 1 | 1 | 100.0% |
| qwen3-235b | zero-shot-current | 1 | 1 | 100.0% |
| qwen3-5-122b | zero-shot-current | 1 | 1 | 100.0% |
| qwen3-8b | zero-shot-current | 1 | 1 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | zero-shot-current | 0.9596 | 0.8450 | 0.8986 | 0.9596 | 0.8450 | 0.8986 | 0.8421 | 0.9697 | 0.9014 | 0.9697 | 0.6809 | 0.6505 |
| gemini-2-5-flash-off | zero-shot-current | 0.9538 | 0.8450 | 0.8961 | 0.9538 | 0.8450 | 0.8961 | 0.8081 | 0.9697 | 0.8815 | 0.9697 | 0.5957 | 0.5654 |
| gemma-3-27b | zero-shot-current | 0.9379 | 0.8470 | 0.8901 | 0.9379 | 0.8470 | 0.8901 | 0.7277 | 0.9879 | 0.8380 | 0.9879 | 0.3511 | 0.3389 |
| llama-3-1-70b | zero-shot-current | 0.9560 | 0.8450 | 0.8971 | 0.9560 | 0.8450 | 0.8971 | 0.8205 | 0.9697 | 0.8889 | 0.9697 | 0.6277 | 0.5974 |
| mistral-small-3-2-24b | zero-shot-current | 0.9561 | 0.8470 | 0.8982 | 0.9561 | 0.8470 | 0.8982 | 0.8232 | 0.9879 | 0.8981 | 0.9879 | 0.6277 | 0.6155 |
| qwen3-235b | zero-shot-current | 0.9580 | 0.8417 | 0.8961 | 0.9580 | 0.8417 | 0.8961 | 0.8289 | 0.9394 | 0.8807 | 0.9394 | 0.6596 | 0.5990 |
| qwen3-5-122b | zero-shot-current | 0.9574 | 0.8456 | 0.8981 | 0.9574 | 0.8456 | 0.8981 | 0.8299 | 0.9758 | 0.8969 | 0.9758 | 0.6489 | 0.6247 |
| qwen3-8b | zero-shot-current | 0.9433 | 0.8443 | 0.8911 | 0.9433 | 0.8443 | 0.8911 | 0.7500 | 0.9636 | 0.8435 | 0.9636 | 0.4362 | 0.3998 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | zero-shot-current | Global | 1 | 1 | 1281 | 54 | 235 | 0.9596 | 0.8450 | 0.8986 |
| gemini-2-5-flash-off | zero-shot-current | Global | 1 | 1 | 1281 | 62 | 235 | 0.9538 | 0.8450 | 0.8961 |
| gemma-3-27b | zero-shot-current | Global | 1 | 1 | 1284 | 85 | 232 | 0.9379 | 0.8470 | 0.8901 |
| llama-3-1-70b | zero-shot-current | Global | 1 | 1 | 1281 | 59 | 235 | 0.9560 | 0.8450 | 0.8971 |
| mistral-small-3-2-24b | zero-shot-current | Global | 1 | 1 | 1284 | 59 | 232 | 0.9561 | 0.8470 | 0.8982 |
| qwen3-235b | zero-shot-current | Global | 1 | 1 | 1276 | 56 | 240 | 0.9580 | 0.8417 | 0.8961 |
| qwen3-5-122b | zero-shot-current | Global | 1 | 1 | 1282 | 57 | 234 | 0.9574 | 0.8456 | 0.8981 |
| qwen3-8b | zero-shot-current | Global | 1 | 1 | 1280 | 77 | 236 | 0.9433 | 0.8443 | 0.8911 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

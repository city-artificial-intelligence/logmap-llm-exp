# Results: mutual-subsumption-anatomy

Coverage: **4/4 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 4 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| gemma-3-27b | bidir-k0 | 1 | 1 | 100.0% |
| llama-3-1-70b | bidir-k0 | 1 | 1 | 100.0% |
| qwen3-5-122b | bidir-k0 | 1 | 1 | 100.0% |
| qwen3-8b | bidir-k0 | 1 | 1 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma-3-27b | bidir-k0 | 0.9536 | 0.8410 | 0.8938 | 0.9536 | 0.8410 | 0.8938 | 0.8021 | 0.9333 | 0.8627 | 0.9333 | 0.5957 | 0.5291 |
| llama-3-1-70b | bidir-k0 | 0.9636 | 0.8391 | 0.8970 | 0.9636 | 0.8391 | 0.8970 | 0.8629 | 0.9152 | 0.8882 | 0.9152 | 0.7447 | 0.6598 |
| qwen3-5-122b | bidir-k0 | 0.9652 | 0.8417 | 0.8992 | 0.9652 | 0.8417 | 0.8992 | 0.8757 | 0.9394 | 0.9064 | 0.9394 | 0.7660 | 0.7054 |
| qwen3-8b | bidir-k0 | 0.9573 | 0.8430 | 0.8965 | 0.9573 | 0.8430 | 0.8965 | 0.8263 | 0.9515 | 0.8845 | 0.9515 | 0.6489 | 0.6005 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma-3-27b | bidir-k0 | Global | 1 | 1 | 1275 | 62 | 241 | 0.9536 | 0.8410 | 0.8938 |
| llama-3-1-70b | bidir-k0 | Global | 1 | 1 | 1272 | 48 | 244 | 0.9636 | 0.8391 | 0.8970 |
| qwen3-5-122b | bidir-k0 | Global | 1 | 1 | 1276 | 46 | 240 | 0.9652 | 0.8417 | 0.8992 |
| qwen3-8b | bidir-k0 | Global | 1 | 1 | 1278 | 57 | 238 | 0.9573 | 0.8430 | 0.8965 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

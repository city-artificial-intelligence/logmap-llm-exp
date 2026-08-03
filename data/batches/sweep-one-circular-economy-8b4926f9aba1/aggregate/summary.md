# Results: sweep-one-circular-economy

Coverage: **18/18 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 18 |

## Groups

| model | completed | expected | coverage |
|---|---|---|---|
| deepseek-v4-flash | 2 | 2 | 100.0% |
| gemini-2-5-flash | 2 | 2 | 100.0% |
| gemma-3-27b | 2 | 2 | 100.0% |
| llama-3-1-70b | 2 | 2 | 100.0% |
| mistral-small-3-2-24b | 2 | 2 | 100.0% |
| plain-logmap | 2 | 2 | 100.0% |
| qwen3-235b | 2 | 2 | 100.0% |
| qwen3-5-122b | 2 | 2 | 100.0% |
| qwen3-8b | 2 | 2 | 100.0% |

## Primary metrics

| model | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 0.5062 | 0.9111 | 0.6508 | 0.5250 | 0.9310 | 0.6469 | 0.3500 | 1.0000 | 0.5000 | 1.0000 | 0.7222 | 0.7222 |
| gemini-2-5-flash | 0.4940 | 0.9111 | 0.6406 | 0.5023 | 0.9310 | 0.6343 | 0.2250 | 1.0000 | 0.3667 | 1.0000 | 0.6111 | 0.6111 |
| gemma-3-27b | 0.4767 | 0.9111 | 0.6260 | 0.4864 | 0.9310 | 0.6204 | 0.1667 | 1.0000 | 0.2857 | 1.0000 | 0.4444 | 0.4444 |
| llama-3-1-70b | 0.4940 | 0.9111 | 0.6406 | 0.5023 | 0.9310 | 0.6343 | 0.2250 | 1.0000 | 0.3667 | 1.0000 | 0.6111 | 0.6111 |
| mistral-small-3-2-24b | 0.5195 | 0.8889 | 0.6557 | 0.5301 | 0.8998 | 0.6478 | 0.2500 | 0.5000 | 0.3333 | 0.5000 | 0.8889 | 0.3889 |
| plain-logmap | 0.5125 | 0.9111 | 0.6560 | 0.5239 | 0.9310 | 0.6500 |  |  |  |  |  |  |
| qwen3-235b | 0.5190 | 0.9111 | 0.6613 | 0.5333 | 0.9310 | 0.6558 | 0.4167 | 1.0000 | 0.5833 | 1.0000 | 0.8333 | 0.8333 |
| qwen3-5-122b | 0.5125 | 0.9111 | 0.6560 | 0.5290 | 0.9310 | 0.6513 | 0.3750 | 1.0000 | 0.5333 | 1.0000 | 0.7778 | 0.7778 |
| qwen3-8b | 0.5062 | 0.9111 | 0.6508 | 0.5197 | 0.9310 | 0.6455 | 0.2917 | 1.0000 | 0.4500 | 1.0000 | 0.7222 | 0.7222 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | Global | 2 | 2 | 41 | 40 | 4 | 0.5062 | 0.9111 | 0.6508 |
| deepseek-v4-flash | M1/class | 2 | 2 | 41 | 35 | 4 | 0.5395 | 0.9111 | 0.6777 |
| deepseek-v4-flash | M2/property | 2 | 2 | 0 | 5 | 0 | 0.0000 |  |  |
| deepseek-v4-flash | UNKNOWN | 2 | 2 | 0 | 0 | 0 |  |  |  |
| gemini-2-5-flash | Global | 2 | 2 | 41 | 42 | 4 | 0.4940 | 0.9111 | 0.6406 |
| gemini-2-5-flash | M1/class | 2 | 2 | 41 | 37 | 4 | 0.5256 | 0.9111 | 0.6667 |
| gemini-2-5-flash | M2/property | 2 | 2 | 0 | 5 | 0 | 0.0000 |  |  |
| gemini-2-5-flash | UNKNOWN | 2 | 2 | 0 | 0 | 0 |  |  |  |
| gemma-3-27b | Global | 2 | 2 | 41 | 45 | 4 | 0.4767 | 0.9111 | 0.6260 |
| gemma-3-27b | M1/class | 2 | 2 | 41 | 37 | 4 | 0.5256 | 0.9111 | 0.6667 |
| gemma-3-27b | M2/property | 2 | 2 | 0 | 8 | 0 | 0.0000 |  |  |
| gemma-3-27b | UNKNOWN | 2 | 2 | 0 | 0 | 0 |  |  |  |
| llama-3-1-70b | Global | 2 | 2 | 41 | 42 | 4 | 0.4940 | 0.9111 | 0.6406 |
| llama-3-1-70b | M1/class | 2 | 2 | 41 | 35 | 4 | 0.5395 | 0.9111 | 0.6777 |
| llama-3-1-70b | M2/property | 2 | 2 | 0 | 7 | 0 | 0.0000 |  |  |
| llama-3-1-70b | UNKNOWN | 2 | 2 | 0 | 0 | 0 |  |  |  |
| mistral-small-3-2-24b | Global | 2 | 2 | 40 | 37 | 5 | 0.5195 | 0.8889 | 0.6557 |
| mistral-small-3-2-24b | M1/class | 2 | 2 | 40 | 34 | 5 | 0.5405 | 0.8889 | 0.6723 |
| mistral-small-3-2-24b | M2/property | 2 | 2 | 0 | 3 | 0 | 0.0000 |  |  |
| mistral-small-3-2-24b | UNKNOWN | 2 | 2 | 0 | 0 | 0 |  |  |  |
| plain-logmap | Global | 2 | 2 | 41 | 39 | 4 | 0.5125 | 0.9111 | 0.6560 |
| plain-logmap | M1/class | 2 | 2 | 41 | 37 | 4 | 0.5256 | 0.9111 | 0.6667 |
| plain-logmap | M2/property | 2 | 2 | 0 | 2 | 0 | 0.0000 |  |  |
| plain-logmap | UNKNOWN | 2 | 2 | 0 | 0 | 0 |  |  |  |
| qwen3-235b | Global | 2 | 2 | 41 | 38 | 4 | 0.5190 | 0.9111 | 0.6613 |
| qwen3-235b | M1/class | 2 | 2 | 41 | 34 | 4 | 0.5467 | 0.9111 | 0.6833 |
| qwen3-235b | M2/property | 2 | 2 | 0 | 4 | 0 | 0.0000 |  |  |
| qwen3-235b | UNKNOWN | 2 | 2 | 0 | 0 | 0 |  |  |  |
| qwen3-5-122b | Global | 2 | 2 | 41 | 39 | 4 | 0.5125 | 0.9111 | 0.6560 |
| qwen3-5-122b | M1/class | 2 | 2 | 41 | 35 | 4 | 0.5395 | 0.9111 | 0.6777 |
| qwen3-5-122b | M2/property | 2 | 2 | 0 | 4 | 0 | 0.0000 |  |  |
| qwen3-5-122b | UNKNOWN | 2 | 2 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | Global | 2 | 2 | 41 | 40 | 4 | 0.5062 | 0.9111 | 0.6508 |
| qwen3-8b | M1/class | 2 | 2 | 41 | 34 | 4 | 0.5467 | 0.9111 | 0.6833 |
| qwen3-8b | M2/property | 2 | 2 | 0 | 6 | 0 | 0.0000 |  |  |
| qwen3-8b | UNKNOWN | 2 | 2 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

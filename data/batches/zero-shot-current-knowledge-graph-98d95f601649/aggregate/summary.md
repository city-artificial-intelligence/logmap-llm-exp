# Results: zero-shot-current-knowledge-graph

Coverage: **40/40 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 40 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | zero-shot-current | 5 | 5 | 100.0% |
| gemini-2-5-flash-off | zero-shot-current | 5 | 5 | 100.0% |
| gemma-3-27b | zero-shot-current | 5 | 5 | 100.0% |
| llama-3-1-70b | zero-shot-current | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | zero-shot-current | 5 | 5 | 100.0% |
| qwen3-235b | zero-shot-current | 5 | 5 | 100.0% |
| qwen3-5-122b | zero-shot-current | 5 | 5 | 100.0% |
| qwen3-8b | zero-shot-current | 5 | 5 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | zero-shot-current | 0.8925 | 0.7296 | 0.8028 | 0.8990 | 0.7000 | 0.7825 | 0.7333 | 0.4881 | 0.5676 | 0.6102 | 0.8765 | 0.5808 |
| gemini-2-5-flash-off | zero-shot-current | 0.8920 | 0.7296 | 0.8027 | 0.8987 | 0.7004 | 0.7827 | 0.6133 | 0.5763 | 0.5700 | 0.7204 | 0.8071 | 0.6042 |
| gemma-3-27b | zero-shot-current | 0.8917 | 0.7307 | 0.8032 | 0.8986 | 0.7023 | 0.7839 | 0.5929 | 0.7437 | 0.6383 | 0.9296 | 0.7318 | 0.7193 |
| llama-3-1-70b | zero-shot-current | 0.8920 | 0.7303 | 0.8031 | 0.8988 | 0.7014 | 0.7833 | 0.5667 | 0.6800 | 0.5989 | 0.8500 | 0.8553 | 0.6691 |
| mistral-small-3-2-24b | zero-shot-current | 0.8926 | 0.7300 | 0.8031 | 0.8992 | 0.7009 | 0.7832 | 0.7385 | 0.5385 | 0.6107 | 0.6731 | 0.9765 | 0.6437 |
| qwen3-235b | zero-shot-current | 0.8927 | 0.7294 | 0.8028 | 0.8992 | 0.6999 | 0.7825 | 0.7500 | 0.4615 | 0.5535 | 0.5769 | 0.9882 | 0.5621 |
| qwen3-5-122b | zero-shot-current | 0.8926 | 0.7304 | 0.8034 | 0.8993 | 0.7018 | 0.7838 | 0.7429 | 0.5889 | 0.6463 | 0.7361 | 0.9765 | 0.7067 |
| qwen3-8b | zero-shot-current | 0.8926 | 0.7296 | 0.8029 | 0.8992 | 0.7002 | 0.7827 | 0.7455 | 0.4030 | 0.5197 | 0.5037 | 0.9824 | 0.4816 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | zero-shot-current | Global | 5 | 5 | 11204 | 1350 | 4153 | 0.8925 | 0.7296 | 0.8028 |
| deepseek-v4-flash-parasail-off | zero-shot-current | CLS | 5 | 5 | 31 | 2 | 18 | 0.9394 | 0.6327 | 0.7561 |
| deepseek-v4-flash-parasail-off | zero-shot-current | INST | 5 | 5 | 11001 | 1336 | 4126 | 0.8917 | 0.7272 | 0.8011 |
| deepseek-v4-flash-parasail-off | zero-shot-current | PROP | 5 | 5 | 172 | 12 | 9 | 0.9348 | 0.9503 | 0.9425 |
| deepseek-v4-flash-parasail-off | zero-shot-current | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| gemini-2-5-flash-off | zero-shot-current | Global | 5 | 5 | 11205 | 1356 | 4152 | 0.8920 | 0.7296 | 0.8027 |
| gemini-2-5-flash-off | zero-shot-current | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| gemini-2-5-flash-off | zero-shot-current | INST | 5 | 5 | 11003 | 1336 | 4124 | 0.8917 | 0.7274 | 0.8012 |
| gemini-2-5-flash-off | zero-shot-current | PROP | 5 | 5 | 172 | 18 | 9 | 0.9053 | 0.9503 | 0.9272 |
| gemini-2-5-flash-off | zero-shot-current | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| gemma-3-27b | zero-shot-current | Global | 5 | 5 | 11222 | 1363 | 4135 | 0.8917 | 0.7307 | 0.8032 |
| gemma-3-27b | zero-shot-current | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| gemma-3-27b | zero-shot-current | INST | 5 | 5 | 11020 | 1342 | 4107 | 0.8914 | 0.7285 | 0.8018 |
| gemma-3-27b | zero-shot-current | PROP | 5 | 5 | 172 | 19 | 9 | 0.9005 | 0.9503 | 0.9247 |
| gemma-3-27b | zero-shot-current | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| llama-3-1-70b | zero-shot-current | Global | 5 | 5 | 11215 | 1358 | 4142 | 0.8920 | 0.7303 | 0.8031 |
| llama-3-1-70b | zero-shot-current | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| llama-3-1-70b | zero-shot-current | INST | 5 | 5 | 11013 | 1338 | 4114 | 0.8917 | 0.7280 | 0.8016 |
| llama-3-1-70b | zero-shot-current | PROP | 5 | 5 | 172 | 18 | 9 | 0.9053 | 0.9503 | 0.9272 |
| llama-3-1-70b | zero-shot-current | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| mistral-small-3-2-24b | zero-shot-current | Global | 5 | 5 | 11210 | 1349 | 4147 | 0.8926 | 0.7300 | 0.8031 |
| mistral-small-3-2-24b | zero-shot-current | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| mistral-small-3-2-24b | zero-shot-current | INST | 5 | 5 | 11008 | 1337 | 4119 | 0.8917 | 0.7277 | 0.8014 |
| mistral-small-3-2-24b | zero-shot-current | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| mistral-small-3-2-24b | zero-shot-current | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-235b | zero-shot-current | Global | 5 | 5 | 11202 | 1347 | 4155 | 0.8927 | 0.7294 | 0.8028 |
| qwen3-235b | zero-shot-current | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| qwen3-235b | zero-shot-current | INST | 5 | 5 | 11000 | 1336 | 4127 | 0.8917 | 0.7272 | 0.8011 |
| qwen3-235b | zero-shot-current | PROP | 5 | 5 | 172 | 9 | 9 | 0.9503 | 0.9503 | 0.9503 |
| qwen3-235b | zero-shot-current | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-5-122b | zero-shot-current | Global | 5 | 5 | 11216 | 1349 | 4141 | 0.8926 | 0.7304 | 0.8034 |
| qwen3-5-122b | zero-shot-current | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| qwen3-5-122b | zero-shot-current | INST | 5 | 5 | 11014 | 1336 | 4113 | 0.8918 | 0.7281 | 0.8017 |
| qwen3-5-122b | zero-shot-current | PROP | 5 | 5 | 172 | 11 | 9 | 0.9399 | 0.9503 | 0.9451 |
| qwen3-5-122b | zero-shot-current | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | zero-shot-current | Global | 5 | 5 | 11205 | 1348 | 4152 | 0.8926 | 0.7296 | 0.8029 |
| qwen3-8b | zero-shot-current | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| qwen3-8b | zero-shot-current | INST | 5 | 5 | 11003 | 1336 | 4124 | 0.8917 | 0.7274 | 0.8012 |
| qwen3-8b | zero-shot-current | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-8b | zero-shot-current | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

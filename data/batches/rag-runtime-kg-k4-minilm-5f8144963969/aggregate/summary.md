# Results: rag-runtime-kg-k4-minilm

Coverage: **40/40 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 40 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | runtime-rag-k4-minilm | 5 | 5 | 100.0% |
| gemini-2-5-flash-off | runtime-rag-k4-minilm | 5 | 5 | 100.0% |
| gemma-3-27b | runtime-rag-k4-minilm | 5 | 5 | 100.0% |
| llama-3-1-70b | runtime-rag-k4-minilm | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | runtime-rag-k4-minilm | 5 | 5 | 100.0% |
| qwen3-235b | runtime-rag-k4-minilm | 5 | 5 | 100.0% |
| qwen3-5-122b | runtime-rag-k4-minilm | 5 | 5 | 100.0% |
| qwen3-8b | runtime-rag-k4-minilm | 5 | 5 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | runtime-rag-k4-minilm | 0.8926 | 0.7299 | 0.8031 | 0.8990 | 0.7005 | 0.7828 | 0.6872 | 0.6296 | 0.6329 | 0.7870 | 0.9424 | 0.7150 |
| gemini-2-5-flash-off | runtime-rag-k4-minilm | 0.8927 | 0.7305 | 0.8035 | 0.8991 | 0.7018 | 0.7837 | 0.6958 | 0.7215 | 0.6980 | 0.9019 | 0.9424 | 0.8298 |
| gemma-3-27b | runtime-rag-k4-minilm | 0.8920 | 0.7309 | 0.8034 | 0.8989 | 0.7024 | 0.7840 | 0.5778 | 0.7704 | 0.6469 | 0.9630 | 0.8494 | 0.7747 |
| llama-3-1-70b | runtime-rag-k4-minilm | 0.8924 | 0.7306 | 0.8034 | 0.8991 | 0.7020 | 0.7838 | 0.6633 | 0.7289 | 0.6836 | 0.9111 | 0.9188 | 0.8096 |
| mistral-small-3-2-24b | runtime-rag-k4-minilm | 0.8924 | 0.7308 | 0.8036 | 0.8989 | 0.7024 | 0.7840 | 0.6400 | 0.7570 | 0.6773 | 0.9463 | 0.8847 | 0.8022 |
| qwen3-235b | runtime-rag-k4-minilm | 0.8927 | 0.7302 | 0.8033 | 0.8991 | 0.7012 | 0.7833 | 0.7000 | 0.6593 | 0.6627 | 0.8241 | 0.9482 | 0.7594 |
| qwen3-5-122b | runtime-rag-k4-minilm | 0.8926 | 0.7304 | 0.8034 | 0.8991 | 0.7015 | 0.7835 | 0.6625 | 0.6141 | 0.6330 | 0.7676 | 0.9424 | 0.6955 |
| qwen3-8b | runtime-rag-k4-minilm | 0.8926 | 0.7297 | 0.8030 | 0.8990 | 0.7002 | 0.7827 | 0.6970 | 0.5089 | 0.5549 | 0.6361 | 0.9482 | 0.5714 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | runtime-rag-k4-minilm | Global | 5 | 5 | 11209 | 1349 | 4148 | 0.8926 | 0.7299 | 0.8031 |
| deepseek-v4-flash-parasail-off | runtime-rag-k4-minilm | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| deepseek-v4-flash-parasail-off | runtime-rag-k4-minilm | INST | 5 | 5 | 11005 | 1336 | 4122 | 0.8917 | 0.7275 | 0.8013 |
| deepseek-v4-flash-parasail-off | runtime-rag-k4-minilm | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| deepseek-v4-flash-parasail-off | runtime-rag-k4-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| gemini-2-5-flash-off | runtime-rag-k4-minilm | Global | 5 | 5 | 11219 | 1349 | 4138 | 0.8927 | 0.7305 | 0.8035 |
| gemini-2-5-flash-off | runtime-rag-k4-minilm | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| gemini-2-5-flash-off | runtime-rag-k4-minilm | INST | 5 | 5 | 11015 | 1336 | 4112 | 0.8918 | 0.7282 | 0.8017 |
| gemini-2-5-flash-off | runtime-rag-k4-minilm | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| gemini-2-5-flash-off | runtime-rag-k4-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| gemma-3-27b | runtime-rag-k4-minilm | Global | 5 | 5 | 11224 | 1359 | 4133 | 0.8920 | 0.7309 | 0.8034 |
| gemma-3-27b | runtime-rag-k4-minilm | CLS | 5 | 5 | 32 | 5 | 17 | 0.8649 | 0.6531 | 0.7442 |
| gemma-3-27b | runtime-rag-k4-minilm | INST | 5 | 5 | 11020 | 1339 | 4107 | 0.8917 | 0.7285 | 0.8019 |
| gemma-3-27b | runtime-rag-k4-minilm | PROP | 5 | 5 | 172 | 15 | 9 | 0.9198 | 0.9503 | 0.9348 |
| gemma-3-27b | runtime-rag-k4-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| llama-3-1-70b | runtime-rag-k4-minilm | Global | 5 | 5 | 11220 | 1353 | 4137 | 0.8924 | 0.7306 | 0.8034 |
| llama-3-1-70b | runtime-rag-k4-minilm | CLS | 5 | 5 | 32 | 4 | 17 | 0.8889 | 0.6531 | 0.7529 |
| llama-3-1-70b | runtime-rag-k4-minilm | INST | 5 | 5 | 11016 | 1337 | 4111 | 0.8918 | 0.7282 | 0.8017 |
| llama-3-1-70b | runtime-rag-k4-minilm | PROP | 5 | 5 | 172 | 12 | 9 | 0.9348 | 0.9503 | 0.9425 |
| llama-3-1-70b | runtime-rag-k4-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| mistral-small-3-2-24b | runtime-rag-k4-minilm | Global | 5 | 5 | 11223 | 1353 | 4134 | 0.8924 | 0.7308 | 0.8036 |
| mistral-small-3-2-24b | runtime-rag-k4-minilm | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| mistral-small-3-2-24b | runtime-rag-k4-minilm | INST | 5 | 5 | 11019 | 1339 | 4108 | 0.8916 | 0.7284 | 0.8018 |
| mistral-small-3-2-24b | runtime-rag-k4-minilm | PROP | 5 | 5 | 172 | 11 | 9 | 0.9399 | 0.9503 | 0.9451 |
| mistral-small-3-2-24b | runtime-rag-k4-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-235b | runtime-rag-k4-minilm | Global | 5 | 5 | 11213 | 1348 | 4144 | 0.8927 | 0.7302 | 0.8033 |
| qwen3-235b | runtime-rag-k4-minilm | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-235b | runtime-rag-k4-minilm | INST | 5 | 5 | 11009 | 1336 | 4118 | 0.8918 | 0.7278 | 0.8015 |
| qwen3-235b | runtime-rag-k4-minilm | PROP | 5 | 5 | 172 | 9 | 9 | 0.9503 | 0.9503 | 0.9503 |
| qwen3-235b | runtime-rag-k4-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-5-122b | runtime-rag-k4-minilm | Global | 5 | 5 | 11217 | 1349 | 4140 | 0.8926 | 0.7304 | 0.8034 |
| qwen3-5-122b | runtime-rag-k4-minilm | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-5-122b | runtime-rag-k4-minilm | INST | 5 | 5 | 11013 | 1336 | 4114 | 0.8918 | 0.7280 | 0.8016 |
| qwen3-5-122b | runtime-rag-k4-minilm | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-5-122b | runtime-rag-k4-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | runtime-rag-k4-minilm | Global | 5 | 5 | 11206 | 1348 | 4151 | 0.8926 | 0.7297 | 0.8030 |
| qwen3-8b | runtime-rag-k4-minilm | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-8b | runtime-rag-k4-minilm | INST | 5 | 5 | 11002 | 1336 | 4125 | 0.8917 | 0.7273 | 0.8012 |
| qwen3-8b | runtime-rag-k4-minilm | PROP | 5 | 5 | 172 | 9 | 9 | 0.9503 | 0.9503 | 0.9503 |
| qwen3-8b | runtime-rag-k4-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

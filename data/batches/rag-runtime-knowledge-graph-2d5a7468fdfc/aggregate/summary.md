# Results: rag-runtime-knowledge-graph

Coverage: **60/140 (42.9%)**

| Status | Jobs |
|---|---:|
| not_run | 80 |
| success | 60 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-high | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| deepseek-v4-flash-high | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| deepseek-v4-flash-off | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| deepseek-v4-flash-off | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| deepseek-v4-flash-off | runtime-rag-k4-sapbert | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | runtime-rag-k4-sapbert | 0 | 5 | 0.0% |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| gemma-3-27b | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| gemma-3-27b | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| gemma-3-27b | runtime-rag-k4-sapbert | 0 | 5 | 0.0% |
| llama-3-1-70b | runtime-rag-k2-minilm | 5 | 5 | 100.0% |
| llama-3-1-70b | runtime-rag-k2-sapbert | 5 | 5 | 100.0% |
| llama-3-1-70b | runtime-rag-k4-sapbert | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | runtime-rag-k2-minilm | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | runtime-rag-k2-sapbert | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | runtime-rag-k4-sapbert | 5 | 5 | 100.0% |
| qwen3-235b | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| qwen3-235b | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| qwen3-235b | runtime-rag-k4-sapbert | 0 | 5 | 0.0% |
| qwen3-5-122b | runtime-rag-k2-minilm | 5 | 5 | 100.0% |
| qwen3-5-122b | runtime-rag-k2-sapbert | 5 | 5 | 100.0% |
| qwen3-5-122b | runtime-rag-k4-sapbert | 5 | 5 | 100.0% |
| qwen3-8b | runtime-rag-k2-minilm | 5 | 5 | 100.0% |
| qwen3-8b | runtime-rag-k2-sapbert | 5 | 5 | 100.0% |
| qwen3-8b | runtime-rag-k4-sapbert | 5 | 5 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-high | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-high | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-off | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-off | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-off | runtime-rag-k4-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | runtime-rag-k4-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k4-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | runtime-rag-k2-minilm | 0.8924 | 0.7305 | 0.8034 | 0.8990 | 0.7018 | 0.7836 | 0.6078 | 0.7081 | 0.6402 | 0.8852 | 0.8906 | 0.7484 |
| llama-3-1-70b | runtime-rag-k2-sapbert | 0.8924 | 0.7305 | 0.8034 | 0.8991 | 0.7016 | 0.7836 | 0.6702 | 0.7141 | 0.6782 | 0.8926 | 0.9247 | 0.7985 |
| llama-3-1-70b | runtime-rag-k4-sapbert | 0.8925 | 0.7305 | 0.8035 | 0.8991 | 0.7018 | 0.7837 | 0.6778 | 0.7215 | 0.6878 | 0.9019 | 0.9306 | 0.8151 |
| mistral-small-3-2-24b | runtime-rag-k2-minilm | 0.8925 | 0.7307 | 0.8035 | 0.8991 | 0.7018 | 0.7837 | 0.6762 | 0.7481 | 0.6969 | 0.9352 | 0.9247 | 0.8411 |
| mistral-small-3-2-24b | runtime-rag-k2-sapbert | 0.8924 | 0.7309 | 0.8036 | 0.8991 | 0.7024 | 0.7841 | 0.6638 | 0.7704 | 0.7019 | 0.9630 | 0.9129 | 0.8541 |
| mistral-small-3-2-24b | runtime-rag-k4-sapbert | 0.8925 | 0.7308 | 0.8036 | 0.8991 | 0.7022 | 0.7840 | 0.6762 | 0.7630 | 0.7063 | 0.9537 | 0.9247 | 0.8596 |
| qwen3-235b | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | runtime-rag-k4-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | runtime-rag-k2-minilm | 0.8926 | 0.7304 | 0.8034 | 0.8991 | 0.7017 | 0.7836 | 0.6500 | 0.6081 | 0.6251 | 0.7602 | 0.9365 | 0.6808 |
| qwen3-5-122b | runtime-rag-k2-sapbert | 0.8927 | 0.7305 | 0.8035 | 0.8991 | 0.7017 | 0.7836 | 0.6625 | 0.6215 | 0.6380 | 0.7769 | 0.9424 | 0.7048 |
| qwen3-5-122b | runtime-rag-k4-sapbert | 0.8926 | 0.7304 | 0.8034 | 0.8991 | 0.7017 | 0.7836 | 0.6600 | 0.6081 | 0.6302 | 0.7602 | 0.9424 | 0.6881 |
| qwen3-8b | runtime-rag-k2-minilm | 0.8927 | 0.7294 | 0.8028 | 0.8990 | 0.6998 | 0.7824 | 0.6750 | 0.3748 | 0.4709 | 0.4685 | 0.9541 | 0.4112 |
| qwen3-8b | runtime-rag-k2-sapbert | 0.8926 | 0.7296 | 0.8029 | 0.8990 | 0.6999 | 0.7824 | 0.6636 | 0.4015 | 0.4876 | 0.5019 | 0.9482 | 0.4371 |
| qwen3-8b | runtime-rag-k4-sapbert | 0.8926 | 0.7301 | 0.8032 | 0.8991 | 0.7009 | 0.7832 | 0.6905 | 0.5652 | 0.5939 | 0.7065 | 0.9424 | 0.6344 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| llama-3-1-70b | runtime-rag-k2-minilm | Global | 5 | 5 | 11218 | 1352 | 4139 | 0.8924 | 0.7305 | 0.8034 |
| llama-3-1-70b | runtime-rag-k2-minilm | CLS | 5 | 5 | 31 | 4 | 18 | 0.8857 | 0.6327 | 0.7381 |
| llama-3-1-70b | runtime-rag-k2-minilm | INST | 5 | 5 | 11015 | 1336 | 4112 | 0.8918 | 0.7282 | 0.8017 |
| llama-3-1-70b | runtime-rag-k2-minilm | PROP | 5 | 5 | 172 | 12 | 9 | 0.9348 | 0.9503 | 0.9425 |
| llama-3-1-70b | runtime-rag-k2-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| llama-3-1-70b | runtime-rag-k2-sapbert | Global | 5 | 5 | 11218 | 1352 | 4139 | 0.8924 | 0.7305 | 0.8034 |
| llama-3-1-70b | runtime-rag-k2-sapbert | CLS | 5 | 5 | 32 | 4 | 17 | 0.8889 | 0.6531 | 0.7529 |
| llama-3-1-70b | runtime-rag-k2-sapbert | INST | 5 | 5 | 11014 | 1336 | 4113 | 0.8918 | 0.7281 | 0.8017 |
| llama-3-1-70b | runtime-rag-k2-sapbert | PROP | 5 | 5 | 172 | 12 | 9 | 0.9348 | 0.9503 | 0.9425 |
| llama-3-1-70b | runtime-rag-k2-sapbert | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| llama-3-1-70b | runtime-rag-k4-sapbert | Global | 5 | 5 | 11219 | 1351 | 4138 | 0.8925 | 0.7305 | 0.8035 |
| llama-3-1-70b | runtime-rag-k4-sapbert | CLS | 5 | 5 | 32 | 4 | 17 | 0.8889 | 0.6531 | 0.7529 |
| llama-3-1-70b | runtime-rag-k4-sapbert | INST | 5 | 5 | 11015 | 1336 | 4112 | 0.8918 | 0.7282 | 0.8017 |
| llama-3-1-70b | runtime-rag-k4-sapbert | PROP | 5 | 5 | 172 | 11 | 9 | 0.9399 | 0.9503 | 0.9451 |
| llama-3-1-70b | runtime-rag-k4-sapbert | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| mistral-small-3-2-24b | runtime-rag-k2-minilm | Global | 5 | 5 | 11221 | 1352 | 4136 | 0.8925 | 0.7307 | 0.8035 |
| mistral-small-3-2-24b | runtime-rag-k2-minilm | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| mistral-small-3-2-24b | runtime-rag-k2-minilm | INST | 5 | 5 | 11017 | 1338 | 4110 | 0.8917 | 0.7283 | 0.8018 |
| mistral-small-3-2-24b | runtime-rag-k2-minilm | PROP | 5 | 5 | 172 | 11 | 9 | 0.9399 | 0.9503 | 0.9451 |
| mistral-small-3-2-24b | runtime-rag-k2-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| mistral-small-3-2-24b | runtime-rag-k2-sapbert | Global | 5 | 5 | 11224 | 1354 | 4133 | 0.8924 | 0.7309 | 0.8036 |
| mistral-small-3-2-24b | runtime-rag-k2-sapbert | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| mistral-small-3-2-24b | runtime-rag-k2-sapbert | INST | 5 | 5 | 11020 | 1340 | 4107 | 0.8916 | 0.7285 | 0.8018 |
| mistral-small-3-2-24b | runtime-rag-k2-sapbert | PROP | 5 | 5 | 172 | 11 | 9 | 0.9399 | 0.9503 | 0.9451 |
| mistral-small-3-2-24b | runtime-rag-k2-sapbert | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| mistral-small-3-2-24b | runtime-rag-k4-sapbert | Global | 5 | 5 | 11223 | 1352 | 4134 | 0.8925 | 0.7308 | 0.8036 |
| mistral-small-3-2-24b | runtime-rag-k4-sapbert | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| mistral-small-3-2-24b | runtime-rag-k4-sapbert | INST | 5 | 5 | 11019 | 1338 | 4108 | 0.8917 | 0.7284 | 0.8018 |
| mistral-small-3-2-24b | runtime-rag-k4-sapbert | PROP | 5 | 5 | 172 | 11 | 9 | 0.9399 | 0.9503 | 0.9451 |
| mistral-small-3-2-24b | runtime-rag-k4-sapbert | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-5-122b | runtime-rag-k2-minilm | Global | 5 | 5 | 11217 | 1350 | 4140 | 0.8926 | 0.7304 | 0.8034 |
| qwen3-5-122b | runtime-rag-k2-minilm | CLS | 5 | 5 | 30 | 3 | 19 | 0.9091 | 0.6122 | 0.7317 |
| qwen3-5-122b | runtime-rag-k2-minilm | INST | 5 | 5 | 11015 | 1336 | 4112 | 0.8918 | 0.7282 | 0.8017 |
| qwen3-5-122b | runtime-rag-k2-minilm | PROP | 5 | 5 | 172 | 11 | 9 | 0.9399 | 0.9503 | 0.9451 |
| qwen3-5-122b | runtime-rag-k2-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-5-122b | runtime-rag-k2-sapbert | Global | 5 | 5 | 11218 | 1349 | 4139 | 0.8927 | 0.7305 | 0.8035 |
| qwen3-5-122b | runtime-rag-k2-sapbert | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-5-122b | runtime-rag-k2-sapbert | INST | 5 | 5 | 11014 | 1336 | 4113 | 0.8918 | 0.7281 | 0.8017 |
| qwen3-5-122b | runtime-rag-k2-sapbert | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-5-122b | runtime-rag-k2-sapbert | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-5-122b | runtime-rag-k4-sapbert | Global | 5 | 5 | 11217 | 1349 | 4140 | 0.8926 | 0.7304 | 0.8034 |
| qwen3-5-122b | runtime-rag-k4-sapbert | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-5-122b | runtime-rag-k4-sapbert | INST | 5 | 5 | 11013 | 1336 | 4114 | 0.8918 | 0.7280 | 0.8016 |
| qwen3-5-122b | runtime-rag-k4-sapbert | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-5-122b | runtime-rag-k4-sapbert | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | runtime-rag-k2-minilm | Global | 5 | 5 | 11202 | 1347 | 4155 | 0.8927 | 0.7294 | 0.8028 |
| qwen3-8b | runtime-rag-k2-minilm | CLS | 5 | 5 | 31 | 2 | 18 | 0.9394 | 0.6327 | 0.7561 |
| qwen3-8b | runtime-rag-k2-minilm | INST | 5 | 5 | 10999 | 1336 | 4128 | 0.8917 | 0.7271 | 0.8010 |
| qwen3-8b | runtime-rag-k2-minilm | PROP | 5 | 5 | 172 | 9 | 9 | 0.9503 | 0.9503 | 0.9503 |
| qwen3-8b | runtime-rag-k2-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | runtime-rag-k2-sapbert | Global | 5 | 5 | 11204 | 1348 | 4153 | 0.8926 | 0.7296 | 0.8029 |
| qwen3-8b | runtime-rag-k2-sapbert | CLS | 5 | 5 | 32 | 2 | 17 | 0.9412 | 0.6531 | 0.7711 |
| qwen3-8b | runtime-rag-k2-sapbert | INST | 5 | 5 | 11000 | 1336 | 4127 | 0.8917 | 0.7272 | 0.8011 |
| qwen3-8b | runtime-rag-k2-sapbert | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-8b | runtime-rag-k2-sapbert | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | runtime-rag-k4-sapbert | Global | 5 | 5 | 11212 | 1349 | 4145 | 0.8926 | 0.7301 | 0.8032 |
| qwen3-8b | runtime-rag-k4-sapbert | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-8b | runtime-rag-k4-sapbert | INST | 5 | 5 | 11008 | 1336 | 4119 | 0.8918 | 0.7277 | 0.8014 |
| qwen3-8b | runtime-rag-k4-sapbert | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-8b | runtime-rag-k4-sapbert | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| marvelcinematicuniverse-marvel-deepseek-v4-flash-high-runtime-rag-k2-minilm-r0-17ac5487 | not_run |  |
| marvelcinematicuniverse-marvel-deepseek-v4-flash-high-runtime-rag-k2-sapbert-r0-3a1e3f4c | not_run |  |
| marvelcinematicuniverse-marvel-deepseek-v4-flash-off-runtime-rag-k2-minilm-r0-caa2c50d | not_run |  |
| marvelcinematicuniverse-marvel-deepseek-v4-flash-off-runtime-rag-k2-sapbert-r0-2d6133bd | not_run |  |
| marvelcinematicuniverse-marvel-deepseek-v4-flash-off-runtime-rag-k4-sapbert-r0-fa978cd9 | not_run |  |
| marvelcinematicuniverse-marvel-gemini-2-5-flash-off-runtime-rag-k2-minilm-r0-64de9d6e | not_run |  |
| marvelcinematicuniverse-marvel-gemini-2-5-flash-off-runtime-rag-k2-sapbert-r0-8d754582 | not_run |  |
| marvelcinematicuniverse-marvel-gemini-2-5-flash-off-runtime-rag-k4-sapbert-r0-2556b305 | not_run |  |
| marvelcinematicuniverse-marvel-gemini-2-5-flash-reason-1028-runtime-rag-k2-minilm-r0-61bea5fc | not_run |  |
| marvelcinematicuniverse-marvel-gemini-2-5-flash-reason-1028-runtime-rag-k2-sapbert-r0-17096021 | not_run |  |
| marvelcinematicuniverse-marvel-gemma-3-27b-runtime-rag-k2-minilm-r0-5c8c913a | not_run |  |
| marvelcinematicuniverse-marvel-gemma-3-27b-runtime-rag-k2-sapbert-r0-beafef11 | not_run |  |
| marvelcinematicuniverse-marvel-gemma-3-27b-runtime-rag-k4-sapbert-r0-8276fae1 | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-235b-runtime-rag-k2-minilm-r0-3b0bc0ad | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-235b-runtime-rag-k2-sapbert-r0-e1d145f9 | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-235b-runtime-rag-k4-sapbert-r0-50a5d353 | not_run |  |
| memoryalpha-memorybeta-deepseek-v4-flash-high-runtime-rag-k2-minilm-r0-ba82981b | not_run |  |
| memoryalpha-memorybeta-deepseek-v4-flash-high-runtime-rag-k2-sapbert-r0-bbab20df | not_run |  |
| memoryalpha-memorybeta-deepseek-v4-flash-off-runtime-rag-k2-minilm-r0-42f9b934 | not_run |  |
| memoryalpha-memorybeta-deepseek-v4-flash-off-runtime-rag-k2-sapbert-r0-f667634d | not_run |  |
| memoryalpha-memorybeta-deepseek-v4-flash-off-runtime-rag-k4-sapbert-r0-c1125534 | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-off-runtime-rag-k2-minilm-r0-a7278d75 | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-off-runtime-rag-k2-sapbert-r0-3d8dca99 | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-off-runtime-rag-k4-sapbert-r0-0201187e | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-reason-1028-runtime-rag-k2-minilm-r0-c592d6a2 | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-reason-1028-runtime-rag-k2-sapbert-r0-47f7e25d | not_run |  |
| memoryalpha-memorybeta-gemma-3-27b-runtime-rag-k2-minilm-r0-f3cdfe8f | not_run |  |
| memoryalpha-memorybeta-gemma-3-27b-runtime-rag-k2-sapbert-r0-c1f6145a | not_run |  |
| memoryalpha-memorybeta-gemma-3-27b-runtime-rag-k4-sapbert-r0-9daf3577 | not_run |  |
| memoryalpha-memorybeta-qwen3-235b-runtime-rag-k2-minilm-r0-104c3951 | not_run |  |
| memoryalpha-memorybeta-qwen3-235b-runtime-rag-k2-sapbert-r0-46d04145 | not_run |  |
| memoryalpha-memorybeta-qwen3-235b-runtime-rag-k4-sapbert-r0-d15b3fed | not_run |  |
| memoryalpha-stexpanded-deepseek-v4-flash-high-runtime-rag-k2-minilm-r0-d10fdd2d | not_run |  |
| memoryalpha-stexpanded-deepseek-v4-flash-high-runtime-rag-k2-sapbert-r0-dbbdb33d | not_run |  |
| memoryalpha-stexpanded-deepseek-v4-flash-off-runtime-rag-k2-minilm-r0-8cc6bf5d | not_run |  |
| memoryalpha-stexpanded-deepseek-v4-flash-off-runtime-rag-k2-sapbert-r0-889e4dc8 | not_run |  |
| memoryalpha-stexpanded-deepseek-v4-flash-off-runtime-rag-k4-sapbert-r0-8ff63cb3 | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-off-runtime-rag-k2-minilm-r0-99bdbe05 | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-off-runtime-rag-k2-sapbert-r0-325974d4 | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-off-runtime-rag-k4-sapbert-r0-9ed39777 | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-reason-1028-runtime-rag-k2-minilm-r0-73fd9a4f | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-reason-1028-runtime-rag-k2-sapbert-r0-15fcd223 | not_run |  |
| memoryalpha-stexpanded-gemma-3-27b-runtime-rag-k2-minilm-r0-82e1c05c | not_run |  |
| memoryalpha-stexpanded-gemma-3-27b-runtime-rag-k2-sapbert-r0-9384d7d6 | not_run |  |
| memoryalpha-stexpanded-gemma-3-27b-runtime-rag-k4-sapbert-r0-94d79eb9 | not_run |  |
| memoryalpha-stexpanded-qwen3-235b-runtime-rag-k2-minilm-r0-5fc575bc | not_run |  |
| memoryalpha-stexpanded-qwen3-235b-runtime-rag-k2-sapbert-r0-5de4a51a | not_run |  |
| memoryalpha-stexpanded-qwen3-235b-runtime-rag-k4-sapbert-r0-07eddee7 | not_run |  |
| starwars-swg-deepseek-v4-flash-high-runtime-rag-k2-minilm-r0-06667d54 | not_run |  |
| starwars-swg-deepseek-v4-flash-high-runtime-rag-k2-sapbert-r0-5f40976e | not_run |  |
| starwars-swg-deepseek-v4-flash-off-runtime-rag-k2-minilm-r0-59ef4e25 | not_run |  |
| starwars-swg-deepseek-v4-flash-off-runtime-rag-k2-sapbert-r0-eae359a2 | not_run |  |
| starwars-swg-deepseek-v4-flash-off-runtime-rag-k4-sapbert-r0-6a013cc4 | not_run |  |
| starwars-swg-gemini-2-5-flash-off-runtime-rag-k2-minilm-r0-de1647a7 | not_run |  |
| starwars-swg-gemini-2-5-flash-off-runtime-rag-k2-sapbert-r0-5b68d07a | not_run |  |
| starwars-swg-gemini-2-5-flash-off-runtime-rag-k4-sapbert-r0-3da1995a | not_run |  |
| starwars-swg-gemini-2-5-flash-reason-1028-runtime-rag-k2-minilm-r0-cf971bc9 | not_run |  |
| starwars-swg-gemini-2-5-flash-reason-1028-runtime-rag-k2-sapbert-r0-26a930c4 | not_run |  |
| starwars-swg-gemma-3-27b-runtime-rag-k2-minilm-r0-7c6b8c93 | not_run |  |
| starwars-swg-gemma-3-27b-runtime-rag-k2-sapbert-r0-89be61ac | not_run |  |
| starwars-swg-gemma-3-27b-runtime-rag-k4-sapbert-r0-584f891b | not_run |  |
| starwars-swg-qwen3-235b-runtime-rag-k2-minilm-r0-578b3a1a | not_run |  |
| starwars-swg-qwen3-235b-runtime-rag-k2-sapbert-r0-7af458ba | not_run |  |
| starwars-swg-qwen3-235b-runtime-rag-k4-sapbert-r0-8a78ff6d | not_run |  |
| starwars-swtor-deepseek-v4-flash-high-runtime-rag-k2-minilm-r0-38d3aad3 | not_run |  |
| starwars-swtor-deepseek-v4-flash-high-runtime-rag-k2-sapbert-r0-054c6de7 | not_run |  |
| starwars-swtor-deepseek-v4-flash-off-runtime-rag-k2-minilm-r0-538e43f6 | not_run |  |
| starwars-swtor-deepseek-v4-flash-off-runtime-rag-k2-sapbert-r0-7d800bae | not_run |  |
| starwars-swtor-deepseek-v4-flash-off-runtime-rag-k4-sapbert-r0-6db9adfb | not_run |  |
| starwars-swtor-gemini-2-5-flash-off-runtime-rag-k2-minilm-r0-7cb1c0ff | not_run |  |
| starwars-swtor-gemini-2-5-flash-off-runtime-rag-k2-sapbert-r0-3ef5bf4f | not_run |  |
| starwars-swtor-gemini-2-5-flash-off-runtime-rag-k4-sapbert-r0-ceb0364c | not_run |  |
| starwars-swtor-gemini-2-5-flash-reason-1028-runtime-rag-k2-minilm-r0-b6d56721 | not_run |  |
| starwars-swtor-gemini-2-5-flash-reason-1028-runtime-rag-k2-sapbert-r0-d1bb76cf | not_run |  |
| starwars-swtor-gemma-3-27b-runtime-rag-k2-minilm-r0-0d272e91 | not_run |  |
| starwars-swtor-gemma-3-27b-runtime-rag-k2-sapbert-r0-c84745ba | not_run |  |
| starwars-swtor-gemma-3-27b-runtime-rag-k4-sapbert-r0-70befc69 | not_run |  |
| starwars-swtor-qwen3-235b-runtime-rag-k2-minilm-r0-a0e757d0 | not_run |  |
| starwars-swtor-qwen3-235b-runtime-rag-k2-sapbert-r0-75b37261 | not_run |  |
| starwars-swtor-qwen3-235b-runtime-rag-k4-sapbert-r0-9516e9ee | not_run |  |

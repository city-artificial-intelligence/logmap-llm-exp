# Results: plain-true-false-knowledge-graph

Coverage: **105/120 (87.5%)**

| Status | Jobs |
|---|---:|
| not_run | 15 |
| success | 105 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | plain-k0 | 0 | 5 | 0.0% |
| deepseek-v4-flash-parasail-off | plain-k2 | 0 | 5 | 0.0% |
| deepseek-v4-flash-parasail-off | plain-k4 | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | plain-k0 | 5 | 5 | 100.0% |
| gemini-2-5-flash-off | plain-k2 | 5 | 5 | 100.0% |
| gemini-2-5-flash-off | plain-k4 | 5 | 5 | 100.0% |
| gemma-3-27b | plain-k0 | 5 | 5 | 100.0% |
| gemma-3-27b | plain-k2 | 5 | 5 | 100.0% |
| gemma-3-27b | plain-k4 | 5 | 5 | 100.0% |
| llama-3-1-70b | plain-k0 | 5 | 5 | 100.0% |
| llama-3-1-70b | plain-k2 | 5 | 5 | 100.0% |
| llama-3-1-70b | plain-k4 | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | plain-k0 | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | plain-k2 | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | plain-k4 | 5 | 5 | 100.0% |
| qwen3-235b | plain-k0 | 5 | 5 | 100.0% |
| qwen3-235b | plain-k2 | 5 | 5 | 100.0% |
| qwen3-235b | plain-k4 | 5 | 5 | 100.0% |
| qwen3-5-122b | plain-k0 | 5 | 5 | 100.0% |
| qwen3-5-122b | plain-k2 | 5 | 5 | 100.0% |
| qwen3-5-122b | plain-k4 | 5 | 5 | 100.0% |
| qwen3-8b | plain-k0 | 5 | 5 | 100.0% |
| qwen3-8b | plain-k2 | 5 | 5 | 100.0% |
| qwen3-8b | plain-k4 | 5 | 5 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | plain-k0 |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-parasail-off | plain-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-parasail-off | plain-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | plain-k0 | 0.8924 | 0.7293 | 0.8027 | 0.8989 | 0.6999 | 0.7824 | 0.6333 | 0.4348 | 0.4787 | 0.5435 | 0.9365 | 0.4641 |
| gemini-2-5-flash-off | plain-k2 | 0.8927 | 0.7305 | 0.8035 | 0.8991 | 0.7018 | 0.7837 | 0.6933 | 0.7081 | 0.6902 | 0.8852 | 0.9424 | 0.8131 |
| gemini-2-5-flash-off | plain-k4 | 0.8925 | 0.7305 | 0.8035 | 0.8991 | 0.7020 | 0.7838 | 0.6745 | 0.7156 | 0.6850 | 0.8944 | 0.9306 | 0.8077 |
| gemma-3-27b | plain-k0 | 0.8923 | 0.7307 | 0.8034 | 0.8991 | 0.7023 | 0.7840 | 0.7143 | 0.7304 | 0.7173 | 0.9130 | 0.8471 | 0.8468 |
| gemma-3-27b | plain-k2 | 0.8922 | 0.7306 | 0.8034 | 0.8989 | 0.7020 | 0.7838 | 0.5515 | 0.6363 | 0.5801 | 0.7954 | 0.8671 | 0.6292 |
| gemma-3-27b | plain-k4 | 0.8923 | 0.7307 | 0.8034 | 0.8990 | 0.7020 | 0.7838 | 0.6551 | 0.7422 | 0.6824 | 0.9278 | 0.9071 | 0.8116 |
| llama-3-1-70b | plain-k0 | 0.8925 | 0.7300 | 0.8031 | 0.8990 | 0.7012 | 0.7833 | 0.6121 | 0.6326 | 0.5976 | 0.7907 | 0.9024 | 0.6687 |
| llama-3-1-70b | plain-k2 | 0.8924 | 0.7304 | 0.8033 | 0.8990 | 0.7016 | 0.7835 | 0.6078 | 0.7007 | 0.6352 | 0.8759 | 0.8906 | 0.7392 |
| llama-3-1-70b | plain-k4 | 0.8925 | 0.7306 | 0.8035 | 0.8991 | 0.7020 | 0.7838 | 0.6778 | 0.7289 | 0.6926 | 0.9111 | 0.9306 | 0.8243 |
| mistral-small-3-2-24b | plain-k0 | 0.8926 | 0.7294 | 0.8028 | 0.8991 | 0.6999 | 0.7825 | 0.7250 | 0.4481 | 0.5361 | 0.5602 | 0.9824 | 0.5381 |
| mistral-small-3-2-24b | plain-k2 | 0.8927 | 0.7305 | 0.8035 | 0.8993 | 0.7016 | 0.7837 | 0.7556 | 0.7274 | 0.7349 | 0.9093 | 0.9765 | 0.8798 |
| mistral-small-3-2-24b | plain-k4 | 0.8926 | 0.7308 | 0.8037 | 0.8993 | 0.7024 | 0.7841 | 0.7474 | 0.7570 | 0.7487 | 0.9463 | 0.9706 | 0.9095 |
| qwen3-235b | plain-k0 | 0.8926 | 0.7292 | 0.8027 | 0.8991 | 0.6994 | 0.7822 | 0.7500 | 0.4393 | 0.5291 | 0.5491 | 0.9882 | 0.5344 |
| qwen3-235b | plain-k2 | 0.8926 | 0.7302 | 0.8033 | 0.8991 | 0.7014 | 0.7835 | 0.6872 | 0.6667 | 0.6629 | 0.8333 | 0.9424 | 0.7613 |
| qwen3-235b | plain-k4 | 0.8926 | 0.7301 | 0.8032 | 0.8991 | 0.7010 | 0.7832 | 0.6872 | 0.6519 | 0.6517 | 0.8148 | 0.9424 | 0.7428 |
| qwen3-5-122b | plain-k0 | 0.8927 | 0.7303 | 0.8034 | 0.8993 | 0.7016 | 0.7837 | 0.7538 | 0.5815 | 0.6464 | 0.7269 | 0.9824 | 0.7048 |
| qwen3-5-122b | plain-k2 | 0.8926 | 0.7303 | 0.8033 | 0.8991 | 0.7015 | 0.7835 | 0.6571 | 0.5874 | 0.6169 | 0.7343 | 0.9424 | 0.6622 |
| qwen3-5-122b | plain-k4 | 0.8926 | 0.7304 | 0.8034 | 0.8991 | 0.7015 | 0.7835 | 0.6600 | 0.6007 | 0.6252 | 0.7509 | 0.9424 | 0.6789 |
| qwen3-8b | plain-k0 | 0.8924 | 0.7302 | 0.8032 | 0.8991 | 0.7012 | 0.7833 | 0.7263 | 0.4933 | 0.5678 | 0.6167 | 0.9588 | 0.5652 |
| qwen3-8b | plain-k2 | 0.8926 | 0.7295 | 0.8029 | 0.8990 | 0.7000 | 0.7825 | 0.6556 | 0.3822 | 0.4731 | 0.4778 | 0.9482 | 0.4131 |
| qwen3-8b | plain-k4 | 0.8926 | 0.7296 | 0.8029 | 0.8990 | 0.6998 | 0.7824 | 0.7000 | 0.5074 | 0.5496 | 0.6343 | 0.9482 | 0.5696 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | plain-k0 | Global | 5 | 5 | 11200 | 1350 | 4157 | 0.8924 | 0.7293 | 0.8027 |
| gemini-2-5-flash-off | plain-k0 | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| gemini-2-5-flash-off | plain-k0 | INST | 5 | 5 | 10998 | 1336 | 4129 | 0.8917 | 0.7270 | 0.8010 |
| gemini-2-5-flash-off | plain-k0 | PROP | 5 | 5 | 172 | 12 | 9 | 0.9348 | 0.9503 | 0.9425 |
| gemini-2-5-flash-off | plain-k0 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| gemini-2-5-flash-off | plain-k2 | Global | 5 | 5 | 11218 | 1349 | 4139 | 0.8927 | 0.7305 | 0.8035 |
| gemini-2-5-flash-off | plain-k2 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| gemini-2-5-flash-off | plain-k2 | INST | 5 | 5 | 11014 | 1336 | 4113 | 0.8918 | 0.7281 | 0.8017 |
| gemini-2-5-flash-off | plain-k2 | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| gemini-2-5-flash-off | plain-k2 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| gemini-2-5-flash-off | plain-k4 | Global | 5 | 5 | 11219 | 1351 | 4138 | 0.8925 | 0.7305 | 0.8035 |
| gemini-2-5-flash-off | plain-k4 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| gemini-2-5-flash-off | plain-k4 | INST | 5 | 5 | 11015 | 1337 | 4112 | 0.8918 | 0.7282 | 0.8017 |
| gemini-2-5-flash-off | plain-k4 | PROP | 5 | 5 | 172 | 11 | 9 | 0.9399 | 0.9503 | 0.9451 |
| gemini-2-5-flash-off | plain-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| gemma-3-27b | plain-k0 | Global | 5 | 5 | 11221 | 1355 | 4136 | 0.8923 | 0.7307 | 0.8034 |
| gemma-3-27b | plain-k0 | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| gemma-3-27b | plain-k0 | INST | 5 | 5 | 11019 | 1338 | 4108 | 0.8917 | 0.7284 | 0.8018 |
| gemma-3-27b | plain-k0 | PROP | 5 | 5 | 172 | 15 | 9 | 0.9198 | 0.9503 | 0.9348 |
| gemma-3-27b | plain-k0 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| gemma-3-27b | plain-k2 | Global | 5 | 5 | 11220 | 1356 | 4137 | 0.8922 | 0.7306 | 0.8034 |
| gemma-3-27b | plain-k2 | CLS | 5 | 5 | 31 | 3 | 18 | 0.9118 | 0.6327 | 0.7470 |
| gemma-3-27b | plain-k2 | INST | 5 | 5 | 11017 | 1339 | 4110 | 0.8916 | 0.7283 | 0.8017 |
| gemma-3-27b | plain-k2 | PROP | 5 | 5 | 172 | 14 | 9 | 0.9247 | 0.9503 | 0.9373 |
| gemma-3-27b | plain-k2 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| gemma-3-27b | plain-k4 | Global | 5 | 5 | 11221 | 1355 | 4136 | 0.8923 | 0.7307 | 0.8034 |
| gemma-3-27b | plain-k4 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| gemma-3-27b | plain-k4 | INST | 5 | 5 | 11017 | 1337 | 4110 | 0.8918 | 0.7283 | 0.8018 |
| gemma-3-27b | plain-k4 | PROP | 5 | 5 | 172 | 15 | 9 | 0.9198 | 0.9503 | 0.9348 |
| gemma-3-27b | plain-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| llama-3-1-70b | plain-k0 | Global | 5 | 5 | 11211 | 1350 | 4146 | 0.8925 | 0.7300 | 0.8031 |
| llama-3-1-70b | plain-k0 | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| llama-3-1-70b | plain-k0 | INST | 5 | 5 | 11009 | 1336 | 4118 | 0.8918 | 0.7278 | 0.8015 |
| llama-3-1-70b | plain-k0 | PROP | 5 | 5 | 172 | 12 | 9 | 0.9348 | 0.9503 | 0.9425 |
| llama-3-1-70b | plain-k0 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| llama-3-1-70b | plain-k2 | Global | 5 | 5 | 11217 | 1352 | 4140 | 0.8924 | 0.7304 | 0.8033 |
| llama-3-1-70b | plain-k2 | CLS | 5 | 5 | 31 | 4 | 18 | 0.8857 | 0.6327 | 0.7381 |
| llama-3-1-70b | plain-k2 | INST | 5 | 5 | 11014 | 1336 | 4113 | 0.8918 | 0.7281 | 0.8017 |
| llama-3-1-70b | plain-k2 | PROP | 5 | 5 | 172 | 12 | 9 | 0.9348 | 0.9503 | 0.9425 |
| llama-3-1-70b | plain-k2 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| llama-3-1-70b | plain-k4 | Global | 5 | 5 | 11220 | 1351 | 4137 | 0.8925 | 0.7306 | 0.8035 |
| llama-3-1-70b | plain-k4 | CLS | 5 | 5 | 32 | 4 | 17 | 0.8889 | 0.6531 | 0.7529 |
| llama-3-1-70b | plain-k4 | INST | 5 | 5 | 11016 | 1336 | 4111 | 0.8918 | 0.7282 | 0.8018 |
| llama-3-1-70b | plain-k4 | PROP | 5 | 5 | 172 | 11 | 9 | 0.9399 | 0.9503 | 0.9451 |
| llama-3-1-70b | plain-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| mistral-small-3-2-24b | plain-k0 | Global | 5 | 5 | 11201 | 1348 | 4156 | 0.8926 | 0.7294 | 0.8028 |
| mistral-small-3-2-24b | plain-k0 | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| mistral-small-3-2-24b | plain-k0 | INST | 5 | 5 | 10999 | 1336 | 4128 | 0.8917 | 0.7271 | 0.8010 |
| mistral-small-3-2-24b | plain-k0 | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| mistral-small-3-2-24b | plain-k0 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| mistral-small-3-2-24b | plain-k2 | Global | 5 | 5 | 11219 | 1349 | 4138 | 0.8927 | 0.7305 | 0.8035 |
| mistral-small-3-2-24b | plain-k2 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| mistral-small-3-2-24b | plain-k2 | INST | 5 | 5 | 11015 | 1337 | 4112 | 0.8918 | 0.7282 | 0.8017 |
| mistral-small-3-2-24b | plain-k2 | PROP | 5 | 5 | 172 | 9 | 9 | 0.9503 | 0.9503 | 0.9503 |
| mistral-small-3-2-24b | plain-k2 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| mistral-small-3-2-24b | plain-k4 | Global | 5 | 5 | 11223 | 1350 | 4134 | 0.8926 | 0.7308 | 0.8037 |
| mistral-small-3-2-24b | plain-k4 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| mistral-small-3-2-24b | plain-k4 | INST | 5 | 5 | 11019 | 1338 | 4108 | 0.8917 | 0.7284 | 0.8018 |
| mistral-small-3-2-24b | plain-k4 | PROP | 5 | 5 | 172 | 9 | 9 | 0.9503 | 0.9503 | 0.9503 |
| mistral-small-3-2-24b | plain-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-235b | plain-k0 | Global | 5 | 5 | 11199 | 1347 | 4158 | 0.8926 | 0.7292 | 0.8027 |
| qwen3-235b | plain-k0 | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| qwen3-235b | plain-k0 | INST | 5 | 5 | 10997 | 1336 | 4130 | 0.8917 | 0.7270 | 0.8009 |
| qwen3-235b | plain-k0 | PROP | 5 | 5 | 172 | 9 | 9 | 0.9503 | 0.9503 | 0.9503 |
| qwen3-235b | plain-k0 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-235b | plain-k2 | Global | 5 | 5 | 11214 | 1349 | 4143 | 0.8926 | 0.7302 | 0.8033 |
| qwen3-235b | plain-k2 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-235b | plain-k2 | INST | 5 | 5 | 11010 | 1336 | 4117 | 0.8918 | 0.7278 | 0.8015 |
| qwen3-235b | plain-k2 | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-235b | plain-k2 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-235b | plain-k4 | Global | 5 | 5 | 11212 | 1349 | 4145 | 0.8926 | 0.7301 | 0.8032 |
| qwen3-235b | plain-k4 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-235b | plain-k4 | INST | 5 | 5 | 11008 | 1336 | 4119 | 0.8918 | 0.7277 | 0.8014 |
| qwen3-235b | plain-k4 | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-235b | plain-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-5-122b | plain-k0 | Global | 5 | 5 | 11215 | 1348 | 4142 | 0.8927 | 0.7303 | 0.8034 |
| qwen3-5-122b | plain-k0 | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| qwen3-5-122b | plain-k0 | INST | 5 | 5 | 11013 | 1336 | 4114 | 0.8918 | 0.7280 | 0.8016 |
| qwen3-5-122b | plain-k0 | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-5-122b | plain-k0 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-5-122b | plain-k2 | Global | 5 | 5 | 11215 | 1349 | 4142 | 0.8926 | 0.7303 | 0.8033 |
| qwen3-5-122b | plain-k2 | CLS | 5 | 5 | 31 | 3 | 18 | 0.9118 | 0.6327 | 0.7470 |
| qwen3-5-122b | plain-k2 | INST | 5 | 5 | 11012 | 1336 | 4115 | 0.8918 | 0.7280 | 0.8016 |
| qwen3-5-122b | plain-k2 | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-5-122b | plain-k2 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-5-122b | plain-k4 | Global | 5 | 5 | 11216 | 1349 | 4141 | 0.8926 | 0.7304 | 0.8034 |
| qwen3-5-122b | plain-k4 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-5-122b | plain-k4 | INST | 5 | 5 | 11012 | 1336 | 4115 | 0.8918 | 0.7280 | 0.8016 |
| qwen3-5-122b | plain-k4 | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-5-122b | plain-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | plain-k0 | Global | 5 | 5 | 11214 | 1352 | 4143 | 0.8924 | 0.7302 | 0.8032 |
| qwen3-8b | plain-k0 | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| qwen3-8b | plain-k0 | INST | 5 | 5 | 11012 | 1336 | 4115 | 0.8918 | 0.7280 | 0.8016 |
| qwen3-8b | plain-k0 | PROP | 5 | 5 | 172 | 14 | 9 | 0.9247 | 0.9503 | 0.9373 |
| qwen3-8b | plain-k0 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | plain-k2 | Global | 5 | 5 | 11203 | 1348 | 4154 | 0.8926 | 0.7295 | 0.8029 |
| qwen3-8b | plain-k2 | CLS | 5 | 5 | 31 | 2 | 18 | 0.9394 | 0.6327 | 0.7561 |
| qwen3-8b | plain-k2 | INST | 5 | 5 | 11000 | 1336 | 4127 | 0.8917 | 0.7272 | 0.8011 |
| qwen3-8b | plain-k2 | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-8b | plain-k2 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | plain-k4 | Global | 5 | 5 | 11205 | 1348 | 4152 | 0.8926 | 0.7296 | 0.8029 |
| qwen3-8b | plain-k4 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-8b | plain-k4 | INST | 5 | 5 | 11001 | 1336 | 4126 | 0.8917 | 0.7272 | 0.8011 |
| qwen3-8b | plain-k4 | PROP | 5 | 5 | 172 | 9 | 9 | 0.9503 | 0.9503 | 0.9503 |
| qwen3-8b | plain-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| marvelcinematicuniverse-marvel-deepseek-v4-flash-parasail-off-plain-k0-r0-31a770ed | not_run |  |
| marvelcinematicuniverse-marvel-deepseek-v4-flash-parasail-off-plain-k2-r0-5a6a65e7 | not_run |  |
| marvelcinematicuniverse-marvel-deepseek-v4-flash-parasail-off-plain-k4-r0-92f192ea | not_run |  |
| memoryalpha-memorybeta-deepseek-v4-flash-parasail-off-plain-k0-r0-e8e77cef | not_run |  |
| memoryalpha-memorybeta-deepseek-v4-flash-parasail-off-plain-k2-r0-99894603 | not_run |  |
| memoryalpha-memorybeta-deepseek-v4-flash-parasail-off-plain-k4-r0-102b44e3 | not_run |  |
| memoryalpha-stexpanded-deepseek-v4-flash-parasail-off-plain-k0-r0-d35d30fb | not_run |  |
| memoryalpha-stexpanded-deepseek-v4-flash-parasail-off-plain-k2-r0-0b6a1198 | not_run |  |
| memoryalpha-stexpanded-deepseek-v4-flash-parasail-off-plain-k4-r0-4169f0eb | not_run |  |
| starwars-swg-deepseek-v4-flash-parasail-off-plain-k0-r0-72ff4dec | not_run |  |
| starwars-swg-deepseek-v4-flash-parasail-off-plain-k2-r0-4913a932 | not_run |  |
| starwars-swg-deepseek-v4-flash-parasail-off-plain-k4-r0-a3209abb | not_run |  |
| starwars-swtor-deepseek-v4-flash-parasail-off-plain-k0-r0-b81f0393 | not_run |  |
| starwars-swtor-deepseek-v4-flash-parasail-off-plain-k2-r0-16ff7e81 | not_run |  |
| starwars-swtor-deepseek-v4-flash-parasail-off-plain-k4-r0-1a70eb69 | not_run |  |

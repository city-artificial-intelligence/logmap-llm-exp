# Results: collective-anchors-knowledge-graph

Coverage: **15/40 (37.5%)**

| Status | Jobs |
|---|---:|
| not_run | 25 |
| success | 15 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | ca-k4 | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | ca-k4 | 0 | 5 | 0.0% |
| gemma-3-27b | ca-k4 | 5 | 5 | 100.0% |
| llama-3-1-70b | ca-k4 | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | ca-k4 | 0 | 5 | 0.0% |
| qwen3-235b | ca-k4 | 0 | 5 | 0.0% |
| qwen3-5-122b | ca-k4 | 0 | 5 | 0.0% |
| qwen3-8b | ca-k4 | 5 | 5 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | ca-k4 | 0.8923 | 0.7307 | 0.8034 | 0.8992 | 0.7018 | 0.7837 | 0.7200 | 0.7481 | 0.7202 | 0.9352 | 0.9412 | 0.8617 |
| llama-3-1-70b | ca-k4 | 0.8922 | 0.7305 | 0.8033 | 0.8988 | 0.7016 | 0.7835 | 0.6571 | 0.7141 | 0.6697 | 0.8926 | 0.8129 | 0.7838 |
| mistral-small-3-2-24b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | ca-k4 | 0.8926 | 0.7292 | 0.8026 | 0.8991 | 0.6991 | 0.7819 | 0.7400 | 0.4378 | 0.5181 | 0.5472 | 0.9824 | 0.5252 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma-3-27b | ca-k4 | Global | 5 | 5 | 11221 | 1355 | 4136 | 0.8923 | 0.7307 | 0.8034 |
| gemma-3-27b | ca-k4 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| gemma-3-27b | ca-k4 | INST | 5 | 5 | 11017 | 1337 | 4110 | 0.8918 | 0.7283 | 0.8018 |
| gemma-3-27b | ca-k4 | PROP | 5 | 5 | 172 | 15 | 9 | 0.9198 | 0.9503 | 0.9348 |
| gemma-3-27b | ca-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| llama-3-1-70b | ca-k4 | Global | 5 | 5 | 11218 | 1355 | 4139 | 0.8922 | 0.7305 | 0.8033 |
| llama-3-1-70b | ca-k4 | CLS | 5 | 5 | 32 | 4 | 17 | 0.8889 | 0.6531 | 0.7529 |
| llama-3-1-70b | ca-k4 | INST | 5 | 5 | 11014 | 1338 | 4113 | 0.8917 | 0.7281 | 0.8016 |
| llama-3-1-70b | ca-k4 | PROP | 5 | 5 | 172 | 13 | 9 | 0.9297 | 0.9503 | 0.9399 |
| llama-3-1-70b | ca-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | ca-k4 | Global | 5 | 5 | 11198 | 1348 | 4159 | 0.8926 | 0.7292 | 0.8026 |
| qwen3-8b | ca-k4 | CLS | 5 | 5 | 31 | 3 | 18 | 0.9118 | 0.6327 | 0.7470 |
| qwen3-8b | ca-k4 | INST | 5 | 5 | 10995 | 1336 | 4132 | 0.8917 | 0.7268 | 0.8009 |
| qwen3-8b | ca-k4 | PROP | 5 | 5 | 172 | 9 | 9 | 0.9503 | 0.9503 | 0.9503 |
| qwen3-8b | ca-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| marvelcinematicuniverse-marvel-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-c7c5f6c4 | not_run |  |
| marvelcinematicuniverse-marvel-gemini-2-5-flash-off-ca-k4-r0-51cb8cd2 | not_run |  |
| marvelcinematicuniverse-marvel-mistral-small-3-2-24b-ca-k4-r0-25a9a1d2 | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-235b-ca-k4-r0-5440084b | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-5-122b-ca-k4-r0-c925e0c8 | not_run |  |
| memoryalpha-memorybeta-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-c8cb1b21 | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-off-ca-k4-r0-01528995 | not_run |  |
| memoryalpha-memorybeta-mistral-small-3-2-24b-ca-k4-r0-a7534e40 | not_run |  |
| memoryalpha-memorybeta-qwen3-235b-ca-k4-r0-5d9e3604 | not_run |  |
| memoryalpha-memorybeta-qwen3-5-122b-ca-k4-r0-c6301e5c | not_run |  |
| memoryalpha-stexpanded-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-ab822695 | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-off-ca-k4-r0-9a07144b | not_run |  |
| memoryalpha-stexpanded-mistral-small-3-2-24b-ca-k4-r0-d672a66a | not_run |  |
| memoryalpha-stexpanded-qwen3-235b-ca-k4-r0-5ab9fd69 | not_run |  |
| memoryalpha-stexpanded-qwen3-5-122b-ca-k4-r0-4138dbc7 | not_run |  |
| starwars-swg-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-7a72eab9 | not_run |  |
| starwars-swg-gemini-2-5-flash-off-ca-k4-r0-1d2700cc | not_run |  |
| starwars-swg-mistral-small-3-2-24b-ca-k4-r0-b452c830 | not_run |  |
| starwars-swg-qwen3-235b-ca-k4-r0-dac8c599 | not_run |  |
| starwars-swg-qwen3-5-122b-ca-k4-r0-ec7c55be | not_run |  |
| starwars-swtor-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-575aae37 | not_run |  |
| starwars-swtor-gemini-2-5-flash-off-ca-k4-r0-1095d201 | not_run |  |
| starwars-swtor-mistral-small-3-2-24b-ca-k4-r0-6038f36b | not_run |  |
| starwars-swtor-qwen3-235b-ca-k4-r0-de689c90 | not_run |  |
| starwars-swtor-qwen3-5-122b-ca-k4-r0-2ade91bf | not_run |  |

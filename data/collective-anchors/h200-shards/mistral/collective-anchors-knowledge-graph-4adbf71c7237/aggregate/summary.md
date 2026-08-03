# Results: collective-anchors-knowledge-graph

Coverage: **5/40 (12.5%)**

| Status | Jobs |
|---|---:|
| not_run | 35 |
| success | 5 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | ca-k4 | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | ca-k4 | 0 | 5 | 0.0% |
| gemma-3-27b | ca-k4 | 0 | 5 | 0.0% |
| llama-3-1-70b | ca-k4 | 0 | 5 | 0.0% |
| mistral-small-3-2-24b | ca-k4 | 5 | 5 | 100.0% |
| qwen3-235b | ca-k4 | 0 | 5 | 0.0% |
| qwen3-5-122b | ca-k4 | 0 | 5 | 0.0% |
| qwen3-8b | ca-k4 | 0 | 5 | 0.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| mistral-small-3-2-24b | ca-k4 | 0.8925 | 0.7306 | 0.8035 | 0.8992 | 0.7018 | 0.7838 | 0.7333 | 0.7348 | 0.7258 | 0.9185 | 0.9588 | 0.8670 |
| qwen3-235b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| mistral-small-3-2-24b | ca-k4 | Global | 5 | 5 | 11220 | 1352 | 4137 | 0.8925 | 0.7306 | 0.8035 |
| mistral-small-3-2-24b | ca-k4 | CLS | 5 | 5 | 32 | 4 | 17 | 0.8889 | 0.6531 | 0.7529 |
| mistral-small-3-2-24b | ca-k4 | INST | 5 | 5 | 11016 | 1337 | 4111 | 0.8918 | 0.7282 | 0.8017 |
| mistral-small-3-2-24b | ca-k4 | PROP | 5 | 5 | 172 | 11 | 9 | 0.9399 | 0.9503 | 0.9451 |
| mistral-small-3-2-24b | ca-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| marvelcinematicuniverse-marvel-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-c7c5f6c4 | not_run |  |
| marvelcinematicuniverse-marvel-gemini-2-5-flash-off-ca-k4-r0-51cb8cd2 | not_run |  |
| marvelcinematicuniverse-marvel-gemma-3-27b-ca-k4-r0-9552adcd | not_run |  |
| marvelcinematicuniverse-marvel-llama-3-1-70b-ca-k4-r0-8dc5e7d1 | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-235b-ca-k4-r0-5440084b | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-5-122b-ca-k4-r0-c925e0c8 | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-8b-ca-k4-r0-d899d9b1 | not_run |  |
| memoryalpha-memorybeta-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-c8cb1b21 | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-off-ca-k4-r0-01528995 | not_run |  |
| memoryalpha-memorybeta-gemma-3-27b-ca-k4-r0-f67bc258 | not_run |  |
| memoryalpha-memorybeta-llama-3-1-70b-ca-k4-r0-5d8e61f6 | not_run |  |
| memoryalpha-memorybeta-qwen3-235b-ca-k4-r0-5d9e3604 | not_run |  |
| memoryalpha-memorybeta-qwen3-5-122b-ca-k4-r0-c6301e5c | not_run |  |
| memoryalpha-memorybeta-qwen3-8b-ca-k4-r0-d1644660 | not_run |  |
| memoryalpha-stexpanded-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-ab822695 | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-off-ca-k4-r0-9a07144b | not_run |  |
| memoryalpha-stexpanded-gemma-3-27b-ca-k4-r0-7a052a88 | not_run |  |
| memoryalpha-stexpanded-llama-3-1-70b-ca-k4-r0-45572867 | not_run |  |
| memoryalpha-stexpanded-qwen3-235b-ca-k4-r0-5ab9fd69 | not_run |  |
| memoryalpha-stexpanded-qwen3-5-122b-ca-k4-r0-4138dbc7 | not_run |  |
| memoryalpha-stexpanded-qwen3-8b-ca-k4-r0-17a83b54 | not_run |  |
| starwars-swg-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-7a72eab9 | not_run |  |
| starwars-swg-gemini-2-5-flash-off-ca-k4-r0-1d2700cc | not_run |  |
| starwars-swg-gemma-3-27b-ca-k4-r0-9cd57fb7 | not_run |  |
| starwars-swg-llama-3-1-70b-ca-k4-r0-dcc09c67 | not_run |  |
| starwars-swg-qwen3-235b-ca-k4-r0-dac8c599 | not_run |  |
| starwars-swg-qwen3-5-122b-ca-k4-r0-ec7c55be | not_run |  |
| starwars-swg-qwen3-8b-ca-k4-r0-6154f746 | not_run |  |
| starwars-swtor-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-575aae37 | not_run |  |
| starwars-swtor-gemini-2-5-flash-off-ca-k4-r0-1095d201 | not_run |  |
| starwars-swtor-gemma-3-27b-ca-k4-r0-135ecc6c | not_run |  |
| starwars-swtor-llama-3-1-70b-ca-k4-r0-2534321f | not_run |  |
| starwars-swtor-qwen3-235b-ca-k4-r0-de689c90 | not_run |  |
| starwars-swtor-qwen3-5-122b-ca-k4-r0-2ade91bf | not_run |  |
| starwars-swtor-qwen3-8b-ca-k4-r0-a15de5ce | not_run |  |

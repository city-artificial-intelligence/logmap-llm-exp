# Results: runtime-donor-v1-knowledge-graph

Coverage: **5/40 (12.5%)**

| Status | Jobs |
|---|---:|
| not_run | 35 |
| success | 5 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | rt-k4 | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | rt-k4 | 0 | 5 | 0.0% |
| gemma-3-27b | rt-k4 | 0 | 5 | 0.0% |
| llama-3-1-70b | rt-k4 | 0 | 5 | 0.0% |
| mistral-small-3-2-24b | rt-k4 | 5 | 5 | 100.0% |
| qwen3-235b | rt-k4 | 0 | 5 | 0.0% |
| qwen3-5-122b | rt-k4 | 0 | 5 | 0.0% |
| qwen3-8b | rt-k4 | 0 | 5 | 0.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| mistral-small-3-2-24b | rt-k4 | 0.8926 | 0.7308 | 0.8037 | 0.8993 | 0.7024 | 0.7841 | 0.7474 | 0.7570 | 0.7487 | 0.9463 | 0.9706 | 0.9095 |
| qwen3-235b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| mistral-small-3-2-24b | rt-k4 | Global | 5 | 5 | 11223 | 1350 | 4134 | 0.8926 | 0.7308 | 0.8037 |
| mistral-small-3-2-24b | rt-k4 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| mistral-small-3-2-24b | rt-k4 | INST | 5 | 5 | 11019 | 1338 | 4108 | 0.8917 | 0.7284 | 0.8018 |
| mistral-small-3-2-24b | rt-k4 | PROP | 5 | 5 | 172 | 9 | 9 | 0.9503 | 0.9503 | 0.9503 |
| mistral-small-3-2-24b | rt-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| marvelcinematicuniverse-marvel-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-225ea9f2 | not_run |  |
| marvelcinematicuniverse-marvel-gemini-2-5-flash-off-rt-k4-r0-86676a5c | not_run |  |
| marvelcinematicuniverse-marvel-gemma-3-27b-rt-k4-r0-8604cf47 | not_run |  |
| marvelcinematicuniverse-marvel-llama-3-1-70b-rt-k4-r0-df7ed3c5 | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-235b-rt-k4-r0-b11fb9c2 | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-5-122b-rt-k4-r0-47714d5b | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-8b-rt-k4-r0-f092cb19 | not_run |  |
| memoryalpha-memorybeta-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-d5526719 | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-off-rt-k4-r0-0d05796b | not_run |  |
| memoryalpha-memorybeta-gemma-3-27b-rt-k4-r0-afc60792 | not_run |  |
| memoryalpha-memorybeta-llama-3-1-70b-rt-k4-r0-d5b1d98b | not_run |  |
| memoryalpha-memorybeta-qwen3-235b-rt-k4-r0-8963f936 | not_run |  |
| memoryalpha-memorybeta-qwen3-5-122b-rt-k4-r0-ddad6dbe | not_run |  |
| memoryalpha-memorybeta-qwen3-8b-rt-k4-r0-834b1e03 | not_run |  |
| memoryalpha-stexpanded-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-d56e0326 | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-off-rt-k4-r0-aaa842fa | not_run |  |
| memoryalpha-stexpanded-gemma-3-27b-rt-k4-r0-959c75b5 | not_run |  |
| memoryalpha-stexpanded-llama-3-1-70b-rt-k4-r0-320a69d4 | not_run |  |
| memoryalpha-stexpanded-qwen3-235b-rt-k4-r0-b0b8a8d4 | not_run |  |
| memoryalpha-stexpanded-qwen3-5-122b-rt-k4-r0-a9ff3bb6 | not_run |  |
| memoryalpha-stexpanded-qwen3-8b-rt-k4-r0-acca9dde | not_run |  |
| starwars-swg-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-9997af39 | not_run |  |
| starwars-swg-gemini-2-5-flash-off-rt-k4-r0-fd2fbfc7 | not_run |  |
| starwars-swg-gemma-3-27b-rt-k4-r0-aa72d831 | not_run |  |
| starwars-swg-llama-3-1-70b-rt-k4-r0-4685c8b0 | not_run |  |
| starwars-swg-qwen3-235b-rt-k4-r0-aacb887d | not_run |  |
| starwars-swg-qwen3-5-122b-rt-k4-r0-b5782f2a | not_run |  |
| starwars-swg-qwen3-8b-rt-k4-r0-85a35be4 | not_run |  |
| starwars-swtor-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-fadb4b04 | not_run |  |
| starwars-swtor-gemini-2-5-flash-off-rt-k4-r0-17f0cf93 | not_run |  |
| starwars-swtor-gemma-3-27b-rt-k4-r0-f71d8e49 | not_run |  |
| starwars-swtor-llama-3-1-70b-rt-k4-r0-e4d930b5 | not_run |  |
| starwars-swtor-qwen3-235b-rt-k4-r0-8bbc5dc2 | not_run |  |
| starwars-swtor-qwen3-5-122b-rt-k4-r0-a8c3037d | not_run |  |
| starwars-swtor-qwen3-8b-rt-k4-r0-27a54f9c | not_run |  |

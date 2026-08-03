# Results: static-fewshot-knowledge-graph

Coverage: **5/30 (16.7%)**

| Status | Jobs |
|---|---:|
| not_run | 25 |
| success | 5 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| gemini-2-5-flash-off | static-k4 | 5 | 5 | 100.0% |
| gemma-3-27b | static-k4 | 0 | 5 | 0.0% |
| llama-3-1-70b | static-k4 | 0 | 5 | 0.0% |
| mistral-small-3-2-24b | static-k4 | 0 | 5 | 0.0% |
| qwen3-5-122b | static-k4 | 0 | 5 | 0.0% |
| qwen3-8b | static-k4 | 0 | 5 | 0.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | static-k4 | 0.8927 | 0.7302 | 0.8033 | 0.8991 | 0.7014 | 0.7834 | 0.7636 | 0.6533 | 0.6985 | 0.8167 | 0.8882 | 0.8020 |
| gemma-3-27b | static-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | static-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| mistral-small-3-2-24b | static-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | static-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | static-k4 |  |  |  |  |  |  |  |  |  |  |  |  |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | static-k4 | Global | 5 | 5 | 11213 | 1348 | 4144 | 0.8927 | 0.7302 | 0.8033 |
| gemini-2-5-flash-off | static-k4 | CLS | 5 | 5 | 31 | 2 | 18 | 0.9394 | 0.6327 | 0.7561 |
| gemini-2-5-flash-off | static-k4 | INST | 5 | 5 | 11010 | 1336 | 4117 | 0.8918 | 0.7278 | 0.8015 |
| gemini-2-5-flash-off | static-k4 | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| gemini-2-5-flash-off | static-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| marvelcinematicuniverse-marvel-gemma-3-27b-static-k4-r0-763feecf | not_run |  |
| marvelcinematicuniverse-marvel-llama-3-1-70b-static-k4-r0-3f617312 | not_run |  |
| marvelcinematicuniverse-marvel-mistral-small-3-2-24b-static-k4-r0-a07a77af | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-5-122b-static-k4-r0-705ade62 | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-8b-static-k4-r0-2b0f3540 | not_run |  |
| memoryalpha-memorybeta-gemma-3-27b-static-k4-r0-2b7367e7 | not_run |  |
| memoryalpha-memorybeta-llama-3-1-70b-static-k4-r0-3230b88c | not_run |  |
| memoryalpha-memorybeta-mistral-small-3-2-24b-static-k4-r0-11193b9a | not_run |  |
| memoryalpha-memorybeta-qwen3-5-122b-static-k4-r0-f29b42c1 | not_run |  |
| memoryalpha-memorybeta-qwen3-8b-static-k4-r0-23fba624 | not_run |  |
| memoryalpha-stexpanded-gemma-3-27b-static-k4-r0-e4b19f9d | not_run |  |
| memoryalpha-stexpanded-llama-3-1-70b-static-k4-r0-9bdfe08b | not_run |  |
| memoryalpha-stexpanded-mistral-small-3-2-24b-static-k4-r0-273aae55 | not_run |  |
| memoryalpha-stexpanded-qwen3-5-122b-static-k4-r0-88a6930f | not_run |  |
| memoryalpha-stexpanded-qwen3-8b-static-k4-r0-de60e675 | not_run |  |
| starwars-swg-gemma-3-27b-static-k4-r0-c3347651 | not_run |  |
| starwars-swg-llama-3-1-70b-static-k4-r0-aaada717 | not_run |  |
| starwars-swg-mistral-small-3-2-24b-static-k4-r0-97be7f0c | not_run |  |
| starwars-swg-qwen3-5-122b-static-k4-r0-699b9e75 | not_run |  |
| starwars-swg-qwen3-8b-static-k4-r0-5e44f587 | not_run |  |
| starwars-swtor-gemma-3-27b-static-k4-r0-bbab602c | not_run |  |
| starwars-swtor-llama-3-1-70b-static-k4-r0-ab409e1a | not_run |  |
| starwars-swtor-mistral-small-3-2-24b-static-k4-r0-ae2f653b | not_run |  |
| starwars-swtor-qwen3-5-122b-static-k4-r0-ec8df846 | not_run |  |
| starwars-swtor-qwen3-8b-static-k4-r0-170811bb | not_run |  |

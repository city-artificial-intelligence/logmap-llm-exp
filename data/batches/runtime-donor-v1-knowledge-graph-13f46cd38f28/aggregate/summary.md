# Results: runtime-donor-v1-knowledge-graph

Coverage: **25/40 (62.5%)**

| Status | Jobs |
|---|---:|
| not_run | 15 |
| success | 25 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | rt-k4 | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | rt-k4 | 5 | 5 | 100.0% |
| gemma-3-27b | rt-k4 | 5 | 5 | 100.0% |
| llama-3-1-70b | rt-k4 | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | rt-k4 | 0 | 5 | 0.0% |
| qwen3-235b | rt-k4 | 0 | 5 | 0.0% |
| qwen3-5-122b | rt-k4 | 5 | 5 | 100.0% |
| qwen3-8b | rt-k4 | 5 | 5 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | rt-k4 | 0.8925 | 0.7305 | 0.8035 | 0.8991 | 0.7020 | 0.7838 | 0.6745 | 0.7156 | 0.6850 | 0.8944 | 0.9306 | 0.8077 |
| gemma-3-27b | rt-k4 | 0.8923 | 0.7307 | 0.8034 | 0.8989 | 0.7020 | 0.7838 | 0.6273 | 0.7422 | 0.6597 | 0.9278 | 0.8729 | 0.7690 |
| llama-3-1-70b | rt-k4 | 0.8925 | 0.7306 | 0.8035 | 0.8991 | 0.7020 | 0.7838 | 0.6778 | 0.7289 | 0.6926 | 0.9111 | 0.9306 | 0.8243 |
| mistral-small-3-2-24b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | rt-k4 | 0.8926 | 0.7304 | 0.8034 | 0.8991 | 0.7016 | 0.7836 | 0.6933 | 0.7007 | 0.6852 | 0.8759 | 0.9424 | 0.8039 |
| qwen3-8b | rt-k4 | 0.8926 | 0.7296 | 0.8029 | 0.8990 | 0.6998 | 0.7824 | 0.7000 | 0.5074 | 0.5496 | 0.6343 | 0.9482 | 0.5696 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | rt-k4 | Global | 5 | 5 | 11219 | 1351 | 4138 | 0.8925 | 0.7305 | 0.8035 |
| gemini-2-5-flash-off | rt-k4 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| gemini-2-5-flash-off | rt-k4 | INST | 5 | 5 | 11015 | 1337 | 4112 | 0.8918 | 0.7282 | 0.8017 |
| gemini-2-5-flash-off | rt-k4 | PROP | 5 | 5 | 172 | 11 | 9 | 0.9399 | 0.9503 | 0.9451 |
| gemini-2-5-flash-off | rt-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| gemma-3-27b | rt-k4 | Global | 5 | 5 | 11221 | 1355 | 4136 | 0.8923 | 0.7307 | 0.8034 |
| gemma-3-27b | rt-k4 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| gemma-3-27b | rt-k4 | INST | 5 | 5 | 11017 | 1338 | 4110 | 0.8917 | 0.7283 | 0.8018 |
| gemma-3-27b | rt-k4 | PROP | 5 | 5 | 172 | 14 | 9 | 0.9247 | 0.9503 | 0.9373 |
| gemma-3-27b | rt-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| llama-3-1-70b | rt-k4 | Global | 5 | 5 | 11220 | 1351 | 4137 | 0.8925 | 0.7306 | 0.8035 |
| llama-3-1-70b | rt-k4 | CLS | 5 | 5 | 32 | 4 | 17 | 0.8889 | 0.6531 | 0.7529 |
| llama-3-1-70b | rt-k4 | INST | 5 | 5 | 11016 | 1336 | 4111 | 0.8918 | 0.7282 | 0.8018 |
| llama-3-1-70b | rt-k4 | PROP | 5 | 5 | 172 | 11 | 9 | 0.9399 | 0.9503 | 0.9451 |
| llama-3-1-70b | rt-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-5-122b | rt-k4 | Global | 5 | 5 | 11217 | 1349 | 4140 | 0.8926 | 0.7304 | 0.8034 |
| qwen3-5-122b | rt-k4 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-5-122b | rt-k4 | INST | 5 | 5 | 11013 | 1336 | 4114 | 0.8918 | 0.7280 | 0.8016 |
| qwen3-5-122b | rt-k4 | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-5-122b | rt-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | rt-k4 | Global | 5 | 5 | 11205 | 1348 | 4152 | 0.8926 | 0.7296 | 0.8029 |
| qwen3-8b | rt-k4 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-8b | rt-k4 | INST | 5 | 5 | 11001 | 1336 | 4126 | 0.8917 | 0.7272 | 0.8011 |
| qwen3-8b | rt-k4 | PROP | 5 | 5 | 172 | 9 | 9 | 0.9503 | 0.9503 | 0.9503 |
| qwen3-8b | rt-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| marvelcinematicuniverse-marvel-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-225ea9f2 | not_run |  |
| marvelcinematicuniverse-marvel-mistral-small-3-2-24b-rt-k4-r0-8b1d37da | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-235b-rt-k4-r0-b11fb9c2 | not_run |  |
| memoryalpha-memorybeta-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-d5526719 | not_run |  |
| memoryalpha-memorybeta-mistral-small-3-2-24b-rt-k4-r0-dde8371f | not_run |  |
| memoryalpha-memorybeta-qwen3-235b-rt-k4-r0-8963f936 | not_run |  |
| memoryalpha-stexpanded-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-d56e0326 | not_run |  |
| memoryalpha-stexpanded-mistral-small-3-2-24b-rt-k4-r0-d419ae56 | not_run |  |
| memoryalpha-stexpanded-qwen3-235b-rt-k4-r0-b0b8a8d4 | not_run |  |
| starwars-swg-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-9997af39 | not_run |  |
| starwars-swg-mistral-small-3-2-24b-rt-k4-r0-7258ab1c | not_run |  |
| starwars-swg-qwen3-235b-rt-k4-r0-aacb887d | not_run |  |
| starwars-swtor-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-fadb4b04 | not_run |  |
| starwars-swtor-mistral-small-3-2-24b-rt-k4-r0-6db1e98f | not_run |  |
| starwars-swtor-qwen3-235b-rt-k4-r0-8bbc5dc2 | not_run |  |

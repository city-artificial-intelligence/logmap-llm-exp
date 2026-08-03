# Results: rag-runtime-knowledge-graph

Coverage: **25/140 (17.9%)**

| Status | Jobs |
|---|---:|
| degraded | 2 |
| not_run | 115 |
| success | 23 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-parasail-high | runtime-rag-k2-minilm | 5 | 5 | 100.0% |
| deepseek-v4-flash-parasail-high | runtime-rag-k2-sapbert | 5 | 5 | 100.0% |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-minilm | 5 | 5 | 100.0% |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-sapbert | 5 | 5 | 100.0% |
| deepseek-v4-flash-parasail-off | runtime-rag-k4-sapbert | 5 | 5 | 100.0% |
| gemini-2-5-flash-off | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | runtime-rag-k4-sapbert | 0 | 5 | 0.0% |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| gemma-3-27b | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| gemma-3-27b | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| gemma-3-27b | runtime-rag-k4-sapbert | 0 | 5 | 0.0% |
| llama-3-1-70b | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| llama-3-1-70b | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| llama-3-1-70b | runtime-rag-k4-sapbert | 0 | 5 | 0.0% |
| mistral-small-3-2-24b | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| mistral-small-3-2-24b | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| mistral-small-3-2-24b | runtime-rag-k4-sapbert | 0 | 5 | 0.0% |
| qwen3-235b | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| qwen3-235b | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| qwen3-235b | runtime-rag-k4-sapbert | 0 | 5 | 0.0% |
| qwen3-5-122b | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| qwen3-5-122b | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| qwen3-5-122b | runtime-rag-k4-sapbert | 0 | 5 | 0.0% |
| qwen3-8b | runtime-rag-k2-minilm | 0 | 5 | 0.0% |
| qwen3-8b | runtime-rag-k2-sapbert | 0 | 5 | 0.0% |
| qwen3-8b | runtime-rag-k4-sapbert | 0 | 5 | 0.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-high | runtime-rag-k2-minilm | 0.8925 | 0.7290 | 0.8026 | 0.8989 | 0.6990 | 0.7819 | 0.6762 | 0.4111 | 0.4570 | 0.5139 | 0.9482 | 0.4492 |
| deepseek-v4-flash-parasail-high | runtime-rag-k2-sapbert | 0.8925 | 0.7291 | 0.8026 | 0.8989 | 0.6989 | 0.7818 | 0.6889 | 0.4304 | 0.4725 | 0.5380 | 0.9482 | 0.4733 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-minilm | 0.8926 | 0.7298 | 0.8031 | 0.8990 | 0.7005 | 0.7828 | 0.6970 | 0.6163 | 0.6285 | 0.7704 | 0.9482 | 0.7057 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-sapbert | 0.8926 | 0.7299 | 0.8031 | 0.8990 | 0.7005 | 0.7828 | 0.6872 | 0.6296 | 0.6329 | 0.7870 | 0.9424 | 0.7150 |
| deepseek-v4-flash-parasail-off | runtime-rag-k4-sapbert | 0.8926 | 0.7298 | 0.8030 | 0.8990 | 0.7003 | 0.7827 | 0.6872 | 0.6222 | 0.6259 | 0.7778 | 0.9424 | 0.7057 |
| gemini-2-5-flash-off | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | runtime-rag-k4-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k4-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | runtime-rag-k4-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| mistral-small-3-2-24b | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| mistral-small-3-2-24b | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| mistral-small-3-2-24b | runtime-rag-k4-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | runtime-rag-k4-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | runtime-rag-k4-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | runtime-rag-k2-minilm |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | runtime-rag-k2-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | runtime-rag-k4-sapbert |  |  |  |  |  |  |  |  |  |  |  |  |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-high | runtime-rag-k2-minilm | Global | 5 | 5 | 11196 | 1348 | 4161 | 0.8925 | 0.7290 | 0.8026 |
| deepseek-v4-flash-parasail-high | runtime-rag-k2-minilm | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| deepseek-v4-flash-parasail-high | runtime-rag-k2-minilm | INST | 5 | 5 | 10994 | 1336 | 4133 | 0.8916 | 0.7268 | 0.8008 |
| deepseek-v4-flash-parasail-high | runtime-rag-k2-minilm | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| deepseek-v4-flash-parasail-high | runtime-rag-k2-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| deepseek-v4-flash-parasail-high | runtime-rag-k2-sapbert | Global | 5 | 5 | 11197 | 1348 | 4160 | 0.8925 | 0.7291 | 0.8026 |
| deepseek-v4-flash-parasail-high | runtime-rag-k2-sapbert | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| deepseek-v4-flash-parasail-high | runtime-rag-k2-sapbert | INST | 5 | 5 | 10995 | 1336 | 4132 | 0.8917 | 0.7268 | 0.8009 |
| deepseek-v4-flash-parasail-high | runtime-rag-k2-sapbert | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| deepseek-v4-flash-parasail-high | runtime-rag-k2-sapbert | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-minilm | Global | 5 | 5 | 11208 | 1348 | 4149 | 0.8926 | 0.7298 | 0.8031 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-minilm | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-minilm | INST | 5 | 5 | 11006 | 1336 | 4121 | 0.8918 | 0.7276 | 0.8013 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-minilm | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-minilm | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-sapbert | Global | 5 | 5 | 11209 | 1349 | 4148 | 0.8926 | 0.7299 | 0.8031 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-sapbert | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-sapbert | INST | 5 | 5 | 11005 | 1336 | 4122 | 0.8917 | 0.7275 | 0.8013 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-sapbert | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2-sapbert | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| deepseek-v4-flash-parasail-off | runtime-rag-k4-sapbert | Global | 5 | 5 | 11208 | 1349 | 4149 | 0.8926 | 0.7298 | 0.8030 |
| deepseek-v4-flash-parasail-off | runtime-rag-k4-sapbert | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| deepseek-v4-flash-parasail-off | runtime-rag-k4-sapbert | INST | 5 | 5 | 11004 | 1336 | 4123 | 0.8917 | 0.7274 | 0.8013 |
| deepseek-v4-flash-parasail-off | runtime-rag-k4-sapbert | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| deepseek-v4-flash-parasail-off | runtime-rag-k4-sapbert | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| marvelcinematicuniverse-marvel-gemini-2-5-flash-off-runtime-rag-k2-minilm-r0-64de9d6e | not_run |  |
| marvelcinematicuniverse-marvel-gemini-2-5-flash-off-runtime-rag-k2-sapbert-r0-8d754582 | not_run |  |
| marvelcinematicuniverse-marvel-gemini-2-5-flash-off-runtime-rag-k4-sapbert-r0-2556b305 | not_run |  |
| marvelcinematicuniverse-marvel-gemini-2-5-flash-reason-1028-runtime-rag-k2-minilm-r0-61bea5fc | not_run |  |
| marvelcinematicuniverse-marvel-gemini-2-5-flash-reason-1028-runtime-rag-k2-sapbert-r0-17096021 | not_run |  |
| marvelcinematicuniverse-marvel-gemma-3-27b-runtime-rag-k2-minilm-r0-5c8c913a | not_run |  |
| marvelcinematicuniverse-marvel-gemma-3-27b-runtime-rag-k2-sapbert-r0-beafef11 | not_run |  |
| marvelcinematicuniverse-marvel-gemma-3-27b-runtime-rag-k4-sapbert-r0-8276fae1 | not_run |  |
| marvelcinematicuniverse-marvel-llama-3-1-70b-runtime-rag-k2-minilm-r0-9302c9f3 | not_run |  |
| marvelcinematicuniverse-marvel-llama-3-1-70b-runtime-rag-k2-sapbert-r0-e4ff64ff | not_run |  |
| marvelcinematicuniverse-marvel-llama-3-1-70b-runtime-rag-k4-sapbert-r0-8f6c13da | not_run |  |
| marvelcinematicuniverse-marvel-mistral-small-3-2-24b-runtime-rag-k2-minilm-r0-e4754c1b | not_run |  |
| marvelcinematicuniverse-marvel-mistral-small-3-2-24b-runtime-rag-k2-sapbert-r0-a417505c | not_run |  |
| marvelcinematicuniverse-marvel-mistral-small-3-2-24b-runtime-rag-k4-sapbert-r0-4c71a4e6 | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-235b-runtime-rag-k2-minilm-r0-3b0bc0ad | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-235b-runtime-rag-k2-sapbert-r0-e1d145f9 | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-235b-runtime-rag-k4-sapbert-r0-50a5d353 | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-5-122b-runtime-rag-k2-minilm-r0-9fa07230 | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-5-122b-runtime-rag-k2-sapbert-r0-acb3779a | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-5-122b-runtime-rag-k4-sapbert-r0-42608dc9 | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-8b-runtime-rag-k2-minilm-r0-3e58ea0b | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-8b-runtime-rag-k2-sapbert-r0-af1c7bbc | not_run |  |
| marvelcinematicuniverse-marvel-qwen3-8b-runtime-rag-k4-sapbert-r0-eed42122 | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-off-runtime-rag-k2-minilm-r0-a7278d75 | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-off-runtime-rag-k2-sapbert-r0-3d8dca99 | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-off-runtime-rag-k4-sapbert-r0-0201187e | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-reason-1028-runtime-rag-k2-minilm-r0-c592d6a2 | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-reason-1028-runtime-rag-k2-sapbert-r0-47f7e25d | not_run |  |
| memoryalpha-memorybeta-gemma-3-27b-runtime-rag-k2-minilm-r0-f3cdfe8f | not_run |  |
| memoryalpha-memorybeta-gemma-3-27b-runtime-rag-k2-sapbert-r0-c1f6145a | not_run |  |
| memoryalpha-memorybeta-gemma-3-27b-runtime-rag-k4-sapbert-r0-9daf3577 | not_run |  |
| memoryalpha-memorybeta-llama-3-1-70b-runtime-rag-k2-minilm-r0-26235ff4 | not_run |  |
| memoryalpha-memorybeta-llama-3-1-70b-runtime-rag-k2-sapbert-r0-e09b62d7 | not_run |  |
| memoryalpha-memorybeta-llama-3-1-70b-runtime-rag-k4-sapbert-r0-55fda53d | not_run |  |
| memoryalpha-memorybeta-mistral-small-3-2-24b-runtime-rag-k2-minilm-r0-cd0025ca | not_run |  |
| memoryalpha-memorybeta-mistral-small-3-2-24b-runtime-rag-k2-sapbert-r0-100f0aef | not_run |  |
| memoryalpha-memorybeta-mistral-small-3-2-24b-runtime-rag-k4-sapbert-r0-6dcbcbc9 | not_run |  |
| memoryalpha-memorybeta-qwen3-235b-runtime-rag-k2-minilm-r0-104c3951 | not_run |  |
| memoryalpha-memorybeta-qwen3-235b-runtime-rag-k2-sapbert-r0-46d04145 | not_run |  |
| memoryalpha-memorybeta-qwen3-235b-runtime-rag-k4-sapbert-r0-d15b3fed | not_run |  |
| memoryalpha-memorybeta-qwen3-5-122b-runtime-rag-k2-minilm-r0-71e27728 | not_run |  |
| memoryalpha-memorybeta-qwen3-5-122b-runtime-rag-k2-sapbert-r0-73378a9a | not_run |  |
| memoryalpha-memorybeta-qwen3-5-122b-runtime-rag-k4-sapbert-r0-d99583ca | not_run |  |
| memoryalpha-memorybeta-qwen3-8b-runtime-rag-k2-minilm-r0-19757923 | not_run |  |
| memoryalpha-memorybeta-qwen3-8b-runtime-rag-k2-sapbert-r0-3f82c93c | not_run |  |
| memoryalpha-memorybeta-qwen3-8b-runtime-rag-k4-sapbert-r0-a170924d | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-off-runtime-rag-k2-minilm-r0-99bdbe05 | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-off-runtime-rag-k2-sapbert-r0-325974d4 | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-off-runtime-rag-k4-sapbert-r0-9ed39777 | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-reason-1028-runtime-rag-k2-minilm-r0-73fd9a4f | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-reason-1028-runtime-rag-k2-sapbert-r0-15fcd223 | not_run |  |
| memoryalpha-stexpanded-gemma-3-27b-runtime-rag-k2-minilm-r0-82e1c05c | not_run |  |
| memoryalpha-stexpanded-gemma-3-27b-runtime-rag-k2-sapbert-r0-9384d7d6 | not_run |  |
| memoryalpha-stexpanded-gemma-3-27b-runtime-rag-k4-sapbert-r0-94d79eb9 | not_run |  |
| memoryalpha-stexpanded-llama-3-1-70b-runtime-rag-k2-minilm-r0-c4c4cc10 | not_run |  |
| memoryalpha-stexpanded-llama-3-1-70b-runtime-rag-k2-sapbert-r0-5f7bd52e | not_run |  |
| memoryalpha-stexpanded-llama-3-1-70b-runtime-rag-k4-sapbert-r0-138ed08b | not_run |  |
| memoryalpha-stexpanded-mistral-small-3-2-24b-runtime-rag-k2-minilm-r0-964783ff | not_run |  |
| memoryalpha-stexpanded-mistral-small-3-2-24b-runtime-rag-k2-sapbert-r0-c16dff48 | not_run |  |
| memoryalpha-stexpanded-mistral-small-3-2-24b-runtime-rag-k4-sapbert-r0-4b9359ce | not_run |  |
| memoryalpha-stexpanded-qwen3-235b-runtime-rag-k2-minilm-r0-5fc575bc | not_run |  |
| memoryalpha-stexpanded-qwen3-235b-runtime-rag-k2-sapbert-r0-5de4a51a | not_run |  |
| memoryalpha-stexpanded-qwen3-235b-runtime-rag-k4-sapbert-r0-07eddee7 | not_run |  |
| memoryalpha-stexpanded-qwen3-5-122b-runtime-rag-k2-minilm-r0-0da997d6 | not_run |  |
| memoryalpha-stexpanded-qwen3-5-122b-runtime-rag-k2-sapbert-r0-2318fe85 | not_run |  |
| memoryalpha-stexpanded-qwen3-5-122b-runtime-rag-k4-sapbert-r0-67d5434e | not_run |  |
| memoryalpha-stexpanded-qwen3-8b-runtime-rag-k2-minilm-r0-f9efe202 | not_run |  |
| memoryalpha-stexpanded-qwen3-8b-runtime-rag-k2-sapbert-r0-94ac8d24 | not_run |  |
| memoryalpha-stexpanded-qwen3-8b-runtime-rag-k4-sapbert-r0-41b10b9b | not_run |  |
| starwars-swg-gemini-2-5-flash-off-runtime-rag-k2-minilm-r0-de1647a7 | not_run |  |
| starwars-swg-gemini-2-5-flash-off-runtime-rag-k2-sapbert-r0-5b68d07a | not_run |  |
| starwars-swg-gemini-2-5-flash-off-runtime-rag-k4-sapbert-r0-3da1995a | not_run |  |
| starwars-swg-gemini-2-5-flash-reason-1028-runtime-rag-k2-minilm-r0-cf971bc9 | not_run |  |
| starwars-swg-gemini-2-5-flash-reason-1028-runtime-rag-k2-sapbert-r0-26a930c4 | not_run |  |
| starwars-swg-gemma-3-27b-runtime-rag-k2-minilm-r0-7c6b8c93 | not_run |  |
| starwars-swg-gemma-3-27b-runtime-rag-k2-sapbert-r0-89be61ac | not_run |  |
| starwars-swg-gemma-3-27b-runtime-rag-k4-sapbert-r0-584f891b | not_run |  |
| starwars-swg-llama-3-1-70b-runtime-rag-k2-minilm-r0-6e06655f | not_run |  |
| starwars-swg-llama-3-1-70b-runtime-rag-k2-sapbert-r0-643ea311 | not_run |  |
| starwars-swg-llama-3-1-70b-runtime-rag-k4-sapbert-r0-cbca4c4b | not_run |  |
| starwars-swg-mistral-small-3-2-24b-runtime-rag-k2-minilm-r0-dfd518a2 | not_run |  |
| starwars-swg-mistral-small-3-2-24b-runtime-rag-k2-sapbert-r0-047c9b30 | not_run |  |
| starwars-swg-mistral-small-3-2-24b-runtime-rag-k4-sapbert-r0-035f7d5f | not_run |  |
| starwars-swg-qwen3-235b-runtime-rag-k2-minilm-r0-578b3a1a | not_run |  |
| starwars-swg-qwen3-235b-runtime-rag-k2-sapbert-r0-7af458ba | not_run |  |
| starwars-swg-qwen3-235b-runtime-rag-k4-sapbert-r0-8a78ff6d | not_run |  |
| starwars-swg-qwen3-5-122b-runtime-rag-k2-minilm-r0-445e7996 | not_run |  |
| starwars-swg-qwen3-5-122b-runtime-rag-k2-sapbert-r0-1df36741 | not_run |  |
| starwars-swg-qwen3-5-122b-runtime-rag-k4-sapbert-r0-4f9b17ce | not_run |  |
| starwars-swg-qwen3-8b-runtime-rag-k2-minilm-r0-3ece6257 | not_run |  |
| starwars-swg-qwen3-8b-runtime-rag-k2-sapbert-r0-fa7b3c97 | not_run |  |
| starwars-swg-qwen3-8b-runtime-rag-k4-sapbert-r0-4856d68d | not_run |  |
| starwars-swtor-gemini-2-5-flash-off-runtime-rag-k2-minilm-r0-7cb1c0ff | not_run |  |
| starwars-swtor-gemini-2-5-flash-off-runtime-rag-k2-sapbert-r0-3ef5bf4f | not_run |  |
| starwars-swtor-gemini-2-5-flash-off-runtime-rag-k4-sapbert-r0-ceb0364c | not_run |  |
| starwars-swtor-gemini-2-5-flash-reason-1028-runtime-rag-k2-minilm-r0-b6d56721 | not_run |  |
| starwars-swtor-gemini-2-5-flash-reason-1028-runtime-rag-k2-sapbert-r0-d1bb76cf | not_run |  |
| starwars-swtor-gemma-3-27b-runtime-rag-k2-minilm-r0-0d272e91 | not_run |  |
| starwars-swtor-gemma-3-27b-runtime-rag-k2-sapbert-r0-c84745ba | not_run |  |
| starwars-swtor-gemma-3-27b-runtime-rag-k4-sapbert-r0-70befc69 | not_run |  |
| starwars-swtor-llama-3-1-70b-runtime-rag-k2-minilm-r0-761947fc | not_run |  |
| starwars-swtor-llama-3-1-70b-runtime-rag-k2-sapbert-r0-1f0f5f8e | not_run |  |
| starwars-swtor-llama-3-1-70b-runtime-rag-k4-sapbert-r0-a8b260cf | not_run |  |
| starwars-swtor-mistral-small-3-2-24b-runtime-rag-k2-minilm-r0-4c7e5c30 | not_run |  |
| starwars-swtor-mistral-small-3-2-24b-runtime-rag-k2-sapbert-r0-c61a49d5 | not_run |  |
| starwars-swtor-mistral-small-3-2-24b-runtime-rag-k4-sapbert-r0-43f9856a | not_run |  |
| starwars-swtor-qwen3-235b-runtime-rag-k2-minilm-r0-a0e757d0 | not_run |  |
| starwars-swtor-qwen3-235b-runtime-rag-k2-sapbert-r0-75b37261 | not_run |  |
| starwars-swtor-qwen3-235b-runtime-rag-k4-sapbert-r0-9516e9ee | not_run |  |
| starwars-swtor-qwen3-5-122b-runtime-rag-k2-minilm-r0-fb977e73 | not_run |  |
| starwars-swtor-qwen3-5-122b-runtime-rag-k2-sapbert-r0-1f0ef435 | not_run |  |
| starwars-swtor-qwen3-5-122b-runtime-rag-k4-sapbert-r0-f84ebb6d | not_run |  |
| starwars-swtor-qwen3-8b-runtime-rag-k2-minilm-r0-43e7fe0f | not_run |  |
| starwars-swtor-qwen3-8b-runtime-rag-k2-sapbert-r0-56821564 | not_run |  |
| starwars-swtor-qwen3-8b-runtime-rag-k4-sapbert-r0-40ce0eab | not_run |  |

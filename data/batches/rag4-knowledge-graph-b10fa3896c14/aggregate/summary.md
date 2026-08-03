# Results: rag4-knowledge-graph

Coverage: **25/40 (62.5%)**

| Status | Jobs |
|---|---:|
| not_run | 15 |
| success | 25 |

## Groups

| model | completed | expected | coverage |
|---|---|---|---|
| deepseek-v4-flash | 0 | 5 | 0.0% |
| gemini-2-5-flash | 0 | 5 | 0.0% |
| gemma-3-27b | 5 | 5 | 100.0% |
| llama-3-1-70b | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | 0 | 5 | 0.0% |
| qwen3-235b | 5 | 5 | 100.0% |
| qwen3-5-122b | 5 | 5 | 100.0% |
| qwen3-8b | 5 | 5 | 100.0% |

## Primary metrics

| model | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | 0.8919 | 0.7309 | 0.8034 | 0.8988 | 0.7026 | 0.7841 | 0.6368 | 0.7778 | 0.6846 | 0.9722 | 0.7776 | 0.8193 |
| llama-3-1-70b | 0.8921 | 0.7306 | 0.8033 | 0.8990 | 0.7018 | 0.7837 | 0.6453 | 0.7348 | 0.6702 | 0.9185 | 0.8953 | 0.7876 |
| mistral-small-3-2-24b |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | 0.8926 | 0.7301 | 0.8032 | 0.8992 | 0.7009 | 0.7831 | 0.7467 | 0.6578 | 0.6895 | 0.8222 | 0.9765 | 0.7928 |
| qwen3-5-122b | 0.8925 | 0.7305 | 0.8035 | 0.8992 | 0.7018 | 0.7837 | 0.7368 | 0.7215 | 0.7232 | 0.9019 | 0.9647 | 0.8577 |
| qwen3-8b | 0.8925 | 0.7294 | 0.8027 | 0.8991 | 0.6993 | 0.7821 | 0.7385 | 0.3793 | 0.4867 | 0.4741 | 0.9765 | 0.4447 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|
| gemma-3-27b | Global | 5 | 5 | 11225 | 1361 | 4132 | 0.8919 | 0.7309 | 0.8034 |
| gemma-3-27b | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| gemma-3-27b | INST | 5 | 5 | 11021 | 1340 | 4106 | 0.8916 | 0.7286 | 0.8019 |
| gemma-3-27b | PROP | 5 | 5 | 172 | 18 | 9 | 0.9053 | 0.9503 | 0.9272 |
| gemma-3-27b | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| llama-3-1-70b | Global | 5 | 5 | 11220 | 1357 | 4137 | 0.8921 | 0.7306 | 0.8033 |
| llama-3-1-70b | CLS | 5 | 5 | 32 | 4 | 17 | 0.8889 | 0.6531 | 0.7529 |
| llama-3-1-70b | INST | 5 | 5 | 11016 | 1337 | 4111 | 0.8918 | 0.7282 | 0.8017 |
| llama-3-1-70b | PROP | 5 | 5 | 172 | 16 | 9 | 0.9149 | 0.9503 | 0.9322 |
| llama-3-1-70b | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-235b | Global | 5 | 5 | 11212 | 1349 | 4145 | 0.8926 | 0.7301 | 0.8032 |
| qwen3-235b | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-235b | INST | 5 | 5 | 11008 | 1337 | 4119 | 0.8917 | 0.7277 | 0.8014 |
| qwen3-235b | PROP | 5 | 5 | 172 | 9 | 9 | 0.9503 | 0.9503 | 0.9503 |
| qwen3-235b | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-5-122b | Global | 5 | 5 | 11219 | 1351 | 4138 | 0.8925 | 0.7305 | 0.8035 |
| qwen3-5-122b | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| qwen3-5-122b | INST | 5 | 5 | 11015 | 1337 | 4112 | 0.8918 | 0.7282 | 0.8017 |
| qwen3-5-122b | PROP | 5 | 5 | 172 | 11 | 9 | 0.9399 | 0.9503 | 0.9451 |
| qwen3-5-122b | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | Global | 5 | 5 | 11201 | 1349 | 4156 | 0.8925 | 0.7294 | 0.8027 |
| qwen3-8b | CLS | 5 | 5 | 31 | 3 | 18 | 0.9118 | 0.6327 | 0.7470 |
| qwen3-8b | INST | 5 | 5 | 10998 | 1336 | 4129 | 0.8917 | 0.7270 | 0.8010 |
| qwen3-8b | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| qwen3-8b | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| marvelcinematicuniverse-marvel-deepseek-v4-flash-query-rag-k4-r0-a7a6991e | not_run |  |
| marvelcinematicuniverse-marvel-gemini-2-5-flash-query-rag-k4-r0-7f2a5962 | not_run |  |
| marvelcinematicuniverse-marvel-mistral-small-3-2-24b-query-rag-k4-r0-f54f7713 | not_run |  |
| memoryalpha-memorybeta-deepseek-v4-flash-query-rag-k4-r0-87a2374c | not_run |  |
| memoryalpha-memorybeta-gemini-2-5-flash-query-rag-k4-r0-7ff355a3 | not_run |  |
| memoryalpha-memorybeta-mistral-small-3-2-24b-query-rag-k4-r0-7e458c03 | not_run |  |
| memoryalpha-stexpanded-deepseek-v4-flash-query-rag-k4-r0-9f175726 | not_run |  |
| memoryalpha-stexpanded-gemini-2-5-flash-query-rag-k4-r0-8a3c6769 | not_run |  |
| memoryalpha-stexpanded-mistral-small-3-2-24b-query-rag-k4-r0-eaadc16b | not_run |  |
| starwars-swg-deepseek-v4-flash-query-rag-k4-r0-f7b75789 | not_run |  |
| starwars-swg-gemini-2-5-flash-query-rag-k4-r0-df4ab2e4 | not_run |  |
| starwars-swg-mistral-small-3-2-24b-query-rag-k4-r0-617aa3c4 | not_run |  |
| starwars-swtor-deepseek-v4-flash-query-rag-k4-r0-19087093 | not_run |  |
| starwars-swtor-gemini-2-5-flash-query-rag-k4-r0-06dcdbe8 | not_run |  |
| starwars-swtor-mistral-small-3-2-24b-query-rag-k4-r0-5faaa3d1 | not_run |  |

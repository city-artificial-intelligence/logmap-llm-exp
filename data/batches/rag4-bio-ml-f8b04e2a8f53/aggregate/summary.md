# Results: rag4-bio-ml

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
| gemma-3-27b | 0.7831 | 0.6553 | 0.7135 | 0.7937 | 0.6637 | 0.7106 | 0.5478 | 0.9453 | 0.6922 | 0.9453 | 0.3367 | 0.2820 |
| llama-3-1-70b | 0.7953 | 0.6554 | 0.7186 | 0.8074 | 0.6639 | 0.7156 | 0.6275 | 0.9365 | 0.7504 | 0.9365 | 0.5215 | 0.4580 |
| mistral-small-3-2-24b |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | 0.7907 | 0.6555 | 0.7168 | 0.8023 | 0.6640 | 0.7139 | 0.5978 | 0.9321 | 0.7264 | 0.9321 | 0.4672 | 0.3993 |
| qwen3-5-122b | 0.8023 | 0.6543 | 0.7207 | 0.8133 | 0.6625 | 0.7179 | 0.6562 | 0.9178 | 0.7649 | 0.9178 | 0.5868 | 0.5046 |
| qwen3-8b | 0.7965 | 0.6516 | 0.7168 | 0.8057 | 0.6598 | 0.7134 | 0.6088 | 0.8824 | 0.7198 | 0.8824 | 0.5093 | 0.3917 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|
| gemma-3-27b | Global | 5 | 5 | 16560 | 4588 | 8710 | 0.7831 | 0.6553 | 0.7135 |
| llama-3-1-70b | Global | 5 | 5 | 16563 | 4262 | 8707 | 0.7953 | 0.6554 | 0.7186 |
| qwen3-235b | Global | 5 | 5 | 16565 | 4385 | 8705 | 0.7907 | 0.6555 | 0.7168 |
| qwen3-5-122b | Global | 5 | 5 | 16533 | 4075 | 8737 | 0.8023 | 0.6543 | 0.7207 |
| qwen3-8b | Global | 5 | 5 | 16467 | 4207 | 8803 | 0.7965 | 0.6516 | 0.7168 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| ncit-doid-deepseek-v4-flash-query-rag-k4-r0-78bae957 | not_run |  |
| ncit-doid-gemini-2-5-flash-query-rag-k4-r0-e7b9ca88 | not_run |  |
| ncit-doid-mistral-small-3-2-24b-query-rag-k4-r0-ca199bf7 | not_run |  |
| omim-ordo-deepseek-v4-flash-query-rag-k4-r0-a8e4fe93 | not_run |  |
| omim-ordo-gemini-2-5-flash-query-rag-k4-r0-7e218ce6 | not_run |  |
| omim-ordo-mistral-small-3-2-24b-query-rag-k4-r0-ec3f5205 | not_run |  |
| snomed-fma-body-deepseek-v4-flash-query-rag-k4-r0-ce15d789 | not_run |  |
| snomed-fma-body-gemini-2-5-flash-query-rag-k4-r0-273e17c0 | not_run |  |
| snomed-fma-body-mistral-small-3-2-24b-query-rag-k4-r0-b8be7642 | not_run |  |
| snomed-ncit-neoplas-deepseek-v4-flash-query-rag-k4-r0-c4a1a69e | not_run |  |
| snomed-ncit-neoplas-gemini-2-5-flash-query-rag-k4-r0-4c62f305 | not_run |  |
| snomed-ncit-neoplas-mistral-small-3-2-24b-query-rag-k4-r0-b314fee8 | not_run |  |
| snomed-ncit-pharm-deepseek-v4-flash-query-rag-k4-r0-0a68391c | not_run |  |
| snomed-ncit-pharm-gemini-2-5-flash-query-rag-k4-r0-b72e3746 | not_run |  |
| snomed-ncit-pharm-mistral-small-3-2-24b-query-rag-k4-r0-b0f0c479 | not_run |  |

# Results: rag-runtime-bio-ml

Coverage: **30/90 (33.3%)**

| Status | Jobs |
|---|---:|
| not_run | 60 |
| success | 30 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-high | runtime-rag-k2 | 0 | 5 | 0.0% |
| deepseek-v4-flash-off | runtime-rag-k2 | 0 | 5 | 0.0% |
| deepseek-v4-flash-off | runtime-rag-k4 | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | runtime-rag-k2 | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | runtime-rag-k4 | 0 | 5 | 0.0% |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2 | 0 | 5 | 0.0% |
| gemma-3-27b | runtime-rag-k2 | 0 | 5 | 0.0% |
| gemma-3-27b | runtime-rag-k4 | 0 | 5 | 0.0% |
| llama-3-1-70b | runtime-rag-k2 | 5 | 5 | 100.0% |
| llama-3-1-70b | runtime-rag-k4 | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | runtime-rag-k2 | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | runtime-rag-k4 | 5 | 5 | 100.0% |
| qwen3-235b | runtime-rag-k2 | 0 | 5 | 0.0% |
| qwen3-235b | runtime-rag-k4 | 0 | 5 | 0.0% |
| qwen3-5-122b | runtime-rag-k2 | 5 | 5 | 100.0% |
| qwen3-5-122b | runtime-rag-k4 | 5 | 5 | 100.0% |
| qwen3-8b | runtime-rag-k2 | 0 | 5 | 0.0% |
| qwen3-8b | runtime-rag-k4 | 0 | 5 | 0.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-high | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-off | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-off | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | runtime-rag-k2 | 0.7970 | 0.6541 | 0.7186 | 0.8101 | 0.6625 | 0.7162 | 0.6422 | 0.9236 | 0.7556 | 0.9236 | 0.5503 | 0.4739 |
| llama-3-1-70b | runtime-rag-k4 | 0.7965 | 0.6545 | 0.7186 | 0.8095 | 0.6629 | 0.7160 | 0.6387 | 0.9265 | 0.7544 | 0.9265 | 0.5411 | 0.4676 |
| mistral-small-3-2-24b | runtime-rag-k2 | 0.7845 | 0.6566 | 0.7149 | 0.7975 | 0.6650 | 0.7124 | 0.5750 | 0.9561 | 0.7152 | 0.9561 | 0.3865 | 0.3427 |
| mistral-small-3-2-24b | runtime-rag-k4 | 0.7830 | 0.6570 | 0.7145 | 0.7965 | 0.6654 | 0.7120 | 0.5696 | 0.9575 | 0.7114 | 0.9575 | 0.3670 | 0.3244 |
| qwen3-235b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | runtime-rag-k2 | 0.8031 | 0.6537 | 0.7207 | 0.8145 | 0.6618 | 0.7179 | 0.6664 | 0.9183 | 0.7719 | 0.9183 | 0.5952 | 0.5135 |
| qwen3-5-122b | runtime-rag-k4 | 0.8025 | 0.6537 | 0.7205 | 0.8143 | 0.6620 | 0.7177 | 0.6648 | 0.9148 | 0.7695 | 0.9148 | 0.5962 | 0.5110 |
| qwen3-8b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| llama-3-1-70b | runtime-rag-k2 | Global | 5 | 5 | 16530 | 4209 | 8740 | 0.7970 | 0.6541 | 0.7186 |
| llama-3-1-70b | runtime-rag-k4 | Global | 5 | 5 | 16540 | 4227 | 8730 | 0.7965 | 0.6545 | 0.7186 |
| mistral-small-3-2-24b | runtime-rag-k2 | Global | 5 | 5 | 16593 | 4559 | 8677 | 0.7845 | 0.6566 | 0.7149 |
| mistral-small-3-2-24b | runtime-rag-k4 | Global | 5 | 5 | 16602 | 4600 | 8668 | 0.7830 | 0.6570 | 0.7145 |
| qwen3-5-122b | runtime-rag-k2 | Global | 5 | 5 | 16518 | 4051 | 8752 | 0.8031 | 0.6537 | 0.7207 |
| qwen3-5-122b | runtime-rag-k4 | Global | 5 | 5 | 16519 | 4065 | 8751 | 0.8025 | 0.6537 | 0.7205 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| ncit-doid-deepseek-v4-flash-high-runtime-rag-k2-r0-20b0180d | not_run |  |
| ncit-doid-deepseek-v4-flash-off-runtime-rag-k2-r0-572586a2 | not_run |  |
| ncit-doid-deepseek-v4-flash-off-runtime-rag-k4-r0-8788cef1 | not_run |  |
| ncit-doid-gemini-2-5-flash-off-runtime-rag-k2-r0-41b4567d | not_run |  |
| ncit-doid-gemini-2-5-flash-off-runtime-rag-k4-r0-f5bd5a88 | not_run |  |
| ncit-doid-gemini-2-5-flash-reason-1028-runtime-rag-k2-r0-5ce93dc5 | not_run |  |
| ncit-doid-gemma-3-27b-runtime-rag-k2-r0-1f6b187c | not_run |  |
| ncit-doid-gemma-3-27b-runtime-rag-k4-r0-159e718e | not_run |  |
| ncit-doid-qwen3-235b-runtime-rag-k2-r0-d00a0cda | not_run |  |
| ncit-doid-qwen3-235b-runtime-rag-k4-r0-9c0ad4ef | not_run |  |
| ncit-doid-qwen3-8b-runtime-rag-k2-r0-48dc7c90 | not_run |  |
| ncit-doid-qwen3-8b-runtime-rag-k4-r0-d32e92d7 | not_run |  |
| omim-ordo-deepseek-v4-flash-high-runtime-rag-k2-r0-4af2fef5 | not_run |  |
| omim-ordo-deepseek-v4-flash-off-runtime-rag-k2-r0-d880e41a | not_run |  |
| omim-ordo-deepseek-v4-flash-off-runtime-rag-k4-r0-8cadf445 | not_run |  |
| omim-ordo-gemini-2-5-flash-off-runtime-rag-k2-r0-9212d547 | not_run |  |
| omim-ordo-gemini-2-5-flash-off-runtime-rag-k4-r0-9e741751 | not_run |  |
| omim-ordo-gemini-2-5-flash-reason-1028-runtime-rag-k2-r0-78a76401 | not_run |  |
| omim-ordo-gemma-3-27b-runtime-rag-k2-r0-b58783e3 | not_run |  |
| omim-ordo-gemma-3-27b-runtime-rag-k4-r0-db40456c | not_run |  |
| omim-ordo-qwen3-235b-runtime-rag-k2-r0-86c5d648 | not_run |  |
| omim-ordo-qwen3-235b-runtime-rag-k4-r0-a5e5fa74 | not_run |  |
| omim-ordo-qwen3-8b-runtime-rag-k2-r0-676d3468 | not_run |  |
| omim-ordo-qwen3-8b-runtime-rag-k4-r0-23590ba6 | not_run |  |
| snomed-fma-body-deepseek-v4-flash-high-runtime-rag-k2-r0-eb69cbbe | not_run |  |
| snomed-fma-body-deepseek-v4-flash-off-runtime-rag-k2-r0-b1824d65 | not_run |  |
| snomed-fma-body-deepseek-v4-flash-off-runtime-rag-k4-r0-9fc4f688 | not_run |  |
| snomed-fma-body-gemini-2-5-flash-off-runtime-rag-k2-r0-90683c78 | not_run |  |
| snomed-fma-body-gemini-2-5-flash-off-runtime-rag-k4-r0-a40a283b | not_run |  |
| snomed-fma-body-gemini-2-5-flash-reason-1028-runtime-rag-k2-r0-0002f2a1 | not_run |  |
| snomed-fma-body-gemma-3-27b-runtime-rag-k2-r0-8109f801 | not_run |  |
| snomed-fma-body-gemma-3-27b-runtime-rag-k4-r0-8d38343f | not_run |  |
| snomed-fma-body-qwen3-235b-runtime-rag-k2-r0-e5f90f3c | not_run |  |
| snomed-fma-body-qwen3-235b-runtime-rag-k4-r0-8ae1c1d7 | not_run |  |
| snomed-fma-body-qwen3-8b-runtime-rag-k2-r0-37bfa0a1 | not_run |  |
| snomed-fma-body-qwen3-8b-runtime-rag-k4-r0-90e731dd | not_run |  |
| snomed-ncit-neoplas-deepseek-v4-flash-high-runtime-rag-k2-r0-c8302c59 | not_run |  |
| snomed-ncit-neoplas-deepseek-v4-flash-off-runtime-rag-k2-r0-283678da | not_run |  |
| snomed-ncit-neoplas-deepseek-v4-flash-off-runtime-rag-k4-r0-7033fe32 | not_run |  |
| snomed-ncit-neoplas-gemini-2-5-flash-off-runtime-rag-k2-r0-b5a78412 | not_run |  |
| snomed-ncit-neoplas-gemini-2-5-flash-off-runtime-rag-k4-r0-c8a87906 | not_run |  |
| snomed-ncit-neoplas-gemini-2-5-flash-reason-1028-runtime-rag-k2-r0-232816be | not_run |  |
| snomed-ncit-neoplas-gemma-3-27b-runtime-rag-k2-r0-9c3c991c | not_run |  |
| snomed-ncit-neoplas-gemma-3-27b-runtime-rag-k4-r0-8c9cfcda | not_run |  |
| snomed-ncit-neoplas-qwen3-235b-runtime-rag-k2-r0-6fcf51b7 | not_run |  |
| snomed-ncit-neoplas-qwen3-235b-runtime-rag-k4-r0-d5529376 | not_run |  |
| snomed-ncit-neoplas-qwen3-8b-runtime-rag-k2-r0-da39d9c4 | not_run |  |
| snomed-ncit-neoplas-qwen3-8b-runtime-rag-k4-r0-a91f5d5a | not_run |  |
| snomed-ncit-pharm-deepseek-v4-flash-high-runtime-rag-k2-r0-2f749519 | not_run |  |
| snomed-ncit-pharm-deepseek-v4-flash-off-runtime-rag-k2-r0-483ba8de | not_run |  |
| snomed-ncit-pharm-deepseek-v4-flash-off-runtime-rag-k4-r0-2584e173 | not_run |  |
| snomed-ncit-pharm-gemini-2-5-flash-off-runtime-rag-k2-r0-2fe38ce8 | not_run |  |
| snomed-ncit-pharm-gemini-2-5-flash-off-runtime-rag-k4-r0-1b22de83 | not_run |  |
| snomed-ncit-pharm-gemini-2-5-flash-reason-1028-runtime-rag-k2-r0-c8d2217a | not_run |  |
| snomed-ncit-pharm-gemma-3-27b-runtime-rag-k2-r0-d727112c | not_run |  |
| snomed-ncit-pharm-gemma-3-27b-runtime-rag-k4-r0-0bc5a8a0 | not_run |  |
| snomed-ncit-pharm-qwen3-235b-runtime-rag-k2-r0-56c00491 | not_run |  |
| snomed-ncit-pharm-qwen3-235b-runtime-rag-k4-r0-1c75c72f | not_run |  |
| snomed-ncit-pharm-qwen3-8b-runtime-rag-k2-r0-ff9d726c | not_run |  |
| snomed-ncit-pharm-qwen3-8b-runtime-rag-k4-r0-449536f6 | not_run |  |

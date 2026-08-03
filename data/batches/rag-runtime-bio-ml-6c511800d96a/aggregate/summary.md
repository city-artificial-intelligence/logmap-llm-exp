# Results: rag-runtime-bio-ml

Coverage: **15/90 (16.7%)**

| Status | Jobs |
|---|---:|
| degraded | 3 |
| not_run | 75 |
| success | 12 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-parasail-high | runtime-rag-k2 | 5 | 5 | 100.0% |
| deepseek-v4-flash-parasail-off | runtime-rag-k2 | 5 | 5 | 100.0% |
| deepseek-v4-flash-parasail-off | runtime-rag-k4 | 5 | 5 | 100.0% |
| gemini-2-5-flash-off | runtime-rag-k2 | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | runtime-rag-k4 | 0 | 5 | 0.0% |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2 | 0 | 5 | 0.0% |
| gemma-3-27b | runtime-rag-k2 | 0 | 5 | 0.0% |
| gemma-3-27b | runtime-rag-k4 | 0 | 5 | 0.0% |
| llama-3-1-70b | runtime-rag-k2 | 0 | 5 | 0.0% |
| llama-3-1-70b | runtime-rag-k4 | 0 | 5 | 0.0% |
| mistral-small-3-2-24b | runtime-rag-k2 | 0 | 5 | 0.0% |
| mistral-small-3-2-24b | runtime-rag-k4 | 0 | 5 | 0.0% |
| qwen3-235b | runtime-rag-k2 | 0 | 5 | 0.0% |
| qwen3-235b | runtime-rag-k4 | 0 | 5 | 0.0% |
| qwen3-5-122b | runtime-rag-k2 | 0 | 5 | 0.0% |
| qwen3-5-122b | runtime-rag-k4 | 0 | 5 | 0.0% |
| qwen3-8b | runtime-rag-k2 | 0 | 5 | 0.0% |
| qwen3-8b | runtime-rag-k4 | 0 | 5 | 0.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-high | runtime-rag-k2 | 0.8129 | 0.6501 | 0.7225 | 0.8248 | 0.6579 | 0.7198 | 0.7423 | 0.8724 | 0.8010 | 0.8724 | 0.7328 | 0.6052 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2 | 0.8026 | 0.6532 | 0.7203 | 0.8149 | 0.6612 | 0.7174 | 0.6725 | 0.9139 | 0.7729 | 0.9139 | 0.6135 | 0.5274 |
| deepseek-v4-flash-parasail-off | runtime-rag-k4 | 0.8030 | 0.6538 | 0.7208 | 0.8156 | 0.6619 | 0.7180 | 0.6786 | 0.9190 | 0.7788 | 0.9190 | 0.6180 | 0.5370 |
| gemini-2-5-flash-off | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| mistral-small-3-2-24b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| mistral-small-3-2-24b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-high | runtime-rag-k2 | Global | 5 | 5 | 16429 | 3781 | 8841 | 0.8129 | 0.6501 | 0.7225 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2 | Global | 5 | 5 | 16507 | 4059 | 8763 | 0.8026 | 0.6532 | 0.7203 |
| deepseek-v4-flash-parasail-off | runtime-rag-k4 | Global | 5 | 5 | 16522 | 4054 | 8748 | 0.8030 | 0.6538 | 0.7208 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| ncit-doid-gemini-2-5-flash-off-runtime-rag-k2-r0-41b4567d | not_run |  |
| ncit-doid-gemini-2-5-flash-off-runtime-rag-k4-r0-f5bd5a88 | not_run |  |
| ncit-doid-gemini-2-5-flash-reason-1028-runtime-rag-k2-r0-5ce93dc5 | not_run |  |
| ncit-doid-gemma-3-27b-runtime-rag-k2-r0-1f6b187c | not_run |  |
| ncit-doid-gemma-3-27b-runtime-rag-k4-r0-159e718e | not_run |  |
| ncit-doid-llama-3-1-70b-runtime-rag-k2-r0-04eee07c | not_run |  |
| ncit-doid-llama-3-1-70b-runtime-rag-k4-r0-b5ebc59d | not_run |  |
| ncit-doid-mistral-small-3-2-24b-runtime-rag-k2-r0-925662cb | not_run |  |
| ncit-doid-mistral-small-3-2-24b-runtime-rag-k4-r0-35aef55e | not_run |  |
| ncit-doid-qwen3-235b-runtime-rag-k2-r0-d00a0cda | not_run |  |
| ncit-doid-qwen3-235b-runtime-rag-k4-r0-9c0ad4ef | not_run |  |
| ncit-doid-qwen3-5-122b-runtime-rag-k2-r0-37712cfc | not_run |  |
| ncit-doid-qwen3-5-122b-runtime-rag-k4-r0-46251e48 | not_run |  |
| ncit-doid-qwen3-8b-runtime-rag-k2-r0-48dc7c90 | not_run |  |
| ncit-doid-qwen3-8b-runtime-rag-k4-r0-d32e92d7 | not_run |  |
| omim-ordo-gemini-2-5-flash-off-runtime-rag-k2-r0-9212d547 | not_run |  |
| omim-ordo-gemini-2-5-flash-off-runtime-rag-k4-r0-9e741751 | not_run |  |
| omim-ordo-gemini-2-5-flash-reason-1028-runtime-rag-k2-r0-78a76401 | not_run |  |
| omim-ordo-gemma-3-27b-runtime-rag-k2-r0-b58783e3 | not_run |  |
| omim-ordo-gemma-3-27b-runtime-rag-k4-r0-db40456c | not_run |  |
| omim-ordo-llama-3-1-70b-runtime-rag-k2-r0-db6a4878 | not_run |  |
| omim-ordo-llama-3-1-70b-runtime-rag-k4-r0-649f7e4d | not_run |  |
| omim-ordo-mistral-small-3-2-24b-runtime-rag-k2-r0-c3a658e3 | not_run |  |
| omim-ordo-mistral-small-3-2-24b-runtime-rag-k4-r0-90154bb5 | not_run |  |
| omim-ordo-qwen3-235b-runtime-rag-k2-r0-86c5d648 | not_run |  |
| omim-ordo-qwen3-235b-runtime-rag-k4-r0-a5e5fa74 | not_run |  |
| omim-ordo-qwen3-5-122b-runtime-rag-k2-r0-dd747cc8 | not_run |  |
| omim-ordo-qwen3-5-122b-runtime-rag-k4-r0-fef6cae2 | not_run |  |
| omim-ordo-qwen3-8b-runtime-rag-k2-r0-676d3468 | not_run |  |
| omim-ordo-qwen3-8b-runtime-rag-k4-r0-23590ba6 | not_run |  |
| snomed-fma-body-gemini-2-5-flash-off-runtime-rag-k2-r0-90683c78 | not_run |  |
| snomed-fma-body-gemini-2-5-flash-off-runtime-rag-k4-r0-a40a283b | not_run |  |
| snomed-fma-body-gemini-2-5-flash-reason-1028-runtime-rag-k2-r0-0002f2a1 | not_run |  |
| snomed-fma-body-gemma-3-27b-runtime-rag-k2-r0-8109f801 | not_run |  |
| snomed-fma-body-gemma-3-27b-runtime-rag-k4-r0-8d38343f | not_run |  |
| snomed-fma-body-llama-3-1-70b-runtime-rag-k2-r0-064a1e14 | not_run |  |
| snomed-fma-body-llama-3-1-70b-runtime-rag-k4-r0-faacad2f | not_run |  |
| snomed-fma-body-mistral-small-3-2-24b-runtime-rag-k2-r0-3a54a940 | not_run |  |
| snomed-fma-body-mistral-small-3-2-24b-runtime-rag-k4-r0-cea5c5d8 | not_run |  |
| snomed-fma-body-qwen3-235b-runtime-rag-k2-r0-e5f90f3c | not_run |  |
| snomed-fma-body-qwen3-235b-runtime-rag-k4-r0-8ae1c1d7 | not_run |  |
| snomed-fma-body-qwen3-5-122b-runtime-rag-k2-r0-52965ce8 | not_run |  |
| snomed-fma-body-qwen3-5-122b-runtime-rag-k4-r0-91f058fa | not_run |  |
| snomed-fma-body-qwen3-8b-runtime-rag-k2-r0-37bfa0a1 | not_run |  |
| snomed-fma-body-qwen3-8b-runtime-rag-k4-r0-90e731dd | not_run |  |
| snomed-ncit-neoplas-gemini-2-5-flash-off-runtime-rag-k2-r0-b5a78412 | not_run |  |
| snomed-ncit-neoplas-gemini-2-5-flash-off-runtime-rag-k4-r0-c8a87906 | not_run |  |
| snomed-ncit-neoplas-gemini-2-5-flash-reason-1028-runtime-rag-k2-r0-232816be | not_run |  |
| snomed-ncit-neoplas-gemma-3-27b-runtime-rag-k2-r0-9c3c991c | not_run |  |
| snomed-ncit-neoplas-gemma-3-27b-runtime-rag-k4-r0-8c9cfcda | not_run |  |
| snomed-ncit-neoplas-llama-3-1-70b-runtime-rag-k2-r0-ec20bd27 | not_run |  |
| snomed-ncit-neoplas-llama-3-1-70b-runtime-rag-k4-r0-a2535938 | not_run |  |
| snomed-ncit-neoplas-mistral-small-3-2-24b-runtime-rag-k2-r0-39b044eb | not_run |  |
| snomed-ncit-neoplas-mistral-small-3-2-24b-runtime-rag-k4-r0-08a325ab | not_run |  |
| snomed-ncit-neoplas-qwen3-235b-runtime-rag-k2-r0-6fcf51b7 | not_run |  |
| snomed-ncit-neoplas-qwen3-235b-runtime-rag-k4-r0-d5529376 | not_run |  |
| snomed-ncit-neoplas-qwen3-5-122b-runtime-rag-k2-r0-3d512c1b | not_run |  |
| snomed-ncit-neoplas-qwen3-5-122b-runtime-rag-k4-r0-3ee99076 | not_run |  |
| snomed-ncit-neoplas-qwen3-8b-runtime-rag-k2-r0-da39d9c4 | not_run |  |
| snomed-ncit-neoplas-qwen3-8b-runtime-rag-k4-r0-a91f5d5a | not_run |  |
| snomed-ncit-pharm-gemini-2-5-flash-off-runtime-rag-k2-r0-2fe38ce8 | not_run |  |
| snomed-ncit-pharm-gemini-2-5-flash-off-runtime-rag-k4-r0-1b22de83 | not_run |  |
| snomed-ncit-pharm-gemini-2-5-flash-reason-1028-runtime-rag-k2-r0-c8d2217a | not_run |  |
| snomed-ncit-pharm-gemma-3-27b-runtime-rag-k2-r0-d727112c | not_run |  |
| snomed-ncit-pharm-gemma-3-27b-runtime-rag-k4-r0-0bc5a8a0 | not_run |  |
| snomed-ncit-pharm-llama-3-1-70b-runtime-rag-k2-r0-36a355e9 | not_run |  |
| snomed-ncit-pharm-llama-3-1-70b-runtime-rag-k4-r0-8ab19ce8 | not_run |  |
| snomed-ncit-pharm-mistral-small-3-2-24b-runtime-rag-k2-r0-530a40b2 | not_run |  |
| snomed-ncit-pharm-mistral-small-3-2-24b-runtime-rag-k4-r0-3357c3aa | not_run |  |
| snomed-ncit-pharm-qwen3-235b-runtime-rag-k2-r0-56c00491 | not_run |  |
| snomed-ncit-pharm-qwen3-235b-runtime-rag-k4-r0-1c75c72f | not_run |  |
| snomed-ncit-pharm-qwen3-5-122b-runtime-rag-k2-r0-051501cf | not_run |  |
| snomed-ncit-pharm-qwen3-5-122b-runtime-rag-k4-r0-58c95219 | not_run |  |
| snomed-ncit-pharm-qwen3-8b-runtime-rag-k2-r0-ff9d726c | not_run |  |
| snomed-ncit-pharm-qwen3-8b-runtime-rag-k4-r0-449536f6 | not_run |  |

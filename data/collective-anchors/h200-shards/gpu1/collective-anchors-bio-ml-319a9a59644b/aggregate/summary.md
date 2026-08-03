# Results: collective-anchors-bio-ml

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
| gemma-3-27b | ca-k4 | 0.7843 | 0.6550 | 0.7139 | 0.7951 | 0.6634 | 0.7109 | 0.5563 | 0.9410 | 0.6976 | 0.9410 | 0.3591 | 0.3001 |
| llama-3-1-70b | ca-k4 | 0.7953 | 0.6558 | 0.7189 | 0.8075 | 0.6643 | 0.7159 | 0.6280 | 0.9401 | 0.7520 | 0.9401 | 0.5169 | 0.4569 |
| mistral-small-3-2-24b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | ca-k4 | 0.7944 | 0.6523 | 0.7164 | 0.8044 | 0.6606 | 0.7132 | 0.5990 | 0.8900 | 0.7158 | 0.8900 | 0.4859 | 0.3759 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma-3-27b | ca-k4 | Global | 5 | 5 | 16552 | 4551 | 8718 | 0.7843 | 0.6550 | 0.7139 |
| llama-3-1-70b | ca-k4 | Global | 5 | 5 | 16573 | 4265 | 8697 | 0.7953 | 0.6558 | 0.7189 |
| qwen3-8b | ca-k4 | Global | 5 | 5 | 16484 | 4267 | 8786 | 0.7944 | 0.6523 | 0.7164 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| ncit-doid-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-ead63d7a | not_run |  |
| ncit-doid-gemini-2-5-flash-off-ca-k4-r0-92553c48 | not_run |  |
| ncit-doid-mistral-small-3-2-24b-ca-k4-r0-6c6fc70f | not_run |  |
| ncit-doid-qwen3-235b-ca-k4-r0-5668c863 | not_run |  |
| ncit-doid-qwen3-5-122b-ca-k4-r0-28549168 | not_run |  |
| omim-ordo-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-aa5f4212 | not_run |  |
| omim-ordo-gemini-2-5-flash-off-ca-k4-r0-26553eb4 | not_run |  |
| omim-ordo-mistral-small-3-2-24b-ca-k4-r0-4ce191c8 | not_run |  |
| omim-ordo-qwen3-235b-ca-k4-r0-841b8221 | not_run |  |
| omim-ordo-qwen3-5-122b-ca-k4-r0-e6011a00 | not_run |  |
| snomed-fma-body-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-e05593d8 | not_run |  |
| snomed-fma-body-gemini-2-5-flash-off-ca-k4-r0-2a0a05d4 | not_run |  |
| snomed-fma-body-mistral-small-3-2-24b-ca-k4-r0-b3befb52 | not_run |  |
| snomed-fma-body-qwen3-235b-ca-k4-r0-2d235d4f | not_run |  |
| snomed-fma-body-qwen3-5-122b-ca-k4-r0-e2c3426f | not_run |  |
| snomed-ncit-neoplas-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-b49809ab | not_run |  |
| snomed-ncit-neoplas-gemini-2-5-flash-off-ca-k4-r0-a6571716 | not_run |  |
| snomed-ncit-neoplas-mistral-small-3-2-24b-ca-k4-r0-282039c0 | not_run |  |
| snomed-ncit-neoplas-qwen3-235b-ca-k4-r0-5078aa4c | not_run |  |
| snomed-ncit-neoplas-qwen3-5-122b-ca-k4-r0-72be1630 | not_run |  |
| snomed-ncit-pharm-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-157b376f | not_run |  |
| snomed-ncit-pharm-gemini-2-5-flash-off-ca-k4-r0-b0efaeee | not_run |  |
| snomed-ncit-pharm-mistral-small-3-2-24b-ca-k4-r0-3a102ade | not_run |  |
| snomed-ncit-pharm-qwen3-235b-ca-k4-r0-14564cda | not_run |  |
| snomed-ncit-pharm-qwen3-5-122b-ca-k4-r0-e32cc83d | not_run |  |

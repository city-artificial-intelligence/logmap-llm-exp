# Results: collective-anchors-bio-ml

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
| mistral-small-3-2-24b | ca-k4 | 0.7866 | 0.6565 | 0.7157 | 0.7978 | 0.6652 | 0.7126 | 0.5737 | 0.9456 | 0.7129 | 0.9456 | 0.3990 | 0.3446 |
| qwen3-235b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| mistral-small-3-2-24b | ca-k4 | Global | 5 | 5 | 16591 | 4502 | 8679 | 0.7866 | 0.6565 | 0.7157 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| ncit-doid-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-ead63d7a | not_run |  |
| ncit-doid-gemini-2-5-flash-off-ca-k4-r0-92553c48 | not_run |  |
| ncit-doid-gemma-3-27b-ca-k4-r0-471bf248 | not_run |  |
| ncit-doid-llama-3-1-70b-ca-k4-r0-e06879c3 | not_run |  |
| ncit-doid-qwen3-235b-ca-k4-r0-5668c863 | not_run |  |
| ncit-doid-qwen3-5-122b-ca-k4-r0-28549168 | not_run |  |
| ncit-doid-qwen3-8b-ca-k4-r0-b21200f4 | not_run |  |
| omim-ordo-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-aa5f4212 | not_run |  |
| omim-ordo-gemini-2-5-flash-off-ca-k4-r0-26553eb4 | not_run |  |
| omim-ordo-gemma-3-27b-ca-k4-r0-066855c8 | not_run |  |
| omim-ordo-llama-3-1-70b-ca-k4-r0-efc5f336 | not_run |  |
| omim-ordo-qwen3-235b-ca-k4-r0-841b8221 | not_run |  |
| omim-ordo-qwen3-5-122b-ca-k4-r0-e6011a00 | not_run |  |
| omim-ordo-qwen3-8b-ca-k4-r0-73f55bba | not_run |  |
| snomed-fma-body-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-e05593d8 | not_run |  |
| snomed-fma-body-gemini-2-5-flash-off-ca-k4-r0-2a0a05d4 | not_run |  |
| snomed-fma-body-gemma-3-27b-ca-k4-r0-deb40da1 | not_run |  |
| snomed-fma-body-llama-3-1-70b-ca-k4-r0-ec544076 | not_run |  |
| snomed-fma-body-qwen3-235b-ca-k4-r0-2d235d4f | not_run |  |
| snomed-fma-body-qwen3-5-122b-ca-k4-r0-e2c3426f | not_run |  |
| snomed-fma-body-qwen3-8b-ca-k4-r0-70be648a | not_run |  |
| snomed-ncit-neoplas-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-b49809ab | not_run |  |
| snomed-ncit-neoplas-gemini-2-5-flash-off-ca-k4-r0-a6571716 | not_run |  |
| snomed-ncit-neoplas-gemma-3-27b-ca-k4-r0-77788c9d | not_run |  |
| snomed-ncit-neoplas-llama-3-1-70b-ca-k4-r0-9aafbc61 | not_run |  |
| snomed-ncit-neoplas-qwen3-235b-ca-k4-r0-5078aa4c | not_run |  |
| snomed-ncit-neoplas-qwen3-5-122b-ca-k4-r0-72be1630 | not_run |  |
| snomed-ncit-neoplas-qwen3-8b-ca-k4-r0-ab07aabf | not_run |  |
| snomed-ncit-pharm-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-157b376f | not_run |  |
| snomed-ncit-pharm-gemini-2-5-flash-off-ca-k4-r0-b0efaeee | not_run |  |
| snomed-ncit-pharm-gemma-3-27b-ca-k4-r0-9df2358a | not_run |  |
| snomed-ncit-pharm-llama-3-1-70b-ca-k4-r0-0d2dbd18 | not_run |  |
| snomed-ncit-pharm-qwen3-235b-ca-k4-r0-14564cda | not_run |  |
| snomed-ncit-pharm-qwen3-5-122b-ca-k4-r0-e32cc83d | not_run |  |
| snomed-ncit-pharm-qwen3-8b-ca-k4-r0-65c6637c | not_run |  |

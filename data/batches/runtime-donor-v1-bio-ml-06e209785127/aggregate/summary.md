# Results: runtime-donor-v1-bio-ml

Coverage: **16/40 (40.0%)**

| Status | Jobs |
|---|---:|
| interrupted | 2 |
| not_run | 22 |
| success | 16 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | rt-k4 | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | rt-k4 | 5 | 5 | 100.0% |
| gemma-3-27b | rt-k4 | 2 | 5 | 40.0% |
| llama-3-1-70b | rt-k4 | 2 | 5 | 40.0% |
| mistral-small-3-2-24b | rt-k4 | 0 | 5 | 0.0% |
| qwen3-235b | rt-k4 | 0 | 5 | 0.0% |
| qwen3-5-122b | rt-k4 | 5 | 5 | 100.0% |
| qwen3-8b | rt-k4 | 2 | 5 | 40.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | rt-k4 | 0.7987 | 0.6545 | 0.7194 | 0.8125 | 0.6626 | 0.7171 | 0.6587 | 0.9265 | 0.7667 | 0.9265 | 0.5720 | 0.4986 |
| gemma-3-27b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| mistral-small-3-2-24b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | rt-k4 | 0.8022 | 0.6539 | 0.7205 | 0.8138 | 0.6622 | 0.7176 | 0.6621 | 0.9162 | 0.7683 | 0.9162 | 0.5919 | 0.5081 |
| qwen3-8b | rt-k4 |  |  |  |  |  |  |  |  |  |  |  |  |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | rt-k4 | Global | 5 | 5 | 16538 | 4169 | 8732 | 0.7987 | 0.6545 | 0.7194 |
| qwen3-5-122b | rt-k4 | Global | 5 | 5 | 16523 | 4073 | 8747 | 0.8022 | 0.6539 | 0.7205 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| ncit-doid-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-e8ee02ea | not_run |  |
| ncit-doid-mistral-small-3-2-24b-rt-k4-r0-412a51f5 | not_run |  |
| ncit-doid-qwen3-235b-rt-k4-r0-c6072218 | not_run |  |
| omim-ordo-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-21a4fca0 | not_run |  |
| omim-ordo-mistral-small-3-2-24b-rt-k4-r0-1b779f3f | not_run |  |
| omim-ordo-qwen3-235b-rt-k4-r0-8dbcb497 | not_run |  |
| snomed-fma-body-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-0fa639ac | not_run |  |
| snomed-fma-body-gemma-3-27b-rt-k4-r0-a49032cf | interrupted |  |
| snomed-fma-body-llama-3-1-70b-rt-k4-r0-4543c029 | interrupted |  |
| snomed-fma-body-mistral-small-3-2-24b-rt-k4-r0-dee19529 | not_run |  |
| snomed-fma-body-qwen3-235b-rt-k4-r0-5db0ac39 | not_run |  |
| snomed-fma-body-qwen3-8b-rt-k4-r0-95075120 | not_run |  |
| snomed-ncit-neoplas-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-eaad27e9 | not_run |  |
| snomed-ncit-neoplas-gemma-3-27b-rt-k4-r0-dd9d06f8 | not_run |  |
| snomed-ncit-neoplas-llama-3-1-70b-rt-k4-r0-c02f02b9 | not_run |  |
| snomed-ncit-neoplas-mistral-small-3-2-24b-rt-k4-r0-cccb2f63 | not_run |  |
| snomed-ncit-neoplas-qwen3-235b-rt-k4-r0-b22b399e | not_run |  |
| snomed-ncit-neoplas-qwen3-8b-rt-k4-r0-1e5ae85c | not_run |  |
| snomed-ncit-pharm-deepseek-v4-flash-gmicloud-fp8-off-rt-k4-r0-9e6e95cb | not_run |  |
| snomed-ncit-pharm-gemma-3-27b-rt-k4-r0-51999feb | not_run |  |
| snomed-ncit-pharm-llama-3-1-70b-rt-k4-r0-f893b730 | not_run |  |
| snomed-ncit-pharm-mistral-small-3-2-24b-rt-k4-r0-eb93ce84 | not_run |  |
| snomed-ncit-pharm-qwen3-235b-rt-k4-r0-18cb1d06 | not_run |  |
| snomed-ncit-pharm-qwen3-8b-rt-k4-r0-62b1d81b | not_run |  |

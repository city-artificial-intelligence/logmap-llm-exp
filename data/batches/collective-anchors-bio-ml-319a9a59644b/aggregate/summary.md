# Results: collective-anchors-bio-ml

Coverage: **25/40 (62.5%)**

| Status | Jobs |
|---|---:|
| not_run | 15 |
| success | 25 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | ca-k4 | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | ca-k4 | 5 | 5 | 100.0% |
| gemma-3-27b | ca-k4 | 5 | 5 | 100.0% |
| llama-3-1-70b | ca-k4 | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | ca-k4 | 0 | 5 | 0.0% |
| qwen3-235b | ca-k4 | 0 | 5 | 0.0% |
| qwen3-5-122b | ca-k4 | 5 | 5 | 100.0% |
| qwen3-8b | ca-k4 | 5 | 5 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | ca-k4 | 0.7993 | 0.6545 | 0.7197 | 0.8122 | 0.6627 | 0.7171 | 0.6546 | 0.9259 | 0.7646 | 0.9259 | 0.5740 | 0.4999 |
| gemma-3-27b | ca-k4 | 0.7845 | 0.6551 | 0.7140 | 0.7954 | 0.6635 | 0.7110 | 0.5570 | 0.9415 | 0.6983 | 0.9415 | 0.3601 | 0.3016 |
| llama-3-1-70b | ca-k4 | 0.7953 | 0.6558 | 0.7189 | 0.8075 | 0.6643 | 0.7159 | 0.6280 | 0.9401 | 0.7520 | 0.9401 | 0.5169 | 0.4569 |
| mistral-small-3-2-24b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | ca-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | ca-k4 | 0.8027 | 0.6540 | 0.7208 | 0.8138 | 0.6623 | 0.7178 | 0.6596 | 0.9131 | 0.7655 | 0.9131 | 0.5919 | 0.5049 |
| qwen3-8b | ca-k4 | 0.7942 | 0.6523 | 0.7163 | 0.8043 | 0.6605 | 0.7131 | 0.5990 | 0.8901 | 0.7159 | 0.8901 | 0.4859 | 0.3760 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | ca-k4 | Global | 5 | 5 | 16540 | 4154 | 8730 | 0.7993 | 0.6545 | 0.7197 |
| gemma-3-27b | ca-k4 | Global | 5 | 5 | 16554 | 4547 | 8716 | 0.7845 | 0.6551 | 0.7140 |
| llama-3-1-70b | ca-k4 | Global | 5 | 5 | 16573 | 4265 | 8697 | 0.7953 | 0.6558 | 0.7189 |
| qwen3-5-122b | ca-k4 | Global | 5 | 5 | 16527 | 4063 | 8743 | 0.8027 | 0.6540 | 0.7208 |
| qwen3-8b | ca-k4 | Global | 5 | 5 | 16483 | 4270 | 8787 | 0.7942 | 0.6523 | 0.7163 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| ncit-doid-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-ead63d7a | not_run |  |
| ncit-doid-mistral-small-3-2-24b-ca-k4-r0-6c6fc70f | not_run |  |
| ncit-doid-qwen3-235b-ca-k4-r0-5668c863 | not_run |  |
| omim-ordo-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-aa5f4212 | not_run |  |
| omim-ordo-mistral-small-3-2-24b-ca-k4-r0-4ce191c8 | not_run |  |
| omim-ordo-qwen3-235b-ca-k4-r0-841b8221 | not_run |  |
| snomed-fma-body-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-e05593d8 | not_run |  |
| snomed-fma-body-mistral-small-3-2-24b-ca-k4-r0-b3befb52 | not_run |  |
| snomed-fma-body-qwen3-235b-ca-k4-r0-2d235d4f | not_run |  |
| snomed-ncit-neoplas-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-b49809ab | not_run |  |
| snomed-ncit-neoplas-mistral-small-3-2-24b-ca-k4-r0-282039c0 | not_run |  |
| snomed-ncit-neoplas-qwen3-235b-ca-k4-r0-5078aa4c | not_run |  |
| snomed-ncit-pharm-deepseek-v4-flash-gmicloud-fp8-off-ca-k4-r0-157b376f | not_run |  |
| snomed-ncit-pharm-mistral-small-3-2-24b-ca-k4-r0-3a102ade | not_run |  |
| snomed-ncit-pharm-qwen3-235b-ca-k4-r0-14564cda | not_run |  |

# Results: static-fewshot-bio-ml

Coverage: **14/30 (46.7%)**

| Status | Jobs |
|---|---:|
| failed | 2 |
| interrupted | 3 |
| not_run | 11 |
| success | 14 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| gemini-2-5-flash-off | static-k4 | 5 | 5 | 100.0% |
| gemma-3-27b | static-k4 | 2 | 5 | 40.0% |
| llama-3-1-70b | static-k4 | 2 | 5 | 40.0% |
| mistral-small-3-2-24b | static-k4 | 0 | 5 | 0.0% |
| qwen3-5-122b | static-k4 | 3 | 5 | 60.0% |
| qwen3-8b | static-k4 | 2 | 5 | 40.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | static-k4 | 0.7983 | 0.6546 | 0.7194 | 0.8119 | 0.6626 | 0.7170 | 0.6569 | 0.9373 | 0.7684 | 0.9373 | 0.5666 | 0.5039 |
| gemma-3-27b | static-k4 | 0.8777 | 0.7074 | 0.7834 | 0.8773 | 0.6838 | 0.7512 | 0.5639 | 0.9571 | 0.7094 | 0.9571 | 0.4433 | 0.4004 |
| llama-3-1-70b | static-k4 | 0.8912 | 0.7085 | 0.7894 | 0.8929 | 0.6848 | 0.7570 | 0.6522 | 0.9710 | 0.7789 | 0.9710 | 0.6028 | 0.5738 |
| mistral-small-3-2-24b | static-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | static-k4 | 0.8017 | 0.7237 | 0.7607 | 0.8202 | 0.7095 | 0.7412 | 0.6955 | 0.9290 | 0.7948 | 0.9290 | 0.6231 | 0.5521 |
| qwen3-8b | static-k4 | 0.8829 | 0.7049 | 0.7839 | 0.8807 | 0.6815 | 0.7519 | 0.5727 | 0.9267 | 0.7078 | 0.9267 | 0.4835 | 0.4102 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | static-k4 | Global | 5 | 5 | 16543 | 4180 | 8727 | 0.7983 | 0.6546 | 0.7194 |
| gemma-3-27b | static-k4 | Global | 2 | 2 | 5947 | 829 | 2460 | 0.8777 | 0.7074 | 0.7834 |
| llama-3-1-70b | static-k4 | Global | 2 | 2 | 5956 | 727 | 2451 | 0.8912 | 0.7085 | 0.7894 |
| qwen3-5-122b | static-k4 | Global | 3 | 3 | 8837 | 2186 | 3374 | 0.8017 | 0.7237 | 0.7607 |
| qwen3-8b | static-k4 | Global | 2 | 2 | 5926 | 786 | 2481 | 0.8829 | 0.7049 | 0.7839 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| ncit-doid-mistral-small-3-2-24b-static-k4-r0-fa7b1c0d | not_run |  |
| omim-ordo-mistral-small-3-2-24b-static-k4-r0-ba0c77b7 | not_run |  |
| snomed-fma-body-gemma-3-27b-static-k4-r0-fbd52a2f | interrupted |  |
| snomed-fma-body-llama-3-1-70b-static-k4-r0-23457443 | interrupted |  |
| snomed-fma-body-mistral-small-3-2-24b-static-k4-r0-d58e900a | not_run |  |
| snomed-fma-body-qwen3-5-122b-static-k4-r0-c743cff8 | failed | job snomed-fma-body-qwen3-5-122b-static-k4-r0-c743cff8 failed; see /home/jon/canonical_projects_folder/logmap-llm-exp/batches/static-fewshot-bio-ml-090c9129f326/jobs/snomed-fma-body-qwen3-5-122b-static-k4-r0-c743cff8/attempts/0001/run.log |
| snomed-fma-body-qwen3-8b-static-k4-r0-af7bac8e | failed | job snomed-fma-body-qwen3-8b-static-k4-r0-af7bac8e failed; see /home/jon/canonical_projects_folder/logmap-llm-exp/batches/static-fewshot-bio-ml-090c9129f326/jobs/snomed-fma-body-qwen3-8b-static-k4-r0-af7bac8e/attempts/0001/run.log |
| snomed-ncit-neoplas-gemma-3-27b-static-k4-r0-807147d2 | not_run |  |
| snomed-ncit-neoplas-llama-3-1-70b-static-k4-r0-28220cd3 | not_run |  |
| snomed-ncit-neoplas-mistral-small-3-2-24b-static-k4-r0-e80809f5 | not_run |  |
| snomed-ncit-neoplas-qwen3-8b-static-k4-r0-5c713f7f | interrupted |  |
| snomed-ncit-pharm-gemma-3-27b-static-k4-r0-a6411e98 | not_run |  |
| snomed-ncit-pharm-llama-3-1-70b-static-k4-r0-8866fb9e | not_run |  |
| snomed-ncit-pharm-mistral-small-3-2-24b-static-k4-r0-64912278 | not_run |  |
| snomed-ncit-pharm-qwen3-5-122b-static-k4-r0-a8613ede | not_run |  |
| snomed-ncit-pharm-qwen3-8b-static-k4-r0-1ee423e6 | not_run |  |

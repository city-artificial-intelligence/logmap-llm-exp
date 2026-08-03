# Results: sweep-one-bio-ml

Coverage: **33/45 (73.3%)**

| Status | Jobs |
|---|---:|
| degraded | 2 |
| not_run | 10 |
| running | 2 |
| success | 31 |

## Groups

| model | completed | expected | coverage |
|---|---|---|---|
| deepseek-v4-flash | 4 | 5 | 80.0% |
| gemini-2-5-flash | 4 | 5 | 80.0% |
| gemma-3-27b | 4 | 5 | 80.0% |
| llama-3-1-70b | 4 | 5 | 80.0% |
| mistral-small-3-2-24b | 4 | 5 | 80.0% |
| plain-logmap | 5 | 5 | 100.0% |
| qwen3-235b | 0 | 5 | 0.0% |
| qwen3-5-122b | 4 | 5 | 80.0% |
| qwen3-8b | 4 | 5 | 80.0% |

## Primary metrics

| model | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 0.8081 | 0.6933 | 0.7463 | 0.8199 | 0.6898 | 0.7335 | 0.6570 | 0.9474 | 0.7747 | 0.9474 | 0.5320 | 0.4795 |
| gemini-2-5-flash | 0.8104 | 0.6925 | 0.7468 | 0.8223 | 0.6887 | 0.7340 | 0.6688 | 0.9410 | 0.7808 | 0.9410 | 0.5549 | 0.4958 |
| gemma-3-27b | 0.7893 | 0.6956 | 0.7395 | 0.7994 | 0.6919 | 0.7265 | 0.5522 | 0.9757 | 0.7042 | 0.9757 | 0.2647 | 0.2403 |
| llama-3-1-70b | 0.8052 | 0.6942 | 0.7456 | 0.8178 | 0.6907 | 0.7328 | 0.6455 | 0.9547 | 0.7690 | 0.9547 | 0.4984 | 0.4531 |
| mistral-small-3-2-24b | 0.8042 | 0.6929 | 0.7444 | 0.8169 | 0.6894 | 0.7316 | 0.6409 | 0.9391 | 0.7595 | 0.9391 | 0.4962 | 0.4353 |
| plain-logmap | 0.7649 | 0.6541 | 0.7052 | 0.7793 | 0.6614 | 0.7001 |  |  |  |  |  |  |
| qwen3-235b |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | 0.8121 | 0.6920 | 0.7473 | 0.8230 | 0.6884 | 0.7346 | 0.6679 | 0.9325 | 0.7782 | 0.9325 | 0.5632 | 0.4956 |
| qwen3-8b | 0.7957 | 0.6936 | 0.7411 | 0.8068 | 0.6898 | 0.7282 | 0.5868 | 0.9563 | 0.7263 | 0.9563 | 0.3702 | 0.3266 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | Global | 4 | 4 | 12489 | 2965 | 5525 | 0.8081 | 0.6933 | 0.7463 |
| gemini-2-5-flash | Global | 4 | 4 | 12474 | 2919 | 5540 | 0.8104 | 0.6925 | 0.7468 |
| gemma-3-27b | Global | 4 | 4 | 12531 | 3346 | 5483 | 0.7893 | 0.6956 | 0.7395 |
| llama-3-1-70b | Global | 4 | 4 | 12505 | 3026 | 5509 | 0.8052 | 0.6942 | 0.7456 |
| mistral-small-3-2-24b | Global | 4 | 4 | 12482 | 3039 | 5532 | 0.8042 | 0.6929 | 0.7444 |
| plain-logmap | Global | 5 | 5 | 16529 | 5079 | 8741 | 0.7649 | 0.6541 | 0.7052 |
| qwen3-5-122b | Global | 4 | 4 | 12466 | 2884 | 5548 | 0.8121 | 0.6920 | 0.7473 |
| qwen3-8b | Global | 4 | 4 | 12495 | 3209 | 5519 | 0.7957 | 0.6936 | 0.7411 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| ncit-doid-qwen3-235b-zero-shot-r0-68bdd13a | not_run |  |
| omim-ordo-qwen3-235b-zero-shot-r0-cacf1041 | not_run |  |
| snomed-fma-body-deepseek-v4-flash-zero-shot-r0-4e4a8e2b | not_run |  |
| snomed-fma-body-gemini-2-5-flash-zero-shot-r0-94220a19 | not_run |  |
| snomed-fma-body-gemma-3-27b-zero-shot-r0-21a240dc | running |  |
| snomed-fma-body-llama-3-1-70b-zero-shot-r0-83a11862 | not_run |  |
| snomed-fma-body-mistral-small-3-2-24b-zero-shot-r0-9d54b08b | not_run |  |
| snomed-fma-body-qwen3-235b-zero-shot-r0-ba119299 | not_run |  |
| snomed-fma-body-qwen3-5-122b-zero-shot-r0-ffa5f616 | not_run |  |
| snomed-fma-body-qwen3-8b-zero-shot-r0-36a98040 | running |  |
| snomed-ncit-neoplas-qwen3-235b-zero-shot-r0-e1886d37 | not_run |  |
| snomed-ncit-pharm-qwen3-235b-zero-shot-r0-11c1b3fa | not_run |  |

# Results: sweep-one-bio-ml-snomed-fma-body

Coverage: **9/9 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 9 |

## Groups

| model | completed | expected | coverage |
|---|---|---|---|
| deepseek-v4-flash | 1 | 1 | 100.0% |
| gemini-2-5-flash | 1 | 1 | 100.0% |
| gemma-3-27b | 1 | 1 | 100.0% |
| llama-3-1-70b | 1 | 1 | 100.0% |
| mistral-small-3-2-24b | 1 | 1 | 100.0% |
| plain-logmap | 1 | 1 | 100.0% |
| qwen3-235b | 1 | 1 | 100.0% |
| qwen3-5-122b | 1 | 1 | 100.0% |
| qwen3-8b | 1 | 1 | 100.0% |

## Primary metrics

| model | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 0.7610 | 0.5642 | 0.6480 | 0.7610 | 0.5642 | 0.6480 | 0.5448 | 0.9566 | 0.6942 | 0.9566 | 0.5250 | 0.4816 |
| gemini-2-5-flash | 0.7588 | 0.5620 | 0.6458 | 0.7588 | 0.5620 | 0.6458 | 0.5182 | 0.8889 | 0.6547 | 0.8889 | 0.5089 | 0.3977 |
| gemma-3-27b | 0.7404 | 0.5639 | 0.6402 | 0.7404 | 0.5639 | 0.6402 | 0.4372 | 0.9431 | 0.5974 | 0.9431 | 0.2786 | 0.2217 |
| llama-3-1-70b | 0.7562 | 0.5622 | 0.6449 | 0.7562 | 0.5622 | 0.6449 | 0.5084 | 0.9024 | 0.6504 | 0.9024 | 0.4815 | 0.3839 |
| mistral-small-3-2-24b | 0.7586 | 0.5623 | 0.6459 | 0.7586 | 0.5623 | 0.6459 | 0.5197 | 0.8916 | 0.6567 | 0.8916 | 0.5105 | 0.4021 |
| plain-logmap | 0.7283 | 0.5637 | 0.6355 | 0.7283 | 0.5637 | 0.6355 |  |  |  |  |  |  |
| qwen3-235b | 0.7715 | 0.5593 | 0.6484 | 0.7715 | 0.5593 | 0.6484 | 0.5936 | 0.8076 | 0.6843 | 0.8076 | 0.6715 | 0.4791 |
| qwen3-5-122b | 0.7681 | 0.5627 | 0.6495 | 0.7681 | 0.5627 | 0.6495 | 0.5884 | 0.9106 | 0.7149 | 0.9106 | 0.6216 | 0.5321 |
| qwen3-8b | 0.7629 | 0.5609 | 0.6465 | 0.7629 | 0.5609 | 0.6465 | 0.5317 | 0.8401 | 0.6513 | 0.8401 | 0.5604 | 0.4005 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | Global | 1 | 1 | 4094 | 1286 | 3162 | 0.7610 | 0.5642 | 0.6480 |
| gemini-2-5-flash | Global | 1 | 1 | 4078 | 1296 | 3178 | 0.7588 | 0.5620 | 0.6458 |
| gemma-3-27b | Global | 1 | 1 | 4092 | 1435 | 3164 | 0.7404 | 0.5639 | 0.6402 |
| llama-3-1-70b | Global | 1 | 1 | 4079 | 1315 | 3177 | 0.7562 | 0.5622 | 0.6449 |
| mistral-small-3-2-24b | Global | 1 | 1 | 4080 | 1298 | 3176 | 0.7586 | 0.5623 | 0.6459 |
| plain-logmap | Global | 1 | 1 | 4090 | 1526 | 3166 | 0.7283 | 0.5637 | 0.6355 |
| qwen3-235b | Global | 1 | 1 | 4058 | 1202 | 3198 | 0.7715 | 0.5593 | 0.6484 |
| qwen3-5-122b | Global | 1 | 1 | 4083 | 1233 | 3173 | 0.7681 | 0.5627 | 0.6495 |
| qwen3-8b | Global | 1 | 1 | 4070 | 1265 | 3186 | 0.7629 | 0.5609 | 0.6465 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

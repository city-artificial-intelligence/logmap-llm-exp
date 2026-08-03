# Results: plain-true-false-recovery-deepseek-gmicloud-knowledge-graph

Coverage: **15/15 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 15 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | plain-k0 | 5 | 5 | 100.0% |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k2 | 5 | 5 | 100.0% |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k4 | 5 | 5 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | plain-k0 | 0.8924 | 0.7296 | 0.8029 | 0.8989 | 0.6998 | 0.7824 | 0.7333 | 0.5074 | 0.5748 | 0.6343 | 0.8706 | 0.5975 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k2 | 0.8926 | 0.7294 | 0.8028 | 0.8990 | 0.6999 | 0.7824 | 0.6833 | 0.5541 | 0.5725 | 0.6926 | 0.9482 | 0.6279 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k4 | 0.8926 | 0.7298 | 0.8030 | 0.8990 | 0.7001 | 0.7826 | 0.6872 | 0.6148 | 0.6186 | 0.7685 | 0.9424 | 0.6965 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | plain-k0 | Global | 5 | 5 | 11205 | 1351 | 4152 | 0.8924 | 0.7296 | 0.8029 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k0 | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k0 | INST | 5 | 5 | 11003 | 1336 | 4124 | 0.8917 | 0.7274 | 0.8012 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k0 | PROP | 5 | 5 | 172 | 13 | 9 | 0.9297 | 0.9503 | 0.9399 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k0 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k2 | Global | 5 | 5 | 11202 | 1348 | 4155 | 0.8926 | 0.7294 | 0.8028 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k2 | CLS | 5 | 5 | 30 | 2 | 19 | 0.9375 | 0.6122 | 0.7407 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k2 | INST | 5 | 5 | 11000 | 1336 | 4127 | 0.8917 | 0.7272 | 0.8011 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k2 | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k2 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k4 | Global | 5 | 5 | 11207 | 1349 | 4150 | 0.8926 | 0.7298 | 0.8030 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k4 | CLS | 5 | 5 | 32 | 3 | 17 | 0.9143 | 0.6531 | 0.7619 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k4 | INST | 5 | 5 | 11003 | 1336 | 4124 | 0.8917 | 0.7274 | 0.8012 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k4 | PROP | 5 | 5 | 172 | 10 | 9 | 0.9451 | 0.9503 | 0.9477 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k4 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

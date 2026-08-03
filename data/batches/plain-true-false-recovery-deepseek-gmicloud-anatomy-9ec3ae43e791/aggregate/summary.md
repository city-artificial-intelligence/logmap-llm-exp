# Results: plain-true-false-recovery-deepseek-gmicloud-anatomy

Coverage: **3/3 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 3 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | plain-k0 | 1 | 1 | 100.0% |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k2 | 1 | 1 | 100.0% |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k4 | 1 | 1 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | plain-k0 | 0.9518 | 0.8470 | 0.8963 | 0.9518 | 0.8470 | 0.8963 | 0.7990 | 0.9879 | 0.8835 | 0.9879 | 0.5638 | 0.5517 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k2 | 0.9608 | 0.8417 | 0.8973 | 0.9608 | 0.8417 | 0.8973 | 0.8470 | 0.9394 | 0.8908 | 0.9394 | 0.7021 | 0.6415 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k4 | 0.9579 | 0.8404 | 0.8953 | 0.9579 | 0.8404 | 0.8953 | 0.8270 | 0.9273 | 0.8743 | 0.9273 | 0.6596 | 0.5868 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | plain-k0 | Global | 1 | 1 | 1284 | 65 | 232 | 0.9518 | 0.8470 | 0.8963 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k2 | Global | 1 | 1 | 1276 | 52 | 240 | 0.9608 | 0.8417 | 0.8973 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k4 | Global | 1 | 1 | 1274 | 56 | 242 | 0.9579 | 0.8404 | 0.8953 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

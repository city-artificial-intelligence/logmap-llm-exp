# Results: plain-true-false-recovery-deepseek-gmicloud-bio-ml

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
| deepseek-v4-flash-gmicloud-fp8-off | plain-k0 | 0.7890 | 0.6570 | 0.7170 | 0.8009 | 0.6655 | 0.7141 | 0.5926 | 0.9577 | 0.7302 | 0.9577 | 0.4350 | 0.3926 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k2 | 0.8034 | 0.6523 | 0.7200 | 0.8157 | 0.6601 | 0.7172 | 0.6772 | 0.9004 | 0.7712 | 0.9004 | 0.6261 | 0.5265 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k4 | 0.8025 | 0.6532 | 0.7202 | 0.8153 | 0.6611 | 0.7175 | 0.6759 | 0.9128 | 0.7745 | 0.9128 | 0.6160 | 0.5289 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | plain-k0 | Global | 5 | 5 | 16603 | 4440 | 8667 | 0.7890 | 0.6570 | 0.7170 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k2 | Global | 5 | 5 | 16483 | 4034 | 8787 | 0.8034 | 0.6523 | 0.7200 |
| deepseek-v4-flash-gmicloud-fp8-off | plain-k4 | Global | 5 | 5 | 16506 | 4061 | 8764 | 0.8025 | 0.6532 | 0.7202 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

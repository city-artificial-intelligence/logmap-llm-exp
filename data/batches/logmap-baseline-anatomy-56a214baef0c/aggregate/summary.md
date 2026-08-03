# Results: logmap-baseline-anatomy

Coverage: **1/1 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 1 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| plain-logmap | k0 | 1 | 1 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 |
|---|---|---|---|---|---|---|---|
| plain-logmap | k0 | 0.9160 | 0.8483 | 0.8808 | 0.9160 | 0.8483 | 0.8808 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| plain-logmap | k0 | Global | 1 | 1 | 1286 | 118 | 230 | 0.9160 | 0.8483 | 0.8808 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

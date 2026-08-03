# Results: logmap-baseline-bio-ml

Coverage: **5/5 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 5 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| plain-logmap | k0 | 5 | 5 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 |
|---|---|---|---|---|---|---|---|
| plain-logmap | k0 | 0.7652 | 0.6541 | 0.7053 | 0.7795 | 0.6614 | 0.7002 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| plain-logmap | k0 | Global | 5 | 5 | 16529 | 5072 | 8741 | 0.7652 | 0.6541 | 0.7053 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

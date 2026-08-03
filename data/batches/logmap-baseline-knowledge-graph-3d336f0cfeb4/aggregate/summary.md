# Results: logmap-baseline-knowledge-graph

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
| plain-logmap | k0 | 0.8926 | 0.7283 | 0.8021 | 0.8989 | 0.6976 | 0.7809 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| plain-logmap | k0 | Global | 5 | 5 | 11184 | 1346 | 4173 | 0.8926 | 0.7283 | 0.8021 |
| plain-logmap | k0 | CLS | 5 | 5 | 31 | 3 | 18 | 0.9118 | 0.6327 | 0.7470 |
| plain-logmap | k0 | INST | 5 | 5 | 10981 | 1336 | 4146 | 0.8915 | 0.7259 | 0.8002 |
| plain-logmap | k0 | PROP | 5 | 5 | 172 | 7 | 9 | 0.9609 | 0.9503 | 0.9556 |
| plain-logmap | k0 | UNKNOWN | 5 | 5 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

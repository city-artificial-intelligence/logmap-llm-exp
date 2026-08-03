# Results: mutual-subsumption-bio-ml

Coverage: **20/20 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 20 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| gemma-3-27b | bidir-k0 | 5 | 5 | 100.0% |
| llama-3-1-70b | bidir-k0 | 5 | 5 | 100.0% |
| qwen3-5-122b | bidir-k0 | 5 | 5 | 100.0% |
| qwen3-8b | bidir-k0 | 5 | 5 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma-3-27b | bidir-k0 | 0.8058 | 0.6485 | 0.7186 | 0.8154 | 0.6563 | 0.7152 | 0.6657 | 0.8346 | 0.7402 | 0.8346 | 0.6401 | 0.4746 |
| llama-3-1-70b | bidir-k0 | 0.8066 | 0.6506 | 0.7202 | 0.8194 | 0.6587 | 0.7175 | 0.6986 | 0.8628 | 0.7708 | 0.8628 | 0.6673 | 0.5301 |
| qwen3-5-122b | bidir-k0 | 0.8143 | 0.6488 | 0.7222 | 0.8264 | 0.6564 | 0.7193 | 0.7571 | 0.8464 | 0.7982 | 0.8464 | 0.7545 | 0.6009 |
| qwen3-8b | bidir-k0 | 0.8009 | 0.6497 | 0.7174 | 0.8123 | 0.6574 | 0.7142 | 0.6521 | 0.8636 | 0.7423 | 0.8636 | 0.6006 | 0.4642 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma-3-27b | bidir-k0 | Global | 5 | 5 | 16388 | 3950 | 8882 | 0.8058 | 0.6485 | 0.7186 |
| llama-3-1-70b | bidir-k0 | Global | 5 | 5 | 16441 | 3943 | 8829 | 0.8066 | 0.6506 | 0.7202 |
| qwen3-5-122b | bidir-k0 | Global | 5 | 5 | 16394 | 3739 | 8876 | 0.8143 | 0.6488 | 0.7222 |
| qwen3-8b | bidir-k0 | Global | 5 | 5 | 16418 | 4081 | 8852 | 0.8009 | 0.6497 | 0.7174 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

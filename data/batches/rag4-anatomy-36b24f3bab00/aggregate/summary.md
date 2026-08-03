# Results: rag4-anatomy

Coverage: **5/8 (62.5%)**

| Status | Jobs |
|---|---:|
| not_run | 3 |
| success | 5 |

## Groups

| model | completed | expected | coverage |
|---|---|---|---|
| deepseek-v4-flash | 0 | 1 | 0.0% |
| gemini-2-5-flash | 0 | 1 | 0.0% |
| gemma-3-27b | 1 | 1 | 100.0% |
| llama-3-1-70b | 1 | 1 | 100.0% |
| mistral-small-3-2-24b | 0 | 1 | 0.0% |
| qwen3-235b | 1 | 1 | 100.0% |
| qwen3-5-122b | 1 | 1 | 100.0% |
| qwen3-8b | 1 | 1 | 100.0% |

## Primary metrics

| model | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | 0.9454 | 0.8456 | 0.8928 | 0.9454 | 0.8456 | 0.8928 | 0.7667 | 0.9758 | 0.8587 | 0.9758 | 0.4787 | 0.4545 |
| llama-3-1-70b | 0.9532 | 0.8463 | 0.8966 | 0.9532 | 0.8463 | 0.8966 | 0.8100 | 0.9818 | 0.8877 | 0.9818 | 0.5957 | 0.5776 |
| mistral-small-3-2-24b |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | 0.9553 | 0.8450 | 0.8967 | 0.9553 | 0.8450 | 0.8967 | 0.8205 | 0.9697 | 0.8889 | 0.9697 | 0.6277 | 0.5974 |
| qwen3-5-122b | 0.9588 | 0.8450 | 0.8983 | 0.9588 | 0.8450 | 0.8983 | 0.8421 | 0.9697 | 0.9014 | 0.9697 | 0.6809 | 0.6505 |
| qwen3-8b | 0.9557 | 0.8397 | 0.8940 | 0.9557 | 0.8397 | 0.8940 | 0.8172 | 0.9212 | 0.8661 | 0.9212 | 0.6383 | 0.5595 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|
| gemma-3-27b | Global | 1 | 1 | 1282 | 74 | 234 | 0.9454 | 0.8456 | 0.8928 |
| llama-3-1-70b | Global | 1 | 1 | 1283 | 63 | 233 | 0.9532 | 0.8463 | 0.8966 |
| qwen3-235b | Global | 1 | 1 | 1281 | 60 | 235 | 0.9553 | 0.8450 | 0.8967 |
| qwen3-5-122b | Global | 1 | 1 | 1281 | 55 | 235 | 0.9588 | 0.8450 | 0.8983 |
| qwen3-8b | Global | 1 | 1 | 1273 | 59 | 243 | 0.9557 | 0.8397 | 0.8940 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| anatomy-deepseek-v4-flash-query-rag-k4-r0-01dc40c1 | not_run |  |
| anatomy-gemini-2-5-flash-query-rag-k4-r0-bae17f0f | not_run |  |
| anatomy-mistral-small-3-2-24b-query-rag-k4-r0-df67e80f | not_run |  |

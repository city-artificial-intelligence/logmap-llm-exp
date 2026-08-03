# Results: plain-true-false-anatomy

Coverage: **21/24 (87.5%)**

| Status | Jobs |
|---|---:|
| not_run | 3 |
| success | 21 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | plain-k0 | 0 | 1 | 0.0% |
| deepseek-v4-flash-parasail-off | plain-k2 | 0 | 1 | 0.0% |
| deepseek-v4-flash-parasail-off | plain-k4 | 0 | 1 | 0.0% |
| gemini-2-5-flash-off | plain-k0 | 1 | 1 | 100.0% |
| gemini-2-5-flash-off | plain-k2 | 1 | 1 | 100.0% |
| gemini-2-5-flash-off | plain-k4 | 1 | 1 | 100.0% |
| gemma-3-27b | plain-k0 | 1 | 1 | 100.0% |
| gemma-3-27b | plain-k2 | 1 | 1 | 100.0% |
| gemma-3-27b | plain-k4 | 1 | 1 | 100.0% |
| llama-3-1-70b | plain-k0 | 1 | 1 | 100.0% |
| llama-3-1-70b | plain-k2 | 1 | 1 | 100.0% |
| llama-3-1-70b | plain-k4 | 1 | 1 | 100.0% |
| mistral-small-3-2-24b | plain-k0 | 1 | 1 | 100.0% |
| mistral-small-3-2-24b | plain-k2 | 1 | 1 | 100.0% |
| mistral-small-3-2-24b | plain-k4 | 1 | 1 | 100.0% |
| qwen3-235b | plain-k0 | 1 | 1 | 100.0% |
| qwen3-235b | plain-k2 | 1 | 1 | 100.0% |
| qwen3-235b | plain-k4 | 1 | 1 | 100.0% |
| qwen3-5-122b | plain-k0 | 1 | 1 | 100.0% |
| qwen3-5-122b | plain-k2 | 1 | 1 | 100.0% |
| qwen3-5-122b | plain-k4 | 1 | 1 | 100.0% |
| qwen3-8b | plain-k0 | 1 | 1 | 100.0% |
| qwen3-8b | plain-k2 | 1 | 1 | 100.0% |
| qwen3-8b | plain-k4 | 1 | 1 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | plain-k0 |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-parasail-off | plain-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-parasail-off | plain-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | plain-k0 | 0.9588 | 0.8450 | 0.8983 | 0.9588 | 0.8450 | 0.8983 | 0.8377 | 0.9697 | 0.8989 | 0.9697 | 0.6702 | 0.6399 |
| gemini-2-5-flash-off | plain-k2 | 0.9545 | 0.8443 | 0.8960 | 0.9545 | 0.8443 | 0.8960 | 0.8112 | 0.9636 | 0.8809 | 0.9636 | 0.6064 | 0.5700 |
| gemini-2-5-flash-off | plain-k4 | 0.9553 | 0.8456 | 0.8971 | 0.9553 | 0.8456 | 0.8971 | 0.8173 | 0.9758 | 0.8895 | 0.9758 | 0.6170 | 0.5928 |
| gemma-3-27b | plain-k0 | 0.9420 | 0.8463 | 0.8916 | 0.9420 | 0.8463 | 0.8916 | 0.7465 | 0.9818 | 0.8482 | 0.9818 | 0.4149 | 0.3967 |
| gemma-3-27b | plain-k2 | 0.9489 | 0.8456 | 0.8943 | 0.9489 | 0.8456 | 0.8943 | 0.7816 | 0.9758 | 0.8679 | 0.9758 | 0.5213 | 0.4970 |
| gemma-3-27b | plain-k4 | 0.9474 | 0.8443 | 0.8929 | 0.9474 | 0.8443 | 0.8929 | 0.7718 | 0.9636 | 0.8571 | 0.9636 | 0.5000 | 0.4636 |
| llama-3-1-70b | plain-k0 | 0.9545 | 0.8450 | 0.8964 | 0.9545 | 0.8450 | 0.8964 | 0.8122 | 0.9697 | 0.8840 | 0.9697 | 0.6064 | 0.5761 |
| llama-3-1-70b | plain-k2 | 0.9587 | 0.8417 | 0.8964 | 0.9587 | 0.8417 | 0.8964 | 0.8333 | 0.9394 | 0.8832 | 0.9394 | 0.6702 | 0.6096 |
| llama-3-1-70b | plain-k4 | 0.9544 | 0.8430 | 0.8953 | 0.9544 | 0.8430 | 0.8953 | 0.8093 | 0.9515 | 0.8747 | 0.9515 | 0.6064 | 0.5579 |
| mistral-small-3-2-24b | plain-k0 | 0.9490 | 0.8463 | 0.8947 | 0.9490 | 0.8463 | 0.8947 | 0.7826 | 0.9818 | 0.8710 | 0.9818 | 0.5213 | 0.5031 |
| mistral-small-3-2-24b | plain-k2 | 0.9525 | 0.8456 | 0.8959 | 0.9525 | 0.8456 | 0.8959 | 0.8010 | 0.9758 | 0.8798 | 0.9758 | 0.5745 | 0.5502 |
| mistral-small-3-2-24b | plain-k4 | 0.9510 | 0.8456 | 0.8953 | 0.9510 | 0.8456 | 0.8953 | 0.7931 | 0.9758 | 0.8750 | 0.9758 | 0.5532 | 0.5289 |
| qwen3-235b | plain-k0 | 0.9588 | 0.8437 | 0.8975 | 0.9588 | 0.8437 | 0.8975 | 0.8360 | 0.9576 | 0.8927 | 0.9576 | 0.6702 | 0.6278 |
| qwen3-235b | plain-k2 | 0.9560 | 0.8456 | 0.8974 | 0.9560 | 0.8456 | 0.8974 | 0.8214 | 0.9758 | 0.8920 | 0.9758 | 0.6277 | 0.6034 |
| qwen3-235b | plain-k4 | 0.9532 | 0.8456 | 0.8962 | 0.9532 | 0.8456 | 0.8962 | 0.8050 | 0.9758 | 0.8822 | 0.9758 | 0.5851 | 0.5609 |
| qwen3-5-122b | plain-k0 | 0.9561 | 0.8470 | 0.8982 | 0.9561 | 0.8470 | 0.8982 | 0.8232 | 0.9879 | 0.8981 | 0.9879 | 0.6277 | 0.6155 |
| qwen3-5-122b | plain-k2 | 0.9580 | 0.8423 | 0.8965 | 0.9580 | 0.8423 | 0.8965 | 0.8298 | 0.9455 | 0.8839 | 0.9455 | 0.6596 | 0.6050 |
| qwen3-5-122b | plain-k4 | 0.9594 | 0.8423 | 0.8971 | 0.9594 | 0.8423 | 0.8971 | 0.8387 | 0.9455 | 0.8889 | 0.9455 | 0.6809 | 0.6263 |
| qwen3-8b | plain-k0 | 0.9413 | 0.8470 | 0.8917 | 0.9413 | 0.8470 | 0.8917 | 0.7443 | 0.9879 | 0.8490 | 0.9879 | 0.4043 | 0.3921 |
| qwen3-8b | plain-k2 | 0.9515 | 0.8410 | 0.8929 | 0.9515 | 0.8410 | 0.8929 | 0.7897 | 0.9333 | 0.8556 | 0.9333 | 0.5638 | 0.4972 |
| qwen3-8b | plain-k4 | 0.9565 | 0.8404 | 0.8947 | 0.9565 | 0.8404 | 0.8947 | 0.8182 | 0.9273 | 0.8693 | 0.9273 | 0.6383 | 0.5656 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | plain-k0 | Global | 1 | 1 | 1281 | 55 | 235 | 0.9588 | 0.8450 | 0.8983 |
| gemini-2-5-flash-off | plain-k2 | Global | 1 | 1 | 1280 | 61 | 236 | 0.9545 | 0.8443 | 0.8960 |
| gemini-2-5-flash-off | plain-k4 | Global | 1 | 1 | 1282 | 60 | 234 | 0.9553 | 0.8456 | 0.8971 |
| gemma-3-27b | plain-k0 | Global | 1 | 1 | 1283 | 79 | 233 | 0.9420 | 0.8463 | 0.8916 |
| gemma-3-27b | plain-k2 | Global | 1 | 1 | 1282 | 69 | 234 | 0.9489 | 0.8456 | 0.8943 |
| gemma-3-27b | plain-k4 | Global | 1 | 1 | 1280 | 71 | 236 | 0.9474 | 0.8443 | 0.8929 |
| llama-3-1-70b | plain-k0 | Global | 1 | 1 | 1281 | 61 | 235 | 0.9545 | 0.8450 | 0.8964 |
| llama-3-1-70b | plain-k2 | Global | 1 | 1 | 1276 | 55 | 240 | 0.9587 | 0.8417 | 0.8964 |
| llama-3-1-70b | plain-k4 | Global | 1 | 1 | 1278 | 61 | 238 | 0.9544 | 0.8430 | 0.8953 |
| mistral-small-3-2-24b | plain-k0 | Global | 1 | 1 | 1283 | 69 | 233 | 0.9490 | 0.8463 | 0.8947 |
| mistral-small-3-2-24b | plain-k2 | Global | 1 | 1 | 1282 | 64 | 234 | 0.9525 | 0.8456 | 0.8959 |
| mistral-small-3-2-24b | plain-k4 | Global | 1 | 1 | 1282 | 66 | 234 | 0.9510 | 0.8456 | 0.8953 |
| qwen3-235b | plain-k0 | Global | 1 | 1 | 1279 | 55 | 237 | 0.9588 | 0.8437 | 0.8975 |
| qwen3-235b | plain-k2 | Global | 1 | 1 | 1282 | 59 | 234 | 0.9560 | 0.8456 | 0.8974 |
| qwen3-235b | plain-k4 | Global | 1 | 1 | 1282 | 63 | 234 | 0.9532 | 0.8456 | 0.8962 |
| qwen3-5-122b | plain-k0 | Global | 1 | 1 | 1284 | 59 | 232 | 0.9561 | 0.8470 | 0.8982 |
| qwen3-5-122b | plain-k2 | Global | 1 | 1 | 1277 | 56 | 239 | 0.9580 | 0.8423 | 0.8965 |
| qwen3-5-122b | plain-k4 | Global | 1 | 1 | 1277 | 54 | 239 | 0.9594 | 0.8423 | 0.8971 |
| qwen3-8b | plain-k0 | Global | 1 | 1 | 1284 | 80 | 232 | 0.9413 | 0.8470 | 0.8917 |
| qwen3-8b | plain-k2 | Global | 1 | 1 | 1275 | 65 | 241 | 0.9515 | 0.8410 | 0.8929 |
| qwen3-8b | plain-k4 | Global | 1 | 1 | 1274 | 58 | 242 | 0.9565 | 0.8404 | 0.8947 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| anatomy-deepseek-v4-flash-parasail-off-plain-k0-r0-ad603422 | not_run |  |
| anatomy-deepseek-v4-flash-parasail-off-plain-k2-r0-f0cf4987 | not_run |  |
| anatomy-deepseek-v4-flash-parasail-off-plain-k4-r0-b6164534 | not_run |  |

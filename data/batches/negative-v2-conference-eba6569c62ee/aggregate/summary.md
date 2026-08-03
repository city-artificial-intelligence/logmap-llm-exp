# Results: negative-v2-conference

Coverage: **189/189 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 189 |

## Groups

| model | completed | expected | coverage |
|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | 21 | 21 | 100.0% |
| gemini-2-5-flash-off | 21 | 21 | 100.0% |
| gemma-3-27b | 21 | 21 | 100.0% |
| llama-3-1-70b | 21 | 21 | 100.0% |
| mistral-small-3-2-24b | 21 | 21 | 100.0% |
| plain-logmap | 21 | 21 | 100.0% |
| qwen3-235b | 21 | 21 | 100.0% |
| qwen3-5-122b | 21 | 21 | 100.0% |
| qwen3-8b | 21 | 21 | 100.0% |

## Primary metrics

| model | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | 0.7930 | 0.5902 | 0.6767 | 0.8178 | 0.6156 | 0.6879 | 0.3135 | 0.4048 | 0.3424 | 0.9444 | 0.2569 | 0.0500 |
| gemini-2-5-flash-off | 0.8100 | 0.5869 | 0.6806 | 0.8354 | 0.6128 | 0.6923 | 0.3730 | 0.3889 | 0.3714 | 0.9074 | 0.6319 | 0.5833 |
| gemma-3-27b | 0.8072 | 0.5902 | 0.6818 | 0.8340 | 0.6156 | 0.6936 | 0.3452 | 0.4048 | 0.3662 | 0.9444 | 0.5486 | 0.3500 |
| llama-3-1-70b | 0.7965 | 0.5902 | 0.6780 | 0.8250 | 0.6156 | 0.6902 | 0.3452 | 0.4048 | 0.3662 | 0.9444 | 0.4375 | 0.3500 |
| mistral-small-3-2-24b | 0.8044 | 0.5934 | 0.6830 | 0.8309 | 0.6188 | 0.6941 | 0.3452 | 0.4286 | 0.3741 | 1.0000 | 0.5069 | 0.4500 |
| plain-logmap | 0.8100 | 0.5869 | 0.6806 | 0.8343 | 0.6133 | 0.6932 |  |  |  |  |  |  |
| qwen3-235b | 0.8136 | 0.5869 | 0.6819 | 0.8367 | 0.6128 | 0.6926 | 0.3651 | 0.3889 | 0.3730 | 0.9074 | 0.6181 | 0.4833 |
| qwen3-5-122b | 0.8027 | 0.5869 | 0.6780 | 0.8302 | 0.6128 | 0.6900 | 0.3413 | 0.3889 | 0.3571 | 0.9074 | 0.5069 | 0.2833 |
| qwen3-8b | 0.8128 | 0.5836 | 0.6794 | 0.8363 | 0.6108 | 0.6914 | 0.2937 | 0.3413 | 0.3079 | 0.7963 | 0.5764 | 0.2833 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-gmicloud-fp8-off | Global | 21 | 21 | 180 | 47 | 125 | 0.7930 | 0.5902 | 0.6767 |
| deepseek-v4-flash-gmicloud-fp8-off | M1/class | 21 | 21 | 167 | 32 | 92 | 0.8392 | 0.6448 | 0.7293 |
| deepseek-v4-flash-gmicloud-fp8-off | M2/property | 21 | 21 | 13 | 15 | 33 | 0.4643 | 0.2826 | 0.3514 |
| deepseek-v4-flash-gmicloud-fp8-off | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| gemini-2-5-flash-off | Global | 21 | 21 | 179 | 42 | 126 | 0.8100 | 0.5869 | 0.6806 |
| gemini-2-5-flash-off | M1/class | 21 | 21 | 166 | 31 | 93 | 0.8426 | 0.6409 | 0.7281 |
| gemini-2-5-flash-off | M2/property | 21 | 21 | 13 | 11 | 33 | 0.5417 | 0.2826 | 0.3714 |
| gemini-2-5-flash-off | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| gemma-3-27b | Global | 21 | 21 | 180 | 43 | 125 | 0.8072 | 0.5902 | 0.6818 |
| gemma-3-27b | M1/class | 21 | 21 | 167 | 31 | 92 | 0.8434 | 0.6448 | 0.7309 |
| gemma-3-27b | M2/property | 21 | 21 | 13 | 12 | 33 | 0.5200 | 0.2826 | 0.3662 |
| gemma-3-27b | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| llama-3-1-70b | Global | 21 | 21 | 180 | 46 | 125 | 0.7965 | 0.5902 | 0.6780 |
| llama-3-1-70b | M1/class | 21 | 21 | 167 | 31 | 92 | 0.8434 | 0.6448 | 0.7309 |
| llama-3-1-70b | M2/property | 21 | 21 | 13 | 15 | 33 | 0.4643 | 0.2826 | 0.3514 |
| llama-3-1-70b | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| mistral-small-3-2-24b | Global | 21 | 21 | 181 | 44 | 124 | 0.8044 | 0.5934 | 0.6830 |
| mistral-small-3-2-24b | M1/class | 21 | 21 | 167 | 32 | 92 | 0.8392 | 0.6448 | 0.7293 |
| mistral-small-3-2-24b | M2/property | 21 | 21 | 14 | 12 | 32 | 0.5385 | 0.3043 | 0.3889 |
| mistral-small-3-2-24b | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| plain-logmap | Global | 21 | 21 | 179 | 42 | 126 | 0.8100 | 0.5869 | 0.6806 |
| plain-logmap | M1/class | 21 | 21 | 166 | 33 | 93 | 0.8342 | 0.6409 | 0.7249 |
| plain-logmap | M2/property | 21 | 21 | 13 | 9 | 33 | 0.5909 | 0.2826 | 0.3824 |
| plain-logmap | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| qwen3-235b | Global | 21 | 21 | 179 | 41 | 126 | 0.8136 | 0.5869 | 0.6819 |
| qwen3-235b | M1/class | 21 | 21 | 166 | 31 | 93 | 0.8426 | 0.6409 | 0.7281 |
| qwen3-235b | M2/property | 21 | 21 | 13 | 10 | 33 | 0.5652 | 0.2826 | 0.3768 |
| qwen3-235b | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| qwen3-5-122b | Global | 21 | 21 | 179 | 44 | 126 | 0.8027 | 0.5869 | 0.6780 |
| qwen3-5-122b | M1/class | 21 | 21 | 166 | 31 | 93 | 0.8426 | 0.6409 | 0.7281 |
| qwen3-5-122b | M2/property | 21 | 21 | 13 | 13 | 33 | 0.5000 | 0.2826 | 0.3611 |
| qwen3-5-122b | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | Global | 21 | 21 | 178 | 41 | 127 | 0.8128 | 0.5836 | 0.6794 |
| qwen3-8b | M1/class | 21 | 21 | 166 | 31 | 93 | 0.8426 | 0.6409 | 0.7281 |
| qwen3-8b | M2/property | 21 | 21 | 12 | 10 | 34 | 0.5455 | 0.2609 | 0.3529 |
| qwen3-8b | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

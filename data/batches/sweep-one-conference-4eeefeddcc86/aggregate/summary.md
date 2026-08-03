# Results: sweep-one-conference

Coverage: **189/189 (100.0%)**

| Status | Jobs |
|---|---:|
| success | 189 |

## Groups

| model | completed | expected | coverage |
|---|---|---|---|
| deepseek-v4-flash | 21 | 21 | 100.0% |
| gemini-2-5-flash | 21 | 21 | 100.0% |
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
| deepseek-v4-flash | 0.8000 | 0.5902 | 0.6792 | 0.8275 | 0.6156 | 0.6908 | 0.3135 | 0.4048 | 0.3424 | 0.9444 | 0.3819 | 0.0500 |
| gemini-2-5-flash | 0.8036 | 0.5902 | 0.6805 | 0.8310 | 0.6156 | 0.6920 | 0.3452 | 0.4048 | 0.3662 | 0.9444 | 0.5069 | 0.3500 |
| gemma-3-27b | 0.8000 | 0.5902 | 0.6792 | 0.8259 | 0.6156 | 0.6903 | 0.3452 | 0.4048 | 0.3662 | 0.9444 | 0.4236 | 0.3500 |
| llama-3-1-70b | 0.7974 | 0.5934 | 0.6805 | 0.8268 | 0.6188 | 0.6922 | 0.3294 | 0.4286 | 0.3646 | 1.0000 | 0.3958 | 0.2500 |
| mistral-small-3-2-24b | 0.8044 | 0.5934 | 0.6830 | 0.8309 | 0.6188 | 0.6941 | 0.3452 | 0.4286 | 0.3741 | 1.0000 | 0.5069 | 0.4500 |
| plain-logmap | 0.8100 | 0.5869 | 0.6806 | 0.8343 | 0.6133 | 0.6932 |  |  |  |  |  |  |
| qwen3-235b | 0.8174 | 0.5869 | 0.6832 | 0.8395 | 0.6128 | 0.6939 | 0.3889 | 0.3889 | 0.3810 | 0.9074 | 0.7014 | 0.6833 |
| qwen3-5-122b | 0.8036 | 0.5902 | 0.6805 | 0.8310 | 0.6156 | 0.6920 | 0.3452 | 0.4048 | 0.3662 | 0.9444 | 0.5069 | 0.3500 |
| qwen3-8b | 0.8128 | 0.5836 | 0.6794 | 0.8363 | 0.6108 | 0.6914 | 0.3016 | 0.3413 | 0.3159 | 0.7963 | 0.6181 | 0.3833 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | Global | 21 | 21 | 180 | 45 | 125 | 0.8000 | 0.5902 | 0.6792 |
| deepseek-v4-flash | M1/class | 21 | 21 | 167 | 32 | 92 | 0.8392 | 0.6448 | 0.7293 |
| deepseek-v4-flash | M2/property | 21 | 21 | 13 | 13 | 33 | 0.5000 | 0.2826 | 0.3611 |
| deepseek-v4-flash | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| gemini-2-5-flash | Global | 21 | 21 | 180 | 44 | 125 | 0.8036 | 0.5902 | 0.6805 |
| gemini-2-5-flash | M1/class | 21 | 21 | 167 | 31 | 92 | 0.8434 | 0.6448 | 0.7309 |
| gemini-2-5-flash | M2/property | 21 | 21 | 13 | 13 | 33 | 0.5000 | 0.2826 | 0.3611 |
| gemini-2-5-flash | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| gemma-3-27b | Global | 21 | 21 | 180 | 45 | 125 | 0.8000 | 0.5902 | 0.6792 |
| gemma-3-27b | M1/class | 21 | 21 | 167 | 31 | 92 | 0.8434 | 0.6448 | 0.7309 |
| gemma-3-27b | M2/property | 21 | 21 | 13 | 14 | 33 | 0.4815 | 0.2826 | 0.3562 |
| gemma-3-27b | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| llama-3-1-70b | Global | 21 | 21 | 181 | 46 | 124 | 0.7974 | 0.5934 | 0.6805 |
| llama-3-1-70b | M1/class | 21 | 21 | 167 | 32 | 92 | 0.8392 | 0.6448 | 0.7293 |
| llama-3-1-70b | M2/property | 21 | 21 | 14 | 14 | 32 | 0.5000 | 0.3043 | 0.3784 |
| llama-3-1-70b | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| mistral-small-3-2-24b | Global | 21 | 21 | 181 | 44 | 124 | 0.8044 | 0.5934 | 0.6830 |
| mistral-small-3-2-24b | M1/class | 21 | 21 | 167 | 32 | 92 | 0.8392 | 0.6448 | 0.7293 |
| mistral-small-3-2-24b | M2/property | 21 | 21 | 14 | 12 | 32 | 0.5385 | 0.3043 | 0.3889 |
| mistral-small-3-2-24b | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| plain-logmap | Global | 21 | 21 | 179 | 42 | 126 | 0.8100 | 0.5869 | 0.6806 |
| plain-logmap | M1/class | 21 | 21 | 166 | 33 | 93 | 0.8342 | 0.6409 | 0.7249 |
| plain-logmap | M2/property | 21 | 21 | 13 | 9 | 33 | 0.5909 | 0.2826 | 0.3824 |
| plain-logmap | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| qwen3-235b | Global | 21 | 21 | 179 | 40 | 126 | 0.8174 | 0.5869 | 0.6832 |
| qwen3-235b | M1/class | 21 | 21 | 166 | 31 | 93 | 0.8426 | 0.6409 | 0.7281 |
| qwen3-235b | M2/property | 21 | 21 | 13 | 9 | 33 | 0.5909 | 0.2826 | 0.3824 |
| qwen3-235b | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| qwen3-5-122b | Global | 21 | 21 | 180 | 44 | 125 | 0.8036 | 0.5902 | 0.6805 |
| qwen3-5-122b | M1/class | 21 | 21 | 167 | 31 | 92 | 0.8434 | 0.6448 | 0.7309 |
| qwen3-5-122b | M2/property | 21 | 21 | 13 | 13 | 33 | 0.5000 | 0.2826 | 0.3611 |
| qwen3-5-122b | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |
| qwen3-8b | Global | 21 | 21 | 178 | 41 | 127 | 0.8128 | 0.5836 | 0.6794 |
| qwen3-8b | M1/class | 21 | 21 | 166 | 31 | 93 | 0.8426 | 0.6409 | 0.7281 |
| qwen3-8b | M2/property | 21 | 21 | 12 | 10 | 34 | 0.5455 | 0.2609 | 0.3529 |
| qwen3-8b | UNKNOWN | 21 | 21 | 0 | 0 | 0 |  |  |  |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

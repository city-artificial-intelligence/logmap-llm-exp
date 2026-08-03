# Results: rag-runtime-anatomy

Coverage: **3/18 (16.7%)**

| Status | Jobs |
|---|---:|
| degraded | 1 |
| not_run | 15 |
| success | 2 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-parasail-high | runtime-rag-k2 | 1 | 1 | 100.0% |
| deepseek-v4-flash-parasail-off | runtime-rag-k2 | 1 | 1 | 100.0% |
| deepseek-v4-flash-parasail-off | runtime-rag-k4 | 1 | 1 | 100.0% |
| gemini-2-5-flash-off | runtime-rag-k2 | 0 | 1 | 0.0% |
| gemini-2-5-flash-off | runtime-rag-k4 | 0 | 1 | 0.0% |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2 | 0 | 1 | 0.0% |
| gemma-3-27b | runtime-rag-k2 | 0 | 1 | 0.0% |
| gemma-3-27b | runtime-rag-k4 | 0 | 1 | 0.0% |
| llama-3-1-70b | runtime-rag-k2 | 0 | 1 | 0.0% |
| llama-3-1-70b | runtime-rag-k4 | 0 | 1 | 0.0% |
| mistral-small-3-2-24b | runtime-rag-k2 | 0 | 1 | 0.0% |
| mistral-small-3-2-24b | runtime-rag-k4 | 0 | 1 | 0.0% |
| qwen3-235b | runtime-rag-k2 | 0 | 1 | 0.0% |
| qwen3-235b | runtime-rag-k4 | 0 | 1 | 0.0% |
| qwen3-5-122b | runtime-rag-k2 | 0 | 1 | 0.0% |
| qwen3-5-122b | runtime-rag-k4 | 0 | 1 | 0.0% |
| qwen3-8b | runtime-rag-k2 | 0 | 1 | 0.0% |
| qwen3-8b | runtime-rag-k4 | 0 | 1 | 0.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-high | runtime-rag-k2 | 0.9652 | 0.8410 | 0.8988 | 0.9652 | 0.8410 | 0.8988 | 0.8750 | 0.9390 | 0.9059 | 0.9390 | 0.7634 | 0.7025 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2 | 0.9623 | 0.8430 | 0.8987 | 0.9623 | 0.8430 | 0.8987 | 0.8579 | 0.9515 | 0.9023 | 0.9515 | 0.7234 | 0.6749 |
| deepseek-v4-flash-parasail-off | runtime-rag-k4 | 0.9594 | 0.8417 | 0.8967 | 0.9594 | 0.8417 | 0.8967 | 0.8378 | 0.9394 | 0.8857 | 0.9394 | 0.6809 | 0.6202 |
| gemini-2-5-flash-off | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-reason-1028 | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemma-3-27b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| llama-3-1-70b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| mistral-small-3-2-24b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| mistral-small-3-2-24b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-235b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-5-122b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | runtime-rag-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| qwen3-8b | runtime-rag-k4 |  |  |  |  |  |  |  |  |  |  |  |  |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-high | runtime-rag-k2 | Global | 1 | 1 | 1275 | 46 | 241 | 0.9652 | 0.8410 | 0.8988 |
| deepseek-v4-flash-parasail-off | runtime-rag-k2 | Global | 1 | 1 | 1278 | 50 | 238 | 0.9623 | 0.8430 | 0.8987 |
| deepseek-v4-flash-parasail-off | runtime-rag-k4 | Global | 1 | 1 | 1276 | 54 | 240 | 0.9594 | 0.8417 | 0.8967 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| anatomy-gemini-2-5-flash-off-runtime-rag-k2-r0-8cd5c8cf | not_run |  |
| anatomy-gemini-2-5-flash-off-runtime-rag-k4-r0-fb1f4d7c | not_run |  |
| anatomy-gemini-2-5-flash-reason-1028-runtime-rag-k2-r0-f0f8400d | not_run |  |
| anatomy-gemma-3-27b-runtime-rag-k2-r0-cc209f8b | not_run |  |
| anatomy-gemma-3-27b-runtime-rag-k4-r0-121dbae7 | not_run |  |
| anatomy-llama-3-1-70b-runtime-rag-k2-r0-5e2522e8 | not_run |  |
| anatomy-llama-3-1-70b-runtime-rag-k4-r0-d14b7c65 | not_run |  |
| anatomy-mistral-small-3-2-24b-runtime-rag-k2-r0-953c662a | not_run |  |
| anatomy-mistral-small-3-2-24b-runtime-rag-k4-r0-0ea016b2 | not_run |  |
| anatomy-qwen3-235b-runtime-rag-k2-r0-57d65a4a | not_run |  |
| anatomy-qwen3-235b-runtime-rag-k4-r0-e589adf5 | not_run |  |
| anatomy-qwen3-5-122b-runtime-rag-k2-r0-decbf508 | not_run |  |
| anatomy-qwen3-5-122b-runtime-rag-k4-r0-76441eea | not_run |  |
| anatomy-qwen3-8b-runtime-rag-k2-r0-097ac0e8 | not_run |  |
| anatomy-qwen3-8b-runtime-rag-k4-r0-5bd630b5 | not_run |  |

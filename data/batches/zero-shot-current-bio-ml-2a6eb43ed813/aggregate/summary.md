# Results: zero-shot-current-bio-ml

Coverage: **40/40 (100.0%)**

| Status | Jobs |
|---|---:|
| degraded | 1 |
| success | 39 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | zero-shot-current | 5 | 5 | 100.0% |
| gemini-2-5-flash-off | zero-shot-current | 5 | 5 | 100.0% |
| gemma-3-27b | zero-shot-current | 5 | 5 | 100.0% |
| llama-3-1-70b | zero-shot-current | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | zero-shot-current | 5 | 5 | 100.0% |
| qwen3-235b | zero-shot-current | 5 | 5 | 100.0% |
| qwen3-5-122b | zero-shot-current | 5 | 5 | 100.0% |
| qwen3-8b | zero-shot-current | 5 | 5 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | zero-shot-current | 0.7973 | 0.6563 | 0.7200 | 0.8094 | 0.6647 | 0.7170 | 0.6429 | 0.9492 | 0.7647 | 0.9492 | 0.5431 | 0.4923 |
| gemini-2-5-flash-off | zero-shot-current | 0.7972 | 0.6549 | 0.7191 | 0.8097 | 0.6633 | 0.7163 | 0.6401 | 0.9300 | 0.7565 | 0.9300 | 0.5465 | 0.4765 |
| gemma-3-27b | zero-shot-current | 0.7771 | 0.6579 | 0.7125 | 0.7881 | 0.6663 | 0.7094 | 0.5310 | 0.9691 | 0.6843 | 0.9691 | 0.2680 | 0.2371 |
| llama-3-1-70b | zero-shot-current | 0.7927 | 0.6563 | 0.7181 | 0.8056 | 0.6650 | 0.7153 | 0.6186 | 0.9443 | 0.7457 | 0.9443 | 0.4933 | 0.4376 |
| mistral-small-3-2-24b | zero-shot-current | 0.7927 | 0.6554 | 0.7175 | 0.8054 | 0.6640 | 0.7145 | 0.6176 | 0.9292 | 0.7395 | 0.9292 | 0.4984 | 0.4276 |
| qwen3-235b | zero-shot-current | 0.8040 | 0.6518 | 0.7199 | 0.8152 | 0.6600 | 0.7168 | 0.6745 | 0.8841 | 0.7636 | 0.8841 | 0.6309 | 0.5150 |
| qwen3-5-122b | zero-shot-current | 0.8011 | 0.6550 | 0.7207 | 0.8122 | 0.6633 | 0.7177 | 0.6529 | 0.9274 | 0.7659 | 0.9274 | 0.5731 | 0.5004 |
| qwen3-8b | zero-shot-current | 0.7877 | 0.6555 | 0.7156 | 0.7984 | 0.6641 | 0.7120 | 0.5779 | 0.9328 | 0.7128 | 0.9328 | 0.4096 | 0.3425 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | zero-shot-current | Global | 5 | 5 | 16585 | 4217 | 8685 | 0.7973 | 0.6563 | 0.7200 |
| gemini-2-5-flash-off | zero-shot-current | Global | 5 | 5 | 16550 | 4210 | 8720 | 0.7972 | 0.6549 | 0.7191 |
| gemma-3-27b | zero-shot-current | Global | 5 | 5 | 16624 | 4767 | 8646 | 0.7771 | 0.6579 | 0.7125 |
| llama-3-1-70b | zero-shot-current | Global | 5 | 5 | 16584 | 4336 | 8686 | 0.7927 | 0.6563 | 0.7181 |
| mistral-small-3-2-24b | zero-shot-current | Global | 5 | 5 | 16562 | 4332 | 8708 | 0.7927 | 0.6554 | 0.7175 |
| qwen3-235b | zero-shot-current | Global | 5 | 5 | 16470 | 4015 | 8800 | 0.8040 | 0.6518 | 0.7199 |
| qwen3-5-122b | zero-shot-current | Global | 5 | 5 | 16551 | 4110 | 8719 | 0.8011 | 0.6550 | 0.7207 |
| qwen3-8b | zero-shot-current | Global | 5 | 5 | 16565 | 4464 | 8705 | 0.7877 | 0.6555 | 0.7156 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

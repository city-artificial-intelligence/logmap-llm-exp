# Results: plain-true-false-bio-ml

Coverage: **105/120 (87.5%)**

| Status | Jobs |
|---|---:|
| not_run | 15 |
| success | 105 |

## Groups

| model | condition | completed | expected | coverage |
|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | plain-k0 | 0 | 5 | 0.0% |
| deepseek-v4-flash-parasail-off | plain-k2 | 0 | 5 | 0.0% |
| deepseek-v4-flash-parasail-off | plain-k4 | 0 | 5 | 0.0% |
| gemini-2-5-flash-off | plain-k0 | 5 | 5 | 100.0% |
| gemini-2-5-flash-off | plain-k2 | 5 | 5 | 100.0% |
| gemini-2-5-flash-off | plain-k4 | 5 | 5 | 100.0% |
| gemma-3-27b | plain-k0 | 5 | 5 | 100.0% |
| gemma-3-27b | plain-k2 | 5 | 5 | 100.0% |
| gemma-3-27b | plain-k4 | 5 | 5 | 100.0% |
| llama-3-1-70b | plain-k0 | 5 | 5 | 100.0% |
| llama-3-1-70b | plain-k2 | 5 | 5 | 100.0% |
| llama-3-1-70b | plain-k4 | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | plain-k0 | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | plain-k2 | 5 | 5 | 100.0% |
| mistral-small-3-2-24b | plain-k4 | 5 | 5 | 100.0% |
| qwen3-235b | plain-k0 | 5 | 5 | 100.0% |
| qwen3-235b | plain-k2 | 5 | 5 | 100.0% |
| qwen3-235b | plain-k4 | 5 | 5 | 100.0% |
| qwen3-5-122b | plain-k0 | 5 | 5 | 100.0% |
| qwen3-5-122b | plain-k2 | 5 | 5 | 100.0% |
| qwen3-5-122b | plain-k4 | 5 | 5 | 100.0% |
| qwen3-8b | plain-k0 | 5 | 5 | 100.0% |
| qwen3-8b | plain-k2 | 5 | 5 | 100.0% |
| qwen3-8b | plain-k4 | 5 | 5 | 100.0% |

## Primary metrics

| model | condition | pooled.global.precision | pooled.global.recall | pooled.global.f1 | mean.global.precision | mean.global.recall | mean.global.f1 | mean.oracle.oracle_precision | mean.oracle.oracle_recall | mean.oracle.oracle_f1 | mean.oracle.sensitivity | mean.oracle.specificity | mean.oracle.youdens_j |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash-parasail-off | plain-k0 |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-parasail-off | plain-k2 |  |  |  |  |  |  |  |  |  |  |  |  |
| deepseek-v4-flash-parasail-off | plain-k4 |  |  |  |  |  |  |  |  |  |  |  |  |
| gemini-2-5-flash-off | plain-k0 | 0.7997 | 0.6541 | 0.7196 | 0.8117 | 0.6624 | 0.7167 | 0.6511 | 0.9190 | 0.7607 | 0.9190 | 0.5742 | 0.4932 |
| gemini-2-5-flash-off | plain-k2 | 0.8004 | 0.6538 | 0.7197 | 0.8136 | 0.6619 | 0.7173 | 0.6636 | 0.9195 | 0.7684 | 0.9195 | 0.5867 | 0.5063 |
| gemini-2-5-flash-off | plain-k4 | 0.7986 | 0.6544 | 0.7193 | 0.8124 | 0.6626 | 0.7170 | 0.6580 | 0.9257 | 0.7660 | 0.9257 | 0.5715 | 0.4972 |
| gemma-3-27b | plain-k0 | 0.7878 | 0.6550 | 0.7153 | 0.7981 | 0.6633 | 0.7118 | 0.5747 | 0.9290 | 0.7089 | 0.9290 | 0.4109 | 0.3399 |
| gemma-3-27b | plain-k2 | 0.7886 | 0.6533 | 0.7146 | 0.8002 | 0.6612 | 0.7121 | 0.5792 | 0.9129 | 0.7064 | 0.9129 | 0.4291 | 0.3420 |
| gemma-3-27b | plain-k4 | 0.7880 | 0.6537 | 0.7146 | 0.7994 | 0.6619 | 0.7119 | 0.5713 | 0.9247 | 0.7042 | 0.9247 | 0.4014 | 0.3261 |
| llama-3-1-70b | plain-k0 | 0.7910 | 0.6565 | 0.7175 | 0.8038 | 0.6651 | 0.7146 | 0.6081 | 0.9470 | 0.7393 | 0.9470 | 0.4680 | 0.4150 |
| llama-3-1-70b | plain-k2 | 0.7978 | 0.6544 | 0.7190 | 0.8108 | 0.6627 | 0.7165 | 0.6462 | 0.9263 | 0.7596 | 0.9263 | 0.5554 | 0.4817 |
| llama-3-1-70b | plain-k4 | 0.7967 | 0.6548 | 0.7188 | 0.8098 | 0.6632 | 0.7162 | 0.6399 | 0.9272 | 0.7555 | 0.9272 | 0.5430 | 0.4702 |
| mistral-small-3-2-24b | plain-k0 | 0.7885 | 0.6562 | 0.7163 | 0.8009 | 0.6647 | 0.7130 | 0.5918 | 0.9422 | 0.7254 | 0.9422 | 0.4324 | 0.3747 |
| mistral-small-3-2-24b | plain-k2 | 0.7885 | 0.6560 | 0.7162 | 0.8015 | 0.6643 | 0.7136 | 0.5942 | 0.9454 | 0.7271 | 0.9454 | 0.4386 | 0.3839 |
| mistral-small-3-2-24b | plain-k4 | 0.7879 | 0.6563 | 0.7161 | 0.8011 | 0.6647 | 0.7134 | 0.5916 | 0.9488 | 0.7264 | 0.9488 | 0.4262 | 0.3751 |
| qwen3-235b | plain-k0 | 0.8012 | 0.6537 | 0.7200 | 0.8127 | 0.6621 | 0.7169 | 0.6589 | 0.9092 | 0.7629 | 0.9092 | 0.5938 | 0.5030 |
| qwen3-235b | plain-k2 | 0.7922 | 0.6543 | 0.7166 | 0.8044 | 0.6625 | 0.7141 | 0.6067 | 0.9253 | 0.7309 | 0.9253 | 0.4833 | 0.4086 |
| qwen3-235b | plain-k4 | 0.7878 | 0.6556 | 0.7156 | 0.7996 | 0.6640 | 0.7130 | 0.5827 | 0.9396 | 0.7172 | 0.9396 | 0.4232 | 0.3628 |
| qwen3-5-122b | plain-k0 | 0.8009 | 0.6555 | 0.7209 | 0.8122 | 0.6639 | 0.7180 | 0.6532 | 0.9359 | 0.7689 | 0.9359 | 0.5708 | 0.5067 |
| qwen3-5-122b | plain-k2 | 0.8028 | 0.6539 | 0.7208 | 0.8144 | 0.6620 | 0.7179 | 0.6658 | 0.9203 | 0.7722 | 0.9203 | 0.5919 | 0.5123 |
| qwen3-5-122b | plain-k4 | 0.8023 | 0.6538 | 0.7205 | 0.8140 | 0.6621 | 0.7176 | 0.6626 | 0.9146 | 0.7681 | 0.9146 | 0.5921 | 0.5067 |
| qwen3-8b | plain-k0 | 0.7823 | 0.6560 | 0.7136 | 0.7931 | 0.6646 | 0.7103 | 0.5507 | 0.9411 | 0.6942 | 0.9411 | 0.3396 | 0.2806 |
| qwen3-8b | plain-k2 | 0.7933 | 0.6527 | 0.7162 | 0.8030 | 0.6609 | 0.7131 | 0.5940 | 0.8991 | 0.7144 | 0.8991 | 0.4770 | 0.3761 |
| qwen3-8b | plain-k4 | 0.7953 | 0.6520 | 0.7166 | 0.8060 | 0.6604 | 0.7136 | 0.6093 | 0.8852 | 0.7211 | 0.8852 | 0.5148 | 0.4000 |

All metrics and contributor counts are in `summary.csv`.

## Pooled alignment strata

| model | condition | stratum | jobs | expected | TP | FP | FN | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2-5-flash-off | plain-k0 | Global | 5 | 5 | 16530 | 4140 | 8740 | 0.7997 | 0.6541 | 0.7196 |
| gemini-2-5-flash-off | plain-k2 | Global | 5 | 5 | 16522 | 4121 | 8748 | 0.8004 | 0.6538 | 0.7197 |
| gemini-2-5-flash-off | plain-k4 | Global | 5 | 5 | 16536 | 4169 | 8734 | 0.7986 | 0.6544 | 0.7193 |
| gemma-3-27b | plain-k0 | Global | 5 | 5 | 16552 | 4459 | 8718 | 0.7878 | 0.6550 | 0.7153 |
| gemma-3-27b | plain-k2 | Global | 5 | 5 | 16508 | 4424 | 8762 | 0.7886 | 0.6533 | 0.7146 |
| gemma-3-27b | plain-k4 | Global | 5 | 5 | 16518 | 4445 | 8752 | 0.7880 | 0.6537 | 0.7146 |
| llama-3-1-70b | plain-k0 | Global | 5 | 5 | 16589 | 4384 | 8681 | 0.7910 | 0.6565 | 0.7175 |
| llama-3-1-70b | plain-k2 | Global | 5 | 5 | 16536 | 4192 | 8734 | 0.7978 | 0.6544 | 0.7190 |
| llama-3-1-70b | plain-k4 | Global | 5 | 5 | 16546 | 4221 | 8724 | 0.7967 | 0.6548 | 0.7188 |
| mistral-small-3-2-24b | plain-k0 | Global | 5 | 5 | 16581 | 4448 | 8689 | 0.7885 | 0.6562 | 0.7163 |
| mistral-small-3-2-24b | plain-k2 | Global | 5 | 5 | 16577 | 4447 | 8693 | 0.7885 | 0.6560 | 0.7162 |
| mistral-small-3-2-24b | plain-k4 | Global | 5 | 5 | 16585 | 4465 | 8685 | 0.7879 | 0.6563 | 0.7161 |
| qwen3-235b | plain-k0 | Global | 5 | 5 | 16518 | 4098 | 8752 | 0.8012 | 0.6537 | 0.7200 |
| qwen3-235b | plain-k2 | Global | 5 | 5 | 16533 | 4337 | 8737 | 0.7922 | 0.6543 | 0.7166 |
| qwen3-235b | plain-k4 | Global | 5 | 5 | 16566 | 4461 | 8704 | 0.7878 | 0.6556 | 0.7156 |
| qwen3-5-122b | plain-k0 | Global | 5 | 5 | 16565 | 4119 | 8705 | 0.8009 | 0.6555 | 0.7209 |
| qwen3-5-122b | plain-k2 | Global | 5 | 5 | 16524 | 4058 | 8746 | 0.8028 | 0.6539 | 0.7208 |
| qwen3-5-122b | plain-k4 | Global | 5 | 5 | 16521 | 4070 | 8749 | 0.8023 | 0.6538 | 0.7205 |
| qwen3-8b | plain-k0 | Global | 5 | 5 | 16578 | 4614 | 8692 | 0.7823 | 0.6560 | 0.7136 |
| qwen3-8b | plain-k2 | Global | 5 | 5 | 16494 | 4298 | 8776 | 0.7933 | 0.6527 | 0.7162 |
| qwen3-8b | plain-k4 | Global | 5 | 5 | 16476 | 4241 | 8794 | 0.7953 | 0.6520 | 0.7166 |

TP/FP/FN are additive. Alignment TN is not defined without an explicit candidate universe.

## Incomplete jobs

| Job | Status | Detail |
|---|---|---|
| ncit-doid-deepseek-v4-flash-parasail-off-plain-k0-r0-51e24130 | not_run |  |
| ncit-doid-deepseek-v4-flash-parasail-off-plain-k2-r0-7a852160 | not_run |  |
| ncit-doid-deepseek-v4-flash-parasail-off-plain-k4-r0-0e1f2399 | not_run |  |
| omim-ordo-deepseek-v4-flash-parasail-off-plain-k0-r0-d6e14f12 | not_run |  |
| omim-ordo-deepseek-v4-flash-parasail-off-plain-k2-r0-050c43c2 | not_run |  |
| omim-ordo-deepseek-v4-flash-parasail-off-plain-k4-r0-0a1c9313 | not_run |  |
| snomed-fma-body-deepseek-v4-flash-parasail-off-plain-k0-r0-9ce246d8 | not_run |  |
| snomed-fma-body-deepseek-v4-flash-parasail-off-plain-k2-r0-1f318547 | not_run |  |
| snomed-fma-body-deepseek-v4-flash-parasail-off-plain-k4-r0-13e0d083 | not_run |  |
| snomed-ncit-neoplas-deepseek-v4-flash-parasail-off-plain-k0-r0-3f874b3d | not_run |  |
| snomed-ncit-neoplas-deepseek-v4-flash-parasail-off-plain-k2-r0-ce8b6c9b | not_run |  |
| snomed-ncit-neoplas-deepseek-v4-flash-parasail-off-plain-k4-r0-25c54c64 | not_run |  |
| snomed-ncit-pharm-deepseek-v4-flash-parasail-off-plain-k0-r0-cf00beb0 | not_run |  |
| snomed-ncit-pharm-deepseek-v4-flash-parasail-off-plain-k2-r0-cba88ec9 | not_run |  |
| snomed-ncit-pharm-deepseek-v4-flash-parasail-off-plain-k4-r0-aabf63b6 | not_run |  |

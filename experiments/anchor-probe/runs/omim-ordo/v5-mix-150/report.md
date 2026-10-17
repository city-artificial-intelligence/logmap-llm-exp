# omim-ordo / v5-mix-150

7 models; probe 150 pairs (50 positive); M_ask 399 pairs (prevalence 0.43).

| model | real_J | real_TPR | real_TNR | probe_J | probe_TPR | probe_TNR | probe_TNR[granularity_child] | probe_TNR[granularity_parent] | probe_TNR[hard_discarded] | real_rank | probe_rank |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3-235B-A22B-Instruct-2507 | 0.718 | 0.983 | 0.736 | 0.700 | 0.900 | 0.800 | 0.848 | 0.824 | 0.760 | 1 | 4 |
| mistralai/mistral-small-3.2-24b-instruct | 0.679 | 0.983 | 0.696 | 0.630 | 0.880 | 0.750 | 0.818 | 0.647 | 0.740 | 2 | 6 |
| deepseek/deepseek-v4-flash | 0.676 | 0.988 | 0.687 | 0.750 | 0.940 | 0.810 | 0.818 | 0.765 | 0.820 | 3 | 1 |
| Llama-3.1-70B-Instruct | 0.671 | 0.988 | 0.683 | 0.730 | 0.940 | 0.790 | 0.758 | 0.647 | 0.860 | 4 | 3 |
| Qwen3.5-122B-A10B | 0.655 | 0.977 | 0.678 | 0.750 | 0.960 | 0.790 | 0.939 | 0.647 | 0.740 | 5 | 1 |
| Qwen3-8B | 0.514 | 0.994 | 0.520 | 0.650 | 0.900 | 0.750 | 0.697 | 0.706 | 0.800 | 6 | 5 |
| Gemma-3-27B | 0.395 | 0.994 | 0.401 | 0.460 | 0.980 | 0.480 | 0.515 | 0.471 | 0.460 | 7 | 7 |

| | value |
|---|---|
| Spearman (probe J vs real J) | 0.25 (bootstrap 95% CI 0.00 to 0.83) |
| regret of the probe's pick | 0.053 (bootstrap mean 0.050, P(<=0.02) 0.10) |
| random pick, mean regret | 0.103 |
| 30 / 50 labelled M_ask pairs, mean regret | 0.029 / 0.022 |
| Dawid-Skene on M_ask (no labels): Spearman / regret | 0.89 / 0.000 |
| noise ceiling: real top model stays top under M_ask bootstrap | 0.92 |

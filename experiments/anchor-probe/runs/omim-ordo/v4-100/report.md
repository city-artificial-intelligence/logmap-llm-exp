# omim-ordo / v4-100

7 models; probe 100 pairs (50 positive); M_ask 399 pairs (prevalence 0.43).

| model | real_J | real_TPR | real_TNR | probe_J | probe_TPR | probe_TNR | probe_TNR[hard_discarded] | real_rank | probe_rank |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3-235B-A22B-Instruct-2507 | 0.718 | 0.983 | 0.736 | 0.620 | 0.900 | 0.720 | 0.720 | 1 | 4 |
| mistralai/mistral-small-3.2-24b-instruct | 0.679 | 0.983 | 0.696 | 0.600 | 0.880 | 0.720 | 0.720 | 2 | 6 |
| deepseek/deepseek-v4-flash | 0.676 | 0.988 | 0.687 | 0.800 | 0.940 | 0.860 | 0.860 | 3 | 1 |
| Llama-3.1-70B-Instruct | 0.671 | 0.988 | 0.683 | 0.780 | 0.940 | 0.840 | 0.840 | 4 | 2 |
| Qwen3.5-122B-A10B | 0.655 | 0.977 | 0.678 | 0.760 | 0.940 | 0.820 | 0.820 | 5 | 3 |
| Qwen3-8B | 0.514 | 0.994 | 0.520 | 0.620 | 0.900 | 0.720 | 0.720 | 6 | 4 |
| Gemma-3-27B | 0.395 | 0.994 | 0.401 | 0.440 | 0.980 | 0.460 | 0.460 | 7 | 7 |

| | value |
|---|---|
| Spearman (probe J vs real J) | 0.23 (bootstrap 95% CI 0.00 to 0.68) |
| regret of the probe's pick | 0.043 (bootstrap mean 0.048, P(<=0.02) 0.11) |
| random pick, mean regret | 0.103 |
| 30 / 50 labelled M_ask pairs, mean regret | 0.029 / 0.022 |
| Dawid-Skene on M_ask (no labels): Spearman / regret | 0.89 / 0.000 |
| noise ceiling: real top model stays top under M_ask bootstrap | 0.93 |

# omim-ordo / v5-g-150

7 models; probe 150 pairs (50 positive); M_ask 399 pairs (prevalence 0.43).

| model | real_J | real_TPR | real_TNR | probe_J | probe_TPR | probe_TNR | probe_TNR[granularity_child] | probe_TNR[granularity_parent] | real_rank | probe_rank |
|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3-235B-A22B-Instruct-2507 | 0.718 | 0.983 | 0.736 | 0.770 | 0.900 | 0.870 | 0.855 | 0.889 | 1 | 2 |
| mistralai/mistral-small-3.2-24b-instruct | 0.679 | 0.983 | 0.696 | 0.620 | 0.880 | 0.740 | 0.709 | 0.778 | 2 | 5 |
| deepseek/deepseek-v4-flash | 0.676 | 0.988 | 0.687 | 0.730 | 0.940 | 0.790 | 0.745 | 0.844 | 3 | 3 |
| Llama-3.1-70B-Instruct | 0.671 | 0.988 | 0.683 | 0.710 | 0.940 | 0.770 | 0.782 | 0.756 | 4 | 4 |
| Qwen3.5-122B-A10B | 0.655 | 0.977 | 0.678 | 0.830 | 0.940 | 0.890 | 0.945 | 0.822 | 5 | 1 |
| Qwen3-8B | 0.514 | 0.994 | 0.520 | 0.570 | 0.900 | 0.670 | 0.636 | 0.711 | 6 | 6 |
| Gemma-3-27B | 0.395 | 0.994 | 0.401 | 0.570 | 0.980 | 0.590 | 0.509 | 0.689 | 7 | 7 |

| | value |
|---|---|
| Spearman (probe J vs real J) | 0.54 (bootstrap 95% CI 0.16 to 0.86) |
| regret of the probe's pick | 0.063 (bootstrap mean 0.056, P(<=0.02) 0.10) |
| random pick, mean regret | 0.103 |
| 30 / 50 labelled M_ask pairs, mean regret | 0.029 / 0.022 |
| Dawid-Skene on M_ask (no labels): Spearman / regret | 0.89 / 0.000 |
| noise ceiling: real top model stays top under M_ask bootstrap | 0.92 |

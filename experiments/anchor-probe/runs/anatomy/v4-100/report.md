# anatomy / v4-100

7 models; probe 100 pairs (50 positive); M_ask 259 pairs (prevalence 0.64).

| model | real_J | real_TPR | real_TNR | probe_J | probe_TPR | probe_TNR | probe_TNR[hard_discarded] | real_rank | probe_rank |
|---|---|---|---|---|---|---|---|---|---|
| deepseek/deepseek-v4-flash | 0.651 | 0.970 | 0.681 | 0.860 | 0.980 | 0.880 | 0.880 | 1 | 1 |
| Qwen3.5-122B-A10B | 0.625 | 0.976 | 0.649 | 0.840 | 0.940 | 0.900 | 0.900 | 2 | 2 |
| mistralai/mistral-small-3.2-24b-instruct | 0.616 | 0.988 | 0.628 | 0.800 | 0.980 | 0.820 | 0.820 | 3 | 4 |
| Qwen3-235B-A22B-Instruct-2507 | 0.599 | 0.939 | 0.660 | 0.840 | 0.940 | 0.900 | 0.900 | 4 | 2 |
| Llama-3.1-70B-Instruct | 0.597 | 0.970 | 0.628 | 0.800 | 0.960 | 0.840 | 0.840 | 5 | 4 |
| Qwen3-8B | 0.400 | 0.964 | 0.436 | 0.680 | 0.980 | 0.700 | 0.700 | 6 | 6 |
| Gemma-3-27B | 0.339 | 0.988 | 0.351 | 0.580 | 0.980 | 0.600 | 0.600 | 7 | 7 |

| | value |
|---|---|
| Spearman (probe J vs real J) | 0.91 (bootstrap 95% CI 0.38 to 0.98) |
| regret of the probe's pick | 0.000 (bootstrap mean 0.029, P(<=0.02) 0.47) |
| random pick, mean regret | 0.104 |
| 30 / 50 labelled M_ask pairs, mean regret | 0.028 / 0.021 |
| Dawid-Skene on M_ask (no labels): Spearman / regret | 0.82 / 0.000 |
| noise ceiling: real top model stays top under M_ask bootstrap | 0.65 |

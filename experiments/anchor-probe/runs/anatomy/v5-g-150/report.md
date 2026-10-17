# anatomy / v5-g-150

7 models; probe 150 pairs (50 positive); M_ask 259 pairs (prevalence 0.64).

| model | real_J | real_TPR | real_TNR | probe_J | probe_TPR | probe_TNR | probe_TNR[granularity_child] | probe_TNR[granularity_parent] | real_rank | probe_rank |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek/deepseek-v4-flash | 0.651 | 0.970 | 0.681 | 0.880 | 0.980 | 0.900 | 0.922 | 0.861 | 1 | 1 |
| Qwen3.5-122B-A10B | 0.625 | 0.976 | 0.649 | 0.880 | 0.940 | 0.940 | 0.938 | 0.944 | 2 | 1 |
| mistralai/mistral-small-3.2-24b-instruct | 0.616 | 0.988 | 0.628 | 0.720 | 0.980 | 0.740 | 0.781 | 0.667 | 3 | 5 |
| Qwen3-235B-A22B-Instruct-2507 | 0.599 | 0.939 | 0.660 | 0.860 | 0.940 | 0.920 | 0.938 | 0.889 | 4 | 3 |
| Llama-3.1-70B-Instruct | 0.597 | 0.970 | 0.628 | 0.810 | 0.960 | 0.850 | 0.875 | 0.806 | 5 | 4 |
| Qwen3-8B | 0.400 | 0.964 | 0.436 | 0.360 | 0.960 | 0.400 | 0.422 | 0.361 | 6 | 6 |
| Gemma-3-27B | 0.339 | 0.988 | 0.351 | 0.310 | 0.980 | 0.330 | 0.359 | 0.278 | 7 | 7 |

| | value |
|---|---|
| Spearman (probe J vs real J) | 0.88 (bootstrap 95% CI 0.39 to 0.96) |
| regret of the probe's pick | 0.013 (bootstrap mean 0.027, P(<=0.02) 0.51) |
| random pick, mean regret | 0.104 |
| 30 / 50 labelled M_ask pairs, mean regret | 0.028 / 0.022 |
| Dawid-Skene on M_ask (no labels): Spearman / regret | 0.82 / 0.000 |
| noise ceiling: real top model stays top under M_ask bootstrap | 0.67 |

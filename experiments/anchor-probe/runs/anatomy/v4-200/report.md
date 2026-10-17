# anatomy / v4-200

7 models; probe 200 pairs (88 positive); M_ask 259 pairs (prevalence 0.64).

| model | real_J | real_TPR | real_TNR | probe_J | probe_TPR | probe_TNR | probe_TNR[hard_discarded] | real_rank | probe_rank |
|---|---|---|---|---|---|---|---|---|---|
| deepseek/deepseek-v4-flash | 0.651 | 0.970 | 0.681 | 0.872 | 0.943 | 0.929 | 0.929 | 1 | 1 |
| Qwen3.5-122B-A10B | 0.625 | 0.976 | 0.649 | 0.829 | 0.909 | 0.920 | 0.920 | 2 | 2 |
| mistralai/mistral-small-3.2-24b-instruct | 0.616 | 0.988 | 0.628 | 0.807 | 0.932 | 0.875 | 0.875 | 3 | 5 |
| Qwen3-235B-A22B-Instruct-2507 | 0.599 | 0.939 | 0.660 | 0.826 | 0.898 | 0.929 | 0.929 | 4 | 3 |
| Llama-3.1-70B-Instruct | 0.597 | 0.970 | 0.628 | 0.816 | 0.932 | 0.884 | 0.884 | 5 | 4 |
| Qwen3-8B | 0.400 | 0.964 | 0.436 | 0.715 | 0.920 | 0.795 | 0.795 | 6 | 6 |
| Gemma-3-27B | 0.339 | 0.988 | 0.351 | 0.566 | 0.932 | 0.634 | 0.634 | 7 | 7 |

| | value |
|---|---|
| Spearman (probe J vs real J) | 0.89 (bootstrap 95% CI 0.43 to 0.96) |
| regret of the probe's pick | 0.000 (bootstrap mean 0.014, P(<=0.02) 0.76) |
| random pick, mean regret | 0.104 |
| 30 / 50 labelled M_ask pairs, mean regret | 0.027 / 0.021 |
| Dawid-Skene on M_ask (no labels): Spearman / regret | 0.82 / 0.000 |
| noise ceiling: real top model stays top under M_ask bootstrap | 0.67 |

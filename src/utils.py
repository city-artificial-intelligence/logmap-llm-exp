import numpy as np


def calculate_logpropgs_confidence(log_probs: dict) -> float:
    for pred_tocken_info in log_probs:
        if pred_tocken_info["token"].strip() not in ["true", "false"]:
            continue
        top_logprobs = pred_tocken_info["top_logprobs"]
        positive_logprob = max([e["logprob"] for e in top_logprobs if e["token"].strip() == "true"], default=np.nan)
        negative_logprob = max([e["logprob"] for e in top_logprobs if e["token"].strip() == "false"], default=np.nan)
        break
    else:
        positive_logprob = np.nan
        negative_logprob = np.nan
    return np.nanmax([np.exp(positive_logprob), np.exp(negative_logprob)])


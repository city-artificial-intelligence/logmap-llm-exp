from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.constants import PRED_COL_DIVIDER, BinaryOutputFormat, LLMCallOutput
from src.evaluate import (
    extend_preds_with_labels_info,
    get_gt_pairs,
    get_pred_pairs,
)
from src.LLM_servers.openai import OpenAIServer
from src.onto_access import OntologyAccess
from src.onto_object import OntologyEntryAttr
from src.utils import calculate_logpropgs_confidence



def extract_llm_compeletion_answer(response: LLMCallOutput) -> bool:
    """Extract the completion answer from the LLM response."""
    if isinstance(response.parsed, BinaryOutputFormat):
        return response.parsed.answer
    raise NotImplementedError()

def process_sample(
    candidate_pairs_line: str,
    llm_oracle: OpenAIServer,
    onto_src: OntologyAccess,
    onto_tgt: OntologyAccess,
    model: str,
    prompt_function: Callable,
    one_more_time: bool = True,
) -> tuple[str, tuple[int, int], float]:
    """Process a single line: generate a prompt, send it to the LLM, and extract the response."""
    try:
        source = candidate_pairs_line.split(PRED_COL_DIVIDER)[0]
        target = candidate_pairs_line.split(PRED_COL_DIVIDER)[1]

        try:
            prompt = prompt_function(OntologyEntryAttr(source, onto_src), OntologyEntryAttr(target, onto_tgt))
        except AssertionError:
            prompt = prompt_function(OntologyEntryAttr(target, onto_src), OntologyEntryAttr(source, onto_tgt))

        response: LLMCallOutput = llm_oracle.ask_sync_question(prompt, model)
        answer = extract_llm_compeletion_answer(response)

        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        confidence = calculate_logpropgs_confidence(response.logprobs)

        token_usage = (input_tokens, output_tokens)
        result = f"{source},{target},{answer},{confidence}"
        return result, token_usage, confidence

    except Exception:
        if one_more_time:
            return process_sample(
                candidate_pairs_line, llm_oracle, onto_src, onto_tgt, model, prompt_function, one_more_time=False
            )
        return f"{source}|{target}|ERROR|{np.nan}", (np.nan, np.nan), np.nan

def samples_process(
    candidate_pairs_lines: list[str],
    llm_oracle: OpenAIServer,
    onto_src: OntologyAccess,
    onto_tgt: OntologyAccess,
    model: str,
    prompt_function: Callable,
) -> tuple[list[str], list[tuple[int, int]], list[float]]:
    """Process lines sequentially."""
    results = []
    tokens_usage = []
    confidences = []

    for line in tqdm(candidate_pairs_lines, desc=f"Processing Lines {prompt_function.__name__}"):
        result, token_usage, confidence = process_sample(line, llm_oracle, onto_src, onto_tgt, model, prompt_function)
        results.append(result)
        tokens_usage.append(token_usage)
        confidences.append(confidence)

    return results, tokens_usage, confidences

def parallel_samples_process(
    candidate_pairs_lines: list[str],
    llm_oracle: OpenAIServer,
    onto_src: OntologyAccess,
    onto_tgt: OntologyAccess,
    model: str,
    max_workers: int,
    prompt_function: Callable,
) -> tuple[list[str], list[tuple[int, int]], list[float]]:
    """Process lines in parallel, with progress tracking using tqdm."""
    results = []
    tokens_usage = []
    confidences = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_line = {
            executor.submit(process_sample, line, llm_oracle, onto_src, onto_tgt, model, prompt_function): line
            for line in candidate_pairs_lines
        }

        for future in tqdm(
            as_completed(future_to_line), total=len(future_to_line), desc=f"Processing Lines {prompt_function.__name__}"
        ):
            result, token_usage, confidence = future.result()
            results.append(result)
            tokens_usage.append(token_usage)
            confidences.append(confidence)

    return results, tokens_usage, confidences

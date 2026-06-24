from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.constants import (
    LOGGER,
    PAIRS_SEPARATOR,
    RESULTS_SEPARATOR,
    USAGE_COLUMNS,
    BinaryOutputFormat,
    BinaryOutputFormatWithReasoning,
    LLMCallOutput,
)
from src.error_taxonomy import (
    RETRY_COUNT_COLUMNS,
    RETRYABLE_ERROR_TYPES,
    ErrorCategory,
    ErrorType,
    classify_error,
)
from src.formatting import (
    format_oracle_pairs_filepath,
    format_oracle_pairs_precomputed_dir,
    format_oracle_pairs_with_prompts_path,
)
from src.LLM_servers.openai import OpenAIServer
from src.onto_access import OntologyAccess
from src.onto_object import OntologyEntryAttr
from src.utils import calculate_logpropgs_confidence


def save_oracle_pairs_with_prompts(
    oracle_candidate_pairs_path: Path,
    src_onto: OntologyAccess,
    tgt_onto: OntologyAccess,
    prompt_functions: list[callable],
    save_dir: Path,
    sep: str,
    max_workers: int = 1,
    skip_annotation: bool = False,
) -> pd.DataFrame:
    base_pairs_df = pd.read_csv(oracle_candidate_pairs_path, sep=sep, header=None)

    for row in tqdm(base_pairs_df.iterrows(), total=base_pairs_df.shape[0], desc="Adding prompts"):
        src_uri, tgt_uri = row[1][0], row[1][1]
        src_entity = OntologyEntryAttr(src_uri, src_onto, skip_annotation=skip_annotation)
        tgt_entity = OntologyEntryAttr(tgt_uri, tgt_onto, skip_annotation=skip_annotation)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(prompt_function, src_entity, tgt_entity): prompt_function
                for prompt_function in prompt_functions
            }
            for future in futures:
                prompt_function = futures[future]
                prompt = future.result()
                base_pairs_df.loc[row[0], prompt_function.__name__] = prompt

    save_dir.mkdir(parents=True, exist_ok=True)
    for prompt_function in [*prompt_functions, None]:
        new_file_path = format_oracle_pairs_with_prompts_path(prompt_function, save_dir)
        columns = base_pairs_df.columns.tolist()[:2] + ([prompt_function.__name__] if prompt_function else [])
        base_pairs_df[columns].to_csv(new_file_path, sep=sep, index=False, header=False)

    return base_pairs_df


def try_load_precomputed_oracle_pairs(
    dataset_name: str, set_name: str, prompt_function: callable | None, sep: str = PAIRS_SEPARATOR, suffix: str = ""
) -> list[tuple[str, str]]:
    oracle_pairs_dir = format_oracle_pairs_precomputed_dir(dataset_name, set_name, suffix=suffix)

    # Try path with prompts
    if prompt_function is not None:
        pairs_path = format_oracle_pairs_with_prompts_path(prompt_function, oracle_pairs_dir, suffix="")
        if pairs_path.exists():
            pairs_df = pd.read_csv(pairs_path, sep=sep, header=None)
            return list(zip(pairs_df[0], pairs_df[1], pairs_df[2]))

    # Try path without prompts
    pairs_path = format_oracle_pairs_with_prompts_path(
        prompt_function=None, oracle_pairs_dir=oracle_pairs_dir, suffix=suffix
    )
    if not pairs_path.exists():
        # Fall back to legacy format
        pairs_path = format_oracle_pairs_filepath(dataset_name, set_name)
        if not pairs_path.exists():
            msg = f"Oracle pairs file not found: {pairs_path}"
            raise FileNotFoundError(msg)

    pairs_df = pd.read_csv(pairs_path, sep=sep, header=None)
    return list(zip(pairs_df[0], pairs_df[1]))


def try_load_partial_results(predictions_path: Path, sep: str = RESULTS_SEPARATOR) -> pd.DataFrame | None:
    if predictions_path.exists():
        return pd.read_csv(predictions_path, sep=sep)
    return None


def extract_llm_compeletion_answer(response: LLMCallOutput) -> bool:
    """Extract the completion answer from the LLM response."""
    if isinstance(response.parsed, (BinaryOutputFormat, BinaryOutputFormatWithReasoning)):
        return response.parsed.answer
    raise NotImplementedError()


def process_sample(
    candidates_pair: tuple[str, str],
    llm_oracle: OpenAIServer,
    onto_src: OntologyAccess,
    onto_tgt: OntologyAccess,
    model: str,
    prompt_function: Callable,
    sleep_time: float,
    max_retries: int = 1,
) -> tuple[list, tuple, int]:
    source, target = candidates_pair[:2]

    if len(candidates_pair) == 2:
        prompt = prompt_function(OntologyEntryAttr(source, onto_src), OntologyEntryAttr(target, onto_tgt))
    else:
        prompt = candidates_pair[2]

    last_error_type = ErrorType.UNKNOWN
    last_error_category = ErrorCategory.UNKNOWN

    # Track retry counts per error type
    retry_counts: dict[ErrorType, int] = {et: 0 for et in ErrorType}

    def _build_retry_values() -> list[int]:
        """Build flat list of retry counts in RETRY_COUNT_COLUMNS order."""
        values = [retry_counts[et] for et in ErrorType]
        values.append(sum(retry_counts.values()))  # retries_total
        return values

    for attempt in range(max_retries + 1):
        try:
            time.sleep(sleep_time)
            response: LLMCallOutput = llm_oracle.ask_sync_question(prompt, model)
            answer = extract_llm_compeletion_answer(response)
            confidence = calculate_logpropgs_confidence(response.logprobs)
            usage = response.usage
            token_usage = usage.to_tuple()
            # No error on success
            result = [source, target, answer, confidence, *token_usage, attempt, "", "", *_build_retry_values()]
            return result, token_usage, attempt
        except Exception as e:  # noqa: BLE001
            error_type, error_category = classify_error(e)
            last_error_type = error_type
            last_error_category = error_category
            retry_counts[error_type] += 1

            # Only retry if the error is retryable
            if error_type not in RETRYABLE_ERROR_TYPES and attempt < max_retries:
                # Non-retryable error: fail immediately
                LOGGER.error(
                    f"Non-retryable error ({error_type.value}) for {candidates_pair}: {e}",
                    exc_info=True,
                )
                nan_usage = (np.nan,) * len(USAGE_COLUMNS)
                return (
                    [source, target, "error", str(np.nan), *nan_usage, attempt,
                     error_type.value, error_category.value, *_build_retry_values()],
                    nan_usage, attempt,
                )

            if attempt == max_retries:
                LOGGER.error(
                    f"Error ({error_type.value}) processing line: {candidates_pair}: {e}",
                    exc_info=True,
                )
                nan_usage = (np.nan,) * len(USAGE_COLUMNS)
                return (
                    [source, target, "error", str(np.nan), *nan_usage, attempt,
                     last_error_type.value, last_error_category.value, *_build_retry_values()],
                    nan_usage, attempt,
                )

    nan_usage = (np.nan,) * len(USAGE_COLUMNS)
    return (
        [source, target, "error", str(np.nan), *nan_usage, max_retries,
         last_error_type.value, last_error_category.value, *_build_retry_values()],
        nan_usage, max_retries,
    )


def parallel_samples_process(
    candidate_pairs: list[tuple[str, str]],
    llm_oracle: OpenAIServer,
    onto_src: OntologyAccess | None,
    onto_tgt: OntologyAccess | None,
    model: str,
    max_workers: int,
    prompt_function: Callable,
    partial_results: pd.DataFrame | None = None,
    sleep_time: float = 0.0,
) -> tuple[list[tuple], list[tuple[int, int]], list[float]]:
    """Process lines in parallel, with progress tracking using tqdm.

    Args:
        candidate_pairs (list[tuple[str, str]]): The list of candidate pairs to process.
        llm_oracle: The LLM oracle server.
        onto_src: The source ontology.
        onto_tgt The target ontology.
        model: The model to use.
        max_workers: The number of workers to use.
        prompt_function: The prompt function to use to generate the prompt, having the signature:
            prompt_function(src: OntologyEntryAttr, tgt: OntologyEntryAttr) -> str.

    Returns:
        tuple[list[tuple], list[tuple[int, int]], list[float]]:
            - results: list of tuples, each with source, target, answer, confidence
            - tokens_usage: list of tuples, each with input tokens, output tokens,
            - confidences: list of floats

    """
    results = []
    tokens_usage = []

    precomputed_results = {}
    prior_retries_map = {}
    if partial_results is not None:
        has_retries_col = "num_retries" in partial_results.columns
        has_error_cols = "error_type" in partial_results.columns
        has_retry_count_cols = "retries_total" in partial_results.columns
        for _, row in partial_results.iterrows():
            key = (row["Source"], row["Target"])
            row_values = row.to_numpy()
            if "error" not in row_values:
                row_list = row.tolist()
                # Pad old-format results missing error_type/error_category columns
                if not has_error_cols:
                    row_list.extend(["", ""])
                # Pad old-format results missing retry count columns
                if not has_retry_count_cols:
                    row_list.extend([0] * len(RETRY_COUNT_COLUMNS))
                precomputed_results[key] = row_list
            else:
                prior = int(row["num_retries"]) if has_retries_col and pd.notna(row.get("num_retries")) else 0
                prior_retries_map[key] = prior

    LOGGER.info(f"{len(precomputed_results)} precomputed results found from {len(candidate_pairs)}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_line = {}
        for pair in candidate_pairs:
            key = (pair[0], pair[1])
            if key in precomputed_results:
                results.append(precomputed_results[key])
                tokens_usage.append((np.nan,) * len(USAGE_COLUMNS))
            else:
                future_to_line[
                    executor.submit(
                        process_sample, pair, llm_oracle, onto_src, onto_tgt, model, prompt_function, sleep_time
                    )
                ] = pair

        for future in tqdm(
            as_completed(future_to_line), total=len(future_to_line), desc=f"Processing Lines {prompt_function.__name__}"
        ):
            result, token_usage, current_retries = future.result()
            key = (result[0], result[1])
            prior = prior_retries_map.get(key, 0)
            total_retries = prior + current_retries + (1 if prior > 0 else 0)
            # num_retries is at index 9 (after: source, target, answer, confidence, 5 usage cols)
            num_retries_idx = 4 + len(USAGE_COLUMNS)  # = 9
            result[num_retries_idx] = total_retries
            results.append(result)
            tokens_usage.append(token_usage)

    ordered_results = []
    ordered_tokens_usage = []
    pair_to_idx = {(res[0], res[1]): idx for idx, res in enumerate(results)}

    for pair in candidate_pairs:
        ordered_results.append(results[pair_to_idx[(pair[0], pair[1])]])
        ordered_tokens_usage.append(tokens_usage[pair_to_idx[(pair[0], pair[1])]])

    confidences = [res[3] for res in ordered_results]
    return ordered_results, ordered_tokens_usage, confidences

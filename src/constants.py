from __future__ import annotations

import logging

from pydantic import BaseModel

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class BinaryOutputFormat(BaseModel):
    answer: bool


class BinaryOutputFormatWithReasoning(BaseModel):
    reasoning: str
    answer: bool


class TokensUsage(BaseModel):
    input_tokens: int | None
    output_tokens: int | None
    input_cached_tokens: int | None = None
    output_reasoning_tokens: int | None = None
    proc_time: float | None = None

    @property
    def columns(self) -> list[str]:
        return ["input_tokens", "output_tokens", "input_cached_tokens", "output_reasoning_tokens", "proc_time"]

    def to_tuple(self) -> tuple:
        return (
            self.input_tokens, self.output_tokens, self.input_cached_tokens,
            self.output_reasoning_tokens, self.proc_time,
        )


USAGE_COLUMNS = ["input_tokens", "output_tokens", "input_cached_tokens", "output_reasoning_tokens", "proc_time"]


def extract_cached_reasoning_tokens(usage: object) -> tuple[int | None, int | None]:
    """Pull (cached_input, reasoning_output) token counts from an OpenAI-style usage object."""
    prompt_details = getattr(usage, "prompt_tokens_details", None)
    completion_details = getattr(usage, "completion_tokens_details", None)
    cached = getattr(prompt_details, "cached_tokens", None) if prompt_details else None
    reasoning = getattr(completion_details, "reasoning_tokens", None) if completion_details else None
    return cached, reasoning


class LLMCallOutput(BaseModel):
    message: str | bool
    usage: TokensUsage
    logprobs: list | None
    parsed: BaseModel | None


PAIRS_SEPARATOR = "|"
GT_COL_DIVIDER = "\t"
RESULTS_SEPARATOR = ","

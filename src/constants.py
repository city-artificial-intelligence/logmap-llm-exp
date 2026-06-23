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


class LLMCallOutput(BaseModel):
    message: str | bool
    usage: TokensUsage
    logprobs: list | None
    parsed: BaseModel | None


PAIRS_SEPARATOR = "|"
GT_COL_DIVIDER = "\t"
RESULTS_SEPARATOR = ","

from __future__ import annotations

import os
from typing import Any

import openai
from pydantic import BaseModel

from src.constants import BinaryOutputFormat, LLMCallOutput, TokensUsage


class GeminiApiServer:
    def __init__(self, **kwargs: dict[str, Any]) -> None:
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
        self.client = openai.OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"), base_url=self.base_url, max_retries=kwargs.get("max_retries", 3)
        )
        self.chat_context = []

        self.response_format = kwargs.get("response_format", BinaryOutputFormat)

        self.top_p = 0.3
        self.temperature = 0
        self.max_tokens = kwargs.get("max_tokens", 100)
        self.thinking_budget = kwargs.get("thinking_budget", 0)
        self.logprobs = True
        self.top_logprobs = 3

        for key, value in kwargs.items():
            setattr(self, key, value)

    def add_system_context(self, message: str) -> None:
        """Add or update the system context in the chat history.

        If a system message exists, it will be updated; otherwise, it will be added.
        """
        if len(self.chat_context) == 0 or self.chat_context[0]["role"] != "system":
            self.chat_context.insert(0, self.wrap_text_message(message, "system"))
        else:
            self.chat_context[0] = self.wrap_text_message(message, "system")

    def add_context(self, message: str, role: str) -> None:
        """Add a message to the chat context."""
        self.chat_context.append(self.wrap_text_message(message, role))

    def set_response_format(self, response_format: BaseModel | dict) -> None:
        """Set the response format for the server."""
        self.response_format = response_format

    def wrap_text_message(self, message: str, role: str) -> dict:
        """Wrap a text message with a role."""
        return {"role": role, "content": message}

    def ask_sync_question(self, message: str, model: str) -> LLMCallOutput:
        """Send a user query to the OpenAI model and optionally update the chat context.

        Args:
            message (str): The user message to process.
            model (str): The model to use for the query.

        Returns:
            LLMServerOutput: Wrapper for the response message, usage, logprobs, and parsed output.

        Raises:
            Exception: If an error occurs during the query.

        """
        try:
            messages = [*self.chat_context, self.wrap_text_message(message, "user")]

            inference_kwargs = {
                "model": model,
                "messages": messages,
                "temperature": self.temperature,
                "top_p": self.top_p,
                # "reasoning_effort": None,
                "response_format": self.response_format,
            }

            import time as _time
            _start = _time.time()
            response = self.client.beta.chat.completions.parse(
                **inference_kwargs,
                extra_body={
                    "extra_body": {
                        "google": {
                            "thinking_config": {"thinking_budget": self.thinking_budget, "include_thoughts": False}
                        }
                    }
                },
            )
            _proc_time = _time.time() - _start

            output_message = response.choices[0].message.content
            usage = TokensUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                input_cached_tokens=getattr(response.usage, 'prompt_tokens_details', None) and getattr(response.usage.prompt_tokens_details, 'cached_tokens', None),
                output_reasoning_tokens=getattr(response.usage, 'completion_tokens_details', None) and getattr(response.usage.completion_tokens_details, 'reasoning_tokens', None),
                proc_time=_proc_time,
            )
            logprobs = []
            parsed_output = response.choices[0].message.parsed
            return LLMCallOutput(message=output_message, usage=usage, logprobs=logprobs, parsed=parsed_output)

        except Exception as e:
            raise e

    def clear_context(self) -> None:
        """Clear the chat context."""
        self.chat_context = []

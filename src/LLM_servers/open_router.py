from __future__ import annotations

import json
import os
from typing import Any

import openai
from pydantic import BaseModel

from src.constants import BinaryOutputFormat, LLMCallOutput, TokensUsage, extract_cached_reasoning_tokens


class OpenRouterServer:
    def __init__(self, api_key: str | None = None, base_url: str | None = None, **kwargs: dict[str, Any]) -> None:
        if api_key is None:
            api_key = os.getenv("OPENROUTER_API_KEY")

        self.base_url = "https://openrouter.ai/api/v1"
        if base_url is not None:
            self.base_url = base_url

        self.client = openai.OpenAI(api_key=api_key, base_url=self.base_url, max_retries=2)
        self.chat_context = []

        self.response_format = kwargs.get("response_format", BinaryOutputFormat)

        self.top_p = 0.3
        self.temperature = 0
        self.max_tokens = kwargs.get("max_tokens", 100)
        self.logprobs = True
        self.top_logprobs = 3
        self.params = kwargs

        self.routes_registry = {
            "qwen/qwen3-vl-8b-instruct": "novita",
            "deepseek/deepseek-chat-v3-0324": "deepinfra",
            "deepseek/deepseek-v4-pro": "deepinfra",
            "deepseek/deepseek-v4-flash": "deepinfra",
            "mistralai/ministral-14b-2512": "mistral",
            "mistralai/ministral-3b-2512": "mistral",
            "mistralai/mistral-nemo": "deepinfra",
            "mistralai/mistral-medium-3-5": "mistral",
            "mistralai/mistral-small-2603": "mistral",
            "google/gemma-3-27b-it": "deepinfra",
            "google/gemma-3-12b-it": "deepinfra",
            "google/gemma-4-31b-it": "deepinfra",
            "google/gemma-4-26b-a4b-it": "deepinfra",
            "meta-llama/llama-4-scout": "deepinfra",
            "meta-llama/llama-4-maverick": "deepinfra",
            "openai/gpt-oss-120b": "deepinfra",
            "openai/gpt-5.5": "openai",
            "openai/gpt-5.4-mini": "openai",
            "anthropic/claude-opus-4.7": "anthropic",
            "x-ai/grok-4.1-fast": "xai",
            "x-ai/grok-4.3": "xai",
            "x-ai/grok-4.20": "xai",
            "ibm-granite/granite-4.1-8b": "ibm",
            "qwen/qwen3-235b-a22b-2507": "deepinfra",
            "qwen/qwen3.6-flash": "deepinfra",
            "qwen/qwen3.6-35b-a3b": "deepinfra",
            "qwen/qwen3.6-max-preview": "deepinfra",
            "qwen/qwen3.5-397b-a17b": "deepinfra",
            "qwen/qwen3.5-9b": "deepinfra",
            "minimax/minimax-m2.7": "minimax",
            "moonshotai/kimi-k2.6": "moonshot",
            "nvidia/nemotron-3-super-120b-a12b": "nvidia",
            "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning": "nvidia",
            "z-ai/glm-5.1": "z-ai",
            "bytedance-seed/seed-2.0-lite": "bytedance-seed",
            "openai/gpt-4o-mini": "openai",
            "openai/gpt-5.4": "openai",
            "openai/gpt-oss-20b": "deepinfra",
            "anthropic/claude-haiku-4.5": "anthropic",
            "deepseek/deepseek-v3.2": "deepinfra",
            "bytedance-seed/seed-2.0-mini": "bytedance-seed",
            "minimax/minimax-m2.5": "minimax",
            "qwen/qwen3-14b": "deepinfra",
            "qwen/qwen3-32b": "deepinfra",
            "qwen/qwen3.5-35b-a3b": "deepinfra",
            "qwen/qwen3.5-122b-a10b": "deepinfra",
            "z-ai/glm-5": "z-ai",
            "google/gemini-2.5-flash": "google-ai-studio",
            "google/gemini-2.5-flash-lite": "google-ai-studio",
            "google/gemini-2.5-pro": "google-ai-studio",
            "google/gemini-3.1-flash-lite-preview": "google-ai-studio",
            "meta-llama/llama-3.1-70b-instruct": "parasail",
            "mistralai/mistral-small-3.2-24b-instruct": "mistral",
            # "google/gemini-3-flash-preview": "google-ai-studio",
            # New candidates surfaced from OpenRouter (2026-06)
            "anthropic/claude-fable-5": "anthropic",
            "google/gemini-3.5-flash": "google-ai-studio",
            "qwen/qwen3.7-plus": "deepinfra",
            "openai/gpt-5.5-pro": "openai",
            # "xiaomi/mimo-v2.5": "<provider>",  # set provider slug before pinning; unpinned = OpenRouter auto-route
        }

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
            model = model.replace("|", "/")

            extra_body = {}

            if route := self.routes_registry.get(model):
                extra_body.setdefault("provider", {})
                extra_body["provider"].setdefault("only", [route])

            inference_kwargs = {
                "model": model,
                "messages": messages,
                "temperature": self.temperature,
                "top_p": self.top_p,
                # "reasoning_effort": None,
                "response_format": self.response_format,
                "extra_body": extra_body,
            }

            # Reasoning parameters (reasoning_effort / thinking_budget) are applied below.
            if self.params.get("reasoning_effort"):
                inference_kwargs["reasoning_effort"] = self.params.get("reasoning_effort")

            if self.params.get("thinking_budget"):
                inference_kwargs.setdefault("extra_body", {})
                inference_kwargs["extra_body"].setdefault("reasoning", {})
                inference_kwargs["extra_body"]["reasoning"]["max_tokens"] = int(self.params.get("thinking_budget"))

            if self.params.get("custom_parsing"):
                inference_kwargs.pop("response_format", None)
                import time as _time
                _start = _time.time()
                response = self.client.beta.chat.completions.parse(**inference_kwargs)
                _proc_time = _time.time() - _start
                output_message = response.choices[0].message.content
                try:
                    parsed_output = self.response_format(**json.loads(output_message))
                except Exception as e:
                    if "true" in output_message.lower()[:20]:
                        answer = True
                    elif "false" in output_message.lower()[:20]:
                        answer = False
                    else:
                        msg = f"Failed to parse the output message: {output_message}"
                        raise RuntimeError(msg) from e

                    parsed_output = self.response_format(answer=answer)

            else:
                import time as _time
                _start = _time.time()
                response = self.client.beta.chat.completions.parse(**inference_kwargs)
                _proc_time = _time.time() - _start
                parsed_output = response.choices[0].message.parsed
                output_message = response.choices[0].message.content

            cached_tokens, reasoning_tokens = extract_cached_reasoning_tokens(response.usage)
            usage = TokensUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                input_cached_tokens=cached_tokens,
                output_reasoning_tokens=reasoning_tokens,
                proc_time=_proc_time,
            )
            try:
                logprobs = response.choices[0].logprobs.model_dump()["content"]
            except AttributeError:
                logprobs = []

            return LLMCallOutput(message=output_message, usage=usage, logprobs=logprobs, parsed=parsed_output)

        except Exception as e:
            raise e

    def clear_context(self) -> None:
        """Clear the chat context."""
        self.chat_context = []

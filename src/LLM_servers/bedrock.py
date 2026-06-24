from __future__ import annotations

from typing import Any

import boto3
from botocore.config import Config

from src.constants import BinaryOutputFormat, LLMCallOutput, TokensUsage

OUTPUT_FORMAT = {
    "tools": [
        {
            "toolSpec": {
                "name": "AnswerFormatter",
                "description": "Wraps the answer in a specific format.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "answer": {
                                "type": "boolean",
                                "description": (
                                    "The answer to the question, either 'True' or 'False'. "
                                    "Do not output any other text."
                                ),
                            },
                        },
                        "required": ["answer"],
                        "description": "Output format for the tool.",
                    }
                },
            }
        }
    ],
    # "toolChoice": {"tool": {"name": "AnswerFormatter"}},
}


# Note: config could be moved to a constants file with per-model hyperparameters.
class BedrockServer:
    def __init__(
        self,
        model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
        region: str = "us-east-1",
        temperature: float = 0,
        top_p: float = 0.3,
        max_tokens: int = 5,
        **kwargs: dict[str, Any],
    ) -> None:
        """Initialize Bedrock-based LLM wrapper compatible with OpenAIServer's interface."""
        self.model_id = model_id
        self.region = region

        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.response_format = OUTPUT_FORMAT
        self.chat_context = []
        self.system_message = ""

        self.client = boto3.client(
            "bedrock-runtime",
            config=Config(read_timeout=60),
            region_name=region,
        )

        for key, value in kwargs.items():
            setattr(self, key, value)

    def add_system_context(self, message: str) -> None:
        self.system_message = message

    def add_context(self, message: str, role: str) -> None:
        self.chat_context.append(self.wrap_text_message(message, role))

    def set_response_format(self, response_format: dict) -> None:
        self.response_format = response_format

    def wrap_text_message(self, message: str, role: str) -> dict:
        return {"role": role, "content": [{"text": message}]}

    def _format_bedrock_messages(self, message: str) -> list:
        """Format OpenAI-style message list into Bedrock-compatible message list."""
        return [*self.chat_context, self.wrap_text_message(message, "user")]

    def _format_system_prompt(self, prompt: str) -> list:
        return [{"text": prompt}]

    def ask_sync_question(self, message: str, model: str | None = None) -> LLMCallOutput:
        try:
            bedrock_messages = self._format_bedrock_messages(message)

            import time as _time
            _start = _time.time()
            response = self.client.converse(
                modelId=model or self.model_id,
                messages=bedrock_messages,
                system=self._format_system_prompt(self.system_message),
                inferenceConfig={
                    "temperature": self.temperature,
                    "topP": self.top_p,
                    "maxTokens": self.max_tokens,
                },
                # toolConfig=self.response_format,
            )
            _proc_time = _time.time() - _start

            response_content = response["output"]["message"]["content"][0]
            if "toolUse" in response_content:
                completion = response_content["toolUse"]["input"]
                answer = completion["answer"] in ["True", "true", True]
            else:
                completion = response_content["text"]
                answer = "true" in completion.lower()

            usage = TokensUsage(
                input_tokens=response["usage"]["inputTokens"],
                output_tokens=response["usage"]["outputTokens"],
                input_cached_tokens=response.get("usage", {}).get("cacheReadInputTokenCount"),
                output_reasoning_tokens=None,
                proc_time=_proc_time,
            )

            return LLMCallOutput(message=completion, usage=usage, logprobs=[], parsed=BinaryOutputFormat(answer=answer))

        except Exception as e:
            msg = f"Bedrock request failed: {e}"
            raise RuntimeError(msg) from e

    def clear_context(self) -> None:
        self.chat_context = []

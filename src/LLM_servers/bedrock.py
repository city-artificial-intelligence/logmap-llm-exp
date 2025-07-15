from typing import Any

import boto3
from botocore.config import Config

from constants import BinaryOutputFormat, LLMCallOutput, TokensUsage


# TODO: move config to some constatnts file and add hyperparameters for the model
class BedrockServer:
    def __init__(
        self,
        model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
        region: str = "us-east-1",
        temperature: float = 0,
        top_p: float = 0.3,
        max_tokens: int = 100,
        **kwargs: dict[str, Any],
    ) -> None:
        """Initialize Bedrock-based LLM wrapper compatible with OpenAIServer's interface."""
        self.model_id = model_id
        self.region = region

        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.response_format = BinaryOutputFormat
        self.chat_context = []

        self.client = boto3.client(
            "bedrock-runtime",
            config=Config(read_timeout=60),
            region_name=region,
        )

        for key, value in kwargs.items():
            setattr(self, key, value)

    def add_system_context(self, message: str) -> None:
        if len(self.chat_context) == 0 or self.chat_context[0]["role"] != "system":
            self.chat_context.insert(0, self.wrap_text_message(message, "system"))
        else:
            self.chat_context[0] = self.wrap_text_message(message, "system")

    def add_context(self, message: str, role: str) -> None:
        self.chat_context.append(self.wrap_text_message(message, role))

    def set_response_format(self, response_format: dict) -> None:
        self.response_format = response_format

    def wrap_text_message(self, message: str, role: str) -> dict:
        return {"role": role, "content": message}

    def _format_bedrock_messages(self, message: str) -> list:
        """Format OpenAI-style message list into Bedrock-compatible message list."""
        formatted_messages = []
        for m in [*self.chat_context, self.wrap_text_message(message, "user")]:
            formatted_messages.append({"role": m["role"], "content": [{"text": m["content"]}]})
        return formatted_messages

    def _format_system_prompt(self, prompt: str) -> list:
        return [{"text": prompt}]

    def ask_sync_question(self, message: str) -> LLMCallOutput:
        try:
            bedrock_messages = self._format_bedrock_messages(message)
            system_prompt = (
                self.chat_context[0]["content"]
                if self.chat_context and self.chat_context[0]["role"] == "system"
                else ""
            )

            # to be utilized in future start_time = time()
            response = self.client.converse(
                modelId=self.model_id,
                messages=bedrock_messages,
                system=self._format_system_prompt(system_prompt),
                inferenceConfig={"temperature": self.temperature, "topP": self.top_p, "maxTokens": self.max_tokens},
            )

            completion = response["output"]["message"]["content"][0]["text"]

            usage = TokensUsage(
                input_tokens=response["usage"]["inputTokens"], output_tokens=response["usage"]["outputTokens"]
            )

            return LLMCallOutput(message=completion, usage=usage, logprobs={"content": []}, parsed=None)

        except Exception as e:
            msg = f"Bedrock request failed: {e}"
            raise RuntimeError(msg) from e

    def clear_context(self) -> None:
        self.chat_context = []

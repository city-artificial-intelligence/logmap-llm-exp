# ruff: noqa: T201
import torch
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

app = FastAPI(title="Qwen Model Server")

# MODEL_NAME = "Qwen/Qwen3-1.7B"
# MODEL_NAME = "Qwen/Qwen3-8B"
MODEL_NAME = "Qwen/Qwen1.5-MoE-A2.7B"

# python3.10 qwen_server_runner.py

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    torch_dtype=torch.float16,
    device_map="auto"
)

class ChatRequest(BaseModel):
    messages: list[dict]
    max_new_tokens: int = 50
    temperature: float = 0.7

@app.post("/chat")
def chat(req: ChatRequest) -> dict:
    text = tokenizer.apply_chat_template(
        req.messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False
    )

    inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # Get token IDs for "True" and "False"
    true_id = tokenizer.convert_tokens_to_ids("True")
    false_id = tokenizer.convert_tokens_to_ids("False")

    def allowed_tokens(batch_id: int, input_ids: list[int]) -> list[int]:  # noqa: ARG001
        # First generated token: only allow "True" or "False"
        if len(input_ids) == inputs.input_ids.shape[1]:
            return [true_id, false_id]
        # After first token, stop generation
        return [tokenizer.eos_token_id]

    outputs = model.generate(
        **inputs,
        max_new_tokens=req.max_new_tokens,
        temperature=req.temperature,
        do_sample=False,
        eos_token_id=model.config.eos_token_id,
        prefix_allowed_tokens_fn=allowed_tokens
    )

    output_ids = outputs[0][len(inputs.input_ids[0]):]
    response = tokenizer.decode(output_ids, skip_special_tokens=True).strip()

    print(f"Generated response: {response}")

    if response not in ["True", "False"]:
        response = "False"

    return {"response": response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

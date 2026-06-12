"""LLM interface: OpenAI chat, vision, embeddings."""

import openai
from . import config

# ============================================================
# OpenAI / DeepSeek 客户端
# OpenAI-compatible client
# ============================================================
client = openai.OpenAI(
    api_key=config.OPENAI_API_KEY,
    base_url="https://api.deepseek.com",
)


def chat(messages, model=None):
    """
    调用 Chat API
    Call chat API
    """

    print("[LLM] Calling:", model or config.OPENAI_MODEL)

    response = client.chat.completions.create(
        model=model or config.OPENAI_MODEL,
        messages=messages,
    )

    return response.choices[0].message.content
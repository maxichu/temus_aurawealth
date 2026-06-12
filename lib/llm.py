"""LLM interface: OpenAI chat, vision, embeddings."""

import openai
from . import config

# ============================================================
# OpenAI 同步客户端 — 模块加载时初始化一次
# Sync OpenAI client — initialized once at module load
# 后续 Feature 会添加 Async 版本 (Async Backend +2)
# ============================================================
client = openai.OpenAI(api_key=config.OPENAI_API_KEY)


def chat(messages, model=None):
    """
    调用 OpenAI Chat API，返回 Assistant 回复文本。
    Call OpenAI Chat API and return the assistant response text.

    Parameters:
        messages: list[dict] — 对话历史 [{role, content}, ...]
        model: str | None — 模型名，默认 config.OPENAI_MODEL

    Returns:
        str — Assistant 回复内容
    """
    response = client.chat.completions.create(
        model=model or config.OPENAI_MODEL,
        messages=messages,
    )
    return response.choices[0].message.content

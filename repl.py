"""
REPL AI Chat — 终端命令行聊天界面
Terminal-based AI chat interface

使用方法 / Usage:
    python repl.py

输入 'exit' 或 'quit' 退出。
Type 'exit' or 'quit' to quit.
"""

import sys
import os

# 确保项目根目录在 sys.path 中，以便 from lib.llm import chat
# Ensure project root is in sys.path so lib package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.llm import chat

# 系统提示词 — 设定 AI 助手的角色
# System prompt — defines the AI assistant's role
SYSTEM_PROMPT = (
    "You are AuraWealth, an AI financial advisor. "
    "Provide concise, helpful advice about wealth management."
)


def main():
    """
    主循环：维护对话历史，逐轮调用 LLM。
    Main loop: maintain conversation history, call LLM each turn.
    """
    # 对话历史：第一条是系统提示词，后续追加用户和 Assistant 消息
    # Conversation history: starts with system prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # 欢迎信息 / Welcome message
    print("=" * 50)
    print("  AuraWealth AI Advisor")
    print("=" * 50)
    print("Type 'exit' or 'quit' to end.\n")

    while True:
        try:
            # 获取用户输入 / Read user input
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D 或 Ctrl+C 时优雅退出
            # Graceful exit on Ctrl+D or Ctrl+C
            print("\nGoodbye!")
            break

        # 退出条件 / Exit condition
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        # 跳过空输入 / Skip empty input
        if not user_input:
            continue

        # 1) 保存用户消息到历史 / Save user message to history
        messages.append({"role": "user", "content": user_input})

        # 2) 调用 LLM 获取回复 / Call LLM for a response
        # chat() 封装了 OpenAI API 调用，返回回复文本
        # chat() wraps the OpenAI API call and returns the response text
        reply = chat(messages)

        # 3) 保存 Assistant 回复到历史，支持后续多轮对话
        #    Save assistant response to history for multi-turn conversation
        messages.append({"role": "assistant", "content": reply})

        # 4) 显示回复 / Display the response
        print(f"AI: {reply}\n")


if __name__ == "__main__":
    main()

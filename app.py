"""AuraWealth — AI Wealth Management Platform."""

"""AuraWealth — AI Wealth Management Platform."""

import streamlit as st

from lib import config
from lib.llm import chat

# ============================================================
# 页面配置
# Page configuration — sets browser tab title, icon, layout
# ============================================================
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="💰",
    layout="wide",
)

# ============================================================
# 侧边栏 — 当前仅显示应用名称，后续 Feature 会扩展
# Sidebar — currently only shows app name, will be extended
# ============================================================
with st.sidebar:
    st.title(config.APP_TITLE)
    st.caption("AI Wealth Management Platform")

# ============================================================
# 主区域标题
# Main area title
# ============================================================
st.header("💬 AI Financial Advisor")

# ============================================================
# 聊天历史记录
# Session State 用于在页面刷新前持久化消息列表
# st.session_state.messages stores [{role, content}, ...]
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
# 渲染聊天历史
# 遍历 session_state 中所有消息，按角色显示
# Iterate all messages and render with chat bubble
# ============================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ============================================================
# 聊天输入框
# 用户输入后立即存入 session_state 并触发 Assistant 回复
# Chat input — user types here, message saved immediately
# ============================================================
if prompt := st.chat_input("Ask me anything about your wealth..."):
    # 1) 显示用户消息 / Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 构造发送给 LLM 的消息历史
    # Build message history for LLM
    messages = []

    for msg in st.session_state.messages:
        messages.append(
            {
                "role": msg["role"],
                "content": msg["content"],
            }
        )

    # 调用本地 LLM 生成回复
    # Generate response from local LLM
    reply = chat(messages)

    # 保存 Assistant 回复
    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply,
        }
    )

    # 显示 Assistant 回复
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(reply)

"""AuraWealth — AI Wealth Management Platform."""

import streamlit as st

from lib import config
from lib.agents import run_agent_workflow
from lib.data import get_portfolio, format_portfolio_context

# ============================================================
# 页面配置 — 浏览器标签标题、图标、布局
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
    # 用户选择器 — 当前活跃用户，后续扩展为每用户独立历史
    # User selector — tracks active user, will drive per-user history
    # ============================================================
    st.divider()

    # 默认当前用户为 Alice / Default active user is Alice
    if "current_user" not in st.session_state:
        st.session_state.current_user = "Alice"

    # Radio 按钮用户切换 / Radio buttons for user switching
    selected = st.radio(
        "Select user",
        ["Alice", "Bob", "Charlie"],
        index=["Alice", "Bob", "Charlie"].index(st.session_state.current_user),
        label_visibility="collapsed",
    )
    st.session_state.current_user = selected

    st.caption(f"Current user: **{selected}**")

    # ============================================================
    # 当前用户投资组合 — 展示在侧边栏，同时传递给 LLM 作为上下文
    # Current portfolio — displayed in sidebar, passed to LLM as context
    # ============================================================
    st.divider()
    st.subheader("Portfolio")

    # 获取当前用户的持仓数据 / Get current user portfolio
    portfolio = get_portfolio(st.session_state.current_user)

    # 逐行显示持仓 / Display each holding as a line item
    for symbol, value in portfolio.items():
        st.write(f"**{symbol}**: ${value:,.0f}")

    # 如果没有持仓 / Fallback for empty portfolio
    if not portfolio:
        st.caption("No holdings")

# ============================================================
# 主区域标题
# Main area title
# ============================================================
st.header("💬 AI Financial Advisor")

# ============================================================
# 聊天历史记录
# Session State 用于在页面刷新前持久化消息列表
# st.session_state.user_histories stores {user: [{role, content}, ...]}, per-user
# ============================================================
if "user_histories" not in st.session_state:
    st.session_state.user_histories = {
        "Alice": [],
        "Bob": [],
        "Charlie": [],
    }

# ============================================================
# 渲染聊天历史
# 遍历 session_state 中所有消息，按角色显示
# Iterate all messages and render with chat bubble
# ============================================================
for msg in st.session_state.user_histories[st.session_state.current_user]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ============================================================
# 聊天输入框
# 用户输入后存入 session_state，然后运行3-Agent工作流
# Chat input — saves user message, then runs 3-agent workflow
# ============================================================
if prompt := st.chat_input("Ask me anything about your wealth..."):
    # 显示用户消息 / Display user message
    st.session_state.user_histories[st.session_state.current_user].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ============================================================
    # 运行 3-Agent 顺序工作流
    # Run 3-agent sequential workflow: Planner -> Research -> Response
    # 中间输出（plan, research）在内部传递，不显示给用户
    # ============================================================
    # ============================================================
    # 构建 UI 数据上下文 — 将当前投资组合传递给 Agent 工作流
    # Build UI data context — inject portfolio into agent workflow
    # ============================================================
    portfolio = get_portfolio(st.session_state.current_user)
    context = format_portfolio_context(st.session_state.current_user, portfolio)
    augmented_prompt = f"{context}\n\nUser Question: {prompt}"

    with st.spinner("AI Advisor is thinking..."):
        reply = run_agent_workflow(augmented_prompt)

    # 显示 Assistant 回复 / Display assistant response
    with st.chat_message("assistant"):
        st.markdown(reply)

    # 保存到会话历史 / Save to session history
    st.session_state.user_histories[st.session_state.current_user].append({"role": "assistant", "content": reply})

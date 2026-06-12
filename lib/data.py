"""Sample financial data and portfolio generation."""

# Stub - sample data added during assessment
"""每用户投资组合数据 / Per-user portfolio data.

每个用户拥有不同的持仓，用于展示和问答。
Each user has different holdings for UI display and Q&A.
"""

# ── 预定义用户投资组合 / Predefined portfolio holdings ──────────────
# 格式: {symbol: market_value_in_USD}
PORTFOLIO_DATA = {
    "Alice": {
        "AAPL": 10000,
        "MSFT": 5000,
        "NVDA": 8000,
    },
    "Bob": {
        "TSLA": 7000,
        "GOOGL": 4000,
    },
    "Charlie": {
        "SPY": 15000,
        "QQQ": 12000,
    },
}


def get_portfolio(username):
    """返回指定用户的投资组合 dict / Return portfolio dict for a user."""
    return PORTFOLIO_DATA.get(username, {})


def format_portfolio_context(username, portfolio):
    """将投资组合格式化为 LLM 上下文文本。

    Format portfolio data as context text for the agent workflow.
    This string is prepended to the user query so the LLM can
    answer questions about the displayed data.

    Example output:
        [Current Portfolio for Alice]
        AAPL: $10,000
        MSFT: $5,000
    """
    lines = [f"[Current Portfolio for {username}]"]
    for symbol, value in portfolio.items():
        lines.append(f"{symbol}: ${value:,}")
    return "\n".join(lines)

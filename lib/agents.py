"""多Agent顺序工作流 / Sequential Agent Workflow

工作流: User Query -> Planner -> Research -> Response -> Final Answer
每个Agent调用 chat() 函数，输出传递给下一个Agent作为上下文。
"""

from .llm import chat

# ============================================================
# Agent 1: Planner — 制定研究计划
# Receives user query, outputs a structured research plan
# ============================================================
PLANNER_SYSTEM = (
    "You are a financial planning agent. "
    "Break down the user's question into a clear research plan. "
    "List 3-5 key areas to investigate. "
    "Output only the plan, no extra commentary."
)


def planner_agent(query):
    """
    制定研究计划 / Create a research plan

    Args:
        query: str — 用户的原始问题 / Original user question

    Returns:
        str — 研究计划文本 / Research plan text
    """
    messages = [
        {"role": "system", "content": PLANNER_SYSTEM},
        {"role": "user", "content": query},
    ]
    return chat(messages)


# ============================================================
# Agent 2: Research — 执行研究
# Receives plan, outputs research data and analysis
# ============================================================
RESEARCH_SYSTEM = (
    "You are a financial research agent. "
    "Based on the plan provided, conduct thorough research. "
    "Provide data, analysis, and comparisons. "
    "Output only the research findings, no extra commentary."
)


def research_agent(query, plan):
    """
    执行研究 / Conduct research based on plan

    Args:
        query: str — 用户原始问题 / Original question
        plan: str — Planner Agent 输出的计划 / Plan from planner

    Returns:
        str — 研究成果文本 / Research findings text
    """
    messages = [
        {"role": "system", "content": RESEARCH_SYSTEM},
        {
            "role": "user",
            "content": f"Question: {query}\n\nPlan: {plan}",
        },
    ]
    return chat(messages)


# ============================================================
# Agent 3: Response — 生成最终回复
# Receives research, outputs final user-facing answer
# ============================================================
RESPONSE_SYSTEM = (
    "You are AuraWealth's response agent. "
    "Based on the research provided, write a clear, actionable final response "
    "for the user. Be concise and helpful. "
    "Format the response for direct display to the user."
)


def response_agent(query, research):
    """
    生成最终回复 / Generate final response from research

    Args:
        query: str — 用户原始问题 / Original question
        research: str — Research Agent 输出的研究结果 / Research findings

    Returns:
        str — 最终回复文本 / Final response text
    """
    messages = [
        {"role": "system", "content": RESPONSE_SYSTEM},
        {
            "role": "user",
            "content": f"Question: {query}\n\nResearch: {research}",
        },
    ]
    return chat(messages)


# ============================================================
# Orchestrator — 串联3个Agent
# Runs all 3 agents sequentially, passes output forward
# ============================================================
def run_agent_workflow(query):
    """
    运行完整3-Agent顺序工作流
    Run full 3-agent sequential workflow

    流程: planner_agent() -> research_agent() -> response_agent()
    每个Agent的输出作为下一个Agent的输入上下文
    最终只返回 response_agent() 的输出

    Args:
        query: str — 用户原始问题 / Original user question

    Returns:
        str — 最终回复 / Final answer to display to user
    """
    plan = planner_agent(query)
    research = research_agent(query, plan)
    answer = response_agent(query, research)
    return answer

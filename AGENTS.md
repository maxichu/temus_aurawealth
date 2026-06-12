# AuraWealth Agents

## Architecture

This project uses a function-calling agent pattern with OpenAI.
No LangChain or CrewAI. Each agent is a Python function with a
tool definition registered in the orchestrator loop.

## Agents

| Agent | Role | Tools |
|-------|------|-------|
| Advisor | General financial advice | chat, search, data lookup |
| Portfolio | Portfolio analysis | query_portfolio, risk_check |
| Research | Market research | web_search, semantic_search |

## Tool-Calling Loop

1. User message → orchestrator
2. LLM decides tool call or direct reply
3. Tool executed → result fed back to LLM
4. LLM produces final response
5. Response shown to user

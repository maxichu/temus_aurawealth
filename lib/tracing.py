"""基础 Trace 日志 — 记录每次用户查询 / Basic trace logging for user queries.

每个 trace 条目记录: timestamp, user, query, workflow
存储为 logs/traces.jsonl，每行一个 JSON 对象。
"""

import json
from datetime import datetime
from pathlib import Path

# ── Trace 文件路径 / Path to the trace log file ────────────────
# 使用项目根目录下的 logs/ 文件夹
TRACE_FILE = Path("logs/traces.jsonl")


def log_trace(
    user,
    query,
    response=None,
    workflow="Planner->Research->Response",
    model=None,
    latency_ms=None,
):
    """记录一条 Trace 到 traces.jsonl。

    Log a trace entry to traces.jsonl.

    Args:
        user: str — 当前用户 / Current user
        query: str — 用户输入的问题 / User query text
        workflow: str — 工作流名称 / Workflow name

    每行格式: {"timestamp": "ISO-8601", "user": "...", "query": "...", "workflow": "..."}
    """
    TRACE_FILE.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "query": query,
        "response": response,
        "workflow": workflow,
        "model": model,
        "latency_ms": latency_ms,
    }

    with open(TRACE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_recent_traces(n=5):
    """读取最近 n 条 Trace 记录。

    Read the most recent n trace entries from traces.jsonl.

    Args:
        n: int — 返回的条数 / Number of recent entries to return

    Returns:
        list[dict] — 最近的 trace 列表，最新在前
    """
    if not TRACE_FILE.exists():
        return []

    with open(TRACE_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 只解析最后 n 行 / Parse only the last n lines
    traces = []
    for line in lines[-n:]:
        line = line.strip()
        if not line:
            continue
        try:
            traces.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    return traces


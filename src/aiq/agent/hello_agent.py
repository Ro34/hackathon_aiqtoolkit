from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.graph import CompiledGraph

from .base import BaseAgent, NO_INPUT_ERROR_MESSAGE

logger = logging.getLogger(__name__)


class HelloAgent(BaseAgent):
    """
    一个最小可用的演示 Agent：
    - 若输入包含“你好”，回复问候并附当前时间；
    - 否则给出说明性回复。
    """

    async def run(self, user_input: str, config: RunnableConfig | None = None) -> AIMessage:
        if not user_input or not user_input.strip():
            return AIMessage(content=NO_INPUT_ERROR_MESSAGE)

        text = user_input.strip()
        if "你好" in text:
            now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
            return AIMessage(content=f"你好！现在时间是 {now}")

        return AIMessage(content="我只会在你对我说“你好”时，回复问候并告知当前时间。")

    async def _build_graph(self, state_schema: type | None = None) -> CompiledGraph:
        # 提供一个最小占位图以满足抽象方法
        from langgraph.graph import StateGraph, END

        class _State(dict):
            pass

        def passthrough(state: _State) -> _State:
            return state

        g = StateGraph(_State)
        g.add_node("pass", passthrough)
        g.set_entry_point("pass")
        g.add_edge("pass", END)
        return g.compile()
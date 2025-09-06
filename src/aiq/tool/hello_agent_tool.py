from __future__ import annotations

from typing import Any, Type

from langchain_core.callbacks import AsyncCallbackManagerForToolRun
from langchain_core.tools import BaseTool

from hackathon_aiqtoolkit.src.aiq.agent import hello_agent


class GreetingTool(BaseTool):
    """一个将 HelloAgent 包装成工具的适配器。"""

    name: str = "greeting_tool"
    description: str = (
        "当用户输入包含'你好'或类似的问候语时使用此工具。"
        "它会返回一个带当前时间的问候。"
    )

    # 如果 HelloAgent 的 __init__ 需要参数，可以在这里定义
    # llm: Any = None
    # tools: list = []

    async def _arun(
        self,
        query: str,
        *,
        run_manager: AsyncCallbackManagerForToolRun | None = None,
        **kwargs: Any,
    ) -> str:
        """使用 HelloAgent 处理问候。"""
        # 注意：BaseAgent的__init__需要llm和tools，即使不用也要传None或空列表
        # 这里的None需要类型忽略，因为类型定义是BaseChatModel
        agent = hello_agent(llm=None, tools=[])  # type: ignore
        response_message = await agent.run(query)
        return response_message.content

    def _run(self, query: str, **kwargs: Any) -> str:
        return "greeting_tool 仅支持异步调用。"
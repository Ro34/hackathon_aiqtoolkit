from __future__ import annotations
from typing import Any

from langchain_core.tools import BaseTool
from langchain_core.callbacks import AsyncCallbackManagerForToolRun

# 这个导入依赖于 HelloAgent 已被创建并且项目被正确安装
from aiq.agent.hello_agent import HelloAgent


class GreetingTool(BaseTool):
    """将 HelloAgent 包装为可被 NAT 调用的 LangChain Tool。"""

    # `name` 是工具的内部标识符
    name: str = "greeting_tool"
    
    # `description` 会被大语言模型（LLM）看到，用来决定何时使用此工具
    description: str = (
        "当用户输入包含“你好”等中文问候语时使用该工具，"
        "返回问候并附当前时间。"
    )

    async def _arun(
        self,
        query: str,
        *,
        run_manager: AsyncCallbackManagerForToolRun | None = None,
        **kwargs: Any,
    ) -> str:
        """这是工具的异步执行逻辑。"""
        # 1. 实例化你的 HelloAgent
        agent = HelloAgent(llm=None, tools=[])  # type: ignore

        # 2. 运行 HelloAgent 并获取返回的消息对象
        response_message = await agent.run(query)

        # 3. 从消息对象中提取内容字符串并返回
        return response_message.content

    def _run(self, query: str, **kwargs: Any) -> str:
        """同步执行的后备方法，避免在非异步环境调用时出错。"""
        return "greeting_tool 仅支持异步调用。"
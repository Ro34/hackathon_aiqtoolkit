# SPDX-FileCopyrightText: Copyright (c) 2025, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
from typing import AsyncIterator

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.framework_enum import LLMFrameworkEnum
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.api_server import AIQChatRequest, AIQChatResponse
from aiq.data_models.component_ref import FunctionRef, LLMRef
from aiq.data_models.function import FunctionBaseConfig
from aiq.utils.type_converter import GlobalTypeConverter

logger = logging.getLogger(__name__)


class DebateAgentWorkflowConfig(FunctionBaseConfig, name="debate_agent"):
    """多 Agent 辩论：同一脚本里实例化两个 ReAct Agent（正方/反方），共享“黑板”记忆，交替 N 轮后输出 Markdown「利弊对比表」。"""

    tool_names: list[FunctionRef] = Field(default_factory=list, description="提供给两个 ReAct Agent 的工具列表")
    llm_name: LLMRef = Field(description="用于两个 ReAct Agent 与总结器的 LLM")
    rounds: int = Field(default=3, description="正反交替的轮数（每轮含正方一次+反方一次）")
    verbose: bool = Field(default=False, description="日志与中间步骤的详细程度")

    # ReAct 相关参数
    include_tool_input_schema_in_tool_description: bool = Field(
        default=True, description="是否在提示中包含工具的输入 schema")
    retry_agent_response_parsing_errors: bool = Field(default=True, description="解析错误时是否重试")
    parse_agent_response_max_retries: int = Field(default=1, description="解析错误重试次数上限")
    tool_call_max_retries: int = Field(default=1, description="工具调用失败时的重试次数")
    max_tool_calls: int = Field(default=6, description="每次 Agent 调用允许的最大工具调用次数")

    # 角色化系统提示（在标准 ReAct SYSTEM_PROMPT 基础上追加）
    pro_role_instructions: str = Field(
        default=(
            "你是正方辩手A，立场是【支持】题目。观点要事实可核验，必要时使用工具检索。"
            "输出要点式中文结论，尽量去重，每次3-5条，末尾给出一句最强论点。"
        ),
        description="正方追加的系统指令")
    con_role_instructions: str = Field(
        default=(
            "你是反方辩手B，立场是【反对】题目。观点要事实可核验，必要时使用工具检索。"
            "输出要点式中文结论，尽量去重，每次3-5条，末尾给出一句最强论点。"
        ),
        description="反方追加的系统指令")

    # 输出控制
    use_openai_api: bool = Field(default=False, description="是否采用 OpenAI ChatCompletions 兼容 I/O")


@register_function(config_type=DebateAgentWorkflowConfig, framework_wrappers=[LLMFrameworkEnum.LANGCHAIN])
async def debate_agent(config: DebateAgentWorkflowConfig, builder: Builder) -> AsyncIterator[FunctionInfo]:
    """注册一个可直接在工作流中调用的辩论函数。"""

    from langchain_core.messages.human import HumanMessage
    from aiq.agent.react_agent.agent import ReActAgentGraph, ReActGraphState, create_react_agent_prompt
    from aiq.agent.react_agent.prompt import SYSTEM_PROMPT
    from aiq.agent.react_agent.register import ReActAgentWorkflowConfig

    # 1) 初始化 LLM 与工具
    llm = await builder.get_llm(config.llm_name, wrapper_type=LLMFrameworkEnum.LANGCHAIN)
    tools = builder.get_tools(tool_names=config.tool_names, wrapper_type=LLMFrameworkEnum.LANGCHAIN)
    if not tools:
        raise ValueError(f"DebateAgent 需要至少一个工具以构造 ReAct Agent，未找到: {config.tool_names}")

    # 2) 为正反两位 ReAct Agent 组装提示词（在标准 ReAct SYSTEM_PROMPT 基础上追加角色指令）
    pro_cfg = ReActAgentWorkflowConfig(
        llm_name=config.llm_name,
        tool_names=[],
        system_prompt=SYSTEM_PROMPT,
        additional_instructions=config.pro_role_instructions,
    )
    con_cfg = ReActAgentWorkflowConfig(
        llm_name=config.llm_name,
        tool_names=[],
        system_prompt=SYSTEM_PROMPT,
        additional_instructions=config.con_role_instructions,
    )
    pro_prompt = create_react_agent_prompt(pro_cfg)
    con_prompt = create_react_agent_prompt(con_cfg)

    # 3) 构建两个 ReAct Agent Graph
    pro_agent = await ReActAgentGraph(
        llm=llm,
        prompt=pro_prompt,
        tools=tools,
        use_tool_schema=config.include_tool_input_schema_in_tool_description,
        detailed_logs=config.verbose,
        retry_agent_response_parsing_errors=config.retry_agent_response_parsing_errors,
        parse_agent_response_max_retries=config.parse_agent_response_max_retries,
        tool_call_max_retries=config.tool_call_max_retries,
        pass_tool_call_errors_to_agent=True,
    ).build_graph()

    con_agent = await ReActAgentGraph(
        llm=llm,
        prompt=con_prompt,
        tools=tools,
        use_tool_schema=config.include_tool_input_schema_in_tool_description,
        detailed_logs=config.verbose,
        retry_agent_response_parsing_errors=config.retry_agent_response_parsing_errors,
        parse_agent_response_max_retries=config.parse_agent_response_max_retries,
        tool_call_max_retries=config.tool_call_max_retries,
        pass_tool_call_errors_to_agent=True,
    ).build_graph()

    def format_blackboard(bb: list[str]) -> str:
        if not bb:
            return "(当前黑板为空)"
        return "\n".join(f"- {x}" for x in bb)

    async def _run_debate(topic: str) -> str:
        blackboard: list[str] = []

        for round_idx in range(1, max(1, config.rounds) + 1):
            # 正方回合
            pro_q = (
                f"辩题: {topic}\n"
                f"你的任务: 站在【支持】立场，基于需要可调用工具，提出新的不重复要点。\n"
                f"共享黑板(可参考但不要复述):\n{format_blackboard(blackboard)}\n"
                f"请用要点式中文输出，最后补充一句当轮最强论点。"
            )
            pro_state = ReActGraphState(messages=[HumanMessage(content=pro_q)])
            pro_state = await pro_agent.ainvoke(
                pro_state, config={'recursion_limit': (config.max_tool_calls + 1) * 2}
            )
            pro_state = ReActGraphState(**pro_state)
            pro_answer = str(pro_state.messages[-1].content)
            blackboard.append(f"第{round_idx}轮·正方：{pro_answer}")

            # 反方回合
            con_q = (
                f"辩题: {topic}\n"
                f"你的任务: 站在【反对】立场，基于需要可调用工具，提出新的不重复要点，反驳黑板中的正方观点。\n"
                f"共享黑板(可参考但不要复述):\n{format_blackboard(blackboard)}\n"
                f"请用要点式中文输出，最后补充一句当轮最强反驳。"
            )
            con_state = ReActGraphState(messages=[HumanMessage(content=con_q)])
            con_state = await con_agent.ainvoke(
                con_state, config={'recursion_limit': (config.max_tool_calls + 1) * 2}
            )
            con_state = ReActGraphState(**con_state)
            con_answer = str(con_state.messages[-1].content)
            blackboard.append(f"第{round_idx}轮·反方：{con_answer}")

        # 4) 生成 Markdown 利弊对比表（直接由 LLM 汇总更稳妥，适合飞书粘贴）
        prompt = (
            "你是会议纪要助手。请把下面黑板中的正反双方观点，汇总为严格的 Markdown 文档：\n"
            "- 顶部一级标题为‘辩论结果’并包含辩题\n"
            "- 一个不超过80字的结论段\n"
            "- 一个三列表格标题为‘利弊对比表’，列名分别为‘要点’、‘正方(利)’、‘反方(弊)’\n"
            "- 每格不超过40字，避免重复，适合直接粘贴到飞书文档\n\n"
            f"辩题: {topic}\n黑板全文:\n" + "\n".join(blackboard)
        )
        md = await llm.ainvoke(prompt)
        return str(getattr(md, 'content', md))

    async def _response_fn(input_message: AIQChatRequest) -> AIQChatResponse:
        try:
            # 取最后一条用户消息作为辩题
            last_user_text = None
            for m in reversed(input_message.messages):
                if m.role == "user":
                    last_user_text = str(m.content)
                    break
            topic = last_user_text or "请给出辩题"

            markdown = await _run_debate(topic)
            return AIQChatResponse.from_string(markdown)
        except Exception as ex:  # pragma: no cover - 保护性返回
            logger.exception("DebateAgent 运行失败: %s", ex, exc_info=ex)
            return AIQChatResponse.from_string("抱歉，辩论流程出现异常。")

    if config.use_openai_api:
        yield FunctionInfo.from_fn(_response_fn, description="多 Agent 辩论，输出 Markdown 利弊对比表")
    else:
        async def _str_api_fn(input_message: str) -> str:
            oai_input = GlobalTypeConverter.get().try_convert(input_message, to_type=AIQChatRequest)
            oai_output = await _response_fn(oai_input)
            return GlobalTypeConverter.get().try_convert(oai_output, to_type=str)

        yield FunctionInfo.from_fn(_str_api_fn, description="多 Agent 辩论，输出 Markdown 利弊对比表")


class DebateRouterConfig(FunctionBaseConfig, name="debate_router"):
    """基于关键词自动路由到辩论或默认聊天工作流。"""

    debate_fn: FunctionRef = Field(description="当触发关键词时调用的辩论函数名")
    default_fn: FunctionRef = Field(description="未触发时的默认函数名（例如 react_agent）")
    trigger_keywords: list[str] = Field(
        default_factory=lambda: ["辩论", "正反", "利弊", "pros and cons", "debate"],
        description="触发辩论的关键词，命中任意一个即触发",
    )
    use_openai_api: bool = Field(default=False, description="是否采用 OpenAI ChatCompletions 兼容 I/O")


@register_function(config_type=DebateRouterConfig)
async def debate_router(config: DebateRouterConfig, builder: Builder) -> AsyncIterator[FunctionInfo]:
    """一个薄路由函数：检查用户输入是否包含关键词，命中则转到 debate_fn，否则转到 default_fn。"""

    import re

    debate_impl = builder.get_function(config.debate_fn)
    default_impl = builder.get_function(config.default_fn)

    def _extract_text(input_message: AIQChatRequest) -> str:
        last_user_text = None
        for m in reversed(input_message.messages):
            if m.role == "user":
                last_user_text = str(m.content)
                break
        return last_user_text or ""

    def _hit_keywords(text: str) -> bool:
        for kw in config.trigger_keywords:
            if re.search(re.escape(kw), text, flags=re.IGNORECASE):
                return True
        return False

    async def _response_fn(input_message: AIQChatRequest) -> AIQChatResponse:
        text = _extract_text(input_message)
        target = debate_impl if _hit_keywords(text) else default_impl
        logger.debug("debate_router -> %s", target.instance_name)
        out = await target.ainvoke(input_message, to_type=AIQChatResponse)
        return out

    if config.use_openai_api:
        yield FunctionInfo.from_fn(_response_fn, description="基于关键词的聊天/辩论自动路由")
    else:
        async def _str_api_fn(input_message: str) -> str:
            oai_input = GlobalTypeConverter.get().try_convert(input_message, to_type=AIQChatRequest)
            oai_output = await _response_fn(oai_input)
            return GlobalTypeConverter.get().try_convert(oai_output, to_type=str)

        yield FunctionInfo.from_fn(_str_api_fn, description="基于关键词的聊天/辩论自动路由")

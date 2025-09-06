import logging

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig

from .greeting_tool import GreetingTool

logger = logging.getLogger(__name__)


class GreetingToolConfig(FunctionBaseConfig, name="greeting_tool"):
    """greeting_tool 的配置模型。"""
    description: str = "当用户问候'你好'时，返回带时间的问候。"


@register_function(config_type=GreetingToolConfig)
async def greeting_tool_workflow(config: GreetingToolConfig, builder: Builder):
    """注册 greeting_tool 的工作流。"""
    try:
        tool = GreetingTool(description=config.description)
        yield FunctionInfo.from_tool(tool)
    except GeneratorExit:
        logger.debug("greeting_tool_workflow 生成器关闭。")

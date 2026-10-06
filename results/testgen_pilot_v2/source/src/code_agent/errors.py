"""统一异常定义，便于上层区分错误来源并做针对性处理。"""
from __future__ import annotations


class CodeAgentError(Exception):
    """项目内所有自定义异常的基类。"""


class ConfigError(CodeAgentError):
    """配置缺失或非法，例如没有填写 API Key。"""


class LLMError(CodeAgentError):
    """LLM 接口调用失败（网络错误、鉴权失败、服务端错误等）。"""


class ToolError(CodeAgentError):
    """工具执行失败（参数错误、路径越界、文件不存在等）。"""
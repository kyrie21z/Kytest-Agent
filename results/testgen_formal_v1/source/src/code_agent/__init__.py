"""Code Agent：一个零第三方依赖、可扩展的代码助手 Agent。

功能：代码审查、代码解释、单元测试生成、重构建议与编程问答。
架构：LLM 客户端 + ReAct/Function Calling 主循环 + 工具注册表 + 会话记忆。
"""

__version__ = "1.0.0"
__all__ = ["__version__"]
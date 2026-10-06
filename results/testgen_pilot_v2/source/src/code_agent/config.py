"""运行配置：优先级为 显式参数 > 环境变量 > .env 文件 > 默认值。

不依赖 python-dotenv，自行解析简单的 KEY=VALUE 文件，保证零第三方依赖。
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

from .errors import ConfigError


def parse_env_file(path: Path) -> Dict[str, str]:
    """解析 .env 文件；文件不存在或格式错误时静默返回已解析内容。"""
    result: Dict[str, str] = {}
    try:
        raw = path.read_text(encoding="utf-8-sig")
    except OSError:
        return result
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            result[key] = value
    return result


def _to_bool(value: Any, default: bool) -> bool:
    if value is None or value == "":
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def _to_int(value: Any, default: int) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _to_float(value: Any, default: float) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


@dataclass
class Settings:
    """全局配置对象。所有路径都会被规范化为绝对路径。"""

    # ---------- LLM ----------
    api_key: str = ""
    base_url: str = ""
    model: str = ""
    temperature: float = 0.2
    # 单次请求的**输出**上限。必须 ≥1：服务端会校验范围（千问要求 [1, 131072]），
    # 传 0 会被直接拒绝。
    llm_max_tokens: int = 2048
    request_timeout: int = 60
    max_retries: int = 3

    # ---------- Agent ----------
    max_steps: int = 8
    max_context_chars: int = 32000
    # 整个 run 的累计 token 预算。0 表示不限——**与输出上限是两件事**。
    # 早期版本把这两个语义压在同一个 `max_tokens` 字段上，导致 Agent 侧设成 0
    # （不限）时，0 被原样当成输出上限发给服务端，请求必然 400。
    max_total_tokens: int = 0

    # ---------- 工作区与安全 ----------
    workspace: Path = field(default_factory=Path.cwd)
    allow_code_execution: bool = True
    execution_mode: str = "sandbox"
    allow_write: bool = True
    exec_timeout: int = 10
    max_exec_timeout: int = 300
    max_file_bytes: int = 200_000

    # ---------- 会话 ----------
    session_dir: Optional[Path] = None

    def __post_init__(self) -> None:
        self.workspace = Path(self.workspace).expanduser().resolve()
        self.session_dir = Path(self.session_dir).expanduser().resolve() if self.session_dir else self.workspace / ".sessions"
        self.max_steps = max(1, int(self.max_steps))
        self.max_context_chars = max(2000, int(self.max_context_chars))
        self.exec_timeout = max(1, int(self.exec_timeout))
        # 输出上限必须落在服务端接受的区间内，否则请求会在第一轮就 400
        self.llm_max_tokens = max(1, int(self.llm_max_tokens))
        self.max_total_tokens = max(0, int(self.max_total_tokens))
        if self.execution_mode not in {"sandbox", "trusted", "disabled"}:
            raise ConfigError("EXECUTION_MODE 必须是 sandbox、trusted 或 disabled")

    # ------------------------------------------------------------------
    # 便捷属性
    # ------------------------------------------------------------------
    @property
    def is_llm_configured(self) -> bool:
        """三项都填写才认为配置完整，避免只填一半时发出必然失败的请求。"""
        return bool(self.api_key and self.base_url and self.model)

    @property
    def masked_api_key(self) -> str:
        if not self.api_key:
            return "(未设置)"
        if len(self.api_key) <= 8:
            return "*" * len(self.api_key)
        return self.api_key[:4] + "*" * (len(self.api_key) - 8) + self.api_key[-4:]

    def require_llm(self) -> None:
        if not self.is_llm_configured:
            raise ConfigError(
                "未配置 LLM：请在 .env 或环境变量中设置 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL，"
                "或使用 `python main.py --mock` 运行离线演示。"
            )

    def describe(self) -> Dict[str, Any]:
        """返回可安全打印的配置摘要（API Key 已脱敏）。"""
        return {
            "base_url": self.base_url or "(未设置)",
            "model": self.model or "(未设置)",
            "api_key": self.masked_api_key,
            "temperature": self.temperature,
            "max_steps": self.max_steps,
            "max_context_chars": self.max_context_chars,
            "workspace": str(self.workspace),
            "allow_code_execution": self.allow_code_execution,
            "execution_mode": self.execution_mode,
            "allow_write": self.allow_write,
            "exec_timeout": self.exec_timeout,
        }

    # ------------------------------------------------------------------
    # 构造
    # ------------------------------------------------------------------
    @classmethod
    def from_env(
        cls,
        workspace: Optional[Any] = None,
        env_file: Optional[Any] = None,
        read_env_file: bool = True,
    ) -> "Settings":
        """从环境变量与 .env 文件构造配置。

        Args:
            workspace: 显式指定的工作区（优先级最高）。
            env_file: 显式指定的 .env 路径。
            read_env_file: 为 False 时完全不读 .env，只看进程环境变量。
                评测与测试需要这个开关：被测实例的工作区是临时目录，
                不应该继承评测机上某处的 `.env`，否则"未配置凭据"的用例会
                变成一次真实网络请求。

        `.env` 的查找顺序：先在工作区里找，找不到再用当前目录。
        这个顺序是刻意的——`-C/--workspace` 应该同时隔离配置与文件访问。
        只看当前目录的话，`code-agent -C ../other-project` 会读到本目录的 `.env`。
        """
        if not read_env_file:
            file_env: Dict[str, str] = {}
            env_path = None
        elif env_file is not None:
            env_path = Path(env_file).expanduser()
            file_env = parse_env_file(env_path)
        else:
            # 只认显式传入的工作区。这里**不**回落到 CODE_AGENT_WORKSPACE：
            # 调用方（CLI）已经解析过该环境变量并把结果作为参数传进来。
            candidate = workspace if workspace is not None else Path.cwd()
            workspace_env = Path(candidate).expanduser() / ".env"
            env_path = workspace_env if workspace_env.is_file() else Path.cwd() / ".env"
            file_env = parse_env_file(env_path)

        def get(key: str, default: str = "") -> str:
            value = os.environ.get(key)
            if value is None or value == "":
                value = file_env.get(key)
            return default if value is None or value == "" else value

        workspace_value = workspace or get("CODE_AGENT_WORKSPACE") or Path.cwd()
        return cls(
            api_key=get("LLM_API_KEY") or get("OPENAI_API_KEY"),
            base_url=get("LLM_BASE_URL"),
            model=get("LLM_MODEL"),
            temperature=_to_float(get("LLM_TEMPERATURE"), 0.2),
            llm_max_tokens=_to_int(get("LLM_MAX_TOKENS"), 2048),
            request_timeout=_to_int(get("LLM_TIMEOUT"), 60),
            max_retries=_to_int(get("LLM_MAX_RETRIES"), 3),
            max_steps=_to_int(get("AGENT_MAX_STEPS"), 8),
            max_context_chars=_to_int(get("AGENT_MAX_CONTEXT_CHARS"), 32000),
            max_total_tokens=_to_int(get("AGENT_MAX_TOTAL_TOKENS"), 0),
            workspace=Path(workspace_value),
            allow_code_execution=_to_bool(get("ALLOW_CODE_EXECUTION"), True),
            execution_mode=get("EXECUTION_MODE", "sandbox"),
            allow_write=_to_bool(get("ALLOW_WRITE"), True),
            exec_timeout=_to_int(get("EXEC_TIMEOUT"), 10),
            max_exec_timeout=_to_int(get("MAX_EXEC_TIMEOUT"), 300),
            max_file_bytes=_to_int(get("MAX_FILE_BYTES"), 200_000),
            session_dir=get("SESSION_DIR") or None,
        )

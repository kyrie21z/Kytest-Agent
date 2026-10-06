"""会话轨迹落盘：append-only JSONL。

为什么必须是 append-only：评测跑到一半崩溃、或某个实例超时被杀时，
**已经产生的轨迹不能丢**。一次性 dump 整份会话的实现会让最后一步的全部证据消失，
而恰恰是崩溃前的那段轨迹最有诊断价值。

行格式：

    {"type":"session", "version":1, "session_id":..., "started_at":..., "model":..., "tools":[...]}
    {"type":"user",    "content":"..."}
    {"type":"assistant","text":"...", "tool_calls":[...], "stop_reason":"...", "usage":{...}}
    {"type":"tool",    "name":"...", "is_error":false, "content":"..."}
    {"type":"result",  "status":"completed", "turns":3, "total_tokens":300}

会话文件保留事件结构和非敏感内容；凭据落盘前脱敏。
体积控制交给调用方（评测时只保留摘要 + 失败样例全文）。
"""
from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence, Tuple

from .agent.events import (
    AssistantMessageEvent,
    ToolCallEnd,
    ToolCallStart,
    TurnEnd,
)
from .message import Usage

SESSION_VERSION = 1


def new_session_id() -> str:
    """生成短的、可读的会话 ID（时间戳 + 随机后缀）。"""
    stamp = time.strftime("%Y%m%d-%H%M%S")
    return f"{stamp}-{uuid.uuid4().hex[:6]}"


_REDACT_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{8,}"),
    re.compile(r"(?i)bearer\s+[^\s\"',;}{]+"),
)
_REDACTED = "***REDACTED***"
_CREDENTIAL_ASSIGNMENT = re.compile(
    r"(?P<label>(?<![\w-])[\"']?(?P<key>[A-Za-z_][A-Za-z0-9_-]*)[\"']?\s*[=:]\s*)"
    r"(?P<value>\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|[^\s,;}{]+)"
)


def _sensitive_key(key: Any) -> bool:
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", str(key)).lower().replace("-", "_")
    return name.endswith(("api_key", "apikey", "secret_access_key", "private_key")) or (
        name.split("_")[-1] in {"secret", "token", "password", "passwd", "pwd",
                               "credential", "credentials", "authorization"}
    )


def redact_text(text: str, secrets: Sequence[str]) -> str:
    """对一段文本做脱敏：先替换已知密钥原文，再套用常见凭据形状。"""
    if not text:
        return text
    for secret in secrets:
        if secret and secret in text:
            text = text.replace(secret, _REDACTED)
    # 完整 JSON 使用键名策略，保留原来的结构；行号代码块等由文本规则处理。
    try:
        parsed = json.loads(text)
    except (ValueError, TypeError):
        parsed = None
    if isinstance(parsed, (dict, list)):
        return json.dumps(_redact_value(parsed, secrets), ensure_ascii=False)
    for pattern in _REDACT_PATTERNS:
        text = pattern.sub(_REDACTED, text)
    def replace_assignment(match: re.Match) -> str:
        if not _sensitive_key(match.group("key")):
            return match.group(0)
        value = match.group("value")
        quote = value[0] if value.startswith(('"', "'")) else ""
        return match.group("label") + quote + _REDACTED + quote
    text = _CREDENTIAL_ASSIGNMENT.sub(replace_assignment, text)
    return text


def _redact_value(value: Any, secrets: Sequence[str], key: Any = None) -> Any:
    """递归脱敏：字符串逐个处理，dict/list 保留结构。

    字典的**键名**命中敏感词时，其字符串值整体替换——这是对 JSON 凭据
    （`{"password": "..."}`）的兜底：文本正则依赖值的书写形状，
    键名规则不依赖。
    """
    if key is not None and _sensitive_key(key):
        # 非字符串凭据、列表与嵌套对象也不应绕过敏感键保护。
        if isinstance(value, dict):
            return {k: _redact_value(v, secrets, key="secret") for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [_redact_value(v, secrets, key="secret") for v in value]
        return _REDACTED
    if isinstance(value, str):
        return redact_text(value, secrets)
    if isinstance(value, dict):
        return {key: _redact_value(item, secrets, key=key) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact_value(item, secrets) for item in value]
    return value


@dataclass
class SessionStore:
    """把事件流写成 JSONL，并在内存里保留同一份副本供展示与复查。

    落盘前统一脱敏（已知密钥原文 + 常见凭据形状）——工具输出可能携带
    .env 内容或带凭据的响应，原样写盘等于把敏感信息持久化。
    写盘失败不抛出（轨迹不能影响 Agent 运行），但**必须可见**：
    失败计数与最后一次原因都会被记录，CLI 结束时如实区分保存状态。
    """

    path: Path
    session_id: str = field(default_factory=new_session_id)
    entries: List[Dict[str, Any]] = field(default_factory=list)
    started_at: float = field(default_factory=time.time)
    secrets: Tuple[str, ...] = ()
    warn: Callable[[str], None] = lambda message: None
    write_errors: int = 0
    last_write_error: str = ""

    @classmethod
    def create(
        cls,
        directory: Path,
        session_id: Optional[str] = None,
        *,
        secrets: Sequence[str] = (),
        warn: Optional[Callable[[str], None]] = None,
    ) -> "SessionStore":
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        session_id = session_id or new_session_id()
        return cls(
            path=directory / f"{session_id}.jsonl",
            session_id=session_id,
            secrets=tuple(s for s in secrets if s),
            warn=warn or (lambda message: None),
        )

    # ------------------------------------------------------------------
    # 写入
    # ------------------------------------------------------------------
    def write(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """追加一条记录。写盘失败不抛出——轨迹记录不能影响 Agent 运行——
        但失败会计数、记录原因，并通过 warn 通道发出一次警告。"""
        self.entries.append(entry)
        payload = json.dumps(_redact_value(entry, list(self.secrets)), ensure_ascii=False)
        try:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(payload + "\n")
        except OSError as exc:
            self.write_errors += 1
            self.last_write_error = f"{type(exc).__name__}: {exc}"
            if self.write_errors == 1:
                # 只在第一次失败时警告：后续每条都警告会刷屏；计数器保证最终可见。
                self.warn(f"警告：会话轨迹写入失败（{self.last_write_error}），后续记录仅保留在内存中。")
        return entry

    def write_header(self, *, workspace: Path, model: str, tools: List[str], mode: str) -> None:
        self.write(
            {
                "type": "session",
                "version": SESSION_VERSION,
                "session_id": self.session_id,
                "started_at": self.started_at,
                "workspace": str(workspace),
                "model": model,
                "tools": tools,
                "mode": mode,
            }
        )

    def record_event(self, event: Any) -> None:
        """把 Agent 事件翻译成轨迹记录。

        只记录"事后复查需要的信息"，不把整个事件对象原样转存——
        事件里有大段只对实时渲染有用的字段（如请求字符数），存下来只会让日志变肥。
        """
        if isinstance(event, ToolCallStart):
            self.write(
                {
                    "type": "tool_call",
                    "turn": event.turn,
                    "id": event.id,
                    "name": event.name,
                    "arguments": event.arguments,
                }
            )
        elif isinstance(event, ToolCallEnd):
            self.write(
                {
                    "type": "tool_result",
                    "turn": event.turn,
                    "id": event.id,
                    "name": event.name,
                    "is_error": event.is_error,
                    "duration_sec": round(event.duration_sec, 3),
                    "content": event.content,
                }
            )
        elif isinstance(event, AssistantMessageEvent):
            self.write(
                {
                    "type": "assistant",
                    "turn": event.turn,
                    "text": event.text,
                    "tool_calls": event.tool_calls,
                    "stop_reason": event.stop_reason,
                    "usage": event.usage,
                }
            )
        elif isinstance(event, TurnEnd):
            self.write(
                {"type": "turn_end", "turn": event.turn, "errors": event.errors}
            )

    def record_user(self, content: str) -> None:
        self.write({"type": "user", "content": content})

    def record_result(self, result: Any) -> None:
        self.write({"type": "result", **result.to_dict()})

    # ------------------------------------------------------------------
    # 读取
    # ------------------------------------------------------------------
    def replay(self) -> Iterator[Dict[str, Any]]:
        """逐行读回轨迹。损坏的行被跳过而不是让整个回放失败。"""
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue

    def summary(self) -> Dict[str, Any]:
        """从落盘内容里重建关键指标，用于"轨迹能否支撑结论"的自检。"""
        counts: Dict[str, int] = {}
        usage = Usage()
        status = ""
        turns = 0
        for entry in self.entries:
            counts[entry.get("type", "?")] = counts.get(entry.get("type", "?"), 0) + 1
            if entry.get("type") == "assistant":
                usage += Usage(
                    input_tokens=int((entry.get("usage") or {}).get("input_tokens") or 0),
                    output_tokens=int((entry.get("usage") or {}).get("output_tokens") or 0),
                )
            elif entry.get("type") == "result":
                status = entry.get("status", "")
                turns = int(entry.get("turns") or 0)
        return {
            "session_id": self.session_id,
            "path": str(self.path),
            "entries": counts,
            "turns": turns,
            "status": status,
            "total_tokens": usage.total_tokens,
            "write_errors": self.write_errors,
        }

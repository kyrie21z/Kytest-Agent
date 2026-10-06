"""模型连通性检查：在花时间跑评测之前，先确认这个模型能撑起我们的 Agent 循环。

它按顺序验证四件事，每件都可能独立失败：

1. **凭据与连通性** —— 能不能发出去、model 名字对不对；
2. **Function Calling** —— 模型是否会返回结构化的 tool_calls；
3. **工具结果回灌** —— 把 `role="tool"` 的消息发回去，模型能否继续；
   这一步是**风险最高**的：文档要求 messages 里 user/assistant 交替、最后一条是 user，
   而我们的循环在每轮工具执行后恰好以 `role="tool"` 结尾。真实 API 是否接受，
   只能实测，不能靠读文档推断。
4. **多轮稳定性** —— 连续两轮工具调用是否都能正常完成。

为什么值得单独写这个脚本：一次配置错误（Key 地域不匹配、模型名拼错、
region endpoint 写错）在批量评测里会表现为 30 个实例全部失败，
而那要花掉十几分钟和真金白银才发现。这里 20 秒就能定位。

用法：
    python scripts/preflight_model.py
    python scripts/preflight_model.py --model qwen3.7-flash-2026-07-15
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from code_agent.config import Settings  # noqa: E402
from code_agent.errors import LLMError  # noqa: E402
from code_agent.llm import OpenAICompatibleLLM  # noqa: E402

EVIDENCE_FUNCTION = {
    "type": "function",
    "function": {
        "name": "read_evidence",
        "description": "读取指定编号的证据条目。当你需要核对某个编号对应的事实内容时使用。",
        "parameters": {
            "type": "object",
            "properties": {
                "evidence_id": {"type": "integer", "description": "证据编号，例如 1"},
            },
            "required": ["evidence_id"],
        },
    },
}

EVIDENCE_TEXT = "证据 1：本项目的测试框架是 pytest，测试文件命名为 test_*.py。"


def _summarize(response) -> str:
    parts = []
    if response.content:
        parts.append(f"文本 {len(response.content)} 字")
    if response.tool_calls:
        names = ", ".join(f"{call.name}({call.arguments})" for call in response.tool_calls)
        parts.append(f"tool_calls=[{names}]")
    parts.append(f"stop={response.raw.get('choices', [{}])[0].get('finish_reason')}")
    usage = response.usage or {}
    if usage:
        parts.append(
            f"tokens={usage.get('prompt_tokens')}/{usage.get('completion_tokens')}"
        )
    return "　".join(parts)


def check(name: str, ok: bool, detail: str) -> bool:
    print(f"  [{'通过' if ok else '失败'}] {name}：{detail}")
    return ok


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="检查模型是否可用于本 Agent")
    parser.add_argument("--model", default=None, help="覆盖 LLM_MODEL")
    parser.add_argument("--base-url", default=None, help="覆盖 LLM_BASE_URL")
    args = parser.parse_args(argv)

    settings = Settings.from_env()
    if args.model:
        settings.model = args.model
    if args.base_url:
        settings.base_url = args.base_url

    print("配置")
    print(f"  base_url = {settings.base_url or '(未设置)'}")
    print(f"  model    = {settings.model or '(未设置)'}")
    print(f"  api_key  = {settings.masked_api_key}")
    print()

    if not settings.is_llm_configured:
        print("未配置完整的 LLM 凭据。请在 code-agent/.env 中填写：")
        print("  LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1")
        print("  LLM_MODEL=qwen3.7-flash")
        print("  LLM_API_KEY=sk-...")
        return 2

    client = OpenAICompatibleLLM(
        api_key=settings.api_key,
        base_url=settings.base_url,
        model=settings.model,
        temperature=settings.temperature,
        max_tokens=settings.llm_max_tokens,
        timeout=settings.request_timeout,
        max_retries=settings.max_retries,
    )

    passed = True
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": "你是一个严谨的助手，需要事实时必须调用工具核对。"},
        {"role": "user", "content": f"请用工具核对证据 1 的内容，然后用一句话复述它。{EVIDENCE_TEXT}"},
    ]

    print("1. 连通性与 Function Calling")
    started = time.monotonic()
    try:
        first = client.chat(messages, [EVIDENCE_FUNCTION])
    except LLMError as exc:
        check("请求发出", False, str(exc))
        print("\n结论：凭据或 base_url/model 有误，先修这里再谈其它。")
        return 1
    latency = time.monotonic() - started
    print(f"      耗时 {latency:.2f}s　{_summarize(first)}")
    passed &= check("请求发出", True, f"{latency:.2f}s")
    passed &= check(
        "返回了结构化 tool_calls",
        bool(first.tool_calls),
        f"{len(first.tool_calls)} 个" if first.tool_calls else "没有工具调用，模型可能不支持或 prompt 不够明确",
    )

    if not first.tool_calls:
        print("\n结论：模型没有发起工具调用。Function Calling 不可用的话，本 Agent 无法工作。")
        return 1

    print("\n2. 工具结果回灌（本循环的关键形状）")
    call = first.tool_calls[0]
    messages.append(
        {
            "role": "assistant",
            "content": first.content or "",
            "tool_calls": [call.to_message()],
        }
    )
    messages.append(
        {
            "role": "tool",
            "tool_call_id": call.id,
            "name": call.name,
            "content": f"[OK] {EVIDENCE_TEXT}",
        }
    )
    print(f"      消息序列以 role='{messages[-1]['role']}' 结尾，共 {len(messages)} 条")
    try:
        second = client.chat(messages, [EVIDENCE_FUNCTION])
    except LLMError as exc:
        passed &= check("接受 tool 消息结尾的序列", False, str(exc))
        print(
            "\n结论：该服务商不接受以 tool 消息结尾的对话。"
            "需要在 Agent 里加一层消息规范化（把 tool 结果合并进 user 消息），"
            "这是必须处理的兼容性问题，不是可以忽略的告警。"
        )
        return 1
    passed &= check("接受 tool 消息结尾的序列", True, _summarize(second))
    passed &= check(
        "基于工具结果给出了回答",
        bool(second.content and second.content.strip()),
        (second.content or "(空)")[:80],
    )

    print("\n3. 连续两轮工具调用")
    messages.append({"role": "assistant", "content": second.content or ""})
    messages.append({"role": "user", "content": "再核对一次证据 1，然后结束。"})
    try:
        third = client.chat(messages, [EVIDENCE_FUNCTION])
    except LLMError as exc:
        passed &= check("第二轮请求", False, str(exc))
    else:
        passed &= check("第二轮请求", True, _summarize(third))

    print()
    if passed:
        print("结论：模型可用于本 Agent。下一步可以跑：")
        print("  python scripts/run_eval.py run --variant A0 --instances 2")
        return 0
    print("结论：存在失败项，先修掉再跑评测。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

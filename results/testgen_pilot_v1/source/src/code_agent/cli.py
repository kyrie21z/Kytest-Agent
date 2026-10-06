"""命令行入口：交互模式 / `--print` / `--mode json`。

三种模式共用同一套 Agent 核心与同一套工具，差别只在"谁订阅事件、怎么渲染"：

    --print       跑一次就退出，最终回答写 stdout，过程写 stderr
    --mode json   每行一个事件的 JSONL，stdout 只放协议记录（供 harness 消费）
    无参数        交互式对话，Ctrl-C 中止当前运行、Ctrl-D 或 exit 退出

约定：
- 退出码 0 表示本次运行正常结束；LLM 失败或超时用 1，便于在脚本里判断。
- 无 API Key 时自动退回离线 Mock，保证"5 分钟可运行"这条要求在任何环境下成立。
"""
from __future__ import annotations

import argparse
import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Any, List, Optional, Sequence

# 以脚本方式直接运行（python src/code_agent/cli.py）时，包不在 sys.path 上。
# 这里补一次，让"零安装即可运行"成立——否则必须先 pip install -e . 才能用。
if __package__ in (None, ""):  # pragma: no cover - 仅脚本运行路径
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from .agent import Agent, RunResult
from .config import Settings
from .errors import ConfigError, ToolError
from .render import EventRenderer, JsonRenderer
from .session import SessionStore
from .tools.factories import available_tool_names, build_registry

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2

# 进程正常结束时这些状态算"成功"；其余在脚本里应当视为失败。
SUCCESS_STATUSES = {"completed", "stopped"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="code-agent",
        description="一个零依赖的编码 Agent：Agent 循环 + 工具调用 + 上下文记忆。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例：\n"
            "  code-agent                                 交互模式\n"
            '  code-agent --print "为 solution.py 生成单元测试"   单次运行\n'
            '  code-agent --mode json --print "解释这段代码" > events.jsonl\n'
            "  code-agent --mock                          无 API Key 的离线演示\n"
        ),
    )
    parser.add_argument("prompt", nargs="*", help="要执行的任务；留空则进入交互模式")
    parser.add_argument("-C", "--workspace", default=None, help="工作目录（默认当前目录）")
    parser.add_argument("-p", "--print", dest="print_mode", action="store_true",
                        help="跑一次就退出，只把最终回答写到 stdout")
    parser.add_argument("--mode", choices=("text", "json"), default="text",
                        help="输出模式：text（默认）或 json（逐行事件 JSONL）")
    parser.add_argument("-m", "--model", default=None, help="覆盖 LLM_MODEL")
    parser.add_argument("--base-url", default=None, help="覆盖 LLM_BASE_URL")
    parser.add_argument("-t", "--tools", default=None,
                        help=f"逗号分隔的工具白名单，可用：{', '.join(available_tool_names())}")
    parser.add_argument("--mock", action="store_true", help="强制使用离线 Mock，不发起网络请求")
    parser.add_argument("--test-generation", action="store_true",
                        help="为 solution.py 启用契约依据、逐条验证和增量保留测试（需要 pytest）")
    parser.add_argument("--execution-mode", choices=("sandbox", "trusted", "disabled"),
                        default=None, help="命令策略：默认 sandbox；trusted 仅用于受信本机代码")
    parser.add_argument("--no-session", action="store_true", help="不写会话轨迹文件")
    parser.add_argument("--session-dir", default=None, help="会话轨迹目录（默认 <workspace>/.sessions）")
    parser.add_argument("--max-turns", type=int, default=None, help="单次运行的 turn 上限")
    parser.add_argument("--max-tokens", type=int, default=None,
                        help="整个 run 的累计 token 预算，0 表示不限（不是单次输出上限）")
    parser.add_argument("--max-output-tokens", type=int, default=None,
                        help="单次请求的输出上限（服务端限制，默认取 LLM_MAX_TOKENS）")
    parser.add_argument("--max-context-chars", type=int, default=None, help="单次请求的上下文预算")
    parser.add_argument("-v", "--verbose", action="store_true", help="在 --print 模式下也显示中间过程")
    parser.add_argument("--no-env-file", action="store_true",
                        help="忽略 .env，只读进程环境变量（用于验证未配置凭据时的行为）")
    return parser


def resolve_settings(args: argparse.Namespace) -> Settings:
    workspace = Path(args.workspace).expanduser() if args.workspace else Path.cwd()
    settings = Settings.from_env(
        workspace=workspace, read_env_file=not getattr(args, "no_env_file", False)
    )
    if args.model:
        settings.model = args.model
    if getattr(args, "execution_mode", None):
        settings.execution_mode = args.execution_mode
    if args.base_url:
        settings.base_url = args.base_url
    if args.max_turns is not None:
        settings.max_steps = max(1, args.max_turns)
    if args.max_tokens is not None:
        settings.max_total_tokens = max(0, args.max_tokens)
    if getattr(args, "max_output_tokens", None) is not None:
        settings.llm_max_tokens = max(1, args.max_output_tokens)
    if args.max_context_chars is not None:
        settings.max_context_chars = max(1000, args.max_context_chars)
    if args.session_dir:
        settings.session_dir = Path(args.session_dir).expanduser()
    elif args.no_session:
        settings.session_dir = None
    return settings


def resolve_tools(args: argparse.Namespace) -> Optional[List[str]]:
    if not args.tools:
        return None
    names = [name.strip() for name in args.tools.split(",") if name.strip()]
    unknown = [name for name in names if name not in set(available_tool_names())]
    if unknown:
        raise ConfigError(
            f"未知工具：{', '.join(unknown)}。可用工具：{', '.join(available_tool_names())}"
        )
    return names


def build_llm(settings: Settings, force_mock: bool) -> tuple[Any, str]:
    """构造 LLM 客户端。返回 (客户端, 描述文本)。"""
    if not force_mock and settings.is_llm_configured:
        from .llm import OpenAICompatibleLLM

        client = OpenAICompatibleLLM(
            api_key=settings.api_key,
            base_url=settings.base_url,
            model=settings.model,
            temperature=settings.temperature,
            max_tokens=settings.llm_max_tokens,
            timeout=settings.request_timeout,
            max_retries=settings.max_retries,
        )
        return client, f"{settings.model} @ {settings.base_url}"

    from .llm import MockLLM

    reason = "（--mock）" if force_mock else "（未配置 LLM_API_KEY，自动退回离线模式）"
    return MockLLM(workspace=settings.workspace), f"离线 Mock {reason}"


def build_agent(
    args: argparse.Namespace,
    settings: Settings,
    on_event,
    *,
    session_enabled: bool = True,
) -> tuple[Agent, Optional[SessionStore], str]:
    llm, description = build_llm(settings, args.mock)
    registry = build_registry(settings, resolve_tools(args))
    finish_hook = None
    prompt = interactive_system_prompt(settings.workspace)
    if getattr(args, "test_generation", False):
        from .testgen import TESTGEN_PROMPT, SubmitTestsTool, make_testgen_hook
        if not settings.allow_write or not settings.allow_code_execution or settings.execution_mode == "disabled":
            raise ConfigError("--test-generation requires writing and code execution")
        tool = registry.get("submit_tests") or registry.register(SubmitTestsTool(settings))
        finish_hook = make_testgen_hook(tool)
        prompt = TESTGEN_PROMPT

    store: Optional[SessionStore] = None
    if session_enabled and settings.session_dir is not None:
        # 已知密钥原文传给脱敏器：工具输出（如读到的 .env、带凭据的响应）
        # 落盘前必须替换，轨迹文件不能变成凭据的持久化副本。
        known_secrets = [s for s in (settings.api_key,) if s]
        store = SessionStore.create(
            settings.session_dir,
            secrets=known_secrets,
            warn=lambda message: print(message, file=sys.stderr, flush=True),
        )
        store.write_header(
            workspace=settings.workspace,
            model=description,
            tools=registry.names(),
            mode="json" if args.mode == "json" else ("print" if args.print_mode else "interactive"),
        )

    def handle_event(event) -> None:
        on_event(event)
        if store is not None:
            store.record_event(event)

    agent = Agent(
        llm=llm,
        tools=registry,
        system_prompt=prompt,
        max_turns=settings.max_steps,
        max_total_tokens=settings.max_total_tokens,
        max_context_chars=settings.max_context_chars,
        on_event=handle_event,
        finish_turn=finish_hook,
    )
    return agent, store, description


def announce_fallback(settings: Settings, force_mock: bool, description: str) -> None:
    """退回离线模式时必须明确告知。

    否则用户看到一段通顺的中文回答，会以为那是真实模型的输出——
    这是最糟的一种失败：静默降级。
    """
    if force_mock:
        print("提示：已按 --mock 参数使用离线模式，不会发起网络请求。", file=sys.stderr)
    elif not settings.is_llm_configured:
        print(
            "提示：未配置 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL，已自动退回离线 Mock 模式。"
            "配置后即可获得真实模型回答（参见 .env.example）。",
            file=sys.stderr,
        )
    elif "离线" in description:
        print(f"提示：当前使用 {description}", file=sys.stderr)


def interactive_system_prompt(workspace: Path) -> str:
    """通用编码 Agent 的系统提示。

    刻意保持通用：不提测试、不提覆盖率、不指定流程。作业里的 A0 就是这个提示，
    A1 及以后的变体才会在这里加入测试专用知识。若在这里写死"必须运行 pytest"，
    反事实对照就失效了。
    """
    return (
        "You are a coding agent. Inspect the workspace and complete the requested "
        "software engineering task using the available tools.\n"
        f"The workspace root is: {workspace}\n"
        "Prefer reading the real code before making claims about it. "
        "When you need to know whether something works, run it with run_command "
        "instead of guessing."
    )


# ----------------------------------------------------------------------
# 三种模式
# ----------------------------------------------------------------------
def run_print(args: argparse.Namespace, settings: Settings) -> int:
    task = " ".join(args.prompt).strip()
    if not task:
        print("错误：--print 需要一个任务描述，例如 code-agent --print \"解释 solution.py\"", file=sys.stderr)
        return EXIT_USAGE

    if args.mode == "json":
        renderer = JsonRenderer(sys.stdout)
    else:
        # 过程信息写 stderr，保证 stdout 只有最终回答（可以安全地重定向）
        renderer = EventRenderer(stream=sys.stdout, verbose=args.verbose, progress=sys.stderr)

    agent, store, description = build_agent(
        args, settings, renderer, session_enabled=not args.no_session
    )
    announce_fallback(settings, args.mock, description)
    agent.state.add_user(task)
    if store is not None:
        store.record_user(task)

    agent.begin_task()  # 新任务：预算从本任务重新计量
    result = agent.run()
    if store is not None:
        store.record_result(result)

    if args.mode == "json":
        submitter = agent.tools.get("submit_tests")
        return EXIT_FAILED if args.test_generation and not submitter.accepted else _exit_code(result)

    if result.final_text:
        print(result.final_text)
    elif result.error:
        print(f"运行失败：{result.error}", file=sys.stderr)
    _print_summary(result)
    submitter = agent.tools.get("submit_tests")
    if args.test_generation and not submitter.accepted:
        print("未生成通过逐条验证的测试；诊断见 testgen_report.json。", file=sys.stderr)
        return EXIT_FAILED
    return _exit_code(result)


def run_interactive(args: argparse.Namespace, settings: Settings) -> int:
    _enable_line_editing()
    renderer = EventRenderer(stream=sys.stdout, verbose=True)
    agent, store, description = build_agent(
        args, settings, renderer, session_enabled=not args.no_session
    )
    announce_fallback(settings, args.mock, description)

    print("Code Agent 交互模式")
    print(f"  工作目录：{settings.workspace}")
    print(f"  模型：{description}")
    print(f"  工具：{', '.join(agent.tools.names())}")
    print(f"  轨迹：{store.path if store else '（未启用）'}")
    print("  输入任务后回车执行；exit / quit 退出，Ctrl-C 中止当前运行。\n")

    while True:
        try:
            line = input("› ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line.lower() in {"exit", "quit", ":q"}:
            break

        agent.state.add_user(line)
        if store is not None:
            store.record_user(line)
        agent.begin_task()  # 新任务：预算从本任务重新计量（会话历史保留，预算不跨任务累计）
        try:
            result = agent.run()
        except KeyboardInterrupt:
            # 用户在运行中按 Ctrl-C：请求中止并等本轮收尾，而不是丢掉整个会话。
            # 中断恢复是**同一个任务**的继续，不再重置预算基线。
            agent.abort()
            result = agent.run()
        if store is not None:
            store.record_result(result)

        if result.final_text:
            print(f"\n{result.final_text}\n")
        elif result.error:
            print(f"\n运行失败：{result.error}\n", file=sys.stderr)
        _print_summary(result)

    if store is not None:
        summary = store.summary()
        if summary.get("write_errors"):
            print(
                f"轨迹不完整：{summary['write_errors']} 条记录写入失败"
                f"（{store.last_write_error}），完整内容仅在内存中。",
                file=sys.stderr,
            )
        else:
            print(f"轨迹已保存：{summary['path']}")
    return EXIT_OK


# ----------------------------------------------------------------------
# 辅助
# ----------------------------------------------------------------------
def _exit_code(result: RunResult) -> int:
    return EXIT_OK if result.status in SUCCESS_STATUSES else EXIT_FAILED


def _print_summary(result: RunResult) -> None:
    print(
        f"[{result.status}] turns={result.turns} llm_calls={result.llm_calls} "
        f"tool_calls={result.tool_calls} tool_errors={result.tool_errors} "
        f"tokens={result.total_tokens} runtime={result.runtime_sec:.2f}s",
        file=sys.stderr,
    )


def _enable_line_editing() -> None:
    """启用行编辑（上下键翻历史）。

    必须先 `find_spec` 再 `import`：这两个模块的**导入副作用**才是目的，
    直接导入会被静态检查判定为"未使用的导入"。
    标准库 `readline` 在 Windows 上不可用，退而尝试 `pyreadline3`；
    两者都没有时交互模式仍然可用，只是没有历史记录。
    """
    for name in ("readline", "pyreadline3"):
        try:
            if importlib.util.find_spec(name) is None:
                continue
            importlib.import_module(name)
            return
        except (ImportError, ValueError):
            continue


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        settings = resolve_settings(args)
    except (ConfigError, ToolError, OSError, SyntaxError) as exc:
        print(f"配置错误：{exc}", file=sys.stderr)
        return EXIT_USAGE

    if not settings.workspace.is_dir():
        print(f"工作目录不存在：{settings.workspace}", file=sys.stderr)
        return EXIT_USAGE

    try:
        if args.print_mode or args.mode == "json":
            return run_print(args, settings)
        return run_interactive(args, settings)
    except (ConfigError, ToolError, OSError, SyntaxError) as exc:
        print(f"配置错误：{exc}", file=sys.stderr)
        return EXIT_USAGE
    except KeyboardInterrupt:
        print("\n已中断。", file=sys.stderr)
        return EXIT_FAILED


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

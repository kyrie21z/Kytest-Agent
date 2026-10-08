"""批量运行器：把 Agent 放到固定实例上跑，采集协议规定的指标。

三个必须做对的地方：

1. **断点续跑**。30 个实例 × N 个变体要跑几十分钟，中途崩溃或手动中断是常态。
   每个实例的结果在跑完时立刻写成独立 JSON 文件，重跑时自动跳过已完成的，
   而不是从头再来。这是"实验能在有限时间里迭代"的前提。
2. **并发**。Agent 运行几乎全在等网络，评测在等子进程，用线程池并发跑实例
   能把墙钟压缩数倍。同步阻塞 + 线程池在这里比 asyncio 简单得多。
3. **每个实例的状态独立**。一个实例抛异常不能影响另一个。异常被捕获后写成
   结构化的失败记录（`eval_error`），仍然计入分母（协议 §5 的 ITT 原则）。
"""
from __future__ import annotations

import json
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from code_agent.agent import Agent, RunResult, TurnDecision  # noqa: E402
from code_agent.assembly import AgentPolicy, GENERAL_PROMPT, create_agent  # noqa: E402
from code_agent.config import Settings  # noqa: E402
from code_agent.tools.factories import GENERAL_TOOL_NAMES, build_registry  # noqa: E402

from .dataset import Instance  # noqa: E402
from .metrics import collect_metrics  # noqa: E402
from .workspace import prepare_workspace  # noqa: E402

# 协议 §3 冻结的 checkpoint。1 能立刻看到"有没有产出"，8 是预算上限。
CHECKPOINTS: tuple = (1, 2, 4, 8)

# 任务提示（协议 §1 冻结）。所有变体完全一致——变体只能改 system prompt、
# 工具集与编排策略。这里多一个字都会让主表失去可比性。
TASK_PROMPT = (
    "Generate unit tests for solution.py in the current directory.\n"
    "Write them to test_solution.py using pytest.\n"
)


@dataclass
class Variant:
    """一个实验条件。

    A0 就是"什么都没加"的那一档：通用 system prompt + 通用工具集。
    A1 及以后通过覆盖这些字段来实现，不改动 Agent 循环本身。

    注意 `llm_max_tokens` 与 `max_total_tokens` 是两件不同的事：
    前者是**单次请求的输出上限**（服务端会校验范围，0 会被拒绝），
    后者是**整个 run 的累计 token 预算**（0 表示不限）。
    把两者混成一个字段，会让"不限预算"变成"输出上限为 0"从而请求必然失败。
    """

    name: str
    description: str = ""
    system_prompt: Optional[str] = None
    tool_names: Sequence[str] = field(default_factory=lambda: tuple(GENERAL_TOOL_NAMES))
    # 预算取值见协议 §8 修订 1（2026-10-06）：A2 一轮修复、A3 全流程的自然循环
    # 在 8 turns/2048 输出上限下会被预算饿死——触顶的 run 只能计入部分质量，
    # 会把"机制无效"和"机制被饿死"混为一谈。checkpoint {1,2,4,8} 不变，
    # 曲线可比较性由测量点保证，与预算上限解耦。
    max_turns: int = 12
    llm_max_tokens: int = 4096
    max_total_tokens: int = 0
    # 系统编排预算（A2/A3 的 finish_turn 钩子，见 eval/hooks.py）。
    # system_runs_cap=0 表示无编排（A0/A1：模型自发决定是否运行测试）。
    # coverage_rounds_cap>0 使 A2 的"通过即收尾"升级为 A3 的"通过后定向补测"。
    system_runs_cap: int = 0
    coverage_rounds_cap: int = 0

    def resolve_system_prompt(self) -> str:
        if self.system_prompt:
            return self.system_prompt
        return GENERAL_PROMPT

    def agent_policy(self) -> AgentPolicy:
        return AgentPolicy(self.resolve_system_prompt(), tuple(self.tool_names),
                           validate_tests="submit_tests" in self.tool_names)


def default_variant(name: str = "A0") -> Variant:
    """按名字返回变体。变体差异只允许落在 Variant 字段上，循环本身只有一份。"""
    if name == "A0":
        return Variant(name=name, description="通用编码 Agent（无测试专用编排）")
    if name == "A1":
        return Variant(
            name=name,
            description="测试感知 Prompting（A0 + 测试知识与规划要求）",
            system_prompt=A1_SYSTEM_PROMPT,
        )
    if name == "A2":
        return Variant(
            name=name,
            description="执行反馈（A1 + 系统 pytest 编排与结构化失败回灌）",
            system_prompt=A1_SYSTEM_PROMPT,
            system_runs_cap=4,
        )
    if name == "A3":
        return Variant(
            name=name,
            description="覆盖率反馈（A2 + 未覆盖行定向补测）",
            system_prompt=A1_SYSTEM_PROMPT,
            system_runs_cap=4,
            coverage_rounds_cap=2,
        )
    if name in {"A4", "A5"}:
        policy = AgentPolicy.test_generation(feedback=name == "A5")
        description = ("契约依据 + 逐测试验证 + 增量保留" if name == "A4" else
                       "A4 + 开发故障反馈（独立评分池）")
        return Variant(name=name, description=description,
                       system_prompt=policy.system_prompt, tool_names=policy.tool_names)
    raise KeyError(f"未知变体 `{name}`")


# A1 的增量只有 prompt：在 A0 的通用提示之上追加测试知识与"先规划后写"的要求
# （开发计划 §5.1）。任务提示（user message）保持冻结不变；工具、预算与循环
# 与 A0 完全一致——A1 − A0 必须只能归因到这段文本。
A1_SYSTEM_PROMPT = (
    GENERAL_PROMPT + "\n\n"
    "You are writing unit tests. Before writing the test file, plan the cases "
    "explicitly, covering:\n"
    "1. Normal cases with typical inputs.\n"
    "2. Boundary cases at the edges of valid input ranges.\n"
    "3. Empty, null, or zero-size inputs.\n"
    "4. Invalid inputs, if the function documents or implies input constraints.\n"
    "5. Exception cases, if the function can raise.\n"
    "\n"
    "Every test must assert the exact expected output for its input (the test "
    "oracle), not merely that the call runs without error. Derive expected values "
    "from the documented behavior of the function."
)


@dataclass
class RunOutcome:
    """一个实例 × 一个变体的完整结果。字段与结果 JSON 一一对应。"""

    instance_id: str
    variant: str
    status: str = "unknown"
    agent: Dict[str, Any] = field(default_factory=dict)
    checkpoints: List[Dict[str, Any]] = field(default_factory=list)
    final: Dict[str, Any] = field(default_factory=dict)
    tests_source: str = ""
    error: str = ""
    environment: Dict[str, Any] = field(default_factory=dict)
    network_attempt: bool = False
    # Agent 是否改写过 solution.py。测量前会恢复原始实现——否则"改实现迁就测试"
    # 会同时虚增通过率与杀伤率（变异体是针对原始实现生成的）。标志供失败分类。
    solution_modified: bool = False
    started_at: float = 0.0
    duration_sec: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "variant": self.variant,
            "status": self.status,
            "agent": self.agent,
            "checkpoints": self.checkpoints,
            "final": self.final,
            "error": self.error,
            "environment": self.environment,
            "network_attempt": self.network_attempt,
            "solution_modified": self.solution_modified,
            "tool_trace": self.agent.get("tool_trace", []),
            "started_at": self.started_at,
            "duration_sec": round(self.duration_sec, 3),
            # 测试源码只保留在独立文件里，避免结果 JSON 膨胀（见 runner 的写盘逻辑）
            "tests_chars": len(self.tests_source),
        }


# 联网类命令的迹象。协议 §4 不封禁这些命令（那会破坏 A0 的通用性），
# 而是事后统计——若某变体的联网比例异常，其结果需要单独说明。
_NETWORK_MARKERS = ("curl", "wget", "pip install", "pip3 install", "git clone", "urllib", "requests.get")


def _detect_network_attempt(registry) -> bool:
    """检查 Agent 是否尝试过联网。"""
    for name, arguments in getattr(registry, "executed", []):
        if name != "run_command":
            continue
        command = str(arguments.get("command") or "").lower()
        if any(marker in command for marker in _NETWORK_MARKERS):
            return True
    return False


def _tool_trace(events: Sequence[Any], limit: int = 60) -> List[Dict[str, Any]]:
    """把工具调用压成紧凑日志。

    **没有这个，失败分类就只是猜测。** 只说"某实例有 6 次工具错误"没有诊断价值；
    要知道错在哪里，就必须留下"调用了什么、报了什么"。

    只保留首行摘要与参数预览，完整输出仍在会话轨迹里——结果 JSON 不能被日志撑爆。
    """
    from code_agent.agent.events import ToolCallEnd, ToolCallStart

    starts: Dict[str, Dict[str, Any]] = {}
    trace: List[Dict[str, Any]] = []
    for event in events:
        if isinstance(event, ToolCallStart):
            starts[event.id] = event
        elif isinstance(event, ToolCallEnd):
            start = starts.get(event.id)
            first_line = ""
            for line in (event.content or "").splitlines():
                if line.strip():
                    first_line = line.strip()[:200]
                    break
            arguments = dict(getattr(start, "arguments", {}) or {}) if start else {}
            preview = {
                key: (value[:80] + "…" if isinstance(value, str) and len(value) > 80 else value)
                for key, value in arguments.items()
            }
            trace.append(
                {
                    "turn": event.turn,
                    "name": event.name,
                    "is_error": event.is_error,
                    "duration_sec": round(event.duration_sec, 3),
                    "arguments": preview,
                    "first_line": first_line,
                }
            )
            if len(trace) >= limit:
                break
    return trace


def _recording_registry(settings: Settings, tool_names: Sequence[str]):
    """包一层注册表以记录调用，用于事后核对 Agent 的实际行为。"""
    from code_agent.tools.base import ToolRegistry

    inner = build_registry(settings, tool_names)

    class Recording(ToolRegistry):
        def __init__(self) -> None:
            super().__init__()
            for tool in inner.tools:
                self.register(tool)
            self.executed: List[tuple] = []

        def execute(self, name: str, arguments: Dict[str, Any]):
            self.executed.append((name, arguments))
            return super().execute(name, arguments)

    return Recording()


def environment_snapshot() -> Dict[str, Any]:
    """记录环境快照。复现的前提是知道当时用的什么。"""
    import platform

    def version_of(module: str) -> str:
        try:
            return str(getattr(__import__(module), "__version__", "unknown"))
        except ImportError:
            return "missing"

    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "pytest": version_of("pytest"),
        "coverage": version_of("coverage"),
    }


def run_single(
    instance: Instance,
    variant: Variant,
    *,
    run_root: Path,
    settings_factory: Callable[[Path], Settings],
    agent_factory: Optional[Callable[[Variant, Settings, Any, Path], Agent]] = None,
    checkpoints: Sequence[int] = CHECKPOINTS,
    max_mutants: int = 20,
    wall_clock_limit: float = 300.0,
    keep_tests: bool = True,
    defer_measurement: bool = False,
    measurement_timeouts: Optional[tuple] = None,
    mutation_operators: Optional[Sequence[str]] = None,
) -> RunOutcome:
    """在一个实例上运行一个变体，并在每个 checkpoint 采集指标。

    Args:
        settings_factory: 由工作区路径构造 Settings。评测层需要自己控制
            `allow_code_execution` 等开关，所以不在这里写死。
        agent_factory: 允许接入自定义 Agent（例如脚本化 LLM 的离线运行）。
            默认构造真实 Agent。
    """
    started = time.time()
    workspace = prepare_workspace(instance, run_root / variant.name / instance.instance_id)
    outcome = RunOutcome(
        instance_id=instance.instance_id,
        variant=variant.name,
        started_at=started,
        environment=environment_snapshot(),
    )
    from .metrics import MEASUREMENT_VERSION
    outcome.environment["measurement_version"] = MEASUREMENT_VERSION

    settings = settings_factory(workspace)
    if variant.name == "A5":
        from code_agent.fault_feedback import HELDOUT_OPERATORS, independent_pools
        independent_pools(instance.solution_source, scoring_limit=max_mutants)
        if mutation_operators is not None and set(mutation_operators) != set(HELDOUT_OPERATORS):
            raise ValueError("A5 scoring must use the held-out operator families")
        mutation_operators = HELDOUT_OPERATORS
    if mutation_operators is not None:
        outcome.environment["mutation_operators"] = list(mutation_operators)
    from .mutation import generate_mutants
    outcome.environment["reference_mutants_total"] = len(generate_mutants(instance.solution_source, max_mutants=max_mutants, operators=mutation_operators))
    settings.max_steps = variant.max_turns
    settings.llm_max_tokens = variant.llm_max_tokens
    settings.max_total_tokens = variant.max_total_tokens
    registry = _recording_registry(settings, variant.tool_names)

    events: List[Any] = []
    result: Optional[RunResult] = None
    metrics: Any = None
    timed_out = False
    finish_hook = None
    generation_started = 0.0
    generation_finished = 0.0
    # Agent 的构造也必须在 try 里：工厂可能因为 LLM 客户端配置错误而抛异常，
    # 构造期的异常和运行期的异常一样，只应该让这一个实例失败，不能让整批倒下。
    agent: Optional[Agent] = None

    try:
        if agent_factory is None:
            # A2/A3 的系统编排钩子：预算>0 时启用（A0/A1 为 None，模型自发验证）
            finish_hook = None
            if variant.system_runs_cap > 0:
                from .hooks import make_guided_hook

                finish_hook = make_guided_hook(
                    workspace,
                    instance.solution_source,
                    max_pytest_runs=variant.system_runs_cap,
                    max_coverage_rounds=variant.coverage_rounds_cap,
                )
            agent = create_agent(settings, variant.agent_policy(), registry=registry,
                                 finish_turn=finish_hook, on_event=events.append)
            finish_hook = agent.finish_turn
            if defer_measurement:
                policy_hook = finish_hook
                def bounded_hook(agent, outcome):
                    decision = policy_hook(agent, outcome) if policy_hook else None
                    if time.monotonic() - generation_started >= wall_clock_limit:
                        return TurnDecision(end=True, reason="generation_timeout")
                    return decision
                bounded_hook.state = getattr(policy_hook, "state", None)
                finish_hook = bounded_hook
                agent.finish_turn = bounded_hook
        else:
            agent = agent_factory(variant, settings, registry, workspace)

        agent.state.add_user(TASK_PROMPT)
        # 一个实例 = 一个任务：预算基线在此建立，checkpoint 的多次 run_until
        # 共享同一基线（任务内累计语义不变）。
        agent.begin_task()
        generation_started = time.monotonic()
        deadline = started + wall_clock_limit
        ended = False

        for checkpoint in (() if defer_measurement else sorted(checkpoints)):
            if time.time() > deadline:
                timed_out = True
                break
            result = agent.run_until(checkpoint)
            # checkpoint 处只测便宜的两层（协议 §3）。变异测试成本高一个数量级，
            # 只在最终采集，否则 30 实例 × 4 checkpoint 会把预算烧在重复测量上。
            metrics = collect_metrics(
                instance, workspace, checkpoint, include_mutation=False, max_mutants=max_mutants
            )
            outcome.checkpoints.append(metrics.to_dict())
            if result.status not in ("paused",):
                # run 已经结束：自然完成、钩子 end、或 abort。绝不能再拉起下一段——
                # 否则钩子的 end 决定会被"顺手"的 agent.run() 覆盖成 completed，
                # 白烧一次 LLM 调用。
                ended = True
                break

        if not timed_out and not ended:
            result = agent.run()
        generation_finished = time.monotonic()
        if defer_measurement:
            timed_out = generation_finished - generation_started >= wall_clock_limit

        metrics = collect_metrics(
            instance, workspace, checkpoint=0, include_mutation=True, max_mutants=max_mutants,
            mutation_operators=mutation_operators,
            **(dict(zip(("pytest_timeout", "coverage_timeout", "mutant_timeout"), measurement_timeouts)) if measurement_timeouts else {})
        )
        # 每次采集的入口都会核查 solution.py 是否被改写过（见 collect_metrics）；
        # 任意一轮发现即置位——该行为是失败分类的一类，必须可见。
        outcome.solution_modified = metrics.solution_modified or any(
            item.get("solution_modified") for item in outcome.checkpoints
        )
        submitter = registry.get("submit_tests")
        outcome.solution_modified |= bool(getattr(submitter, "sut_restorations", 0)) or any(
            a.get("solution_restored") for a in getattr(getattr(finish_hook, "state", None), "actions", []))
        metrics.solution_modified = outcome.solution_modified
        if outcome.solution_modified and metrics.mutants_total:
            metrics.mutation_score = 0.0
            metrics.mutation_upper_bound = 0.0
            metrics.mutation_status = "solution_modified"
        outcome.final = metrics.to_dict()
        outcome.status = _resolve_status(result, timed_out, metrics)
    except Exception:  # noqa: BLE001 - 单实例异常不能让整批实验倒下
        outcome.status = "eval_error"
        outcome.error = traceback.format_exc(limit=6)
    finally:
        state = getattr(agent, "state", None)
        # 钩子以 end 收尾时，core 把 TurnDecision.reason 塞进 RunResult.error；
        # 良性收尾原因在这里归位成 None，避免结果 JSON 里出现"成功性错误"。
        _BENIGN_STOP_REASONS = {"tests_passed", "coverage_full", "development_targets_exhausted", "development_budget_exhausted", "development_no_progress"}
        agent_error = getattr(result, "error", None) if result else None
        if agent_error in _BENIGN_STOP_REASONS:
            agent_error = None
        outcome.agent = {
            "status": getattr(result, "status", "unknown") if result else "unknown",
            # turns 必须取累计值 `state.turn_index`，不能取 `RunResult.turns`：
            # 后者是"本次调用跑了几个 turn"，而 checkpoint 循环会多次调用 run_until，
            # 每次的返回值都覆盖上一次——`paused` 时它甚至是 0。
            # 用错来源会让报告显示 turns=0，而实例实际跑了 8 个 turn。
            "turns": getattr(state, "turn_index", 0),
            "llm_calls": getattr(state, "llm_calls", 0),
            "tool_calls": getattr(state, "tool_calls", 0),
            "tool_errors": getattr(state, "tool_errors", 0),
            "tool_calls_skipped": getattr(state, "tool_calls_skipped", 0),
            "input_tokens": getattr(getattr(state, "usage", None), "input_tokens", 0),
            "output_tokens": getattr(getattr(state, "usage", None), "output_tokens", 0),
            "total_tokens": getattr(getattr(state, "usage", None), "total_tokens", 0),
            "final_text": getattr(result, "final_text", "") if result else "",
            "error": agent_error,
            "stop_reason": getattr(result, "error", None) if result else None,
            "system_actions": list(getattr(getattr(finish_hook, "state", None), "actions", [])),
            "tool_trace": _tool_trace(events),
        }
        if defer_measurement and generation_started:
            outcome.agent["generation_seconds"] = round((generation_finished or time.monotonic()) - generation_started, 3)
            outcome.agent["measurement_deferred"] = True
        submitter = registry.get("submit_tests")
        if submitter is not None:
            outcome.agent["testgen"] = {
                "accepted": list(submitter.accepted.values()), "attempts": submitter.attempts,
                "subprocess_runs": submitter.subprocess_runs,
                "validation_seconds": round(submitter.validation_seconds, 3),
                "quality_actions": submitter.quality_actions,
            }
        inspector = registry.get("inspect_survivors")
        if inspector is not None:
            outcome.agent["fault_feedback"] = inspector.actions
        outcome.network_attempt = _detect_network_attempt(registry)
        outcome.duration_sec = time.time() - started

        from .workspace import read_tests

        outcome.tests_source = read_tests(workspace) if keep_tests else ""

    return outcome


def _resolve_status(result: Optional[RunResult], timed_out: bool, metrics) -> str:
    """把 Agent 运行状态与测量结果合成协议 §5 的单一状态字段。"""
    if timed_out:
        return "timeout"
    if not metrics.has_tests:
        return "no_tests"
    if metrics.pytest.process.timed_out:
        return "reference_timeout"
    if not metrics.pytest.import_ok:
        return "import_error"
    if not metrics.pytest.all_pass:
        return "partial_pass"
    agent_status = getattr(result, "status", "")
    if agent_status == "llm_error":
        return "llm_error"
    if agent_status == "max_turns":
        return "max_turns"
    return "all_pass"


def run_batch(
    instances: Sequence[Instance],
    variants: Sequence[Variant],
    *,
    output_dir: Path,
    settings_factory: Callable[[Path], Settings],
    agent_factory: Optional[Callable[[Variant, Settings, Any, Path], Agent]] = None,
    checkpoints: Sequence[int] = CHECKPOINTS,
    max_mutants: int = 20,
    concurrency: int = 4,
    resume: bool = True,
    wall_clock_limit: float = 300.0,
    on_result: Optional[Callable[[RunOutcome], None]] = None,
    mutation_operators: Optional[Sequence[str]] = None,
) -> List[RunOutcome]:
    """批量运行。按 (variant, instance) 展开任务，支持续跑与并发。"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if any(v.name == "A5" for v in variants):
        from code_agent.fault_feedback import HELDOUT_OPERATORS
        if mutation_operators is not None and set(mutation_operators) != set(HELDOUT_OPERATORS):
            raise ValueError("A5 comparisons must use the held-out scoring families for every condition")
        mutation_operators = HELDOUT_OPERATORS
    from .mutation import default_operators
    expected_pool = set(mutation_operators or default_operators())
    from .metrics import MEASUREMENT_VERSION
    for saved in output_dir.glob("*/*.json"):
        payload = json.loads(saved.read_text(encoding="utf-8"))
        saved_version = payload.get("environment", {}).get("measurement_version") or payload.get("final", {}).get("measurement_version")
        if saved_version != MEASUREMENT_VERSION:
            raise ValueError("Measurement version changed; use a new output directory")
        saved_pool = payload.get("environment", {}).get("mutation_operators") or default_operators()
        if set(saved_pool) != expected_pool:
            raise ValueError("Saved scoring pool differs; use a new output directory")
    if mutation_operators is not None and (output_dir / "official_baseline.json").exists():
        raise ValueError("Existing official baseline has no matching scoring-pool receipt; use a new output directory")
    jobs = [(variant, instance) for variant in variants for instance in instances]

    pending = []
    for variant, instance in jobs:
        target = _result_path(output_dir, variant.name, instance.instance_id)
        if resume and target.exists():
            continue
        pending.append((variant, instance))

    skipped = len(jobs) - len(pending)
    print(f"共 {len(jobs)} 个任务，跳过已完成 {skipped} 个，本次执行 {len(pending)} 个")
    if not pending:
        return load_results(output_dir)

    completed: List[RunOutcome] = []
    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as pool:
        futures = {
            pool.submit(
                run_single,
                instance,
                variant,
                run_root=output_dir / "workspaces",
                settings_factory=settings_factory,
                agent_factory=agent_factory,
                checkpoints=checkpoints,
                max_mutants=max_mutants,
                wall_clock_limit=wall_clock_limit,
                mutation_operators=mutation_operators,
            ): (variant, instance)
            for variant, instance in pending
        }
        for future in as_completed(futures):
            variant, instance = futures[future]
            try:
                outcome = future.result()
            except Exception:  # noqa: BLE001 - 兜底，保证批处理继续
                outcome = RunOutcome(
                    instance_id=instance.instance_id,
                    variant=variant.name,
                    status="eval_error",
                    error=traceback.format_exc(limit=6),
                    environment={"mutation_operators": list(mutation_operators)} if mutation_operators is not None else {},
                )
            from .mutation import generate_mutants
            outcome.environment.setdefault("measurement_version", MEASUREMENT_VERSION)
            outcome.environment.setdefault("reference_mutants_total", len(generate_mutants(instance.solution_source, max_mutants=max_mutants, operators=mutation_operators)))
            write_result(output_dir, outcome)
            completed.append(outcome)
            print(
                f"  [{outcome.status:<13}] {variant.name}/{instance.instance_id:<16} "
                f"turns={outcome.agent.get('turns', 0):<3} "
                f"cov={outcome.final.get('line_coverage', 0):.0%} "
                f"mut={outcome.final.get('mutation_score')} "
                f"{outcome.duration_sec:.0f}s"
            )
            if on_result is not None:
                on_result(outcome)

    return load_results(output_dir)


# ----------------------------------------------------------------------
# 结果读写
# ----------------------------------------------------------------------
def _result_path(output_dir: Path, variant: str, instance_id: str) -> Path:
    safe = instance_id.replace("/", "__")
    return Path(output_dir) / variant / f"{safe}.json"


def write_result(output_dir: Path, outcome: RunOutcome) -> Path:
    """写结果。每个实例一个文件——这就是断点续跑的实现方式。"""
    target = _result_path(Path(output_dir), outcome.variant, outcome.instance_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(outcome.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if outcome.tests_source:
        target.with_suffix(".tests.py").write_text(outcome.tests_source, encoding="utf-8")
    return target


def load_results(output_dir: Path) -> List[RunOutcome]:
    """读回全部结果。字段缺失时用默认值补齐，便于协议演进后仍能汇总旧数据。"""
    outcomes: List[RunOutcome] = []
    for path in sorted(Path(output_dir).glob("*/*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        outcome = RunOutcome(
            instance_id=payload.get("instance_id", path.stem),
            variant=payload.get("variant", path.parent.name),
        )
        outcome.status = payload.get("status", "unknown")
        outcome.agent = payload.get("agent") or {}
        outcome.checkpoints = payload.get("checkpoints") or []
        outcome.final = payload.get("final") or {}
        outcome.error = payload.get("error", "")
        outcome.environment = payload.get("environment") or {}
        outcome.network_attempt = bool(payload.get("network_attempt"))
        outcome.started_at = float(payload.get("started_at") or 0.0)
        outcome.duration_sec = float(payload.get("duration_sec") or 0.0)
        tests_path = path.with_suffix(".tests.py")
        if tests_path.exists():
            outcome.tests_source = tests_path.read_text(encoding="utf-8", errors="replace")
        outcomes.append(outcome)
    return outcomes

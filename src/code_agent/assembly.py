"""Agent assembly shared by CLI, Web and evaluation adapters.

Policies describe prompt, tools and validation explicitly. Entry-point defaults,
session storage, wall-clock limits and measurements stay with their adapters.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Sequence

from .agent import Agent
from .config import Settings
from .errors import ConfigError
from .tools.factories import GENERAL_TOOL_NAMES, build_registry

GENERAL_PROMPT = (
    "You are a coding agent. Inspect the workspace and complete the requested "
    "software engineering task using the available tools."
)


@dataclass(frozen=True)
class AgentPolicy:
    system_prompt: str
    tool_names: Sequence[str] = GENERAL_TOOL_NAMES
    validate_tests: bool = False

    @classmethod
    def test_generation(cls, *, feedback: bool = False,
                        tool_names: Optional[Sequence[str]] = None) -> AgentPolicy:
        from .testgen import TESTGEN_PROMPT
        names = tuple(tool_names) if tool_names is not None else GENERAL_TOOL_NAMES
        prompt = TESTGEN_PROMPT
        required = ("submit_tests",)
        if feedback:
            from .fault_feedback import FAULT_PROMPT
            prompt += FAULT_PROMPT
            required += ("inspect_survivors",)
        return cls(prompt, tuple(dict.fromkeys((*names, *required))), validate_tests=True)

    @classmethod
    def interactive(cls, settings: Settings, tool_names: Optional[Sequence[str]] = None,
                    *, test_generation: bool = False, fault_feedback: bool = False) -> AgentPolicy:
        names = tuple(tool_names) if tool_names is not None else GENERAL_TOOL_NAMES
        if "inspect_survivors" in names and "submit_tests" not in names:
            raise ConfigError("inspect_survivors requires submit_tests in --tools")
        if test_generation or fault_feedback:
            if not settings.allow_write or not settings.allow_code_execution or settings.execution_mode == "disabled":
                raise ConfigError("--test-generation requires writing and code execution")
            return cls.test_generation(feedback=fault_feedback, tool_names=names)
        prompt = (
            GENERAL_PROMPT + "\n"
            f"The workspace root is: {settings.workspace}\n"
            "Prefer reading the real code before making claims about it. "
            "When you need to know whether something works, run it with run_command "
            "instead of guessing."
        )
        return cls(prompt, names)


def build_llm(settings: Settings, force_mock: bool = False) -> tuple[Any, str]:
    """Construct a client without making requests; describe explicit/offline selection."""
    from .llm import MockLLM, OpenAICompatibleLLM
    if not force_mock and settings.is_llm_configured:
        client = OpenAICompatibleLLM(
            api_key=settings.api_key, base_url=settings.base_url, model=settings.model,
            temperature=settings.temperature, max_tokens=settings.llm_max_tokens,
            timeout=settings.request_timeout, max_retries=settings.max_retries,
        )
        return client, f"{settings.model} @ {settings.base_url}"
    reason = "（--mock）" if force_mock else "（未配置 LLM_API_KEY，自动退回离线模式）"
    return MockLLM(workspace=settings.workspace), f"离线 Mock {reason}"


def create_agent(settings: Settings, policy: AgentPolicy, *, llm=None, registry=None,
                 finish_turn=None, on_event=None) -> Agent:
    """Assemble dependencies once; supplied clients/registries retain their identity.

    Tool presence alone never enables test validation. Evaluation opts in through
    its policy; CLI custom tool lists keep their existing generic prompt and hook.
    A validation policy takes precedence over a guided hook, as in evaluation.
    """
    registry = registry if registry is not None else build_registry(settings, policy.tool_names)
    if policy.validate_tests:
        tool = registry.get("submit_tests")
        if tool is None:
            raise ConfigError("Test-generation policy requires submit_tests")
        finish_turn = tool.generation.finish_turn
    return Agent(
        llm=llm if llm is not None else build_llm(settings)[0],
        tools=registry, system_prompt=policy.system_prompt,
        max_turns=settings.max_steps, max_total_tokens=settings.max_total_tokens,
        max_context_chars=settings.max_context_chars,
        finish_turn=finish_turn, on_event=on_event,
    )

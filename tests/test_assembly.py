"""Shared assembly preserves policy differences, injection and runtime limits."""
import pytest

from code_agent import cli
from code_agent.agent import TurnDecision
from code_agent.assembly import AgentPolicy, GENERAL_PROMPT, build_llm, create_agent
from code_agent.config import Settings
from code_agent.errors import ConfigError
from code_agent.llm import MockLLM, OpenAICompatibleLLM
from code_agent.tools.factories import GENERAL_TOOL_NAMES, build_registry
from eval.runner import Variant, default_variant
from tests.helpers import ScriptedLLM, text_response, tool_response

SOURCE = ('def increment(n):\n'
          '    """Given a positive integer n, return the integer n plus one."""\n'
          '    return n + 1\n')


def test_model_settings_and_offline_selection_need_no_network(tmp_path):
    settings = Settings(workspace=tmp_path, api_key="fake-key", base_url="https://example.invalid/v1",
                        model="test-model", temperature=.7, llm_max_tokens=512,
                        request_timeout=17, max_retries=2)
    client, description = build_llm(settings)
    assert isinstance(client, OpenAICompatibleLLM)
    assert (client.api_key, client.base_url, client.model, client.temperature,
            client.max_tokens, client.timeout, client.max_retries) == (
                settings.api_key, settings.base_url, settings.model, settings.temperature,
                settings.llm_max_tokens, settings.request_timeout, settings.max_retries)
    assert settings.api_key not in description
    forced, description = build_llm(settings, force_mock=True)
    assert isinstance(forced, MockLLM) and "--mock" in description
    fallback, description = build_llm(Settings(workspace=tmp_path))
    assert isinstance(fallback, MockLLM) and fallback.workspace == settings.workspace
    assert "未配置" in description


@pytest.mark.parametrize("steps,tokens,status", [(1, 0, "max_turns"), (4, 120, "max_tokens")])
def test_injected_dependencies_events_and_budgets_work_together(tmp_path, steps, tokens, status):
    (tmp_path / "note.txt").write_text("observed content")
    settings = Settings(workspace=tmp_path, max_steps=steps, max_total_tokens=tokens,
                        max_context_chars=2400)
    policy = AgentPolicy("custom prompt", ("read_file",))
    registry = build_registry(settings, policy.tool_names)
    llm = ScriptedLLM([tool_response(("read_file", {"path": "note.txt"}))])
    events = []
    agent = create_agent(settings, policy, llm=llm, registry=registry,
                         finish_turn=lambda *_: TurnDecision(continue_=True), on_event=events.append)
    agent.state.add_user("read note.txt")
    result = agent.run()
    assert agent.llm is llm and agent.tools is registry
    assert agent.max_context_chars == settings.max_context_chars
    assert result.status == status and result.turns == result.tool_calls == llm.calls == 1
    assert llm.requests[0][0] == {"role": "system", "content": "custom prompt"}
    assert "observed content" in next(e for e in events if e.type == "tool_call_end").content
    assert events[-1].type == "run_end"
    assert not (tmp_path / ".sessions").exists()


def test_generic_assembly_needs_no_test_source(tmp_path):
    agent = create_agent(Settings(workspace=tmp_path), AgentPolicy(GENERAL_PROMPT),
                         llm=ScriptedLLM([text_response("done")]))
    agent.state.add_user("explain a concept")
    assert set(agent.tools.names()) == set(GENERAL_TOOL_NAMES)
    assert agent.finish_turn is None and agent.run().status == "completed"


@pytest.mark.parametrize("flag", [None, "--test-generation", "--fault-feedback"])
def test_cli_custom_tools_do_not_implicitly_enable_validation(tmp_path, flag):
    (tmp_path / "solution.py").write_text(SOURCE)
    flags = ["--mock", "--no-session", "--tools", "submit_tests"]
    args = cli.build_parser().parse_args(flags + ([flag] if flag else []))
    original = vars(args).copy()
    agent, store, _ = cli.build_agent(args, Settings(workspace=tmp_path), lambda _: None,
                                    session_enabled=False)
    assert vars(args) == original and store is None
    if flag is None:
        assert agent.finish_turn is None
        assert GENERAL_PROMPT in agent.state.system_prompt
        assert str(tmp_path) in agent.state.system_prompt
        assert agent.tools.names() == ["submit_tests"]
    else:
        assert agent.finish_turn is not None
        assert agent.state.system_prompt == default_variant("A5" if flag == "--fault-feedback" else "A4").system_prompt
        expected = ["submit_tests"] + (["inspect_survivors"] if flag == "--fault-feedback" else [])
        assert agent.tools.names() == sorted(expected)
        if flag == "--fault-feedback":
            submitter, inspector = agent.tools.get("submit_tests"), agent.tools.get("inspect_survivors")
            assert inspector.submitter is submitter and submitter.inspector is inspector


@pytest.mark.parametrize("options", [{"allow_write": False}, {"allow_code_execution": False},
                                   {"execution_mode": "disabled"}])
def test_interactive_validation_checks_execution_permissions(tmp_path, options):
    settings = Settings(workspace=tmp_path, **options)
    with pytest.raises(ConfigError, match="requires writing and code execution"):
        AgentPolicy.interactive(settings, fault_feedback=True)


def test_evaluation_prompt_is_separate_from_interactive_context(tmp_path):
    formal = default_variant("A0").agent_policy()
    interactive = AgentPolicy.interactive(Settings(workspace=tmp_path))
    assert formal.system_prompt == GENERAL_PROMPT
    assert interactive.system_prompt.startswith(GENERAL_PROMPT + "\n")
    assert str(tmp_path) in interactive.system_prompt
    assert formal.tool_names == interactive.tool_names == GENERAL_TOOL_NAMES
    assert not formal.validate_tests and not interactive.validate_tests


def test_evaluation_validation_preserves_custom_prompt_and_overrides_guided_hook(tmp_path):
    (tmp_path / "solution.py").write_text(SOURCE)
    variant = Variant("custom", system_prompt="custom evaluation prompt", tool_names=("submit_tests",))
    llm = ScriptedLLM([text_response("done without tests")])
    agent = create_agent(Settings(workspace=tmp_path, max_steps=1), variant.agent_policy(), llm=llm,
                         finish_turn=lambda *_: TurnDecision(end=True, reason="guided hook"))
    agent.state.add_user("generate tests")
    result = agent.run()
    assert result.status == "max_turns"
    assert llm.requests[0][0]["content"] == variant.system_prompt
    assert any("submit_tests" in message["content"] for message in agent.state.messages)


def test_validation_policy_rejects_missing_submitter(tmp_path):
    with pytest.raises(ConfigError, match="requires submit_tests"):
        create_agent(Settings(workspace=tmp_path), AgentPolicy(GENERAL_PROMPT, (), validate_tests=True),
                     llm=ScriptedLLM([]))

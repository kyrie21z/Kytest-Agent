"""Offline, scripted demonstration of the production A4 feedback loop (not an eval)."""
import argparse
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from code_agent.agent import Agent
from code_agent.config import Settings
from code_agent.llm import LLMResponse, MockLLM, ToolCall
from code_agent.testgen import TESTGEN_PROMPT, make_testgen_hook
from code_agent.tools.factories import build_registry


def candidate(name, expression):
    return {"name": name, "code": f"from solution import increment\ndef {name}():\n    assert {expression}\n",
            "contract_quote": "Given a positive integer n, return the integer n plus one.",
            "input_domain": "positive integer", "oracle_reason": "Derive n+1 arithmetically from the documented contract",
            "fault_hypothesis": "An off-by-one result or a wrong return type"}


def response(cases):
    return LLMResponse(tool_calls=[ToolCall("demo", "submit_tests", json.dumps({"cases": cases}))],
                       usage={"prompt_tokens": 10, "completion_tokens": 20})


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    workspace = args.output or Path(tempfile.mkdtemp(prefix="testgen-demo-"))
    workspace.mkdir(parents=True, exist_ok=True)
    sut = workspace / "solution.py"
    if sut.exists():
        raise SystemExit("Use an empty demo output directory")
    sut.write_text('def increment(n):\n    """Given a positive integer n, return the integer n plus one."""\n    return n + 1\n')
    settings = Settings(workspace=workspace)
    registry = build_registry(settings, ("read_file", "submit_tests"))
    submitter = registry.get("submit_tests")
    llm = MockLLM(responses=[response([candidate("test_valid", "increment(2) == 3"),
                                    candidate("test_wrong", "increment(3) == 99"),
                                    candidate("test_invalid", "increment(0) == 1")]),
                             response([candidate("test_wrong", "increment(3) == 4"),
                                       candidate("test_type", "isinstance(increment(2), int)")]),
                             LLMResponse(content="Accepted three tests; the wrong assertion was repaired and the invalid input was refused.")])
    def event(e):
        if getattr(e, "name", None) == "submit_tests" and hasattr(e, "content"):
            print(e.content, flush=True)
    agent = Agent(llm=llm, tools=registry, system_prompt=TESTGEN_PROMPT, max_turns=4,
                  finish_turn=make_testgen_hook(submitter), on_event=event)
    agent.state.add_user("Generate tests for solution.py")
    print("Offline scripted LLM: demonstrates the real tool loop, not model quality.", flush=True)
    result = agent.run()
    if len(submitter.accepted) != 3 or result.status != "completed":
        raise SystemExit("Demo acceptance failed")
    print(result.final_text); print(f"Artifacts: {workspace}")


if __name__ == "__main__":
    main()

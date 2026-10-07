"""Explicitly scripted demo; the tools, files, and pytest execution are real."""
import ast
import json
import re
import time

from ..llm import LLMResponse, ToolCall

SOURCE = '''def classify(value, low, high):
    """For low <= high: -1 below, +1 above, 0 inside [low, high]."""
    if value < low:
        return -1
    if value > high:
        return 1
    return 0
'''
TASK = "为 solution.py 生成 pytest 单元测试，覆盖正常值、上下边界和退化区间；运行测试并报告真实结果。不要修改目标源码。"
TESTS = '''from solution import classify


def test_inside():
    assert classify(5, 2, 8) == 0


def test_below():
    assert classify(1, 2, 8) == -1


def test_above():
    assert classify(9, 2, 8) == 1


def test_inclusive_bounds():
    assert classify(2, 2, 8) == 0
    assert classify(8, 2, 8) == 0


def test_single_point_interval():
    assert classify(3, 3, 3) == 0
    assert classify(2, 3, 3) == -1
    assert classify(4, 3, 3) == 1
'''


class DemoLLM:
    name = "离线演示（脚本化模型）"

    def __init__(self, delay=0.6, variant="A0"):
        self.calls = 0
        self.delay = delay
        self.variant = variant

    def chat(self, messages, tools=None):
        self.calls += 1
        time.sleep(self.delay)
        steps = [
            ("读取目标代码，确认函数契约。", "read_file", {"path": "solution.py"}),
            ("上下界包含在区间内；为三个分支和退化区间写入测试。", "write_file",
             {"path": "test_solution.py", "content": TESTS}),
            ("运行刚写入的测试，把实际结果带回 Agent。", "run_command",
             {"command": 'python -m pytest test_solution.py -q', "timeout": 15}),
        ]
        if self.variant == "A4":
            # The same five final tests as A0; two deliberately bad proposals
            # expose the real validator, not model quality differences.
            reasons = ["区间内部返回0", "下方返回-1", "上方返回1", "上下边界属于区间", "单点区间包含该点"]
            cases = [{"name":fn.name, "code":"from solution import classify\n\n"+ast.get_source_segment(TESTS,fn)+"\n",
                      "contract_quote":"For low <= high: -1 below, +1 above, 0 inside [low, high].",
                      "input_domain":"整数，low <= high", "oracle_reason":reason,
                      "fault_hypothesis":"错误处理区间位置或包含边界"}
                     for fn,reason in zip(ast.parse(TESTS).body[1:],reasons)]
            wrong_boundary = {**cases[3], "code":cases[3]["code"].replace("classify(2, 2, 8) == 0", "classify(2, 2, 8) == -1")}
            wrong_quote = {**cases[4], "contract_quote":"Invalid inputs must raise ValueError."}
            steps = [steps[0],
                ("脚本示例刻意提交两个错误候选：边界预期错误、契约引用不存在。观察真实验证器拒绝它们。",
                 "submit_tests", {"cases":cases[:3]+[wrong_boundary,wrong_quote]}),
                ("修正两个候选，重新提交；已接受的测试继续保留。",
                 "submit_tests", {"cases":cases[3:]}), steps[2]]
        if self.calls <= len(steps):
            text, name, args = steps[self.calls-1]
            return LLMResponse(content=text,
                tool_calls=[ToolCall(id=f"demo_{self.calls}", name=name, arguments=json.dumps(args))],
                raw={"choices": [{"finish_reason": "tool_calls"}]})
        observation = messages[-1].get("content", "")
        passed = re.search(r"\b(\d+) passed\b", observation)
        text = (f"已生成 test_solution.py，实际执行 {passed.group(1)} 项测试通过。覆盖正常值、上下边界和退化区间。"
                if passed and observation.startswith("[OK]")
                else "测试验证未通过。请查看执行输出，处理环境或测试错误后重新运行。")
        return LLMResponse(content=text, raw={"choices": [{"finish_reason": "stop"}]})

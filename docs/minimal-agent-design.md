# Minimal General Agent 设计说明

本文件记录**为什么这样实现**，而不是实现了什么。目标读者是评审者和三天后的作者本人。

对应代码：`src/code_agent/agent/`、`src/code_agent/message.py`、`src/code_agent/tools/`。

---

## 1. 定位

这不是作业的最终形态，而是作业的**自变量零点**。

开发计划（`Test Generation Agent Dev Plan.md`）要在 A0→A3 之间做累计消融，因此这个
Minimal General Agent 同时承担两个角色：

1. 交付物中"能通过 CLI 交互的 Agent"这一硬性要求（占分 40%）；
2. 实验里的 **A0 对照条件**——一个真正通用、不含任何测试专用编排的编码 Agent。

第 2 个角色决定了它的设计约束比"能跑就行"严格得多。

## 2. 输入约束

| 来源 | 约束 |
|---|---|
| 作业要求 | Agent 循环（输入→推理→工具调用→输出）；至少一种工具；CLI 可交互；上下文记忆；错误处理与重试 |
| 评分表 | 功能完整性 40%（含边界情况）、Agent 架构 30%、代码质量 20%、文档 10% |
| 实验设计 | A0 必须保持通用（不能内置 pytest/覆盖率编排）；变体之间只能靠配置区分；必须在固定 turn 数处可取快照；测量不得依赖解析 stdout |
| 时间 | 距截止约 2 天，因此工程复杂度必须受控 |

## 3. 第一性原理推导

### 3.1 四个消费者，一个内核

同一套 Agent 有四个消费者，它们的要求互相冲突：

| 消费者 | 要什么 | 不要什么 |
|---|---|---|
| 人类演示（CLI） | 可读文本、逐步可见 | 结构化噪音 |
| 批量评测 harness | 无人值守、结构化结果、可并发 | 任何 `print` |
| 指标测量 | 在固定 turn 数处的快照 | 提前跑完 |
| 复现者 | 完整轨迹、可重放 | 丢失中间状态 |

四条约束压出的唯一结论：

> **Agent 核心不知道输出介质的任何信息，它只发事件。所有输出都是事件的订阅者。**

如果 Agent 内部有 `print()`，harness 就只能靠正则解析 stdout 取指标——这是最脆弱的
一种测量方式。因此核心零 IO，`cli.py`（待实现）与 `runner.py`（待实现）都只是订阅者。

这一点有外部佐证：Pi Agent 的整个 CLI 包里 `new Agent(` 只出现一次
（`packages/coding-agent/src/core/sdk.ts:387`），交互模式、print 模式、JSON 模式、
RPC 模式全部是同一套核心的订阅者。我们的结构与之同构。

### 3.2 变体是配置，不是代码分支

实验设计的目标是 `A_i − A_(i−1)` 能对应一个可解释的机制增量。如果每个变体各写一份
循环，"每一级同时改了多个变量"的结构性风险就无法排除。

因此主循环只有一份，差异收敛到四个注入点：

| 注入点 | 承载的变体差异 |
|---|---|
| `tools` | 工具集（A0 只有通用工具） |
| `system_prompt` | 策略文本（A1 的测试知识） |
| `max_turns` 等预算 | 预算约束 |
| `before_turn` / `finish_turn` | A2/A3 的反馈编排 |

### 3.3 turn 是预算原子，且必须可挂起

`turn` 的定义：**一次 LLM 调用 + 它触发的全部工具执行**。采用这个定义的理由是它是
唯一能同时充当"预算单位"和"检查点单位"的粒度。

固定预算质量曲线要求在第 1/2/4/8 个 turn 处取样。这条需求直接约束了 API：

```python
agent.run_until(1)   # → paused，可在此时评测工作区
agent.run_until(2)   # 继续，状态与计数器连续
agent.run()          # 跑到自然结束或预算耗尽
```

一个"一跑到底"的 `run()` 无法做预算对照实验。因此 `run_until` 不是便利方法，
而是实验设计对架构提出的硬性要求。

### 3.4 A0 的通用性边界划在工具集上

最危险的地方是**工具集本身**。如果 A0 自带 `run_pytest`，A0 就不再是通用 Agent，
反事实对照失效。因此：

- A0 只拿 `read_file` / `write_file` / `list_files` / `search_code` /（待实现）`run_command`；
- 装配开关集中在 `tools/factories.py` 一个函数里，并由测试守住（见 `test_default_registry_is_general_purpose_only`）；
- A0 **可以**自己用 shell 跑 pytest——那是要观察的**涌现行为**，不是要禁止的行为。
  真正的自变量是"反馈由谁触发"：模型自发（非确定性）还是系统编排（确定性）。

## 4. 接口契约

### 4.1 消息

```python
AssistantMessage(content: list[TextBlock | ToolCallBlock], stop_reason, usage, error_message)
```

**工具调用是 content block 的一种，不是与文本平行的字段。** 这样文本里出现
`{"name": ..., "arguments": ...}` 这类伪造内容时永远不会被误判成工具调用——
纯文本协议最典型的失败模式被结构性排除。

`stop_reason ∈ {stop, length, tool_use, error, aborted}`。错误是数据：LLM 层不向循环
抛异常表达请求失败，而是返回 `stop_reason="error"` 的消息，由循环决定如何记账。
这样一次 API 抖动只会污染一个 run 的状态，不会让整批判评测崩溃。

### 4.2 事件

`RunStart / TurnStart / AssistantMessageEvent / ToolCallStart / ToolCallEnd / TurnEnd / RunEnd / ErrorEvent`

全部是可 `json.dumps` 的 dataclass，事件里的消息是普通 dict（不是内部对象引用），
因此订阅者无法反向修改 Agent 状态。

事件名沿用 Pi 的 `AgentEvent`（`packages/agent/src/types.ts:514-529`）中的必要子集，
省略了 `message_update` / `tool_execution_update`——本层不做流式。

### 4.3 工具

```python
class Tool:
    name: str; description: str; parameters: dict   # JSON Schema
    def run(self, **kwargs) -> ToolResult
```

- 构造签名统一在基类处理（接受 `Settings` 或路径），避免子类漏写 `__init__`
  而悄悄继承错误签名——这是实际发生过的缺陷，现在由
  `test_every_assemblable_tool_constructs_and_exposes_a_valid_schema` 守住。
- 未知工具、参数非法、工具抛异常都转成一条 `is_error` 的观察结果，不是崩溃。
- `ToolResult.terminate` 允许工具请求"这批跑完就结束"，但只在**整批**工具都要求
  终止时才生效，避免单个工具劫持整轮对话。

## 5. 消息序列不变量

这是全套实现里唯一会让真实 API 直接返回 400 的地方，因此单独成节：

> `role="tool"` 的消息必须紧跟在带 `tool_calls` 的 `assistant` 消息之后。

实现方式：上下文裁剪以**组**为单位，一个组是"一条 assistant 消息 + 它触发的全部 tool
消息"，整体保留或整体丢弃，结构上不可能切出孤立的 tool 消息。

保留优先级：第一条消息（任务描述）> 最新一组 > 预算。也就是说预算是软约束，
两端的硬优先级优先。裁剪后若仍超预算，对超长内容做保留头尾的截断并留下
`[...已折叠 N 字符]` 标记，让模型知道自己漏看了东西。

`assert_message_sequence_valid()`（`tests/helpers.py`）把这条不变量变成可执行断言，
在多个测试里被调用。`AgentState.pending_tool_calls()` 用于事后检测未配对的调用。

## 6. 命令执行：`run_command` 的三个硬问题

命令执行是 A0 唯一的"与代码交互"能力。没有它，模型只能读写文件，无法验证自己写的
东西能不能跑；同时"Agent 会不会自发运行测试"这一观察项也无从测量。

它带来的三个问题都不是"跑一下 subprocess"能解决的：

**1. 超时后必须杀掉整棵进程树。** `subprocess` 的 timeout 只终止直接子进程。
`python -m pytest` 会再 fork 出自己，只杀父进程会留下孤儿持续占用 CPU——
并行评测 30 个实例时这是机器级故障。Windows 用 `taskkill /F /T`，POSIX 用进程组。
测试 `test_grandchild_process_is_killed_too` 通过扫描系统进程表来验证这一点。

**2. readline 阻塞会让超时永不触发。** `for line in proc.stdout` 在子进程不换行地
持续输出时会卡死，超时逻辑根本没机会执行。实现改用后台收集线程 + 主线程
`wait(timeout)`，让超时始终由主线程掌控。见 `test_timeout_still_fires_when_child_floods_output`。

**3. 命令字符串的平台语义不同。** 这是最容易写错的一处：

| 方案 | 问题 |
|---|---|
| Windows 上用 `shlex.split(text, posix=False)` | **引号被原样保留**，`"C:\a b\x.py"` 带着引号传给子进程，必然失败 |
| "找到 argv[0] 位置后切掉再递归" | `str.find` 会命中引号**内部**的同名文本，从引号中间切开，后续全部错位 |
| **实际采用**：两次 `CommandLineToArgvW` | 先解析出全部 token（引号由系统剥掉），再逐个 token 重建命令行并重新解析。不做任何字符串位置推算 |

第二个坑是实际发生的：`python "C:\tmp\python\run me.py" python --flag` 中 argv[0] 的
文本出现在引号内部，切点算错。验收方式是让一个真实子进程打印 `sys.argv` 回来对比
（`test_split_command_matches_what_the_child_process_actually_receives`），
而不是只和手写的预期列表比。

另外三个有意的设计选择：

- **命令不经过 shell**：`;`、`&&`、`|` 都是普通参数。这排除了注入面，也让"Agent 到底
  执行了什么"在轨迹里可以逐参数核对。代价是模型不能写管道，需要分多次调用。
- **工作区保持干净**：命令以 `PYTHONDONTWRITEBYTECODE=1` 运行。评测时工作区同时是
  被测代码与 Agent 产物的载体，多出 `__pycache__` 会污染快照与后续比对。
- **输出保留头尾**：构建/测试输出的关键信息在末尾（失败摘要、错误堆栈），只留开头
  会把这些全丢掉。

## 7. CLI：三种模式，一个内核

CLI 是"核心零 IO"这条约束的兑现处。`cli.py` 里没有业务逻辑，只有参数解析与装配；
所有展示决策集中在 `render.py`。三种模式的差别仅在于"谁订阅事件、怎么渲染"：

| 模式 | 订阅者 | stdout | stderr |
|---|---|---|---|
| 交互 | `EventRenderer(verbose=True)` | 思考、工具调用、回答 | 运行摘要 |
| `--print` | `EventRenderer(verbose=False)` | **只有最终回答** | 过程信息 |
| `--mode json` | `JsonRenderer` | 逐行事件 JSONL | 提示信息 |

两个刻意的决定：

**stdout 与 stderr 严格分离。** 过程信息写 stderr，因此
`python main.py --print "任务" > answer.txt` 拿到的文件里只有回答，可以直接喂给下游
脚本。JSON 模式的 stdout 是协议通道，混入任何人类可读文本都会破坏它——
由 `test_json_mode_keeps_stdout_free_of_human_text` 逐行 `json.loads` 守住。

**离线模式不静默降级。** 没有 API Key 时会退回规则模拟，并在 stderr 明确提示。
否则用户看到一段通顺的中文回答，会以为那是真实模型的输出——静默降级是最糟的失败模式。
这条同样有测试（`test_missing_credentials_fall_back_to_mock_without_crashing`）。

零安装运行通过 `main.py` 完成（把 `src/` 插入 `sys.path`），安装后则用
`code-agent` 命令（`pyproject.toml` 的 console script）。

## 8. 轨迹落盘：为什么必须 append-only

评测跑到一半崩溃、或某个实例超时被杀时，**已经产生的轨迹不能丢**。一次性 dump
整份会话的实现会让崩溃前那一步的全部证据消失，而恰恰是那段最有诊断价值。

因此每行一条记录，写入即落盘：

```
{"type":"session",  ...工作目录、模型、工具、模式}
{"type":"user",     "content":"..."}
{"type":"assistant","text":"...", "tool_calls":[...], "stop_reason":"...", "usage":{...}}
{"type":"tool_call", "name":"read_file", "arguments":{...}}
{"type":"tool_result","name":"read_file", "is_error":false, "content":"<完整输出>"}
{"type":"result",   "status":"completed", "turns":3, "total_tokens":300}
```

工具输出保留非敏感内容与事件结构，不做摘要；复评整改版在落盘前对
已知密钥、敏感键名、JSON 和环境变量赋值脱敏。
体积控制交给调用方（评测时只保留失败样例的全文）。

## 9. 被否决的方案

| 方案 | 否决理由 |
|---|---|
| 流式 SSE 解析 | 引入"工具参数是半截 JSON"这一整类失败模式（Pi 为此写了三层抢救解析器）。非流式响应天然是完整 JSON。代价仅是长请求可能撞网关超时，用 `max_tokens` 上限 + 指数退避重试覆盖。工具执行本就要等流结束才开始，所以流式不改变总墙钟。 |
| asyncio | 会把整条调用栈改成 async。阻塞 IO + `ThreadPoolExecutor` 已足够并发跑 4~8 个评测实例。 |
| 并行工具执行（Pi 的默认） | turn 语义与轨迹时间线变得不确定，对实验是纯噪声。改顺序执行。 |
| 多 provider 目录、OAuth、成本模型 | 会引入跨 provider 混杂变量。只保留 OpenAI 兼容 + 离线 Mock。 |
| TUI、RPC、SDK、扩展、skills、MCP、sub-agent、plan mode | 与评分和实验目标都无关。Pi 自身也明确不做 sub-agent 与 plan mode。 |
| 会话树（append-only JSONL + parentId + 追溯编辑） | Pi 用 2000 行实现的能力。我们只需要"留下轨迹"，扁平 JSONL 足够。 |
| 交互式 steering / follow-up 队列 | 作业不需要撤销与中途插话。`abort()` + turn 边界检查已覆盖 Ctrl-C 场景。 |
| `readline` 的 Windows 兼容层（`pyreadline3`） | 有则用、无则降级，不列为依赖。行编辑只是体验优化。 |

## 10. 与 Pi Agent 的对照

| 本项目 | Pi Agent | 说明 |
|---|---|---|
| `agent/core.py` | `packages/agent/src/agent-loop.ts` | 主循环；我们砍掉了 steering/follow-up 队列与并行工具执行 |
| `agent/events.py` | `packages/agent/src/types.ts:514-529` | 事件子集 |
| `agent/state.py` | `packages/ai/src/utils/transcript.ts` + `compaction/` | 我们用按组裁剪代替 1100 行压缩 |
| `message.py` | `packages/ai/src/types.ts:397-612` | 消息与 content block |
| `proc.py` | 无对应（Pi 依赖 Node 的 child_process） | 进程执行、超时、进程树清理 |
| `tools/base.py` | `packages/agent/src/types.ts:464-497` | 工具接口；`terminate` 语义一致 |
| `tools/shell_tools.py` | `packages/coding-agent/src/core/tools/bash.ts` | 命令执行工具 |
| `tools/factories.py` | `packages/coding-agent/src/core/tools/index.ts:164-222` | 工具集装配与预设 |
| `cli.py` | `packages/coding-agent/src/modes/print-mode.ts` | print / JSON / 交互三种模式 |
| `render.py` | `packages/coding-agent/src/modes/json-event.ts` | 事件 → 文本 / JSONL |
| `session.py` | `packages/coding-agent/src/core/session-manager.ts` | 我们只保留扁平 append-only JSONL，砍掉分支树与追溯编辑 |

参考实现笔记（含逐行引用）见 `../../docs/pi-architecture-notes.md`。

## 11. 当前状态

已完成：

- `message.py`：消息与用量类型、OpenAI usage 归一化；
- `agent/events.py`：事件类型；
- `agent/state.py`：消息历史、按组裁剪、配对不变量检查；
- `agent/core.py`：主循环、turn 语义、预算、`run_until` 检查点、错误收口；
- `proc.py`：进程执行、超时、进程树清理、跨平台命令行解析；
- `tools/shell_tools.py`：`run_command` 工具；
- `tools/factories.py`：工具装配与 A0 通用性边界；
- `cli.py` + `render.py`：三种交互模式、流分离、退出码；
- `session.py`：append-only 轨迹落盘；
- `llm.py` 的 `MockLLM`：离线规则模拟，可跑出完整多轮循环；
- 114 条测试；`scripts/demo_offline.py` 离线端到端演示。

待实现：

| 项 | 阶段 | 阻塞了什么 |
|---|---|---|
| 评测 harness（runner / metrics） | 4 | A0~A3 消融实验的全部数据 |
| 变异测试引擎 | 4 | RQ3 的主终点（mutation score） |

以下阶段3状态是历史设计快照；当前评测层已实现，验收见 README。

已知限制与当前边界：

- 命令不经 shell，因此模型无法使用管道与重定向。这是安全与可核对性的取舍。
- `run_command` 使用当前解释器所在的 Python 环境，工作区没有独立虚拟环境。
  评测时需要保证该环境装有 pytest 与 coverage。
- 破坏性命令护栏（`_DENY_PATTERNS`）是**防误操作的护栏，不是安全边界**。
  本文原实现仅做目录分离，未建立权限隔离。复评整改版默认使用 Linux Bubblewrap，
  挂载工作区及只读运行库并隔离网络；不可用时拒绝命令执行。显式 trusted 模式
  仅供受信本机代码使用，拥有宿主机权限；详见 README 的命令执行边界。
- 会话轨迹不设体积上限。跑大批量实验时需要外部轮转，否则结果目录会迅速膨胀。

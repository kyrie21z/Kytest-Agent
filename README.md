# Code Agent

一个**零第三方依赖**的编码 Agent：实现「输入 → 推理 → 工具调用 → 观察 → 输出」的完整
Agent 循环，可通过命令行交互。它同时是"测试生成 Agent"实验的通用基线（A0）。

**默认保持通用 Agent；A4/A5 是实验功能。** 新增契约依据、逐条验证、增量保留
及独立开发故障反馈。有效开发对照的30个run中，A0/A4通过率和杀伤率均为100%，
A4 token约增加0.4%、生成时间约增加51%，未显示质量收益，因此不替换默认模式。
结果见 [开发试验报告](results/testgen_pilot_v2/report.md)。环境诊断轮v1已标记不可比。
正式20例的新A0/A4对照已完成：A4通过率100%（A0为90%），有效杀伤率69.27%
（A0为66.44%），差2.83个百分点未检出显著性；token增加15.8%，生成时间增加52.2%。
结果见 [正式20例报告](results/testgen_formal_v1/report.md)，新旧A0分数不混入配对。
A0–A3 的80份记录属于历史版本（v2 难例集20例），历史结论不自动适用于修复后实现。结论与数据见
[Design.md](Design.md) 与 [results/v2_ablation/ANALYSIS.md](results/v2_ablation/ANALYSIS.md)。

## 快速开始

运行 Agent 只依赖 Python 标准库。**不需要安装任何第三方包，也不需要 API Key。**
测试与统计分析的依赖见 `requirements.txt`（分三档注释，按需安装：测试 `pip install pytest coverage`，
统计分析额外 `pip install scipy`）。

```bash
cd code-agent

# 1. 交互模式：输入任务，Agent 一步一步调用工具完成
python main.py

# 2. 单次运行：只把最终回答写到 stdout
python main.py --print "为 solution.py 生成单元测试"

# 3. 无 API Key 的离线演示（未配置时也会自动退回离线模式）
python main.py --mock --print "解释 solution.py"

# 4. 跑测试
python -m pytest tests/ -q
```

`python main.py` 开箱即用，无需 `pip install`。若安装了包，也可以用 `code-agent` 命令。

### 评测（需要 .env 中配置 OpenAI 兼容 API）

```bash
# 消融主跑（A0–A3 × v2 难例集 20 例，约 350 万 token）
python scripts/run_eval.py run --variant A0,A1,A2,A3 \
    --dataset benchmarks/humaneval_plus_v2_20.jsonl --output results/current_ablation --concurrency 6

# 从历史原始 JSON 生成 input-output-v1 派生结果并同步当前表格
# 保留原始 CSV / summary / report；不发起模型请求
python scripts/analyze_ablation.py --write-docs
```

### 配置真实模型

复制 `.env.example` 为 `.env` 并填写（或直接设置同名环境变量）：

```bash
LLM_API_KEY=sk-...
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

任何 OpenAI 兼容接口都可用。未配置时会**明确提示**已退回离线模式，不会静默降级。

## 三种输出模式

### 契约约束与逐测试验证（A4）

```bash
# 目标目录包含 solution.py；当前解释器需要安装 pytest
python main.py -C /path/to/function --test-generation --max-turns 12 \
    --max-output-tokens 4096 --print "为 solution.py 生成单元测试"
```

模型通过 `submit_tests` 提交独立候选，记录docstring原文依据、输入域、预期结果
推导和要捕捉的错误。工具检查可识别的显式输入约束，逐条隔离运行，报告错误断言
或超时，再用合并回归检查保留通过的测试。失败候选不能替换已接受的测试。
产物为 `test_solution.py` 和包含接受/拒绝依据的 `testgen_report.json`。
已有测试作为不可删除的基底参与合并回归；基底自身失败时保留原文并报告失败。
默认不加载该工具，A0保持通用；A4没有“pytest通过就立即收尾”的钩子。

元数据与自然语言推导仍需审核；未识别的约束标为未检查。参考实现上通过不等于
证明规范正确，也不等于发现更多缺陷。新机制的开发试验规则见
[docs/testgen-pilot.md](docs/testgen-pilot.md)，新结果与历史A0–A3分开报告。

```bash
# 无API请求的脚本化演示：错误断言修复、非法输入拒绝、增量保留
python scripts/demo_testgen.py
```

演示使用脚本化LLM和真实验证工具，不作为模型效果证据。

### A4正式20例评测

使用固定v2难例集，新A0和A4各20个run、同模型/预算/环境；每条件每例只采样一次。
主指标要求参考实现通过且未改写SUT，否则有效杀伤率为0，避免失败断言虚增分数。
平均差+2.83个百分点，95%配对bootstrap区间[-6.01,+12.71]，Wilcoxon p=0.4652；
改善/持平/退步为2/16/2。不能据此证明总体收益或质量等价。

```bash
# 只生成报告，不调用模型
python scripts/run_testgen_formal.py --report-only

# 新模型采样必须使用新目录，不能改写已冻结记录
python scripts/run_testgen_formal.py --output results/testgen_formal_new
```

协议见 [docs/testgen-formal.md](docs/testgen-formal.md)，逐实例解释见
[CASE_ANALYSIS.md](results/testgen_formal_v1/CASE_ANALYSIS.md)。测试262项通过、4项Windows
检查跳过。该集已有历史评测和失败分析，不能称为全新未见保留集。

### 独立开发故障反馈（A5）

```bash
# 包含A4验证；最多两轮开发故障反馈，用于定向追加测试
python main.py -C /path/to/function --fault-feedback --max-turns 12 \
    --max-output-tokens 4096 --print "为 solution.py 生成单元测试"

# 无API请求：真实Agent闭环，生成结束后再用独立评分故障验证
python scripts/demo_fault_feedback.py
```

`inspect_survivors` 给出已接受套件漏检的开发改动，追加候选仍经逐条与合并验证。
反馈与评分采用不同算子家族，并核对AST指纹无交集。两次套件相同的查询复用缓存；
超时与疑似等价改动不算检出。A5评分仅覆盖保留家族，基线须用相同评分池重测。
协议与限制见 [docs/fault-feedback.md](docs/fault-feedback.md)。A5尚无真实模型对照
结果；控制演示的独立边界故障检出从0/2到2/2，只证明闭环可运行。

| 模式 | 命令 | stdout | stderr |
|---|---|---|---|
| 交互 | `python main.py` | 每轮思考、工具调用、回答 | 运行摘要 |
| 单次 | `python main.py --print "任务"` | **只有最终回答** | 过程信息（可丢弃） |
| JSON | `python main.py --mode json --print "任务"` | **逐行事件 JSONL** | 提示信息 |

stdout 与 stderr 严格分离，因此可以安全地重定向：

```bash
python main.py --print "解释 solution.py" > answer.txt        # 只留回答
python main.py --mode json --print "解释 solution.py" > events.jsonl   # 给程序消费
```

JSON 模式每行一个事件，`run_start` 开头、`run_end` 结尾：

```json
{"type": "run_start", "tools": ["list_files", "read_file", "run_command", "search_code", "write_file"]}
{"type": "turn_start", "turn": 1, "request_messages": 2, "request_chars": 412}
{"type": "assistant_message", "turn": 1, "text": "先看工作区里有哪些文件。", "tool_calls": [...]}
{"type": "tool_call_end", "turn": 1, "name": "list_files", "is_error": false, "content": "目录 `.` 共列出 1 项：\n  solution.py"}
{"type": "run_end", "status": "completed", "turns": 3}
```

退出码：`0` 运行正常结束，`1` 运行失败（LLM 报错、超时），`2` 参数或配置错误。

## 命令行选项

```
-C, --workspace DIR   工作目录（默认当前目录）
-p, --print           跑一次就退出，只把最终回答写到 stdout
    --mode {text,json} 输出模式
-m, --model NAME      覆盖 LLM_MODEL
    --base-url URL    覆盖 LLM_BASE_URL
-t, --tools LIST      工具白名单，如 read_file,run_command
    --mock            强制离线模式，不发起网络请求
    --execution-mode {sandbox,trusted,disabled}  命令执行策略，默认 sandbox
    --no-session      不写会话轨迹
    --session-dir DIR 轨迹目录（默认 <workspace>/.sessions）
    --max-turns N     单次运行的 turn 上限
    --max-tokens N    token 上限，0 表示不限
    --max-context-chars N  单次请求的上下文预算
-v, --verbose         在 --print 模式下也显示中间过程
```

## 命令执行边界

默认 `EXECUTION_MODE=sandbox`：Linux 需要安装 Bubblewrap（`bwrap`），
子进程只看到工作区、只读 `/usr`、`/bin`、`/lib`、`/lib64` 和当前 Python/venv 安装目录，
以及私有 `/tmp`、`/run`、`/proc`、`/dev`。宿主机其他文件路径不可见，网络关闭。
`ALLOW_WRITE=false` 使工作区只读（私有临时目录仍可写）；
`ALLOW_CODE_EXECUTION=false` 或 `EXECUTION_MODE=disabled` 完全禁止命令执行。
隔离缺失或初始化失败时返回错误，不自动回落。
评测器执行生成测试时也使用同一隔离；覆盖率及变异产物写入临时工作区。
CLI 的 trusted 选择不会关闭评测器的默认隔离。

Windows/macOS 或未安装 Bubblewrap 时，读写工具仍可用；只有对受信代码才显式使用
`python main.py --execution-mode trusted` 或 `EXECUTION_MODE=trusted`。
该模式拥有当前用户的宿主机文件和网络权限；`ALLOW_WRITE=false` 时拒绝该模式的命令，
因为无法强制只读。命令黑名单和临时目录都不构成权限隔离。
Python 包本身仍为零第三方运行依赖；安全命令执行另需上述系统工具。

输出按64K字符块采集，保留上限后继续排空；大文件分段读取也采用有界读取，
单行最多保留2000字符并标记截断，不先将整行载入内存。
交互模式的 Ctrl-C 只取消当前任务；下一任务保留历史并重新计量预算。
同一任务的 `run_until` 多次调用继续共享预算。

## 会话轨迹

每次运行都会在 `<workspace>/.sessions/<时间戳>-<随机>.jsonl` 留下一份 **append-only**
的完整轨迹：会话头（工作目录、模型、工具、模式）、用户输入、每次 LLM 回复、
每次工具调用与完整输出、运行结果。

append-only 是刻意的：评测跑到一半崩溃、或实例超时被杀时，**已经产生的轨迹不会丢**，
而崩溃前那段往往最有诊断价值。轨迹保留事件结构及非敏感内容；配置密钥、结构化敏感字段和常见凭据文本在落盘前脱敏。

## 项目结构

```
code-agent/
├── main.py                  # 零安装入口：python main.py
├── src/code_agent/          # ★ Agent 本体（零第三方依赖）
│   ├── cli.py               # 命令行：交互 / --print / --mode json
│   ├── render.py            # 事件渲染：文本与 JSONL 两种订阅者
│   ├── session.py           # 轨迹落盘：append-only JSONL
│   ├── message.py           # 消息与用量类型：Agent 循环与 LLM 层之间的契约
│   ├── llm.py               # LLM 客户端：OpenAI 兼容 + 指数退避重试 + 离线 Mock
│   ├── config.py            # 配置：显式参数 > 环境变量 > .env > 默认值
│   ├── errors.py            # 异常分层
│   ├── proc.py              # 进程执行：超时、进程树清理、跨平台命令行解析
│   ├── agent/
│   │   ├── core.py          # ★ Agent 主循环（唯一的循环实现）
│   │   ├── events.py        # 事件：Agent 唯一的输出通道
│   │   └── state.py         # 消息历史 + 上下文裁剪 + 配对不变量检查
│   └── tools/
│       ├── base.py          # Tool / ToolResult / ToolRegistry / 路径沙箱
│       ├── file_tools.py    # read_file / write_file / list_files / search_code
│       ├── shell_tools.py   # run_command（命令执行，含超时与护栏）
│       ├── code_tools.py    # check_syntax / analyze_code（静态分析）
│       └── factories.py     # ★ 工具集装配：变体差异的唯一开关点
├── tests/                   # 回归及复评验收测试
├── docs/
│   ├── minimal-agent-design.md    # 为什么这样实现
│   └── evaluation-protocol.md     # 评测口径（冻结 + 3 条修订记录）
├── Design.md                # ★ 设计文档（问题定义 → 架构 → 消融 → 结论）
├── benchmarks/              # 冻结数据集：全集 164 例 / 评测集 v2（20 难例）/ 筛查与选型记录
├── eval/                    # 评测层：数据集、指标、变异引擎、编排钩子、runner、报告
└── scripts/
    ├── demo_offline.py      # 离线端到端演示（含 Agent 自发运行 pytest）
    ├── freeze_dataset.py    # 下载并固化数据集
    ├── make_screening_set.py      # 生成筛查集（排除评测集实例）
    ├── select_eval_v2.py    # 按冻结准则选出 v2 难例集
    ├── calibrate_instrument.py    # 变异引擎校准
    ├── check_contamination.py     # 记忆污染检查（语义等价扰动）
    ├── analyze_ablation.py  # 预注册配对统计（Wilcoxon + bootstrap + Holm）
    └── run_eval.py          # 评测入口
```

## 设计要点

**Agent 核心零 IO。** 核心不 `print`、不读 stdin，只发出事件（`agent/events.py`）。
CLI 与评测 harness 都是同一套核心的订阅者——批量评测因此不需要解析 stdout 来取指标。
CLI 里没有任何业务逻辑，只有展示决策（全部集中在 `render.py`）。

**变体是配置，不是代码分支。** 主循环只有一份，差异通过 `tools`、`system_prompt`、
预算、`before_turn`/`finish_turn` 钩子注入。这是消融实验能成立的前提：变体之间的
diff 全部是配置，混叠变量在架构层就不可能发生。

**`run_until(n)` 支持在任意 turn 数处挂起并继续。** 固定预算质量曲线需要在第
1/2/4/8 个 turn 处取样，一个"一跑到底"的 `run()` 无法做这类对照实验。

**错误是数据。** LLM 请求失败不抛异常，而是转成 `stop_reason="error"` 的消息并结束本次
run；工具失败、未知工具、参数非法都只是一条 `is_error` 的观察结果。单次 API 抖动
不会让整批评测崩溃。

**命令执行是通用能力，不含测试专用知识。** `run_command` 不识别 pytest、不解析测试
结果、不做自动重试；它只执行命令并带回真实输出。A0 会不会自发用它跑测试，是我们要
观察的行为，而不是预先编排好的流程。

**离线模式不静默降级。** 没有 API Key 时会在 stderr 明确提示，避免用户把模拟输出
误当成真实模型回答。

详细理由见 [`docs/minimal-agent-design.md`](docs/minimal-agent-design.md)。

## 测试

```bash
python -m pytest tests/ -q                  # 完整回归
python -m pytest tests/test_cli.py -q       # 只跑 CLI（子进程级）
python -m pytest tests/test_state.py -q     # 只跑上下文裁剪
python -m pytest tests/test_proc.py -q      # 只跑进程执行
python -m pytest tests/test_eval_mutation.py -q   # 只跑变异引擎
python -m pytest tests/test_eval_hooks.py -q      # 只跑 A2/A3 编排钩子
```

测试覆盖的关键不变量：

| 不变量 | 位置 |
|---|---|
| 每个 tool 消息必须能对应到前面的 assistant tool_call（否则真实 API 返回 400） | `test_state.py` / `helpers.py: assert_message_sequence_valid` |
| 模型输出被 `max_tokens` 截断时，工具调用一律不执行 | `test_core.py: test_truncated_output_never_executes_tool_calls` |
| 工具抛异常不会中断循环，只变成一条错误观察结果 | `test_core.py: test_tool_exception_is_contained_and_reported` |
| `run_until` 连续采样时计数器单调累计 | `test_core.py: test_run_until_snapshots_produce_a_monotonic_quality_curve` |
| 超时会杀掉整棵进程树，不留孤儿进程 | `test_proc.py: test_grandchild_process_is_killed_too` |
| 命令参数切分与子进程真实收到的 argv 一致 | `test_proc.py: test_split_command_matches_what_the_child_process_actually_receives` |
| `--print` 模式的 stdout 里没有任何过程信息 | `test_cli.py: test_print_mode_writes_only_the_final_answer_to_stdout` |
| JSON 模式的 stdout 每行都是合法 JSON 事件 | `test_cli.py: test_json_mode_keeps_stdout_free_of_human_text` |
| 轨迹文件按 append-only 写入且工具输出完整 | `test_cli.py: test_session_records_tool_results_with_full_content` |
| A0 的工具集不含任何测试专用能力 | `test_integration_tools.py: test_default_registry_is_general_purpose_only` |
| 每个变异体只与原程序差一处，且生成完全确定 | `test_eval_mutation.py: test_generation_is_deterministic` |
| 强测试的杀伤率显著高于弱测试 | `test_eval_mutation.py: test_strong_tests_score_much_higher_than_weak_tests` |
| "测量失败"不能被伪装成"测了满分" | `test_eval_mutation.py: test_import_error_is_distinguished_from_assertion_failure` |
| 所有启动过的运行都进分母（ITT 原则） | `test_eval_runner.py: test_every_started_run_counts_toward_the_denominator` |
| 改写 solution.py 不能进入测量口径，且必须留下可见标志 | `test_eval_runner.py: test_solution_modified_is_restored_before_final_measurement` |
| 钩子：失败回灌 → 修复 → 通过收尾（A2 闭环） | `test_eval_hooks.py: test_fail_then_repair_then_pass` |
| 钩子：测试文件无变化时不重复运行（防预算泄漏） | `test_eval_hooks.py: test_unchanged_tests_do_not_trigger_rerun` |
| 钩子：覆盖率定向反馈与轮数上限（A3） | `test_eval_hooks.py: test_coverage_feedback_and_rounds_cap` |
| run 结束后不得被拉起幽灵轮次 | `test_eval_runner.py: test_run_single_reports_cumulative_turns_not_the_last_call` |

CLI 测试通过真实子进程调用，因为这一层的价值恰在进程边界上（流分离、退出码、零安装）。
除评测层需要 `coverage` 外，所有测试都不联网、不需要 API Key、结果确定。

## 实验结果（摘要）

表格来自 `results/v2_ablation/derived/v1/`，token=input+output，不重复计入缓存；
token 数量不代表实际费用。原始记录、旧 CSV/summary/report 保留为历史证据，
派生清单记录输入 SHA-256。重算命令见快速开始。

完整数据与分析见 [`Design.md`](Design.md) 与
[`results/v2_ablation/ANALYSIS.md`](results/v2_ablation/ANALYSIS.md)。

<!-- ablation:main:start -->
| Variant | All-Pass | Line Cov. | Mutation（主终点） | Turns | Tokens | Runtime |
|---|---:|---:|---:|---:|---:|---:|
| A0 | 95.0% | 95.0% | 70.4% ± 17.6% | 5.8 | 25,079 | 142s |
| A1 | 90.0% | 90.0% | 69.3% ± 19.2% | 6.0 | 34,034 | 209s |
| A2 | 95.0% | 95.0% | 70.6% ± 21.3% | 3.1 | 14,830 | 155s |
| A3 | 90.0% | 90.0% | 66.6% ± 23.4% | 3.2 | 12,770 | 195s |
| 官方测试锚点 | 100.0% | 100.0% | 69.4% ± 14.6% | — | — | — |
<!-- ablation:main:end -->

三个有证据的结论：通用 Agent 的自发水平已接近官方测试（RQ1）；执行反馈的价值
在效率侧：质量未检出显著差异（未证明等价），token −56.43%（RQ2）；本次记录中的覆盖率定向反馈未显示杀伤率增量（RQ3）。
主终点配对比较经 Holm 校正后均不显著（n=20 的检出下限约 9 个百分点），
报告为"未检测到差异"而非"无差异"。

## 路线图

| 阶段 | 内容 | 状态 |
|---|---|---|
| 1 | Agent 内核（消息、事件、状态、主循环） | ✅ 完成 |
| 2 | `run_command` 工具与执行沙箱 | ✅ 完成 |
| 3 | CLI（三种模式）+ 轨迹落盘 + 离线 Mock | ✅ 完成 |
| 4a | 评测层：数据集、指标、变异引擎、编排钩子、runner、报告 + 仪器校准 | ✅ 完成 |
| 4b | A0–A3 历史消融与派生重算；修复后版本尚未重新采样 | 历史结果保留 |
| 5 | 文档收尾（Design.md / README / 选型与修订记录） | ✅ 完成 |

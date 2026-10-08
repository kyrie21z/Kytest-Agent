# Kytest Agent：Python Test Generation Agent

面向 Python 函数的测试生成 Agent：读取源码与任务，通过模型与工具的循环生成、执行和修正 pytest 测试。Web 将通用 Agent（A0）与契约候选验证（A4）放在同一输入下并行运行，展示工具轨迹、测试质量和运行成本。

**[下载57秒演示视频](https://raw.githubusercontent.com/kyrie21z/Kytest-Agent/main/docs/demo.mp4)** · [A0/A4 机制](#a0-与-a4-如何不同) · [实验结果](#实验结果) · [快速开始](#快速开始) · [设计说明](Design.md)

![同一输入下的 A0 / A4 真实结果对比](docs/demo-overview.png)

保存案例 MBPP/304 中，A0 有6项参考失败；A4 的6项测试全部通过，检出3/4个固定故障。截图与视频来自同一题的两次独立真实运行；视频的等待片段为8倍速，操作与结果保持原速。这是筛选的展示案例，完整口径见[案例说明](docs/rotation-example.md)。

## A0 与 A4 如何不同

测试生成需要解决三个问题：**能运行、能识别错误、能核查过程**。提示可以引导模型提出测试，实际执行才能发现语法错误、错误预期和套件冲突；测试通过后，还需要独立评价断言的判别力。

![A0 与 A4 的共享循环、工具和独立评价](docs/agent-architecture.png)

| 设计 | A0：通用 Agent | A4：契约候选验证 |
|---|---|---|
| 生成方式 | 自主读取、写入与运行测试 | 提交候选及契约依据、输入域、预期值理由 |
| 接受条件 | 模型决定何时验证与结束 | 契约检查、逐条执行、合并回归通过后接受 |
| 产物维护 | 模型直接维护测试文件 | 系统保留接受项，恢复被改写的目标源码 |
| 可核查记录 | 模型公开说明与工具轨迹 | 同样的轨迹，加上逐条接受、拒绝与修正记录 |

两组共享 Agent 核心、输入、模型配置与名义预算，各用独立工作区和状态。生成结束后执行相同的参考复验、覆盖率与固定故障评价，结果不回灌模型；A4 额外验证的执行成本单独记录。契约依据和参考通过仍不能认证所有预期值正确，质量收益由完整实验判断。

## 实验结果

MBPP **20题 × 每条件3次**，共180次生成；先聚合每题的三次结果，再比较20个任务。A5 在 A4 上增加有界开发故障反馈。

| 条件 | 有效产出 | 确认独立检出率 | 平均 token | 生成耗时 |
|---|---:|---:|---:|---:|
| A0：通用 | 49/60 | 68.81% | 20,688 | 45.1秒 |
| A4：候选验证 | 59/60 | 74.94% | 21,827 | 53.0秒 |
| A5：开发故障反馈 | 59/60 | 74.90% | 16,735 | 54.6秒 |

A4−A0 的观测差为 **+6.13个百分点**，95%任务 bootstrap 区间为 **[−5.12, +17.26]**，Holm p=0.7466，未通过预设统计验收。因此默认保留 A0，A4/A5 为可选机制。无效产出的主分数计0；token 是返回用量，不代表账单，生成耗时不含最终评价。

[实验摘要](submission/EXPERIMENTS.md)列出 A0～A5 的两组对照、指标定义、成本和限制；[派生证据](submission/evidence/README.md)提供280条记录的统计复核入口。两组协议不同，分数分别比较。

## 快速开始

推荐 **Ubuntu 或 Ubuntu WSL、Python ≥3.9**。首次体验无需模型密钥。

Ubuntu/WSL 首次使用时安装虚拟环境与默认命令隔离组件：

```bash
sudo apt install python3-venv bubblewrap
```

从 GitHub 获取源码并启动 Web：

```bash
git clone https://github.com/kyrie21z/Kytest-Agent.git
cd Kytest-Agent
python3 -m venv ~/.venvs/kytest-agent-homework
source ~/.venvs/kytest-agent-homework/bin/activate
python -m pip install -r requirements.txt
python web.py
```

打开 **http://127.0.0.1:8765**，点击 **“查看已保存差异案例”**。页面读取真实运行记录，展示两组工具轨迹、测试与质量结果，可下载产物，不产生新模型调用。

如果从提交包开始，先进入 `code-agent/`，再从创建虚拟环境这一步执行；包根目录的 `demo.mp4` 可直接播放。按 Ctrl-C 结束服务。

## 使用方式

| 方式 | 需要密钥 | 实际发生什么 |
|---|---|---|
| 已保存差异案例 | 否 | 查看此前真实运行的公开事件、测试与评价 |
| 离线演示 · 脚本化 | 否 | 固定模型响应，实际执行工具、候选验证和 pytest |
| 真实模型 | 是 | 当场请求模型并执行工具，结果与耗时可能变化 |

1. 查看 A0/A4 机制卡片，选择或编辑源码与任务。
2. 点击 **“同一输入对比 A0 / A4”**，同时启动两组 Agent。
3. 检查工具参数、返回结果、A4 候选依据与接受记录。
4. 对照测试有效性、覆盖率、固定故障检出、轮次与 token，下载产物。

离线脚本使用固定输入，两组最终测试相同；A4 的刻意错误候选用于展示拒绝与修正，其质量和模拟用量不计为真实模型成绩。取消“跟随最新”可检查历史事件；“停止两组”会取消后续动作，当前请求或工具需先结束。详细操作见[演示说明](docs/demo.md)。

<details>
<summary><strong>配置真实模型与使用命令行</strong></summary>

### 配置真实模型

在项目根目录复制 `.env.example` 为 `.env`，填写支持工具调用的 OpenAI 兼容服务配置：

```dotenv
LLM_API_KEY=你的密钥
LLM_BASE_URL=服务的兼容API地址
LLM_MODEL=支持工具调用的模型名
```

三项填写后重启 `python web.py`，选择“真实模型”。两组各自产生模型请求；密钥保留在服务端，`.env` 不进入 Git。

### 使用命令行

```bash
python main.py -C examples --test-generation --max-turns 12 \
  --max-output-tokens 4096 --max-tokens 30000 \
  --print "为 solution.py 生成 pytest 测试，覆盖正常值与包含边界"
```

`examples/solution.py` 中的 `classify` 约定区间内返回0、下方返回−1、上方返回1，包含两个端点。将 `-C examples` 换成自己的工作区，确保包含 `solution.py`。

| 策略 | 命令选项 |
|---|---|
| A0：通用 | 去掉 `--test-generation` |
| A4：候选验证 | `--test-generation` |
| A5：开发故障反馈 | `--fault-feedback` |

去掉 `--print` 进入连续对话，输入 `exit` 退出；Ctrl-C 中止当前任务。`--mode json` 输出逐行事件，`--no-session` 关闭默认保存到工作区 `.sessions/` 的脱敏轨迹；完整参数见 `python main.py --help`。CLI 缺少配置时提示使用 Mock，Web 的真实模式在缺少配置时不可选。

</details>

## 结果与验证

最终产物是 `test_solution.py`；A4/A5 另有 `testgen_report.json`，A5 另有 `fault_feedback.json`。CLI 写入指定工作区；Web 通过页面下载测试、验证报告与运行记录，需在服务结束前保存。

测试有效性、语句/分支覆盖率、固定故障检出和运行成本分别报告。空测试、全部跳过、采集不完整或目标源码被改写不能确认为有效。未配置的故障池与未测量指标标注为未测；覆盖率不能替代断言的判别力，参考通过表示与参考实现一致。

运行工程回归、统计复核与离线工具闭环：

```bash
python -m pytest tests/ -q
python scripts/reproduce_submission.py
python scripts/demo_offline.py
```

统计复核检查280条既有记录的成员、固定分母、均值和配对统计，成功输出 `all_matches: true`。离线闭环实际读取源码、写入测试并执行 pytest，预期5项测试通过。以上均无需模型密钥，不重新生成真实模型实验或改写冻结记录。

## 代码与设计

| 入口 | 内容 |
|---|---|
| [src/code_agent/](https://github.com/kyrie21z/Kytest-Agent/tree/main/src/code_agent) | Agent 循环、集中装配、模型适配、工具与测试生成状态 |
| [eval/](https://github.com/kyrie21z/Kytest-Agent/tree/main/eval) | 独立测量、实验冻结、运行与结果汇总 |
| [tests/](https://github.com/kyrie21z/Kytest-Agent/tree/main/tests) | 工程行为与执行事实的回归测试 |
| [Design.md](Design.md) | 需求、架构、机制、预算和设计取舍 |

Agent 核心使用 Python 标准库；pytest、coverage 与 SciPy 用于执行、测量及统计。项目支持自包含的 Python 函数测试，复杂依赖、服务与跨系统集成不在当前支持范围内。

<details>
<summary><strong>常见问题</strong></summary>

| 问题 | 处理 |
|---|---|
| 没有密钥 | 查看保存案例或运行脚本演示；真实生成需填写三项模型配置 |
| pytest/coverage 不可用 | 激活虚拟环境，在同一解释器中运行 `python -m pip install -r requirements.txt` |
| Bubblewrap 不可用 | 检查安装及用户命名空间支持；保存案例仍可查看，`trusted` 仅用于受信本机代码 |
| 8765端口占用 | 运行 `python web.py --port 0`，使用终端打印的地址 |
| 等待过久或预算结束 | 查看结束状态，可停止后续动作；累计 token 与任务时间为轮间软限制 |

默认隔离依赖 Bubblewrap，虚拟环境放在 Linux 文件系统中可避免含空格路径带来的执行问题。候选验证限制测试形式；复杂契约和预期值仍需审核。总体质量判断依据完整实验，展示样例只代表对应运行。

</details>

GitHub 仓库：[kyrie21z/Kytest-Agent](https://github.com/kyrie21z/Kytest-Agent)

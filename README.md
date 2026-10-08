# Kytest Agent：Python Test Generation Agent

为 Python 函数生成、执行和修正 pytest 测试。提供**通用生成**与**契约验证**两种路径，在同一输入下并行展示工具调用、测试质量和运行成本。

**[下载 57 秒演示视频](https://raw.githubusercontent.com/kyrie21z/Kytest-Agent/main/docs/demo.mp4)** · [快速开始](#快速开始) · [设计](Design.md) · [评价结果](docs/evaluation.md)

![同一输入下的测试与运行成本对比](docs/demo-overview.png)

保存的区间旋转案例中，通用生成有 6 项测试失败；契约验证的 6 项测试全部通过，检出 3/4 个固定故障。它是筛选的展示案例，不能代表总体质量；截图与视频来自同一题的两次独立运行。

## 两种生成路径

![共享 Agent 循环与两种生成路径](docs/agent-architecture.png)

| 路径 | 如何生成与验证 | 适合观察什么 |
|---|---|---|
| 通用生成 | 模型自主读取源码、写测试、运行命令 | 自主编排与修正过程 |
| 契约验证 | 候选附契约与预期值依据，逐条执行、合并回归后保留 | 每项测试的接受、拒绝与修正依据 |

两组共享核心、输入、模型配置和名义预算，各用独立工作区。生成结束后采用相同的参考复验、覆盖率与固定故障评价；评价结果不回灌模型。界面中的 A0、A4 分别对应这两条路径。

## 快速开始

推荐 Ubuntu / Ubuntu WSL，Python ≥3.9。首次体验无需模型密钥。

```bash
sudo apt install python3-venv bubblewrap
git clone https://github.com/kyrie21z/Kytest-Agent.git
cd Kytest-Agent
python3 -m venv ~/.venvs/kytest-agent
source ~/.venvs/kytest-agent/bin/activate
python -m pip install -r requirements.txt
python web.py
```

打开 **http://127.0.0.1:8765**，点击 **“查看已保存差异案例”**，即可查看真实运行的工具轨迹、测试和评价。按 Ctrl-C 结束服务；端口占用时使用 `python web.py --port 0`。

从提交包开始时，先进入 `code-agent/`，再从创建虚拟环境这一步执行。

## 运行自己的任务

1. 复制 `.env.example` 为 `.env`，填写 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`，重启服务并选择“真实模型”。
2. 输入源码与任务，点击 **“同一输入对比 A0 / A4”**，同时启动两组 Agent。
3. 查看执行过程、测试与质量评价，下载测试、验证报告和运行记录。

无密钥时也可选择“离线演示”，以固定模型响应实际运行工具与 pytest。它展示机制，不能用于比较模型能力。操作、CLI 和可选开发故障反馈见[使用说明](docs/demo.md)。

## 验证与适用范围

```bash
python -m pytest tests/ -q
python scripts/verify_evaluation.py
python scripts/demo_offline.py
```

工程测试检查执行与状态管理；统计复核核对既有实验的 180 条记录，成功输出 `all_matches: true`；离线演示预期生成 5 项通过的测试。三者均无需模型密钥。

项目支持自包含的 Python 函数。契约验证能约束候选形式并保留通过项，预期值仍需审核。默认命令隔离依赖 Bubblewrap；不可用时拒绝执行。Agent 核心使用标准库，pytest、coverage 和 SciPy 分别用于测试执行、测量和统计。

代码位于 [`src/code_agent/`](https://github.com/kyrie21z/Kytest-Agent/tree/main/src/code_agent)，工程测试位于 [`tests/`](https://github.com/kyrie21z/Kytest-Agent/tree/main/tests)。架构与取舍见 [Design.md](Design.md)，实验结论与证据见[评价说明](docs/evaluation.md)。

GitHub 仓库：[kyrie21z/Kytest-Agent](https://github.com/kyrie21z/Kytest-Agent)

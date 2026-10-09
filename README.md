# Kytest Agent：Python Test Generation Agent

*Generate, execute, and validate pytest tests with an LLM-powered coding agent.*

读取 Python 源码，调用工具生成并执行 pytest 测试，再根据执行反馈修正测试的 Code Agent。主要面向自包含 Python 函数；提供通用生成与契约验证两条共享核心的路径。

[Demo](#demo) · [快速开始](#快速开始) · [Design](Design.md) · [Evaluation](docs/evaluation.md) · [GitHub 仓库](https://github.com/kyrie21z/Kytest-Agent)

## 工作流程

**输入：** Python 源码与测试任务。**处理：** Agent 读取文件、生成测试、执行工具、获取反馈并继续修正。**输出：** pytest 测试文件、工具轨迹及已完成的验证记录。

与一次返回代码的 LLM 请求相比，这里有实际文件操作与测试执行反馈。Agent 是否执行成功需要查看工具结果；模型说“完成”并不能证明测试通过。

## 快速开始

推荐 **Ubuntu / Ubuntu WSL、Python 3.11**，最低 Python 3.9；CI 检查覆盖 3.9、3.11 与 Ubuntu 24.04 默认的 3.12。请确保 `python3` 指向所选版本。命令执行需要 Linux Bubblewrap 及允许用户命名空间的宿主策略。原生 Windows 未作为等价执行环境验证；隔离边界见[安全说明](docs/security.md)。

```bash
sudo apt-get update
sudo apt-get install python3-venv bubblewrap
git clone https://github.com/kyrie21z/Kytest-Agent.git
cd Kytest-Agent
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python web.py
```

服务输出本地地址；打开 **http://127.0.0.1:8765**，点击 **“查看已保存差异案例”**。成功后能看到标为保存案例的历史工具轨迹、测试与结果，**不会请求模型或生成新测试**。按 Ctrl-C 结束服务；端口占用时用 `python web.py --port 0`，访问输出的地址。

| 体验 | API Key | 实际行为 |
|---|---|---|
| Saved Case／保存案例 | 无需 | 读取已保存的真实运行记录，不请求模型、不执行新生成 |
| Offline Demo／离线演示 | 无需 | 使用预定义模型响应，实际调用工具并执行 pytest |
| Real LLM／真实模型 | 需要 | 请求配置的模型，读取输入并生成、执行和修正测试 |

验证无密钥的离线闭环：

```bash
python scripts/demo_offline.py
```

成功时脚本在临时工作区生成测试，实际执行 pytest，并输出 **`pytest exit=0；5 passed`**。临时文件随演示结束清理；整个过程不请求真实模型，模拟 token 用量不代表真实成本。

若 Ubuntu 上出现 `Failed RTM_NEWADDR: Operation not permitted`，按[安全说明](docs/security.md#默认-sandbox)检查 Bubblewrap 的 AppArmor 授权；隔离失败不会自动切换执行模式。

运行自己的新任务时，复制 [`.env.example`](.env.example) 为 `.env`，填写 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`，重启服务并选择“真实模型”。完整配置见[使用说明](docs/demo.md#配置真实模型)。不同模型、预算与运行可能产生不同结果。

## Demo

![同一输入下的测试与运行成本对比](docs/demo-overview.png)

[观看或下载 57 秒演示视频](docs/demo.mp4)：同一输入下并行执行 A0 / A4，展示工具调用、测试评价、轮次与 token。等待片段为 8 倍速。

截图对应已保存的区间旋转案例：A0 有 18 项通过、6 项失败；A4 的 6 项全部通过，检出固定故障 3/4。视频来自同一题的另一次真实运行，A4 检出 4/4。它们是精选单例，不能代表总体质量；点击保存案例只是读取历史记录。操作与指标解释见[演示说明](docs/demo.md)。

## 生成模式

![共享 Agent 循环与两种生成路径](docs/agent-architecture.png)

| 路径 | 生成与验证方式 | 使用限制 |
|---|---|---|
| A0／通用生成（默认） | 模型自主读取源码、写测试、运行命令并修正 | 是否充分执行和验证取决于实际工具轨迹 |
| A4／契约验证 | 候选附契约与预期值依据，逐条执行、合并回归后保留 | 支持有限、可检查的测试形式；预期值仍需审核 |

两者共享 Agent 核心、工具执行边界与模型配置；Web 对比使用独立状态与工作区。最终参考复验、覆盖率与固定故障评价采用相同流程，不回灌模型。A4 的总体质量优势尚未通过预设验收，详见[评价说明](docs/evaluation.md)。可选的 A5 开发故障反馈入口见[CLI 操作说明](docs/demo.md#命令行)。

## CLI 与 Web

Web 中输入源码和任务，点击“同一输入对比 A0 / A4”同时启动两组 Agent，查看工具参数、结果与成本，下载测试和验证记录。选择“离线演示”只运行固定示例；自由输入生成需要真实模型配置。

CLI 在指定工作区运行：

```bash
python main.py --help
python main.py -C examples --test-generation --print "为 solution.py 生成 pytest 测试，覆盖正常值与包含边界"
```

去掉 `--test-generation` 使用 A0；将 `-C examples` 换成自己的源码工作区。详细操作、预算、事件输出和恢复说明见 [docs/demo.md](docs/demo.md)。

## 安全与局限

默认命令隔离使用 Linux Bubblewrap，限制宿主路径、网络和执行环境；隔离不可用时拒绝执行。`trusted` 是显式选择，会给予代码宿主进程的实际权限，不适用于不可信输入。Web 监听本地 Loopback，不为未经认证的公网多用户部署设计。

不要在源码、任务或公开运行记录中放入密钥。项目主要面向自包含 Python 函数；pytest 通过不保证预期值完全正确，覆盖率不等于测试质量。执行边界、凭据与任务范围见 [docs/security.md](docs/security.md)。

## 评价与工程验证

评价检查测试有效性、覆盖率、固定故障检出，以及调用、token 和时间成本。固定故障分数只适用于对应故障集合；既有 A0–A5 矩阵、统计结论及证据见 [docs/evaluation.md](docs/evaluation.md)。

```bash
python -m pytest tests/ -q
python scripts/demo_offline.py
python scripts/verify_evaluation.py
```

工程测试覆盖执行、状态管理、Sandbox 与 Web HTTP 路径；离线演示验证实际工具闭环；统计复核应输出 `all_matches: true`，只核对已有 180 条记录与派生统计，**不重新执行模型实验或完整程序重放**。这些检查均不需要 API Key。

## 文档与许可证

- [Design.md](Design.md)：架构、工具协议与设计取舍。
- [docs/demo.md](docs/demo.md)：真实模型配置、Web / CLI 操作与演示素材。
- [docs/evaluation.md](docs/evaluation.md)：指标、实验矩阵与证据边界。
- [docs/security.md](docs/security.md)：执行权限、平台限制与适用范围。
- [Apache-2.0](LICENSE) 与[第三方材料说明](docs/third-party.md)：原创代码授权及独立素材许可。

源码位于 `src/code_agent/`，工程测试位于 `tests/`。Agent 核心使用标准库；pytest、coverage 与 SciPy 分别用于测试执行、测量与统计。

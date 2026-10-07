# Code Agent：代码助手与测试生成

一个可通过CLI交互的代码助手，主要演示任务是为Python函数生成可运行的单元测试。
核心流程是**输入 → LLM → 工具调用 → 工具结果回灌 → 输出**，运行层只依赖Python标准库。

## 1. 运行

以下命令在包含`main.py`的项目根目录运行。

Python ≥3.9。命令执行默认使用Linux/WSL的Bubblewrap隔离；Ubuntu可用
`sudo apt install bubblewrap`安装。测试依赖用以下命令安装：

```bash
python -m pip install -r requirements.txt

# 不需要密钥：用脚本化模型、真实文件工具和pytest演示完整闭环
python scripts/demo_offline.py
# 预期：生成5项测试并实际执行，通过后报告任务完成

# CLI离线交互；Mock明确标记，不作为真实模型效果证据
python main.py -C examples --mock --no-session --print "解释 solution.py"
```

## 2. 使用真实模型

复制`.env.example`为`.env`，填写自己的OpenAI兼容服务配置：

```dotenv
LLM_API_KEY=你的密钥
LLM_BASE_URL=服务的兼容API地址
LLM_MODEL=支持工具调用的模型名
```

```bash
# 默认通用Agent，可连续对话；exit退出，Ctrl-C中止当前任务
python main.py -C examples

# 可选测试生成模式：候选契约、逐条验证、保留已接受测试
python main.py -C examples --test-generation --max-turns 12 \
  --max-output-tokens 4096 --max-tokens 30000 \
  --print "为 solution.py 生成测试，覆盖正常值和包含边界"

# 可选开发故障反馈；仍属实验功能
python main.py -C examples --fault-feedback --max-turns 12 \
  --print "为 solution.py 生成测试"
```

示例函数`classify(value, low, high)`约定：区间内返回0，下方返回−1，上方返回1。
例如`classify(2, 2, 8) == 0`。测试生成模式输出`test_solution.py`及
`testgen_report.json`；反馈模式另有`fault_feedback.json`。

`.env`不进入提交包；缺少模型配置时CLI明确提示退回Mock。`--mode json`输出
逐行事件，普通`--print`只向stdout写最终回答。默认会话保存到工作区的`.sessions/`。

## 3. 验证

```bash
python -m pytest tests/ -q
python scripts/reproduce_submission.py
```

前者验证提交包内的核心回归子集；完整研究回归保留在仓库。后者从280行派生
记录重算两组实验均值和配对统计，不请求模型、不重写历史记录。
已从ZIP独立解压验证：258项通过、4项Windows专用检查跳过；环境为Python
3.13.13、pytest 9.1.1、SciPy 1.18.1。回执见`submission/evidence/acceptance.json`。
真实模型工具闭环样例见`submission/evidence/real_run/`，为明确标注的展示样例。

## 4. 设计与实验结论

- [Design.md](Design.md)：组件职责、执行流程、接口、错误处理与取舍。
- [EXPERIMENTS.md](EXPERIMENTS.md)：A0～A5定义、两组主要对照及证据边界。

默认保留通用Agent。最新20题重复实验中，A0/A4/A5确认独立检出率为
68.81%/74.94%/74.90%，**质量优势未通过预设统计验收**。功能可运行与总体质量
提升是两个不同结论；覆盖率、参考通过也不能代替有效断言与故障判别力。

## 5. 常见问题与范围

| 问题 | 处理 |
|---|---|
| 没有API Key | 可运行离线演示；真实模型任务需自行配置 |
| pytest不可用 | 在启动Agent的同一Python环境安装requirements |
| Bubblewrap不可用 | 默认拒绝执行；可用`disabled`禁用命令，或明确选择`trusted`处理受信本机代码，后者拥有宿主权限 |
| 工具参数、路径或调用失败 | 作为可定位的观察结果回灌；按步骤、请求及命令边界结束 |
| 测试通过但发现不了缺陷 | 通过只说明兼容参考；检查独立预期值和能区分错误行为的边界输入 |

支持函数级Python测试生成，不承诺任意仓库环境、所有自然语言契约或复杂oracle
都可自动验证。总token预算在请求之间检查，是软上限。

## 提交与档案

```bash
python scripts/build_submission.py --output /tmp/code-agent-coursework
```

此命令按白名单构建提交目录及ZIP：保留运行代码、核心回归、演示和精简证据。
完整研究仓库：[Kytest-Agent](https://github.com/kyrie21z/Kytest-Agent)；
[精简前冻结版本](https://github.com/kyrie21z/Kytest-Agent/tree/e34bb5c8770f85815612e5669a50a02a0c5f5532)
保留全部历史实验、源码快照和详细报告。作业原要求提交压缩包小于200M，
最终上传时应以“学号姓名”命名；本项目不包含身份信息或可选视频。

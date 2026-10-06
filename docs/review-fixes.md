# 复评整改验收

报告中的四项问题已在 `code-agent/` 修复。完整回归：**214 passed、4 skipped、0 failed**。
新增32项行为验收；4项跳过均为Windows命令行解析检查。当前验证环境为Linux/WSL、
Python 3.13.13，版本明细见 verification/review-fixes/environment.json。

| 对应问题 | 当前行为 | 验收证据 |
|---|---|---|
| F3 取消后新任务失效 | 新任务解除取消并重设任务预算；同任务checkpoint共用预算。中断的工具批次补齐结果，剩余调用不执行。 | 真实CLI SIGINT后实际产生第二次HTTP请求并完成；轮数、调用数和token预算回归通过。 |
| A4 凭据落盘 | 已知密钥、带前缀环境变量、JSON敏感键、嵌套工具参数及输出脱敏，事件结构与非敏感字段保留。 | 原评审模拟值均不再落盘；普通事件、路径和token计数仍可读取。 |
| Q3 命令边界与读取内存 | 默认Bubblewrap仅挂载工作区与只读运行库，隔离网络；工作区遵循ALLOW_WRITE。生成测试的评测进程也隔离。输出与长行按有界长度读取。 | 外部哨兵及越界符号链接不可访问；只读下命令写入失败；8MiB无换行输出只保存1000字符，父进程Python分配峰值283507字节。另测16MiB输出与8MiB文件长行均通过内存上限断言。 |
| D2 统计及文档口径 | 保留原始JSON/CSV/summary/report，从input+output生成input-output-v1派生数据；杀伤率保留小数，非有限统计量报错。三份文档共用生成表格。 | A0/A1/A2/A3均值为25079.35、34034.10、14829.80、12770.15；主比较p值0.4652088、0.7150007、0.5929801，与独立参考计算一致。 |

当前默认安全执行依赖 **Linux + Bubblewrap**。不可用时拒绝命令执行，不自动回落。
Windows/macOS可继续使用文件工具；受信本机代码可显式选择trusted模式，其宿主机权限
边界见README。Windows实际执行未在本次现场验证。

5份历史A0测试套件各在正确实现上复跑3次，分别检测独立注入的故障并在恢复后通过。
80份历史运行的源码、测试副本与记录内部一致；951份已有results文件的SHA-256保持不变
（修订的ANALYSIS文档不计入历史原始文件）。原压缩包及两份评审报告保留。

没有新增真实模型采样或外部模型请求。上述统计属于历史记录的重新分析，
不认证历史模型调用的外部真实性，也不证明修复后版本与历史版本的模型表现等价。
token数量不代表实际收费。本整改说明不另行给出评审分数。

复验命令（先按requirements.txt安装测试与分析依赖）：

```bash
python -m pytest tests/ -q -ra
python scripts/analyze_ablation.py --write-docs
```

派生数据位于 `results/v2_ablation/derived/v1/`，包含CSV、summary、输入SHA-256清单、
配对检验、表格及报告。第二条命令保留原始数据并同步README、Design和ANALYSIS中的标记表格。

完整输出与复评脚本的新副本保存在 `verification/review-fixes/`。
`verify_fixes.py` 检查保存的行为证据、当前统计、表格一致性和历史文件哈希，输出acceptance.json。
本次运行所有检查通过；pytest.log保存完整回归结果。旧评审证据目录没有改写。

```bash
python verification/review-fixes/verify_fixes.py .
```

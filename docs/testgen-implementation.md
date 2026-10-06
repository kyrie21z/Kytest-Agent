# 测试生成实现与验收

目标是让新增测试具备可审核的契约/oracle/故障依据，并避免一条错误或超时测试
破坏整份套件。CLI `--test-generation` 与实验A4共用生产工具和同一Agent循环。

1. `submit_tests` 每次提交至多6个自包含候选，每条记录docstring原文、输入域、
   oracle推导和具体故障假设。按显式范围、正整数、非空及正整数列表约束检查
   可解析字面量；未知表达式不伪装成完整验证。预条件不自动推导成异常承诺。
2. 每候选在只含原SUT和该候选的隔离目录中执行，2秒超时并清理进程树。
   错误断言、语法/收集错误、超时及SUT改写分别反馈。批次返回保持完整JSON，
   详细诊断落入testgen_report.json。缺pytest或缺隔离执行能力时拒绝。
3. 候选通过后跑5秒合并回归，确认与既有测试兼容才接受。接受的名字不可重写，
   不同导入别名独立绑定。已有用户测试作为基底保留，不能默默丢弃；基底失败时
   原文不变。每轮恢复原SUT和接受的套件，不使用pytest通过作为提前停止条件。

反馈是参考实现上的执行结果，不暴露最终评分变异体。元数据是可审核的模型声明，
不是规范正确性的证明；通过也不保证新增缺陷检测能力。A5通过 `--fault-feedback`
开启定向补测：私有接受套件先在原实现通过，再执行最多8个开发故障候选。
每次返回至多3条具体未检出改动，完整开发记录保存到fault_feedback.json；
最多两轮已改变套件的查询。评分池按不同家族独立保留，AST指纹无交集。
协议见docs/fault-feedback.md。旧变异引擎移入生产模块，所有冻结实例的候选
元数据与源码逐一比较，算法输出不变。

回归证据：258 passed、4 Windows专属跳过、0 failed，见
verification/testgen-v1/pytest.log。新增44项验收覆盖错误oracle、逐条超时、
输入约束、局部import、导入冲突、保留已有测试、修改SUT拒绝、权限/体积/预算、
CLI真实HTTP闭环、共同Python/pytest环境、具体故障反馈、缓存/两轮预算、超时不计检出、
反馈/评分AST分离、批量统一评分池、拒绝混用旧记录与环境不可比结果不得晋级。
历史966份数据/基准文件的SHA-256未变。五份冻结数据集共353个条目核对变异引擎
输出完全相同，开发/评分AST池无交集，见engine-compatibility.json。

开发试验见docs/testgen-pilot.md。v1因A0使用缺pytest的系统Python而不可比较，
整轮30个run和源码保留，不能作为A4优势证据。修正PATH与共同命令硬上限后，
v2重新冻结并运行30个run。源码快照、输入哈希、完整任务序列和实际token均保留。
五个开发实例的结果不能外推为独立评测优势。

有效v2的30个run：两条件通过率与有效杀伤率均100%；A0/A4 token均值为
21234.93/21326.47，生成秒数为28.89/43.56。A4耗时增加50.8%，未达到事先冻结
的严格质量增益条件，未启动完整评测，也未替换通用默认模式。
这些run评估的是A4；新增A5只有控制演示与功能回归证据，尚无真实模型质量结论。
verification/testgen-v1/pilot-replay.json记录独立重放全部30份有效套件：参考测试与
每份评分池的杀伤数均与原始记录相同，32份冻结文件及派生汇总也一致。
fault-demo/receipt.json记录生成结束后评分的控制演示，检出从0/2到2/2。

复验：

```bash
python -m pytest tests/ -q -ra
python scripts/demo_testgen.py
python scripts/demo_fault_feedback.py
python scripts/audit_ablation_mechanisms.py
python scripts/run_testgen_pilot.py --report-only
python scripts/verify_testgen_evidence.py --receipt /tmp/kytest-pilot-replay.json
```

后两条不调用模型；最后一条重放全部保存套件及其变异测试。重新模型采样必须使用新输出目录；
代码/协议/数据改变后不允许续跑旧实验目录。受支持环境为当前Linux/WSL沙箱；
其它平台需自行验证，trusted模式只能用于受信代码。

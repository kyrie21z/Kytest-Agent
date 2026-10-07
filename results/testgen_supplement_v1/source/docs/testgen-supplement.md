# A1–A3正式20例补测协议（模型请求前冻结）

用户批准补齐修复后版本的消融证据。本轮只新增A1/A2/A3各20次，共60个真实
模型run；重用testgen_formal_v1的A0/A4各20份记录形成100份描述性对照。
不重采样A0/A4、不启用A5、不按结果改提示词、策略或变异池。

1. 全部使用humaneval_plus_v2_20.jsonl原20例，每条件每例一次。继承正式轮的
   qwen3.7-flash、temperature=0.2、12 turns、单请求输出4096、累计30000
   input+output token软上限、上下文32000字符、60秒请求、1次网络重试。
   生成300秒在turn间检查，通用命令硬上限10秒；实际超额照实保留。
2. A1提示与通用工具不变；A2仍最多4次系统pytest、通过即收尾；A3仍最多
   4次系统pytest、2轮覆盖率反馈。内部pytest 90秒、coverage执行180秒及
   JSON导出120秒上限保持不变；全部内部验证时间属于生成成本，可能越过
   turn间的软时限。只修复延后评分包装层的日志state透传；不改变执行决策。
3. 并发2，60任务用seed=20261006固定打乱，该seed不控制模型随机采样。
   不采checkpoint分数。生成结束后统一评分：参考pytest 10秒、coverage
   20秒、每评分变异体5秒；原六家族确定性前20个，超时不计检出且留分母。
4. 主分数沿用有效杀伤率：原实现all_pass且未改写SUT才计killed/total，否则0。
   总变异体数来自冻结原SUT；无套件、异常、超时均保留在ITT。结构上无变异体
   才披露并排除杀伤率均值。系统钩子曾恢复被改写SUT也标记修改，不能逃过门槛。
   同时报告原始杀伤率、通过率、覆盖率、token、生成/评分耗时、实际预算超额。
5. 补测前固定三项配对：A1−A0、A2−A1、A3−A2。报告20实例平均差、10000次
   bootstrap 95%区间、Wilcoxon双侧p、三项Holm校正、改善/持平/退步。
   全持平时明确标注且p=1。A4−A0原结论保留，不重新纳入新的多重比较族。
   统计A2/A3的PASS/FAIL/TIMEOUT、系统执行次数、coverage_full/incomplete、
   激活补测的实例数及SUT恢复行为；零激活时不声称验证了定向补测效果。

A0/A4先前已运行，A1–A3是后来补测，不是五条件同期随机实验。记录重用原件
SHA-256、全部共享模型配置和源文件差异；跨批次A1−A0为探索性对照，存在时间/
服务变化混杂。一次采样、曾评测过的20例与可能等价变异体限制总体解释。
若需稳定优势结论，应另行预注册五条件交错重复；本授权不启动该扩展实验。

先核验同一Python/pytest及沙箱文件、凭据和网络边界，保存环境和源码快照。
60次全部生成完成后，独立离线重放保存套件与全部评分变异体，保留原记录、
报告任何差异，不用重放结果替换失败采样。历史及A0/A4已发布文件保持字节不变。

```bash
python scripts/run_testgen_supplement.py --prepare-only
python scripts/run_testgen_supplement.py
python scripts/run_testgen_supplement.py --report-only
```

默认输出results/testgen_supplement_v1；仅prepare-only和report-only不调用模型。

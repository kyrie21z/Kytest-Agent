# 历史机制复核

2026-10-06离线重放保存测试，未新采样模型。observations.json记录当前Linux沙箱下的
3秒诊断上限、原测试SHA-256、pytest原始输出；该上限不是历史上限，不能替代历史成绩。

mechanism-counts.json直接按80份原始记录统计动作：A3有18次coverage_full，
0次coverage_incomplete；两个退步实例在覆盖率阶段前TIMEOUT。
mutation-diagnostics.json重放HumanEval128的A0/A1套件，确认A1漏检乘法改除法；
159的<=改<在两个分支交界处返回相同值，是等价变异体，80%不是可改进余量。

冻结JSON、测试、CSV和summary均未改写；文档中的错误机制解释已修正。

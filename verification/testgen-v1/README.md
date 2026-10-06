# 测试生成验收（2026-10-06）

目录名v1指本次验收包，包含有效开发试验v2的重放；不代表环境诊断轮可比较。

1. pytest.log / acceptance.json：258 passed、4 Windows专属跳过、0 failed。
2. demo/：真实生产工具处理错误oracle、非法输入、修复与增量保留；脚本化LLM。
3. fault-demo/：真实Agent与沙箱的定向补测；生成结束后测量独立边界故障，0/2→2/2。
   该控制演示不构成真实模型质量提升证据。
4. pilot-replay.json：离线重放有效v2全部30份套件的参考测试和所有评分变异体，
   核对32份冻结文件和汇总，结果均一致。
5. protected-files.json：原有966份数据/基准文件与父提交字节一致；两轮各32份
   试验源码快照均符合各自请求前manifest。历史ANALYSIS文字勘误单独提交。

engine-compatibility.json补充核对五份冻结数据集的353个条目：变异引擎输出与
试验冻结版逐一相同，开发/评分AST池无交集。

有效30-run结果见results/testgen_pilot_v2/report.md；环境不公平的首轮完整保留
在results/testgen_pilot_v1并标记不可比较。A4没有达到冻结的质量增益条件，
不替换默认模式、不进入完整评测。A5暂无真实模型对照结果。

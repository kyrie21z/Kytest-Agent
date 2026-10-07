# 正式20例验收

1. admission-tests.log：83项相关检查通过。pytest.log：262 passed、4项Windows专属跳过。
2. protected-files.json：父提交ba48816中的1161份已发布数据/基准文件字节未变。
3. replay.json：40个任务、37份冻结代码/数据/协议哈希和保存套件的独立离线重放。
4. minpath-domain-audit.json：单案例的事后敏感性复验；不替换预注册主分数。
5. acceptance.json：最终成本、超额软预算、联网/改写行为及验收计数。

原始模型记录在results/testgen_formal_v1/A0和A4；完整运行配置、任务次序和输入
SHA-256在manifest.json，实际源码在source/。manifest中的source_revision是
工作基线提交；冻结文件哈希和源码快照才定义本轮实际执行内容。

40个真实模型run全部进入ITT；只比较当前A0/A4，不混入历史A0或五例开发结果。
同一模型每例仅一次采样，正式集曾经用于评测与失败分析，不称为新未见保留集。

# 测试生成质量 v2 验收

1. manifest.json / source/：最终实现、协议、相关测试与核验脚本的冻结源码和SHA-256。
2. pytest.log：发布版本完整项目tests/；294项通过、4项Windows专属跳过。
3. demo-receipt.json / accepted-tests.json：真实Agent、脚本化LLM、沙箱和pytest的自动开发反馈闭环。开发故障检出1/3→3/3，新增M1/M2，停止原因为development_targets_exhausted。
4. independent-replay.json / before.tests.py / after.tests.py / solution.py：生成结束后由独立eval测量器重放，保留家族故障检出0/2→2/2，原实现始终通过；开发与评分池AST无交集。
5. protected-files.json / acceptance.json / verify_evidence.py：此前1507份研究文件未变，及可重复执行的回执核验。

没有请求真实模型。该小型受控演示验证机制与反例修复，不估计总体收益；
此前100份模型记录属于旧生成/测量版本，不作为新A4/A5成绩。
验收需在对应发布提交运行；以后代码演进应另建新证据，不覆盖本快照。

```bash
python verification/testgen-quality-v2/verify_evidence.py
```

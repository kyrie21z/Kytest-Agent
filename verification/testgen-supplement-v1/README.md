# A1–A3补测验收

1. admission-tests.log / pytest.log：窄范围37项通过；项目tests/共268项通过、4项Windows专属跳过。
2. protected-files.json：父提交15e7733已发布的1284份results/benchmarks文件SHA-256。
3. replay.json / effective-replay.json：60份套件独立重放；参考通过状态和有效主分数60/60一致，原始变异计数59/60一致。独立汇总100份原记录与主报告一致。
4. diagnostics.json / prime-fib-variability.json：8份失败套件、100份有限字面量域检查、minPath敏感性以及两次固定种子控制；均不替换主分数。
5. acceptance.json / verify_receipts.py：最终验收及无需调用模型或重新评分的文件与重放回执核验。

源码、协议、数据和任务次序冻结于results/testgen_supplement_v1/manifest.json
和source/；A0/A4重用路径与每份文件哈希同样记录。共享引擎唯一变化为延后
评分包装层透传日志state，不改变提示词、生成决策或停止条件。

模型生成记录不可由重放结果替换。五条件分属两个采样批次且每例仅采样一次；
跨批次比较为探索性，未显著不证明等价，机制未激活不证明机制无效。

原始replay.json的all_match=false保留：A1/prime_fib原先12检出/8超时，重放
13检出/7超时。种子0/1分别复现13/7与12/8，差异在M18；参考套件始终失败，
有效主分数始终为0。不能将这次验收描述成全部原始计数确定性复现。

```bash
python verification/testgen-supplement-v1/verify_receipts.py
```

# 复评整改验收证据

源码完整回归：214通过、4项Windows专用检查跳过。acceptance.json记录逐项验收。
行为检查仅使用本地合成HTTP服务、模拟凭据和临时文件；没有真实模型请求。

在项目根目录，安装requirements.txt中的依赖后运行：

```bash
python verification/review-fixes/verify_fixes.py .
```

该命令检查保存的证据、当前统计及文档一致性，并验证951份历史results文件的SHA-256。
要重新执行行为探针，可运行：

```bash
python verification/review-fixes/independent_checks.py .
python verification/review-fixes/additional_checks.py .
python verification/review-fixes/interactive_abort_probe.py .
python verification/review-fixes/analysis_consistency.py .
```

生成的新输出会写回本目录。interactive_abort_probe的实际SIGINT检查需要POSIX。
验收说明见../../docs/review-fixes.md。统计重算由scripts/analyze_ablation.py提供，
历史输入JSON/CSV/summary/report保留，当前口径使用derived/v1派生数据。

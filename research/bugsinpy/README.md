# BugsInPy 探索脚本归档

这些脚本用于早期数据集可执行性、项目选择和 fail-to-pass（F2P）样例探索，不参与当前 Agent、评价或演示流程。它们从 `scripts/` 原样迁移，保留当时的硬编码工作目录和运行假设；没有合并或改写实验逻辑。

迁移前源码见 [8b03b4b 中的 scripts/](https://github.com/kyrie21z/Kytest-Agent/tree/8b03b4b/scripts)。历史实验的 `results/**/source/` 快照仍保留原路径与内容。

| 文件 | 原路径 | 用途 |
|---|---|---|
| [_recon_bugsinpy.py](_recon_bugsinpy.py) | `scripts/_recon_bugsinpy.py` | 检查 BugsInPy 元数据和项目分布 |
| [_pick_project.py](_pick_project.py) | `scripts/_pick_project.py` | 筛选可离线执行、可收集的项目 |
| [_probe_f2p.py](_probe_f2p.py) | `scripts/_probe_f2p.py` | 探查 buggy/fixed 执行差异 |
| [_sweep_f2p.py](_sweep_f2p.py) | `scripts/_sweep_f2p.py` | 初次批量筛选 F2P 样例 |
| [_f2p_sweep2.py](_f2p_sweep2.py) | `scripts/_f2p_sweep2.py` | 第二次探索筛选 |
| [_f2p_sweep3.py](_f2p_sweep3.py) | `scripts/_f2p_sweep3.py` | 第三次探索筛选 |
| [_diag_test.py](_diag_test.py) | `scripts/_diag_test.py` | 诊断目标测试未暴露缺陷的原因 |

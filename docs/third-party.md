# 许可证范围与第三方材料

仓库权利人已确认将本项目原创代码按根目录 [Apache-2.0](../LICENSE) 授权。该授权不替代第三方材料的原许可证，不表示本项目拥有这些材料的全部版权。

## 分发材料

| 材料 | 来源与处理 | 保留的授权与署名 |
|---|---|---|
| `src/code_agent/web/data/rotation.json`、`src/code_agent/web/examples.py` 中的旋转源码与故障副本 | Google Research 的 MBPP/304；保存记录同时包含本项目的任务、工具事件、生成测试和测量 | Google Research 原仓库 Apache-2.0；原许可保留在 [`web/data/LICENSE`](../src/code_agent/web/data/LICENSE) |
| `tests/fixtures/humaneval.jsonl` | 从 EvalPlus 的 HumanEval+ 发布包固定选取 30 例；字段重组与输入契约用于本项目离线工程回归，原 HumanEval 的参考断言并非 Plus 增强输入 | HumanEval 的 MIT 许可及 OpenAI 版权说明保留在 [HumanEval-MIT.txt](licenses/HumanEval-MIT.txt)，EvalPlus 的 Apache-2.0 许可及版权说明保留在 [EvalPlus-Apache-2.0.txt](licenses/EvalPlus-Apache-2.0.txt) |
| `docs/evidence/` | 本项目对 MBPP 实验结果的派生数值、任务标识、哈希与统计期望 | 不重新授权 MBPP 数据集；来源及原件可通过[评价说明](evaluation.md)与固定档案追溯 |
| `docs/demo-overview.png`、`docs/agent-architecture.png`、`docs/demo.mp4` | 本项目界面截图、架构素材与操作录制；可能显示第三方示例代码、模型输出和服务名称 | 项目原创展示部分不改变其中引用代码与其他第三方内容的授权；服务名称和标识不代表背书 |

固定 MBPP 来源为 Google Research 提交 `f82046ba5aabbbb427dbfd38a254d26bff08b533`，下载记录与原件保存在[开发档案](https://github.com/kyrie21z/Kytest-Agent/blob/development-archive-20261008/benchmarks/mbpp_quality_v2/download.json)。保存案例与故障副本用于本项目展示和测量，不能视为未经改编的上游数据集。

HumanEval 回归数据的选取与字段说明见[原有来源记录](https://github.com/kyrie21z/Kytest-Agent/blob/development-archive-20261008/benchmarks/DATASET.md)。本阶段只补充许可与署名，未改写数据、示例源码、已有媒体或统计记录。

## 上游依据

- [Google Research 根许可证](https://github.com/google-research/google-research/blob/f82046ba5aabbbb427dbfd38a254d26bff08b533/LICENSE)与 [MBPP 说明](https://github.com/google-research/google-research/tree/f82046ba5aabbbb427dbfd38a254d26bff08b533/mbpp)。
- [OpenAI HumanEval MIT 许可证](https://github.com/openai/human-eval/blob/master/LICENSE)。
- [EvalPlus Apache-2.0 许可证](https://github.com/evalplus/evalplus/blob/master/LICENSE)。

pytest、coverage 与 SciPy 通过依赖文件安装，各自保留上游许可证。本阶段未向仓库复制这些依赖的实现。开源协议也不授予第三方模型服务、商标或未知来源内容的额外权利。

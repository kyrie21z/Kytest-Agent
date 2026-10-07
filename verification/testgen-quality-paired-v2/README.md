# 当前v2新任务重复配对验收

本目录承接5a4e3bb的质量机制，修复代数消去型弱输出锚点，并记录新真实模型
验收。此前`verification/testgen-quality-v2/`是对应旧提交的独立验收快照；保留
原件，不要求它的源码哈希在后续修订上仍与活动文件相同。

1. `mechanism-acceptance.json`：新反例`r-r==0`在执行前拒绝；独立预期值的候选
   接受并实际检测`n+1`改成`n-1`，独立评分器的正确套件重放也通过。
2. `pytest.log`：306项通过，4项Windows专属跳过。24项SyntaxWarning来自保留的
   上游MBPP正则字符串，不改写官方原件；后续事件观察器的定向检查另行通过。
3. `protected-files.json`：历史results、benchmarks、verification共1563份旧文件
   的SHA-256与大小；后续验收必须证明这些字节未被新实验覆盖。
4. `../../results/testgen_quality_paired_v2/manifest.json`与`source/`：20个MBPP新任务，
   A0/A4/A5各3次生成，共180个run；源码、任务顺序、模型、预算与统计程序先于
   请求冻结。协议见`source/docs/testgen-quality-paired-v2.md`。
5. 新实验原件、`generation/`中的完整请求与工具观察、`summary.json`以及独立
   重放回执组成模型效果证据。脚本化机制检查不能代替这部分。

```bash
# 从已保存原件重新生成任务层配对报告；不调用模型
python scripts/run_quality_paired_v2.py --report-only

# 独立执行最终套件和A5反馈前后套件；不调用模型、不回写原件
python scripts/verify_quality_paired_v2.py \
  --receipt /tmp/quality-paired-independent.json
```

只有满足预注册的实际增益、区间、Holm显著性及有效产出率条件，才验收本轮
相对A0的质量优势；预算为轮间软上限，未知及可能等价故障保留分母。
公开MBPP可能存在模型预训练接触，本实验不宣称模型未见或真实缺陷迁移。

## 最终验收：生成完成，质量优势和严格重放未通过

180/180真实生成完成，20题每条件各3次；公共服务准入另外一次调用不计成绩。
`model-run.log`的180行与结果元组、状态和token逐项相同；无重复任务、无部分
轨迹重启。45份冻结文件与当前文件逐项SHA-256一致。

| 条件 | 有效产出 | 确认独立检出率 | 平均token | 生成秒数 |
|---|---:|---:|---:|---:|
| A0 | 49/60 | 68.81% | 20688 | 45.1 |
| A4 | 59/60 | 74.94% | 21827 | 53.0 |
| A5 | 59/60 | 74.90% | 16735 | 54.6 |

A4−A0为+6.13个百分点、区间[-5.12,+17.26]，A5−A0为+6.09、区间[-3.65,+16.07]；
两项Holm p均为0.7466。预设质量验收未通过，A5−A4未检出平均质量差异，也
不证明等价。默认保持A0，A4/A5为实验功能。配对统计独立复算全部一致。

`independent-replay.json`：冻结主分数180/180一致，参考状态、原始检出计数和
变异状态各179/180一致；`primary_all_match=false`，脚本退出1，完整日志见
`independent-replay.log`。唯一差异为A0/MBPP/71 repeat_1的随机大列表测试：
原始失败、主分数0；离线重放恰好通过、原始检出0/7变成5/7。0分保留，未替换
原始有效性、记录或分数；主分数一致不代表参考有效性复现成功。

`stochastic-reference-diagnostic.json`和同名日志：原参考在seed 0–999的1000份
输入中18次正确、982次排序错误。原套件在seed 0–19均失败，163/166均通过；
22次pytest与直接调用相符，源码未变。两项通过种子是搜索得到的诊断见证，
不是新增质量样本。上游实现gap降到0后可能提前结束，官方样例准入不足以
证明全域正确；有效产出率不能解释为oracle正确率。可重现：

```bash
python verification/testgen-quality-paired-v2/diagnose_reference.py
```

A5有59份套件经过开发检查、72个套件阶段，其中22个阶段反馈进入后续模型
请求；离线重放仅1份新增独立检出、0份丢失检出。MBPP/127 repeat_2从2/3到3/3，
不能据此证明总体因果收益。完整解释见
[CASE_ANALYSIS.md](../../results/testgen_quality_paired_v2/CASE_ANALYSIS.md)。

`model-artifacts.json`保存重放前589份原件的SHA-256与大小，
`model-artifact-preservation.json`证明重放后589/589不变；包括180份最终JSON、
178份套件、180份完整生成轨迹和45份源快照等。1563份历史文件同样不变。
`trajectory-audit.json`记录候选拒绝、工具错误、成本和停止原因；
`acceptance.json`分别记录软件、生成完成、严格重放差异及质量未验收。

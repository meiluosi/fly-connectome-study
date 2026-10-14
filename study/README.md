# fly-mb-compartments

问题：真实蘑菇体连线上，隔间划分的**内容**对持续学习中的遗忘有没有贡献？

## 结论（经独立审查与第二轮确认之后，详见 `study/RESULTS_round2_audit.md`）
这个项目的**主要发现是负面的**，并且包含一次被独立审查推翻的过程：
1. 门控隔间"减少遗忘"的优势**主要是学习量混杂**：预先登记的匹配学习量检验（两个电路，26 个可比格子，20 个等价、25 个均值为负）显示，匹配学习量下分隔间与不分隔间无实质差异，不分隔间甚至略少遗忘。
2. 有界乘法规则**不是**低遗忘的来源：无界加法规则在同样学习量下遗忘更少（22 个可比格子全部为负；MR 判定成立，FR 证据不足但方向一致）。
3. "同隔间 MBON 的 KC 输入重叠度因果影响遗忘"**未被确认**：控制 KC 入度同质性与学习量后，两个电路的偏回归系数都包含 0。
4. 真实 vs 打乱隔间的差异：男性数据有一致的小正差异，女性数据没有，未确认。
5. 回路不是更好的持续学习学习器：修正后的 EWC 最终准确率 8/8 更高，遗忘 6/8 更低。
6. 隔间标签与 DAN→MBON 连接高度一致（91%–93%），但部分来自共享解剖，不是独立证据。
7. KC 稀疏化（调全局增益与 APL 抑制）没有产生稀疏、广覆盖、气味特异的编码；回路在稀疏化 LIF 编码上学不好，匹配学习量比较在 raw 编码上仍无法检验，基线排序（回路不如 EWC）8/8 稳健，LIF 这条线按止损线收尾。详见 `study/RESULTS_lif2.md`。
8. 编码层接回真实 LIF 后，回路仍不如 EWC（8/8）；但未调参的 LIF 给出稠密、缺乏气味特异性的 KC 编码（67% 的 KC 活跃），匹配学习量比较在该编码下无法进行。详见 `study/RESULTS_matched_lif.md`。

## 数据
MaleCNS v1.0（右半球：2045 KC、49 MBON、16 隔间）。大文件在 `data_annot/`（可由 `repos/drosophila-brain-mlx/tools/fetch_male_cns.sh` 的链接重新下载）。

## 链路（研究 → 代码 → 文档）
| 阶段 | 内容 | 文件 |
|---|---|---|
| 调研 | 文献与开源项目盘点，确认空白 | `repos/`（clfly、flybench、mlx 引擎） |
| 数据 | 隔间标签解析与映射 | `study/compartments.py`、`mb_annotations_malecns.csv` |
| 结构 | DAN→MBON 同隔间 91%（打乱 11%）；KC×MBON 隔间矩阵 | `structure.py`、`kc_mbon.py` |
| 模型 | v1 失败（衰减伪影）→ v2 双向有界规则 → v3 真实 PN→KC 编码 | `DESIGN.md`、`learn_v2.py`、`learn_v3.py` |
| 验证 | 预先登记的扫描（T、分配、编码、衰减） | `PREREG_sweep.md`、`sweep.py`、`RESULTS_sweep.md` |
| 机制 | 重叠度与共享突触解释小趋势 | `mech.py`、`RESULTS_mech.md` |
| 因果/复核/v4/基线 | 重叠度剂量反应、左半球、行为读出、delta 与 EWC | `core.py`、`causal.py`、`replicate_left.py`、`core4.py`、`exp_v4.py`、`RESULTS_causal_left_v4.md` |
| 确认性实验 | 预先登记（新种子、新划分、FlyWire 独立数据集、相似气味任务、EWC 与多头基线） | `PREREG_confirm.md`、`core_fw.py`、`exp_confirm.py`、`analysis_confirm.py`、`RESULTS_confirm.md`、`DEVIATIONS.md` |
| 审查与第二轮 | 三份独立 agent 报告、消融（`PREREG_ablation.md`）、修正后确认（`PREREG_round2.md`） | `verification/`、`ablate.py`、`round2_A.py`、`round2_B.py`、`RESULTS_round2_audit.md` |
| 匹配学习量与 LIF | 预先登记的匹配学习量检验；MaleCNS LIF 编码 | `PREREG_matched.md`、`matched.py`、`PREREG_lif.md`、`prep_lif.py`、`run_lif.py`、`lif_experiment.py`、`RESULTS_matched_lif.md` |
| KC 稀疏化 | APL 抑制与增益扫描；稀疏化编码上的下游检验 | `PREREG_lif2.md`、`lif_sparsify.py`、`run_lif2.py`、`lif_experiment2.py`、`RESULTS_lif2.md` |
| 评估 | 对项目价值的批判性评估 | 项目根目录 `ASSESSMENT.md` |
| 写作 | 博客与图 | 项目根目录的 `BLOG.md`、`figures/` |

## 环境
`study/.venv` 不随迁移复制，重建：`cd study && uv venv --python 3.13 && uv pip install pandas pyarrow numpy matplotlib scipy`。
MLX 脑模型在 `repos/drosophila-brain-mlx/.venv`（本研究的学习模型不依赖它）。

## 局限
单半球、固定学习率、简化学习规则、种子不等于个体；机制部分为事后探索；静默 KC 的解释（非嗅觉型）未核对文献。

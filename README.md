# 真实果蝇连接组能否当作学习与优化的归纳偏置？（预先登记式检验）

用 Janelia MaleCNS 的蘑菇体真实连线（65 个嗅觉小球 → 2045 个 Kenyon 细胞 → 49 个输出神经元），在五类任务里检验“真实连线是否优于打乱 / 随机稀疏 / 线性学习器”。结论与讲解见 `FINAL_SUMMARY.md`、`PROJECT_EXPLAINER.html`。

| 目录 | 内容 |
|---|---|
| `study/` | 隔间与遗忘（预先登记、LIF 引擎接入、独立审查） |
| `ml-cl-audit/` | 对一篇“果蝇启发”持续学习论文（FlyModel）的公平审计 |
| `fly-foraging/` | 觅食、果蝇群、元学习，及交互网页（`web/`） |
| `fly-tsp/` | 旅行商问题：v1 / `v2/` / `v3/`，各含预先登记、结果、独立审查 |

每个实验都有 `PREREG_*.md`（运行前写下的判定标准）与 `*.sha256`（冻结文件哈希）、`RESULTS_*.md`、`DEVIATIONS*.md` 和 `verification/`（独立审查报告）。

## 复现
- 大数据与第三方仓库不在本仓库里：`data_annot/`（MaleCNS / FlyWire 注释，见 `repos/drosophila-brain-mlx/tools/fetch_male_cns.sh`）、`ml-cl-audit/data/`（MNIST/CIFAR-100，由 torchvision 下载）、`repos/`（clfly、flybench、drosophila-brain-mlx 的克隆）。
- 环境：各子目录自建虚拟环境（`uv venv --python 3.13`；`ml-cl-audit` 需要 torch），多进程脚本请设 `OMP_NUM_THREADS=1`。
- 数据来源：Janelia MaleCNS v1.0（CC BY 4.0）。

## 博客与 skill
- 博客系列（7 篇，含配图 SVG）：[`blog/`](blog/README.md)；通俗讲解页：`PROJECT_EXPLAINER.html`；最终总结：`FINAL_SUMMARY.md`。
- 遗忘检验：`fly-foraging/forget/`；元学习重跑：`fly-foraging/meta2/`（逐项结果合并在 `forget/results_all.json`）。
- 由协议提炼的 skill 链路已独立成仓库：<https://github.com/meiluosi/research-writing-skills>。

# 项目状态（2026-10-05）

## 已完成
- 调研：`survey/literature.md`、`survey/feasibility.md`（两个独立 agent）；提案 `PROPOSAL.md`。
- 指标库 `clmetrics.py` + 合成数据测试（通过）。
- 特征：`data/features/{mnist20,cifar100,cifar100_224}.npz`（LeNet5@KMNIST 84 维；ResNet18 512 维，32×32 与 224×224 两种）。
- 复现（`REPLICATION_NOTES.md`，含附录 A、B；哈希已记录）：**MNIST-20 复现成功**（最终 0.707 对 0.75，10 类时 0.817 对 0.86，memory loss 0.089 对 0.07）；**CIFAR-100 数值未复现**（32×32 特征 0.340，224 特征 0.508，论文约 0.41），作为"弱/强特征"两个区间，只做相对比较。
- 预先登记 `PREREG_audit.md`（哈希已记录）；实现与健全性测试：`cl_baselines.py` + `test_audit.py`、`cl_backprop.py` + `test_backprop.py`（均通过，其中含"EWC λ=0 与微调逐位相同"）。
- 偏离与补充：`DEVIATIONS.md`（探索性的无截断与表示×分类器对照，已标注非预先登记）。

## 初步数字（从运行日志读出，**尚未经过 `analysis_audit.py` 与独立审查，不得引用**）
测试集最终准确率（类增量，类别已见集上的 argmax）：

| 方法 | MNIST-20 | CIFAR-100-A (32×32) | CIFAR-100-B (224×224) |
|---|---|---|---|
| FlyModel F0（论文设定） | 0.7065 | 0.3395 | 0.5084 |
| NCM（欧氏） | 0.6008 | 0.2730 | 0.5331 |
| NCM（余弦） | 0.5964 | 0.2778 | 0.5407 |
| 类和点积（无扩展无 WTA） | 0.2984 | 0.1509 | 0.2037 |
| **SLDA**（验证集选收缩） | **0.7603** | **0.3997** | **0.6393** |
| 稠密 + L2（F2） | 0.1447 | 0.2126 | 0.4410 |
| 稠密 + min-max（F2b，论文的稠密对照） | 0.0490 | 0.0100 | 0.0100 |
- 初步读法：SLDA 在三个基准上都高于 FlyModel（+0.054、+0.060、+0.131）；强特征上连简单的 NCM 也不低于 FlyModel；F2b 恰好塌到随机水平。这些**必须由预先登记的分析脚本与独立审查确认**后才能作结论。
- MNIST-20 的探索性结果：稠密+L2+不截断约 0.11；F0 去掉截断约 0.48–0.50；稀疏扩展上的 NCM 约 0.63。含义：稠密对照的失败不是权重饱和，更像是类和点积打分规则的偏置；表示与分类器规则在论文的对照里是混在一起的（待完整结果确认）。

## 还没完成（需要续跑）
所有阶段都有缓存，`results/*.json` 会保留已完成的条目，重新运行同一命令只会补跑缺失项。
```bash
cd ml-cl-audit
.venv/bin/python audit_run.py mnist20 proto          # 已完成
.venv/bin/python audit_run.py mnist20 supp           # 探索性对照（进行中）
.venv/bin/python audit_run.py mnist20 backprop 3     # 反向传播基线（进行中，较慢）
.venv/bin/python audit_run.py cifar100 proto         # 进行中（F0/F1 尚缺）
.venv/bin/python audit_run.py cifar100_224 proto     # 进行中（F0/F1 尚缺）
.venv/bin/python audit_run.py cifar100 backprop 3    # 未开始（预计较长）
.venv/bin/python audit_run.py cifar100_224 backprop 3
.venv/bin/python audit_run.py <bench> offline 3      # 离线上界
.venv/bin/python audit_run.py <bench> supp           # 探索性对照
.venv/bin/python audit_run.py <bench> backprop_multi 3   # 5 遍灵敏度（可能因耗时缺失，按登记规则如实报告）
.venv/bin/python analysis_audit.py                   # 全部完成后按登记判据出结论
```

## 运行状况（写于 2026-10-05 晚）
- 进程在后台跑：mnist20 backprop（CPU）、cifar100 与 cifar100_224 的 proto（FlyModel F0/F1 仍在跑）、cifar100 与 cifar100_224 的 backprop（MPS，单次约 480 秒，完整网格估计数小时，可能超出登记的 3 小时预算 → 按登记规则如实报告缺失）。
- 若应用退出，按上面的命令续跑即可（有缓存）。CIFAR 的 backprop 请带 `AUDIT_DEVICE=mps`。

## 之后
1. `analysis_audit.py` 出结论；2. 起无上下文的 agent 独立审查实现与统计，写入 `verification/`，据此更正；3. 写作（博客/报告）并更新 `ASSESSMENT.md`。

## 已知待办与风险
- 反向传播基线在 CIFAR-100（隐层 20000）上单次运行约数分钟，完整网格较慢；超过登记的 3 小时预算则如实报告缺失。
- 复现的 CIFAR-100 绝对数字与论文不同，所有 CIFAR 结论只作相对比较。

## 更新（2026-10-05 22:10）
CIFAR-100 两个区间的反向传播基线因机器过载（负载均值约 70，单次运行升到约 1070 秒）被**暂停**（不是放弃）；已完成的缓存保留。先让 MNIST-20 基线与 CIFAR 原型类阶段独立跑完，再顺序（不并行）续跑 CIFAR 基线：`AUDIT_DEVICE=mps .venv/bin/python audit_run.py cifar100 backprop 2`。若总耗时超出登记的 3 小时预算，按登记规则如实报告缺失，不缩水网格。


## 更新（2026-10-10）
- 所有快阶段与 MNIST-20 反向传播基线（扩展网格 + 交错流）已完成；CIFAR-100-B 的离线上界可能还在补最后几个种子（不影响 H1–H3）。
- 分析：`.venv/bin/python analysis_audit.py` → `RESULTS_audit_auto.md`；人工整理的结果在 `RESULTS_audit.md`；博客草稿 `BLOG.md`；价值评估 `ASSESSMENT.md`；独立审查 `verification/`。
- **未完成**：CIFAR-100 两个区间的反向传播基线（微调/EWC/回放），按登记规则如实报告缺失；若要补，顺序运行（不要并行）：`AUDIT_DEVICE=mps AUDIT_STREAM=inter .venv/bin/python audit_run.py cifar100_224 backprop 2`。
- 5 遍训练灵敏度（`backprop_multi`）未做。

- （2026-10-11）全部快阶段已完成，CIFAR-100-B 的离线上界补满 5 个种子（0.677）；没有实验进程在跑。剩余未做：CIFAR-100 反向传播基线、5 遍灵敏度。

# 预先登记：第四阶段 0c（保守的无监督适应：连线作初始化）

写于运行测试之前。冻结文件与哈希：`PREREG_v4_stage0c.sha256`。阶段 0 的 `+ad`（eta_p = 0.05）约 15 次激活后只剩原柱 46%，把连线冲掉了（见 `verification/review_stage0.md` 第 9 条），0c 换成保守强度。

## 问题
允许 PN→KC 做小幅无监督 Hebbian 适应（活跃 KC 的输入向当前训练气味移动，柱总权重守恒）之后，真实连线的起点是否仍有样本效率优势？适应本身是否提高样本效率？

## 设计
- 规则同阶段 0 的 `adapt`（300 个训练气味），只改强度 eta_p ∈ {0.003, 0.01, 0.03}；eta_p = 0 为不适应的对照（同一流程）。
- 学习器 real、shuffled、random；任务 door_class、door_teacher_real、teacher_pert（后两个有连线相关的结构；door_class 是真实气味 + 随机类别）。
- 学习率沿用 `tuning_v4b.json` 的各（任务，学习器）值，适应不改它。
- 测试种子 5000–5099；预试（种子 1000–1005）显示 eta_p = 0.01 时柱的余弦保留约 0.93（每个 KC 约 15 次激活后剩原柱的约 86%），选为 headline；0.003、0.03 为敏感性（描述性）。
- 评估同 0b（配对差、自助法、三档，s = 0.03，meaningful-strict 要求区间下界也 ≥ s）。

**主结论族（6 个，99.2% 区间，auc，eta_p = 0.01）：** 每个任务 (1) real+ad − random+ad；(2) real+ad − real（适应对真实连线的效果）。

## 解读规则（预测不是判据）
- 若 real+ad − random+ad 在 teacher_pert 上仍为 real 更好 meaningful，则说明连线起点在温和适应后保留优势；若缩到 small-real/等价，则适应抹平了差距。
- (2) 为正且 meaningful 才可说适应提高了样本效率；为负或等价则 +ad 在这个设置里没有帮助。
- 预测：适应的效果为 small-real 或等价，不提高样本效率；teacher_pert 上 real 的优势保留。

## 已知局限（接受）
规则是任选的一种 Hebbian 形式，不是真实可塑性；只测三档强度；柱保留用余弦衡量，不代表功能保留。

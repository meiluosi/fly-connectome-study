# 预先登记：第四阶段 6b（觅食环境里的隔间学习器）

写于运行测试之前。冻结文件与哈希：`PREREG_v4_stage6b.sha256`（含调参结果，调参先于冻结）。把阶段 4 的隔间学习器（PAM/PPL1 簇、多巴胺预测误差抑制，`forage_comp.py`）放进 `fly-foraging/forage.py` 的觅食场（不改该文件），回答阶段 4 留下的问题：持续学习里的边缘优势在觅食（奖励反转、冲突气味）里还在吗？

## 设计
- 世界：`forage.World`，T = 6000，第 3000 步奖励反转；两种类型 consistent、conflict（相似气味相反号）。
- 学习器：global（`forage.MB`，原有规则，连线 P0）；comp_real（真实簇）；comp_shuf（簇标签在 48 个 MBON 间随机重排，每个世界一次）；comp_shufbal（重排但两个簇的 KC→MBON 突触总量在真实值 ±10% 内）；no_learning（健全性对照）。读出符号、更新规则与阶段 4 相同；PN→KC 都用真实 P0。
- 调参：在调参世界（种子 20–39）上，每个（世界类型，学习器）从 eta ∈ {0.15, 0.4, 0.8} × g_learn ∈ {1, 2, 3}（k_turn = 1.4 固定）中选总净奖励最高者；global 同样重新调（不沿用之前的 0.4/2.0）。
- 测试：200 个全新世界（种子 400–599），智能体种子 5000+世界种子，簇随机数种子 7000+世界种子；配对差，自助法 10000 次。
- 判据同觅食评估：等价边界 ±6（总净奖励）；meaningful-strict 要求区间下界也 ≥ 6。

## 主结论族（4 个，98.8% 区间）
consistent 与 conflict 各两个：comp_real − global；comp_real − comp_shufbal。其余（comp_shuf、no_learning、global − comp_shufbal）为描述性，95% 区间。

## 解读规则与预测（预测不是判据）
- comp_real 对 global：阶段 4 里样本效率不优于 global，持续学习里有边缘的保留优势；觅食同时需要两者，预测等价或略差。
- comp_real 对 comp_shufbal：阶段 4 里 comp_shufbal 差得多，但审查指出这主要是学习水平的差别；预测 comp_real 更好，但这只说明真实划分属于能学会的一类，不说明它特殊（沿用阶段 4 的审查结论）。
- 觅食环境里的任何结论都只对这个玩具场有效；觅食的噪声较大（同一世界重跑约 5 的波动），所以边界 ±6。

## 已知局限（接受）
同阶段 4：簇划分的 PAM = 奖励 / PPL1 = 惩罚是通行假设；DAN→MBON 突触数据已确认每个 MBON 的簇归属（见 `NOTES_v4_stage6a.md`），但不验证效价；规则无对侧增强与遗忘；调参网格粗。

# 预先登记：第四阶段 6d（觅食环境里的有界隔间学习器）

写于运行测试之前。冻结文件与哈希：`PREREG_v4_stage6d.sha256`（含调参结果，调参先于冻结）。6b、6c 的结果保留不动。

## 为什么有 6d
对 6b/6c 的独立审查（`verification/review_stage6.md`）发现 CompMB 的抑制没有上界：g = eta·relu(delta)，delta 最大可到 2，g > 1 时 q 变号并被放大（eta = 4.0 时 q ∈ [−6.9, +9.5]）。把 g 截断到 ≤ 1 的对照里，consistent 世界的 comp_real 只有约 8，不截断是 54，所以 6c 的 consistent 优势来自变号放大的区间，不是阶段 4 的有界规则。6d 用有界版本重新评估。

## 设计
- 学习器：`forage_comp_b.CompMBB`，更新 g = min(eta·relu(delta), 1)，其余同 `CompMB`（簇划分、读出符号、中心化不变）；global 仍是 `forage.MB`（它在大 eta 下也轻度越界，保持原样作为参照）；簇变体 comp_real、comp_shuf、comp_shufbal，no_learning。
- 网格：eta ∈ {0.4, 0.8, 2, 4} × g_learn ∈ {1, 2, 3, 6, 10}（k_turn = 1.4），所有学习器同一网格；调参世界 20–39；测试世界 800–999（全新）。
- 世界、判据（±6）、主结论族（4 个，98.8% 区间）、解读规则同 6b。

## 预测（不是判据）
consistent 里 comp_real 显著低于 global（有界后失去放大区间）；conflict 里与 6c 相近（略差于 global）。若这一预测成立，6c 的 consistent 优势应归因于无界更新。

## 已知局限
网格仍可能碰边（g_learn = 10 是上界）；global 不是严格有界的（它在 eta ≥ 0.8 时轻度越界）；觅食场噪声大；其余同 6b。

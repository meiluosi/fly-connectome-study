# 第四阶段 6b / 6c：觅食环境里的隔间学习器（登记：`PREREG_v4_stage6b.md`、`PREREG_v4_stage6c.md`；数字：`RESULTS_v4_stage6b.md`、`RESULTS_v4_stage6c.md`）

这两个阶段没有做独立审查。阶段 4 的隔间学习器（PAM/PPL1 簇、多巴胺预测误差抑制）放进 `fly-foraging/forage.py` 的觅食场，200 个全新世界，T = 6000，第 3000 步奖励反转，consistent 与 conflict 两种世界；等价边界 ±6。

## 6b（登记的第一次评估）
| | consistent | conflict |
|---|---|---|
| global | +51.9 | +36.2 |
| comp_real | +4.9 | +13.4 |
| comp_real − global | −47.0（meaningful-strict） | −22.8（meaningful-strict） |
| comp_real − comp_shufbal | −24.1 | −9.1（边缘） |

三个隔间学习器的最佳学习率都落在网格上界 0.8。一次未登记的诊断（12 个世界）显示更大的学习率和 g_learn 下 comp_real 能到约 40 到 64，所以这个差距很可能主要是网格太窄。

## 6c（登记的偏离重跑：网格 eta ∈ {0.4, 0.8, 2, 4} × g_learn ∈ {1, 2, 3, 6}，所有学习器同一网格；新世界种子 600–799）
| | consistent | conflict |
|---|---|---|
| global | +45.2 | +32.4 |
| comp_real | +53.8 | +23.2 |
| comp_real − global | +8.6 [+2.4, +14.6]，meaningful（边缘） | −9.3 [−14.9, −3.7]，meaningful（边缘） |
| comp_real − comp_shufbal | +1.4，不确定 | −7.9 [−14.6, −0.6]，meaningful（边缘） |

## 怎么读
- **6b 的大差距是调参网格造成的。** 网格放宽后 comp_real 在 consistent 世界里追平并略超 global，在 conflict 世界里略差；两个方向的差距都只是边缘（区间下界低于 6）。所以觅食里没有测出隔间学习器的稳定优势或劣势。
- **comp_real 与簇标签重排的版本：** consistent 里不确定，conflict 里 comp_real 略差（−7.9，边缘）。阶段 4 里“真实划分比重排好”的方向在觅食里没有重现。
- 学习率落点：comp_real 在 consistent 里最佳学习率是网格上界 4.0（g_learn = 1），仍可能没到最优；conflict 里 g_learn 全部落在上界 6。网格依然粗。
- 单个世界的奖励噪声大（global 在 6b 与 6c 的 consistent 世界里分别是 +51.9 与 +45.2，来自不同的世界样本）。
- 局限同阶段 4：PAM = 奖励 / PPL1 = 惩罚是通行假设；规则只抑制；觅食场是玩具场。

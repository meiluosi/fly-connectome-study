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

## 独立审查后的更正（`verification/review_stage6.md`）
- **CompMB 的抑制没有上界，6c consistent 世界里的优势依赖这一点。** 更新式 `q -= g·code·NB·q` 里 g = eta·relu(delta)，delta 最大可到 2；g 超过 1 时 q 变号并被放大。eta = 4.0 时 q 的范围是 [−6.9, +9.5]，eta = 0.8 时已经到 −0.07。原规则 `forage.MB` 在它的最佳 eta 0.8 下也越界（q 从 −0.43 到 1.44），但程度轻。审查用 g 截断到不超过 1 的对照（调参世界 20–39，consistent，g_learn = 1）：eta = 2、4、8 时都只有 8.2，不截断的 eta = 4 是 54.0、eta = 8 是 56.4；g_learn = 2 时截断版本全部是 −1.0。所以 6c 里 comp_real 在 consistent 世界的 +53.8 来自一个变号并放大的区间，不是阶段 4 的有界规则。conflict 世界几乎不受影响（截断 29.5，不截断 30.2）。文档和登记里“有界”的说法对两个学习器都不准确。
- **阶段 4 的结果不受此影响：** 阶段 4 里 comp 学习器的调参学习率最高是 0.05（持续学习）和 0.05 以下（样本效率任务），g = eta·relu(e) ≤ 0.1，远没有超过 1；只有 unsigned 学习器选到过大的学习率，它本来就学不会。
- **“6b 的差距是网格造成的，没有稳定的优势或劣势”比数据更强。** 6c 的 98.8% 区间是 consistent +8.6 [+2.4, +14.6]、conflict −9.3 [−14.9, −3.7]，都不含 0、符号相反、都不等价。6c 登记的判定规则是“仍明显更差则 6b 成立；等价则 6b 是调参造成的”，两种情形都没有发生。两个预测也都没有应验：comp_real 对 global 在 consistent 里更好（预测是等价或略差）；comp_real 对 comp_shufbal 在 conflict 里是 −7.9 [−14.6, −0.6]，不是等价。conflict 的差距从 −22.8 缩到 −9.3 但没有消失；6b 与 6c 的测试世界不同，conflict 里 global 的设置从 g_learn = 1 变到 6，不能直接比较。
- **网格边缘问题比我写的更重：** comp_real 在 consistent 里 eta = 4.0 是上界、g_learn = 1.0 是下界；conflict 里 g_learn = 6 对 global、comp_real、comp_shufbal 都是上界；global conflict 的 eta = 0.4 是下界。延伸调参世界：comp_real consistent 在 eta = 8 时 56.4 到 56.6，之后下降；conflict 在 (2, 15) 达到 33.0；global conflict 的 (0.4, 6) = 43.6 是一个尖峰，(0.4, 10) 只有 29.9，在测试世界里降到 32.4（选择偏差）。
- **6a 不是循环的，但检验很弱：** 我重算得到 49/49 MBON 有 DAN 输入，48/48 一致。簇来自 DAN 的 `type`（PAM*/PPL1*），隔间名没有用到。一致几乎是定义性的、事先可以预期：41/49 个 MBON 的 DAN 输入有 90% 以上来自同一个簇，46/49 在 80% 以上；最弱的是 MBON33（59 对 158）、MBON30（58 对 156）、MBON10（12 对 4，20 对 4）。39/49 个 MBON 同时接收两个簇，8 个的总权重低于 30。PPL1 DAN 只有 16 个，却占了 20388 总权重里的 5647。我没有把 6b/6c 用数据划分重跑一遍。效价（PAM = 奖励）依然没有验证。
- 6b 与 6c 对同一假设实际有 8 个检验，主结论族只在单个阶段内校正。

## 能说什么
觅食里没有证据表明隔间学习器优于原规则；6c 的结果在 consistent 世界里的“优势”依赖变号放大的区间，不应当作隔间结构的作用。有界版本见 6d（如已运行）。

## 6d（登记：`PREREG_v4_stage6d.md`，数字：`RESULTS_v4_stage6d.md`）：有界版本
用 g = min(eta·relu(delta), 1) 的有界更新，网格 eta ∈ {0.4, 0.8, 2, 4} × g_learn ∈ {1, 2, 3, 6, 10}，新世界种子 800–999，主结论族 98.8% 区间：
| | consistent | conflict |
|---|---|---|
| global | +49.4 | +34.9 |
| comp_real（有界） | +27.1 | +32.3 |
| comp_real − global | −22.3 [−28.1, −16.8]，meaningful-strict | −2.6 [−8.7, +3.2]，不确定 |
| comp_real − comp_shufbal | −1.9 [−7.8, +3.9]，不确定 | +3.4 [−3.2, +10.2]，不确定 |
| comp_real − comp_shuf | −0.6，等价 | +4.6，不确定 |

- 登记的预测应验：有界之后 consistent 世界里的 comp_real 明显低于 global（−22.3），6c 的 +8.6 确实来自变号放大的区间；conflict 世界里与 global 无法区分。
- 真实簇划分与重排的划分在觅食里无法区分（区间都含 0）。阶段 4 里“真实划分比重排好”的方向在觅食里没有重现。
- 局限：comp_real 选到 g_learn = 10（网格上界），所以仍可能没到最优；global 不是严格有界的；觅食场噪声大。
- 合并 6b、6c、6d 的读法：觅食里没有证据表明隔间学习器优于原规则；在 consistent 世界里它更差，在 conflict 世界里无法区分；簇划分的真实与否没有可测出的差别。

# 结果（第四阶段 2：行为现象复现，自动生成）

每个学习器 100 个世界（种子 5000–5099），固定学习率 0.05，不调参。

## 判据 C1–C4（每个学习器）

| 学习器 | C1 梯度：各重叠度的平均响应（6,5,4,3,2,0） | C1 通过 | C2 稀疏→稠密的相对下降：相似 / 不相似 | C2 通过 | C3 反转：翻转所需试验数（中位数）/ 30 次内翻转比例 | C3 通过 | C4 消退：末值/峰值 | C4 通过 |
|---|---|---|---|---|---|---|---|---|
| real | 0.34, 0.24, 0.17, 0.12, 0.08, 0.02 | 是 | 0.31 / 0.15（差 +0.16 [+0.12, +0.20]） | 是 | 5 / 1.00 | 是 | 0.18 | 是 |
| shuffled | 0.34, 0.25, 0.19, 0.13, 0.09, 0.02 | 是 | 0.36 / 0.15（差 +0.21 [+0.20, +0.22]） | 是 | 5 / 1.00 | 是 | 0.18 | 是 |
| random | 0.23, 0.17, 0.12, 0.08, 0.05, 0.01 | 是 | 0.44 / 0.22（差 +0.23 [+0.21, +0.24]） | 是 | 7 / 1.00 | 是 | 0.37 | 否 |
| real_binary | 0.26, 0.19, 0.14, 0.10, 0.07, 0.02 | 是 | 0.45 / 0.24（差 +0.22 [+0.18, +0.25]） | 是 | 6 / 1.00 | 是 | 0.31 | 否 |
| real_wshuf | 0.34, 0.24, 0.18, 0.12, 0.08, 0.02 | 是 | 0.33 / 0.15（差 +0.18 [+0.15, +0.21]） | 是 | 5 / 1.00 | 是 | 0.18 | 是 |

## 连线对比（主结论族 8 个，99.4% 区间；A − B，三档，s：spec 0.05、aplsel 0.10、flip 5 次、ratio 0.10）

- ★spec: real − shuffled = -0.002 [-0.003, +0.000] → **equivalent**
- ★spec: real − random = +0.097 [+0.094, +0.100] → **meaningful**
- ★aplsel: real − shuffled = -0.049 [-0.110, +0.008] → **uncertain**
- ★aplsel: real − random = -0.067 [-0.128, -0.011] → **small-real**
- ★flip: real − shuffled = +0.000 [+0.000, +0.000] → **equivalent**
- ★flip: real − random = -1.600 [-1.730, -1.470] → **small-real**
- ★ratio: real − shuffled = +0.001 [-0.001, +0.002] → **equivalent**
- ★ratio: real − random = -0.185 [-0.193, -0.177] → **meaningful**

描述性（95% 区间）：real − real_binary / real_wshuf

- spec: real − real_binary = +0.085 [+0.076, +0.094] → meaningful
- spec: real − real_wshuf = +0.001 [-0.001, +0.002] → equivalent
- aplsel: real − real_binary = -0.059 [-0.093, -0.025] → small-real
- aplsel: real − real_wshuf = -0.023 [-0.076, +0.029] → equivalent
- flip: real − real_binary = -1.110 [-1.230, -0.990] → small-real
- flip: real − real_wshuf = +0.000 [+0.000, +0.000] → equivalent
- ratio: real − real_binary = -0.132 [-0.147, -0.117] → meaningful
- ratio: real − real_wshuf = -0.000 [-0.001, +0.001] → equivalent

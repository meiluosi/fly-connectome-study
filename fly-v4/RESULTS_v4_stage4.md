# 结果（第四阶段 4：效价专门化隔间 + 多巴胺时序规则，自动生成）

三档判定，s = 0.03（准确率点）；主结论族（★，7 个）99.3% 区间，其余 95%；100 个测试世界（种子 5000–5099）。

## A. 时序现象（单个气味，3 次配对，学习率 0.3）

| 学习器 | 变体 | 奖励 ISI −0.5 | 奖励 +0.5 | 惩罚 −0.5 | 惩罚 +0.5 | 奖励 +8 | 奖励 −8 | P1 符号 | P2 衰减 | P3 隔间特异 |
|---|---|---|---|---|---|---|---|---|---|---|
| comp_real | intact | -0.241 | +0.307 | +0.275 | -0.350 | +0.008 | -0.002 | 是 | 是 | 是 |
| comp_real | notiming | +0.000 | +0.307 | +0.000 | -0.350 | +0.008 | +0.000 | — | — | — |
| comp_shuf | intact | -0.220 | +0.280 | +0.297 | -0.377 | +0.007 | -0.002 | 是 | 是 | 是 |
| comp_shuf | notiming | +0.000 | +0.280 | +0.000 | -0.377 | +0.007 | +0.000 | — | — | — |
| comp_shufbal | intact | -0.226 | +0.288 | +0.290 | -0.369 | +0.007 | -0.002 | 是 | 是 | 是 |
| comp_shufbal | notiming | +0.000 | +0.288 | +0.000 | -0.369 | +0.007 | +0.000 | — | — | — |

## B. 样本效率任务（auc；每个（任务，学习器）调参后的学习率）


### door_class
| 学习器 | 学习率 | auc | 50 次后 | 最终 |
|---|---|---|---|---|
| global | 0.05 | 0.674 | 0.647 | 0.694 |
| comp_real | 0.05 | 0.667 | 0.644 | 0.683 |
| comp_shuf | 0.005 | 0.594 | 0.596 | 0.596 |
| comp_shufbal | 0.02 | 0.644 | 0.633 | 0.650 |
| unsigned | 0.005 | 0.501 | 0.499 | 0.497 |

配对差（auc）：
- ★comp_real − global: -0.006 [-0.013, +0.000] → **equivalent**
- ★comp_real − comp_shufbal: +0.023 [+0.006, +0.043] → **small-real**
- comp_real − comp_shuf: +0.073 [+0.054, +0.093] → **meaningful-strict**
- comp_real − unsigned: +0.167 [+0.150, +0.184] → **meaningful-strict**
- global − comp_shufbal: +0.029 [+0.018, +0.042] → **small-real**

### door_teacher_real
| 学习器 | 学习率 | auc | 50 次后 | 最终 |
|---|---|---|---|---|
| global | 0.05 | 0.768 | 0.727 | 0.809 |
| comp_real | 0.05 | 0.741 | 0.700 | 0.771 |
| comp_shuf | 0.02 | 0.619 | 0.609 | 0.628 |
| comp_shufbal | 0.05 | 0.692 | 0.681 | 0.706 |
| unsigned | 1.0 | 0.236 | 0.220 | 0.234 |

配对差（auc）：
- comp_real − global: -0.027 [-0.030, -0.024] → **small-real**
- comp_real − comp_shufbal: +0.049 [+0.036, +0.062] → **meaningful-strict**
- comp_real − comp_shuf: +0.122 [+0.101, +0.143] → **meaningful-strict**
- comp_real − unsigned: +0.505 [+0.495, +0.515] → **meaningful-strict**
- global − comp_shufbal: +0.076 [+0.063, +0.089] → **meaningful-strict**

### linear_teacher
| 学习器 | 学习率 | auc | 50 次后 | 最终 |
|---|---|---|---|---|
| global | 0.05 | 0.666 | 0.612 | 0.716 |
| comp_real | 0.02 | 0.649 | 0.601 | 0.692 |
| comp_shuf | 0.02 | 0.553 | 0.552 | 0.555 |
| comp_shufbal | 0.01 | 0.582 | 0.585 | 0.591 |
| unsigned | 0.05 | 0.494 | 0.491 | 0.497 |

配对差（auc）：
- ★comp_real − global: -0.018 [-0.024, -0.012] → **small-real**
- ★comp_real − comp_shufbal: +0.067 [+0.050, +0.083] → **meaningful-strict**
- comp_real − comp_shuf: +0.096 [+0.081, +0.110] → **meaningful-strict**
- comp_real − unsigned: +0.154 [+0.145, +0.163] → **meaningful-strict**
- global − comp_shufbal: +0.084 [+0.072, +0.096] → **meaningful-strict**

### teacher_real
| 学习器 | 学习率 | auc | 50 次后 | 最终 |
|---|---|---|---|---|
| global | 0.15 | 0.766 | 0.716 | 0.810 |
| comp_real | 0.05 | 0.701 | 0.647 | 0.744 |
| comp_shuf | 0.05 | 0.589 | 0.588 | 0.588 |
| comp_shufbal | 0.05 | 0.643 | 0.633 | 0.653 |
| unsigned | 1.0 | 0.397 | 0.372 | 0.408 |

配对差（auc）：
- comp_real − global: -0.065 [-0.071, -0.059] → **meaningful-strict**
- comp_real − comp_shufbal: +0.059 [+0.046, +0.071] → **meaningful-strict**
- comp_real − comp_shuf: +0.113 [+0.093, +0.132] → **meaningful-strict**
- comp_real − unsigned: +0.305 [+0.296, +0.313] → **meaningful-strict**
- global − comp_shufbal: +0.123 [+0.109, +0.137] → **meaningful-strict**

## C. 持续学习（4 个任务各 10 个气味，随机 ±1 标签，依次学习，最后测全部 40 个）

| 学习器 | 学习率 | 刚学完时 | 最终 | 遗忘（归一化） |
|---|---|---|---|---|
| global | 0.02 | 0.940 | 0.802 | 0.314 |
| global (匹配学习量) | 0.01 | 0.902 | 0.798 | 0.254 |
| comp_real | 0.05 | 0.905 | 0.846 | 0.144 |
| comp_shuf | 0.05 | 0.727 | 0.645 | 2.151 |
| comp_shufbal | 0.01 | 0.811 | 0.726 | 0.280 |
| unsigned | 0.4 | 0.490 | 0.490 | 0.000 |

配对差（最终准确率）：
- ★comp_real − global: +0.044 [+0.024, +0.065] → **meaningful (边缘)**
- ★comp_real − global_matched: +0.048 [+0.029, +0.067] → **meaningful (边缘)**
- ★comp_real − comp_shufbal: +0.119 [+0.091, +0.149] → **meaningful-strict**
- comp_real − comp_shuf: +0.200 [+0.169, +0.232] → **meaningful-strict**
- comp_real − unsigned: +0.356 [+0.338, +0.373] → **meaningful-strict**

学习量—最终准确率的前沿（全部学习率，描述性）：

| 学习率 | global 刚学完 / 最终 | comp_real 刚学完 / 最终 |
|---|---|---|
| 0.005 | 0.875 / 0.785 | 0.838 / 0.774 |
| 0.01 | 0.902 / 0.798 | 0.852 / 0.789 |
| 0.02 | 0.940 / 0.802 | 0.874 / 0.813 |
| 0.05 | 0.973 / 0.776 | 0.905 / 0.846 |
| 0.15 | 0.988 / 0.745 | 0.923 / 0.843 |
| 0.4 | 0.974 / 0.723 | 0.902 / 0.818 |
| 1.0 | 0.799 / 0.608 | 0.900 / 0.816 |

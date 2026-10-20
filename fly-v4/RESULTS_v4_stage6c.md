# 结果（第四阶段 6c：觅食环境里的隔间学习器（更宽的调参网格），自动生成）

200 个全新世界（种子 600–799），T = 6000，第 3000 步奖励反转；指标 = 总净奖励；等价边界 ±6；主结论族（★，4 个）98.8% 区间，其余 95%。


## consistent
| 学习器 | 学习率 / g_learn | 净奖励 |
|---|---|---|
| global | 0.8 / 2.0 | +45.2 |
| comp_real | 4.0 / 1.0 | +53.8 |
| comp_shuf | 4.0 / 1.0 | +49.7 |
| comp_shufbal | 4.0 / 1.0 | +52.4 |
| no_learning | — | -1.3 |

配对差：
- ★comp_real − global: +8.6 [+2.4, +14.6] → **meaningful (边缘)**
- ★comp_real − comp_shufbal: +1.4 [-5.0, +8.0] → **uncertain**
- comp_real − comp_shuf: +4.1 [-0.6, +9.0] → **uncertain**
- comp_real − no_learning: +55.1 [+50.7, +59.5] → **meaningful-strict**
- global − no_learning: +46.5 [+43.7, +49.5] → **meaningful-strict**
- global − comp_shufbal: -7.2 [-11.9, -2.4] → **meaningful (边缘)**

## conflict
| 学习器 | 学习率 / g_learn | 净奖励 |
|---|---|---|
| global | 0.4 / 6.0 | +32.4 |
| comp_real | 2.0 / 6.0 | +23.2 |
| comp_shuf | 2.0 / 6.0 | +21.6 |
| comp_shufbal | 0.8 / 6.0 | +31.0 |
| no_learning | — | -0.0 |

配对差：
- ★comp_real − global: -9.3 [-14.9, -3.7] → **meaningful (边缘)**
- ★comp_real − comp_shufbal: -7.9 [-14.6, -0.6] → **meaningful (边缘)**
- comp_real − comp_shuf: +1.6 [-2.9, +6.3] → **uncertain**
- comp_real − no_learning: +23.2 [+19.3, +27.2] → **meaningful-strict**
- global − no_learning: +32.5 [+29.1, +35.8] → **meaningful-strict**
- global − comp_shufbal: +1.4 [-3.5, +6.1] → **uncertain**

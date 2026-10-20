# 结果（第四阶段 6b：觅食环境里的隔间学习器，自动生成）

200 个全新世界（种子 400–599），T = 6000，第 3000 步奖励反转；指标 = 总净奖励；等价边界 ±6；主结论族（★，4 个）98.8% 区间，其余 95%。


## consistent
| 学习器 | 学习率 / g_learn | 净奖励 |
|---|---|---|
| global | 0.8 / 2.0 | +51.9 |
| comp_real | 0.8 / 1.0 | +4.9 |
| comp_shuf | 0.8 / 3.0 | +27.1 |
| comp_shufbal | 0.8 / 3.0 | +29.0 |
| no_learning | — | -0.2 |

配对差：
- ★comp_real − global: -47.0 [-52.3, -41.5] → **meaningful-strict**
- ★comp_real − comp_shufbal: -24.1 [-31.1, -17.3] → **meaningful-strict**
- comp_real − comp_shuf: -22.2 [-27.4, -16.8] → **meaningful-strict**
- comp_real − no_learning: +5.2 [+2.4, +8.0] → **small-real**
- global − no_learning: +52.1 [+48.8, +55.6] → **meaningful-strict**
- global − comp_shufbal: +22.9 [+17.9, +28.0] → **meaningful-strict**

## conflict
| 学习器 | 学习率 / g_learn | 净奖励 |
|---|---|---|
| global | 0.4 / 1.0 | +36.2 |
| comp_real | 0.8 / 1.0 | +13.4 |
| comp_shuf | 0.8 / 3.0 | +22.2 |
| comp_shufbal | 0.8 / 3.0 | +22.5 |
| no_learning | — | -1.4 |

配对差：
- ★comp_real − global: -22.8 [-26.5, -19.0] → **meaningful-strict**
- ★comp_real − comp_shufbal: -9.1 [-14.5, -3.6] → **meaningful (边缘)**
- comp_real − comp_shuf: -8.8 [-13.3, -4.4] → **meaningful (边缘)**
- comp_real − no_learning: +14.8 [+12.7, +16.9] → **meaningful-strict**
- global − no_learning: +37.6 [+35.1, +40.1] → **meaningful-strict**
- global − comp_shufbal: +13.7 [+9.1, +18.3] → **meaningful-strict**

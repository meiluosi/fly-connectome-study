# 结果（第四阶段 6d：觅食环境里的有界隔间学习器，自动生成）

200 个全新世界（种子 800–999），T = 6000，第 3000 步奖励反转；指标 = 总净奖励；等价边界 ±6；主结论族（★，4 个）98.8% 区间，其余 95%。


## consistent
| 学习器 | 学习率 / g_learn | 净奖励 |
|---|---|---|
| global | 0.8 / 2.0 | +49.4 |
| comp_real | 2.0 / 10.0 | +27.1 |
| comp_shuf | 2.0 / 10.0 | +27.7 |
| comp_shufbal | 0.4 / 10.0 | +29.1 |
| no_learning | — | +0.0 |

配对差：
- ★comp_real − global: -22.3 [-28.1, -16.8] → **meaningful-strict**
- ★comp_real − comp_shufbal: -1.9 [-7.8, +3.9] → **uncertain**
- comp_real − comp_shuf: -0.6 [-5.5, +4.4] → **equivalent**
- comp_real − no_learning: +27.1 [+23.2, +31.0] → **meaningful-strict**
- global − no_learning: +49.4 [+46.4, +52.4] → **meaningful-strict**
- global − comp_shufbal: +20.4 [+16.3, +24.5] → **meaningful-strict**

## conflict
| 学习器 | 学习率 / g_learn | 净奖励 |
|---|---|---|
| global | 0.4 / 6.0 | +34.9 |
| comp_real | 0.8 / 10.0 | +32.3 |
| comp_shuf | 4.0 / 6.0 | +27.7 |
| comp_shufbal | 2.0 / 3.0 | +28.9 |
| no_learning | — | -0.3 |

配对差：
- ★comp_real − global: -2.6 [-8.7, +3.2] → **uncertain**
- ★comp_real − comp_shufbal: +3.4 [-3.2, +10.2] → **uncertain**
- comp_real − comp_shuf: +4.6 [-0.7, +9.9] → **uncertain**
- comp_real − no_learning: +32.6 [+28.8, +36.5] → **meaningful-strict**
- global − no_learning: +35.2 [+31.9, +38.5] → **meaningful-strict**
- global − comp_shufbal: +6.0 [+1.0, +11.0] → **small-real**

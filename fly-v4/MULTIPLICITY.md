# 全局多重比较再分析（67 个主结论对比，fly-v4 阶段 0–6d）

各阶段的区间已按阶段内的主结论族校正（见各 PREREG）。这里把所有阶段的星标对比放进**一个**族，从区间反推正态近似的标准误和双侧 p 值，做 Holm 与 Benjamini–Hochberg 校正（α = 0.05）。这是近似，目的是看哪些头条结论在全局校正下还成立，不替代各阶段的分析。同一假设在多个阶段被检验（例如“真实 vs 随机稀疏”），所以实际独立的检验比 67 个少，但相关性使得校正偏保守的方向未知，这里不做依赖修正。

| 阶段 | 对比 | 均值 [阶段区间] | 阶段判定 | p（近似） | Holm 调整 p | BH 调整 p | 全局 Holm 下显著 |
|---|---|---|---|---|---|---|---|
| 0 | teacher_real：real − shuffled | +0.081 [+0.073, +0.089] | meaningful | 0 | 0 | 0 | 是 |
| 0 | teacher_real：real − random | +0.083 [+0.076, +0.092] | meaningful | 0 | 0 | 0 | 是 |
| 0 | door_class：real − random | -0.001 [-0.006, +0.004] | equivalent | 0.59 | 1 | 0.61 | 否 |
| 0 | door_class：real+ad − random+ad | +0.003 [-0.003, +0.009] | equivalent | 0.18 | 1 | 0.22 | 否 |
| 0 | door_teacher_real：real − random | +0.033 [+0.027, +0.039] | meaningful | 0 | 0 | 0 | 是 |
| 0 | door_teacher_real：real+ad − random+ad | -0.002 [-0.008, +0.005] | equivalent | 0.41 | 1 | 0.48 | 否 |
| 0b | teacher_pert：real − shuffled | +0.064 [+0.058, +0.071] | meaningful-strict | 0 | 0 | 0 | 是 |
| 0b | teacher_pert：real − random | +0.066 [+0.059, +0.074] | meaningful-strict | 0 | 0 | 0 | 是 |
| 0b | teacher_shuf：shuffled − random | +0.001 [-0.002, +0.005] | equivalent | 0.45 | 1 | 0.5 | 否 |
| 0b | door_class：real − shuffled | +0.008 [+0.005, +0.012] | small-real | 1.3e-09 | 5e-08 | 2.9e-09 | 是 |
| 0b | door_class：real − random | -0.001 [-0.006, +0.004] | equivalent | 0.6 | 1 | 0.61 | 否 |
| 0c | door_class：eta_p=0.01: real+ad − random+ad | -0.004 [-0.009, +0.001] | equivalent | 0.034 | 0.61 | 0.045 | 否 |
| 0c | door_class：eta_p=0.01: real+ad − real（适应的效果） | -0.001 [-0.005, +0.002] | equivalent | 0.45 | 1 | 0.5 | 否 |
| 0c | door_teacher_real：eta_p=0.01: real+ad − random+ad | +0.013 [+0.006, +0.019] | small-real | 1.1e-07 | 3.8e-06 | 2.2e-07 | 是 |
| 0c | door_teacher_real：eta_p=0.01: real+ad − real（适应的效果） | -0.021 [-0.024, -0.017] | small-real | 0 | 0 | 0 | 是 |
| 0c | teacher_pert：eta_p=0.01: real+ad − random+ad | +0.062 [+0.055, +0.069] | meaningful-strict | 0 | 0 | 0 | 是 |
| 0c | teacher_pert：eta_p=0.01: real+ad − real（适应的效果） | +0.004 [+0.003, +0.005] | small-real | 0 | 0 | 0 | 是 |
| 2 | 连线对比（主结论族：spec: real − shuffled | -0.002 [-0.003, +0.000] | equivalent | 0.00025 | 0.0075 | 0.00044 | 是 |
| 2 | 连线对比（主结论族：spec: real − random | +0.097 [+0.094, +0.100] | meaningful | 0 | 0 | 0 | 是 |
| 2 | 连线对比（主结论族：aplsel: real − shuffled | -0.049 [-0.110, +0.008] | uncertain | 0.022 | 0.47 | 0.032 | 否 |
| 2 | 连线对比（主结论族：aplsel: real − random | -0.067 [-0.128, -0.011] | small-real | 0.0016 | 0.045 | 0.0027 | 是 |
| 2 | 连线对比（主结论族：flip: real − shuffled | +0.000 [+0.000, +0.000] | equivalent | 0 | 0 | 0 | 是 |
| 2 | 连线对比（主结论族：flip: real − random | -1.600 [-1.730, -1.470] | small-real | 0 | 0 | 0 | 是 |
| 2 | 连线对比（主结论族：ratio: real − shuffled | +0.001 [-0.001, +0.002] | equivalent | 0.067 | 1 | 0.088 | 否 |
| 2 | 连线对比（主结论族：ratio: real − random | -0.185 [-0.193, -0.177] | meaningful | 0 | 0 | 0 | 是 |
| 3 | teacher_M_R：M_L − random | +0.057 [+0.051, +0.064] | meaningful-strict | 0 | 0 | 0 | 是 |
| 3 | teacher_M_R：F_R − random | +0.036 [+0.030, +0.043] | meaningful-strict | 0 | 0 | 0 | 是 |
| 3 | teacher_M_R：F_R − marg_F_R | +0.006 [+0.002, +0.010] | small-real | 3.8e-05 | 0.0012 | 6.8e-05 | 是 |
| 3 | teacher_F_R：F_L − random | +0.041 [+0.036, +0.047] | meaningful-strict | 0 | 0 | 0 | 是 |
| 3 | teacher_F_R：M_R − random | +0.027 [+0.022, +0.032] | small-real | 0 | 0 | 0 | 是 |
| 3 | teacher_F_R：M_R − marg_M_R | -0.002 [-0.006, +0.001] | equivalent | 0.12 | 1 | 0.15 | 否 |
| 3 | door_class：M_R − F_R | +0.000 [-0.004, +0.005] | equivalent | 1 | 1 | 1 | 否 |
| 3 | door_class：M_R − random | +0.000 [-0.005, +0.005] | equivalent | 1 | 1 | 1 | 否 |
| 4 | door_class：comp_real − global | -0.006 [-0.013, +0.000] | equivalent | 0.013 | 0.29 | 0.019 | 否 |
| 4 | door_class：comp_real − comp_shufbal | +0.023 [+0.006, +0.043] | small-real | 0.0008 | 0.022 | 0.0013 | 是 |
| 4 | linear_teacher：comp_real − global | -0.018 [-0.024, -0.012] | small-real | 6.7e-16 | 2.9e-14 | 1.8e-15 | 是 |
| 4 | linear_teacher：comp_real − comp_shufbal | +0.067 [+0.050, +0.083] | meaningful-strict | 0 | 0 | 0 | 是 |
| 4 | C.：comp_real − global | +0.044 [+0.024, +0.065] | meaningful | 7.1e-09 | 2.6e-07 | 1.5e-08 | 是 |
| 4 | C.：comp_real − global_matched | +0.048 [+0.029, +0.067] | meaningful | 9.6e-12 | 3.7e-10 | 2.2e-11 | 是 |
| 4 | C.：comp_real − comp_shufbal | +0.119 [+0.091, +0.149] | meaningful-strict | 0 | 0 | 0 | 是 |
| 5 | 主结论族：1. door_teacher_real real：post-hoc，active 409 的超额损失 | +0.045 [+0.027, +0.065] | meaningful | 7.6e-11 | 2.9e-09 | 1.7e-10 | 是 |
| 5 | 主结论族：2. door_teacher_real real：post-hoc，active 818 的超额损失 | +0.124 [+0.103, +0.147] | meaningful-strict | 0 | 0 | 0 | 是 |
| 5 | 主结论族：3. door_teacher_real real：post-hoc，hub 818 的超额损失 | +0.052 [+0.033, +0.071] | meaningful-strict | 5.5e-14 | 2.3e-12 | 1.4e-13 | 是 |
| 5 | 主结论族：4. door_teacher_real：active 409 超额损失，real − shuffled | +0.009 [-0.005, +0.024] | equivalent | 0.088 | 1 | 0.11 | 否 |
| 5 | 主结论族：5. door_teacher_real：active 409 超额损失，real − random 连线 | +0.035 [+0.018, +0.052] | meaningful | 1.5e-08 | 5.4e-07 | 3.1e-08 | 是 |
| 5 | 主结论族：6. door_class real：post-hoc，active 409 的超额损失 | +0.003 [-0.011, +0.017] | equivalent | 0.56 | 1 | 0.6 | 否 |
| 5 | 主结论族：7. door_class real：post-hoc，active 818 的超额损失 | +0.043 [+0.026, +0.060] | meaningful | 3.6e-12 | 1.5e-10 | 8.7e-12 | 是 |
| 5 | 主结论族：8. door_teacher_real real：训练前移除，active 409 的超额损失 | -0.010 [-0.020, -0.000] | small-real | 0.006 | 0.14 | 0.0091 | 否 |
| 5b | 主结论族：1. door_class real：post，hub 13 个通道的超额损失 | +0.019 [+0.002, +0.035] | small-real | 0.0019 | 0.049 | 0.003 | 是 |
| 5b | 主结论族：2. door_class real：post，bridger 13 个通道的超额损失 | +0.003 [-0.009, +0.015] | equivalent | 0.5 | 1 | 0.55 | 否 |
| 5b | 主结论族：3. door_class real：pre，hub 13 个通道的超额损失 | +0.012 [-0.001, +0.026] | equivalent | 0.017 | 0.36 | 0.024 | 否 |
| 5b | 主结论族：4. door_teacher_real real：pre，hub 13 个通道的超额损失（教师用同一连线，循环，见登记） | +0.068 [+0.054, +0.083] | meaningful-strict | 0 | 0 | 0 | 是 |
| 5b | 主结论族：5. door_teacher_real real：pre，bridger 13 个通道的超额损失 | -0.009 [-0.021, +0.001] | equivalent | 0.027 | 0.52 | 0.037 | 否 |
| 5b | 主结论族：6. door_teacher_real：post，hub 13 的超额损失，real − shuffled | +0.059 [+0.038, +0.081] | meaningful-strict | 1.4e-13 | 5.6e-12 | 3.4e-13 | 是 |
| 5b | 主结论族：7. door_class：post，hub 13 的超额损失，real − shuffled | +0.017 [-0.004, +0.037] | uncertain | 0.025 | 0.51 | 0.035 | 否 |
| 6b | consistent：comp_real − global | -47.000 [-52.300, -41.500] | meaningful-strict | 0 | 0 | 0 | 是 |
| 6b | consistent：comp_real − comp_shufbal | -24.100 [-31.100, -17.300] | meaningful-strict | 0 | 0 | 0 | 是 |
| 6b | conflict：comp_real − global | -22.800 [-26.500, -19.000] | meaningful-strict | 0 | 0 | 0 | 是 |
| 6b | conflict：comp_real − comp_shufbal | -9.100 [-14.500, -3.600] | meaningful | 2.7e-05 | 0.0009 | 5.2e-05 | 是 |
| 6c | consistent：comp_real − global | +8.600 [+2.400, +14.600] | meaningful | 0.0004 | 0.012 | 0.00068 | 是 |
| 6c | consistent：comp_real − comp_shufbal | +1.400 [-5.000, +8.000] | uncertain | 0.59 | 1 | 0.61 | 否 |
| 6c | conflict：comp_real − global | -9.300 [-14.900, -3.700] | meaningful | 3e-05 | 0.00097 | 5.6e-05 | 是 |
| 6c | conflict：comp_real − comp_shufbal | -7.900 [-14.600, -0.600] | meaningful | 0.0046 | 0.11 | 0.0071 | 否 |
| 6d | consistent：comp_real − global | -22.300 [-28.100, -16.800] | meaningful-strict | 0 | 0 | 0 | 是 |
| 6d | consistent：comp_real − comp_shufbal | -1.900 [-7.800, +3.900] | uncertain | 0.41 | 1 | 0.48 | 否 |
| 6d | conflict：comp_real − global | -2.600 [-8.700, +3.200] | uncertain | 0.27 | 1 | 0.33 | 否 |
| 6d | conflict：comp_real − comp_shufbal | +3.400 [-3.200, +10.200] | uncertain | 0.2 | 1 | 0.25 | 否 |

全局 Holm 下 42/67 个显著；其中阶段内判定为 meaningful-strict 的有 16 个。阶段内判定为“meaningful（边缘）”或 small-real 的结果，在全局校正后是否仍显著，见表中最后一列；显著只表示区间不含 0，不表示效应超过最小有意义效应。

## 解读与限制
- **范围：** 只包含 fly-v4（阶段 0 到 6d）里在 RESULTS 文件中以星标打印的 67 个对比；早先几条线（隔间与遗忘、FlyModel 审计、觅食、元学习、旅行商）的头条结论不在此表内，它们各自有预先登记的族。有两个登记的头条对比（阶段 0 的 linear_teacher 的 linear − real，阶段 0b 的 teacher_shuf 的 shuffled − real）是在门槛部分打印的，不带星标，没有被解析进来。
- **p 值是从区间反推的正态近似**，阶段内的区间是自助法区间；阶段 6 的 98.8% 区间只有 200 个世界；这里的显著只表示区间不含 0，不表示效应达到预设的最小有意义效应。
- **全局 Holm 下 42/67 个显著；阶段内标为 meaningful-strict 的 16 个都是其中的一部分。** 在“阶段内判定为 meaningful 或 small-real”的结果里，只有两个在全局校正后不再显著：阶段 5 的对比 8（训练前移除、active 409，−0.010）和阶段 6c 的 conflict 里 comp_real − comp_shufbal（−7.9）。这两个本来就是边缘结果。所以统一校正不改变各阶段的头条结论，主要的不确定性来自效应量和设计（审查指出的混杂），不是多重比较。
- 同一假设（真实 vs 打乱 / 随机稀疏）在多个阶段被检验，这些检验并不独立；这个表没有对依赖做修正。

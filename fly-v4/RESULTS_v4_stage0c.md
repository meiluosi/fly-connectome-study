# 结果（第四阶段 0c：保守的无监督适应，自动生成）

三档判定，s = 0.03；主结论族（★，6 个）99.2% 区间，其余 95%；100 个测试世界。headline 适应强度 eta_p = 0.01。


## door_class
| 学习器 | eta_p=0.0 auc | eta_p=0.003 auc | eta_p=0.01 auc | eta_p=0.03 auc | eta_p=0.01 的柱保留（余弦） |
|---|---|---|---|---|---|
| real | 0.674 | 0.674 | 0.672 | 0.665 | 0.93 |
| shuffled | 0.665 | 0.666 | 0.665 | 0.660 | 0.93 |
| random | 0.675 | 0.679 | 0.676 | 0.664 | 0.99 |

配对差（auc）：
- eta_p=0.003: real+ad − random+ad = -0.005 [-0.009, -0.002] → **small-real**
- eta_p=0.003: real+ad − shuffled+ad = +0.008 [+0.005, +0.010] → **small-real**
- ★eta_p=0.01: real+ad − random+ad = -0.004 [-0.009, +0.001] → **equivalent**
- eta_p=0.01: real+ad − shuffled+ad = +0.008 [+0.005, +0.010] → **small-real**
- eta_p=0.03: real+ad − random+ad = +0.001 [-0.002, +0.004] → **equivalent**
- eta_p=0.03: real+ad − shuffled+ad = +0.005 [+0.003, +0.008] → **small-real**
- eta_p=0.003: real+ad − real（适应的效果）= -0.000 [-0.001, +0.001] → **equivalent**
- eta_p=0.003: random+ad − random（适应的效果）= +0.004 [+0.002, +0.007] → **small-real**
- ★eta_p=0.01: real+ad − real（适应的效果）= -0.001 [-0.005, +0.002] → **equivalent**
- eta_p=0.01: random+ad − random（适应的效果）= +0.002 [-0.002, +0.005] → **equivalent**
- eta_p=0.03: real+ad − real（适应的效果）= -0.008 [-0.013, -0.004] → **small-real**
- eta_p=0.03: random+ad − random（适应的效果）= -0.010 [-0.015, -0.005] → **small-real**
- 参照 eta_p=0: real − random = -0.001 [-0.004, +0.002] → equivalent

## door_teacher_real
| 学习器 | eta_p=0.0 auc | eta_p=0.003 auc | eta_p=0.01 auc | eta_p=0.03 auc | eta_p=0.01 的柱保留（余弦） |
|---|---|---|---|---|---|
| real | 0.768 | 0.759 | 0.747 | 0.714 | 0.93 |
| shuffled | 0.740 | 0.737 | 0.725 | 0.703 | 0.93 |
| random | 0.734 | 0.741 | 0.734 | 0.714 | 0.99 |

配对差（auc）：
- eta_p=0.003: real+ad − random+ad = +0.018 [+0.013, +0.023] → **small-real**
- eta_p=0.003: real+ad − shuffled+ad = +0.023 [+0.019, +0.026] → **small-real**
- ★eta_p=0.01: real+ad − random+ad = +0.013 [+0.006, +0.019] → **small-real**
- eta_p=0.01: real+ad − shuffled+ad = +0.022 [+0.019, +0.026] → **small-real**
- eta_p=0.03: real+ad − random+ad = -0.000 [-0.005, +0.004] → **equivalent**
- eta_p=0.03: real+ad − shuffled+ad = +0.011 [+0.008, +0.013] → **small-real**
- eta_p=0.003: real+ad − real（适应的效果）= -0.008 [-0.010, -0.007] → **small-real**
- eta_p=0.003: random+ad − random（适应的效果）= +0.007 [+0.005, +0.009] → **small-real**
- ★eta_p=0.01: real+ad − real（适应的效果）= -0.021 [-0.024, -0.017] → **small-real**
- eta_p=0.01: random+ad − random（适应的效果）= +0.000 [-0.002, +0.003] → **equivalent**
- eta_p=0.03: real+ad − real（适应的效果）= -0.054 [-0.059, -0.049] → **meaningful-strict**
- eta_p=0.03: random+ad − random（适应的效果）= -0.020 [-0.024, -0.016] → **small-real**
- 参照 eta_p=0: real − random = +0.034 [+0.029, +0.038] → meaningful (边缘)

## teacher_pert
| 学习器 | eta_p=0.0 auc | eta_p=0.003 auc | eta_p=0.01 auc | eta_p=0.03 auc | eta_p=0.01 的柱保留（余弦） |
|---|---|---|---|---|---|
| real | 0.733 | 0.735 | 0.737 | 0.738 | 0.94 |
| shuffled | 0.669 | 0.672 | 0.677 | 0.683 | 0.94 |
| random | 0.667 | 0.676 | 0.676 | 0.676 | 1.00 |

配对差（auc）：
- eta_p=0.003: real+ad − random+ad = +0.059 [+0.055, +0.064] → **meaningful-strict**
- eta_p=0.003: real+ad − shuffled+ad = +0.063 [+0.058, +0.068] → **meaningful-strict**
- ★eta_p=0.01: real+ad − random+ad = +0.062 [+0.055, +0.069] → **meaningful-strict**
- eta_p=0.01: real+ad − shuffled+ad = +0.060 [+0.055, +0.065] → **meaningful-strict**
- eta_p=0.03: real+ad − random+ad = +0.062 [+0.058, +0.067] → **meaningful-strict**
- eta_p=0.03: real+ad − shuffled+ad = +0.056 [+0.051, +0.060] → **meaningful-strict**
- eta_p=0.003: real+ad − real（适应的效果）= +0.002 [+0.001, +0.002] → **small-real**
- eta_p=0.003: random+ad − random（适应的效果）= +0.009 [+0.006, +0.012] → **small-real**
- ★eta_p=0.01: real+ad − real（适应的效果）= +0.004 [+0.003, +0.005] → **small-real**
- eta_p=0.01: random+ad − random（适应的效果）= +0.009 [+0.006, +0.012] → **small-real**
- eta_p=0.03: real+ad − real（适应的效果）= +0.005 [+0.004, +0.006] → **small-real**
- eta_p=0.03: random+ad − random（适应的效果）= +0.009 [+0.006, +0.012] → **small-real**
- 参照 eta_p=0: real − random = +0.066 [+0.061, +0.072] → meaningful-strict

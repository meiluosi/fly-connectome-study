# 结果（第四阶段 3：个体差异，自动生成）

三档判定，s = 0.03；主结论族（★，8 个）99.4% 区间，其余 95%；100 个测试世界（种子 5000–5099）；headline 学习率 0.05，0.15 为描述性。


## teacher_M_R
| 学习器 | auc（学习率 0.05） | auc（0.15） | 50 次后（0.05） | 最终（0.05） |
|---|---|---|---|---|
| M_R | 0.704 | 0.693 | 0.649 | 0.748 |
| M_L | 0.693 | 0.682 | 0.644 | 0.734 |
| F_R | 0.673 | 0.659 | 0.627 | 0.718 |
| F_L | 0.672 | 0.658 | 0.622 | 0.715 |
| shuf_M_R | 0.637 | 0.620 | 0.581 | 0.684 |
| shuf_F_R | 0.639 | 0.621 | 0.583 | 0.683 |
| marg_M_R | 0.670 | 0.655 | 0.613 | 0.719 |
| marg_F_R | 0.666 | 0.651 | 0.612 | 0.714 |
| random | 0.636 | 0.630 | 0.581 | 0.689 |

配对差（auc；A − B；学习率 0.05）：
- ★M_L − random: +0.057 [+0.051, +0.064] → **meaningful-strict**（学习率 0.15: +0.052 → meaningful-strict）
- ★F_R − random: +0.036 [+0.030, +0.043] → **meaningful-strict**（学习率 0.15: +0.029 → small-real）
- ★F_R − marg_F_R: +0.006 [+0.002, +0.010] → **small-real**（学习率 0.15: +0.009 → small-real）
- M_R − M_L: +0.010 [+0.008, +0.013] → **small-real**（学习率 0.15: +0.011 → small-real）
- F_R − F_L: +0.001 [-0.001, +0.003] → **equivalent**（学习率 0.15: +0.001 → equivalent）
- M_R − F_R: +0.031 [+0.028, +0.034] → **meaningful (边缘)**（学习率 0.15: +0.034 → meaningful-strict）
- M_L − F_L: +0.022 [+0.019, +0.024] → **small-real**（学习率 0.15: +0.024 → small-real）
- M_R − random: +0.067 [+0.063, +0.072] → **meaningful-strict**（学习率 0.15: +0.063 → meaningful-strict）
- F_L − random: +0.035 [+0.031, +0.039] → **meaningful-strict**（学习率 0.15: +0.028 → small-real）
- marg_M_R − random: +0.034 [+0.031, +0.037] → **meaningful-strict**（学习率 0.15: +0.025 → small-real）
- marg_F_R − random: +0.030 [+0.026, +0.033] → **meaningful (边缘)**（学习率 0.15: +0.021 → small-real）
- M_R − marg_M_R: +0.034 [+0.031, +0.037] → **meaningful-strict**（学习率 0.15: +0.038 → meaningful-strict）
- M_R − shuf_M_R: +0.067 [+0.063, +0.070] → **meaningful-strict**（学习率 0.15: +0.073 → meaningful-strict）
- F_R − shuf_F_R: +0.034 [+0.030, +0.038] → **meaningful-strict**（学习率 0.15: +0.038 → meaningful-strict）

## teacher_F_R
| 学习器 | auc（学习率 0.05） | auc（0.15） | 50 次后（0.05） | 最终（0.05） |
|---|---|---|---|---|
| M_R | 0.660 | 0.646 | 0.610 | 0.701 |
| M_L | 0.662 | 0.650 | 0.619 | 0.699 |
| F_R | 0.690 | 0.675 | 0.640 | 0.731 |
| F_L | 0.675 | 0.659 | 0.621 | 0.716 |
| shuf_M_R | 0.634 | 0.617 | 0.582 | 0.672 |
| shuf_F_R | 0.637 | 0.619 | 0.585 | 0.678 |
| marg_M_R | 0.663 | 0.647 | 0.612 | 0.703 |
| marg_F_R | 0.670 | 0.653 | 0.618 | 0.712 |
| random | 0.634 | 0.627 | 0.579 | 0.681 |

配对差（auc；A − B；学习率 0.05）：
- ★F_L − random: +0.041 [+0.036, +0.047] → **meaningful-strict**（学习率 0.15: +0.032 → meaningful (边缘)）
- ★M_R − random: +0.027 [+0.022, +0.032] → **small-real**（学习率 0.15: +0.019 → small-real）
- ★M_R − marg_M_R: -0.002 [-0.006, +0.001] → **equivalent**（学习率 0.15: -0.001 → equivalent）
- M_R − M_L: -0.002 [-0.005, +0.000] → **equivalent**（学习率 0.15: -0.004 → small-real）
- F_R − F_L: +0.015 [+0.013, +0.018] → **small-real**（学习率 0.15: +0.016 → small-real）
- M_R − F_R: -0.030 [-0.033, -0.027] → **meaningful (边缘)**（学习率 0.15: -0.029 → small-real）
- M_L − F_L: -0.013 [-0.015, -0.010] → **small-real**（学习率 0.15: -0.009 → small-real）
- F_R − random: +0.057 [+0.053, +0.061] → **meaningful-strict**（学习率 0.15: +0.048 → meaningful-strict）
- M_L − random: +0.029 [+0.025, +0.033] → **small-real**（学习率 0.15: +0.023 → small-real）
- marg_M_R − random: +0.029 [+0.026, +0.033] → **small-real**（学习率 0.15: +0.020 → small-real）
- marg_F_R − random: +0.036 [+0.033, +0.040] → **meaningful-strict**（学习率 0.15: +0.026 → small-real）
- F_R − marg_F_R: +0.020 [+0.018, +0.023] → **small-real**（学习率 0.15: +0.022 → small-real）
- M_R − shuf_M_R: +0.026 [+0.023, +0.029] → **small-real**（学习率 0.15: +0.029 → small-real）
- F_R − shuf_F_R: +0.053 [+0.050, +0.057] → **meaningful-strict**（学习率 0.15: +0.056 → meaningful-strict）

## teacher_M_L
| 学习器 | auc（学习率 0.05） | auc（0.15） | 50 次后（0.05） | 最终（0.05） |
|---|---|---|---|---|
| M_R | 0.652 | 0.641 | 0.598 | 0.693 |
| M_L | 0.675 | 0.664 | 0.617 | 0.718 |
| F_R | 0.649 | 0.636 | 0.599 | 0.688 |
| F_L | 0.646 | 0.633 | 0.592 | 0.689 |
| shuf_M_R | 0.617 | 0.604 | 0.570 | 0.659 |
| shuf_F_R | 0.618 | 0.603 | 0.570 | 0.659 |
| marg_M_R | 0.648 | 0.636 | 0.592 | 0.694 |
| marg_F_R | 0.646 | 0.632 | 0.592 | 0.690 |
| random | 0.616 | 0.611 | 0.566 | 0.666 |

配对差（auc；A − B；学习率 0.05）：
- M_R − M_L: -0.023 [-0.026, -0.021] → **small-real**（学习率 0.15: -0.023 → small-real）
- F_R − F_L: +0.003 [+0.002, +0.005] → **small-real**（学习率 0.15: +0.004 → small-real）
- M_R − F_R: +0.003 [+0.001, +0.005] → **small-real**（学习率 0.15: +0.004 → small-real）
- M_L − F_L: +0.030 [+0.027, +0.032] → **small-real**（学习率 0.15: +0.031 → meaningful (边缘)）
- M_R − random: +0.035 [+0.032, +0.039] → **meaningful-strict**（学习率 0.15: +0.030 → small-real）
- F_R − random: +0.033 [+0.029, +0.036] → **meaningful (边缘)**（学习率 0.15: +0.025 → small-real）
- M_L − random: +0.059 [+0.055, +0.063] → **meaningful-strict**（学习率 0.15: +0.053 → meaningful-strict）
- F_L − random: +0.029 [+0.026, +0.032] → **small-real**（学习率 0.15: +0.022 → small-real）
- marg_M_R − random: +0.032 [+0.029, +0.035] → **meaningful (边缘)**（学习率 0.15: +0.025 → small-real）
- marg_F_R − random: +0.030 [+0.027, +0.033] → **small-real**（学习率 0.15: +0.021 → small-real）
- M_R − marg_M_R: +0.004 [+0.001, +0.006] → **small-real**（学习率 0.15: +0.005 → small-real）
- F_R − marg_F_R: +0.003 [+0.001, +0.005] → **small-real**（学习率 0.15: +0.004 → small-real）
- M_R − shuf_M_R: +0.035 [+0.031, +0.038] → **meaningful-strict**（学习率 0.15: +0.037 → meaningful-strict）
- F_R − shuf_F_R: +0.030 [+0.027, +0.034] → **meaningful (边缘)**（学习率 0.15: +0.033 → meaningful-strict）

## teacher_F_L
| 学习器 | auc（学习率 0.05） | auc（0.15） | 50 次后（0.05） | 最终（0.05） |
|---|---|---|---|---|
| M_R | 0.624 | 0.609 | 0.574 | 0.659 |
| M_L | 0.620 | 0.608 | 0.571 | 0.654 |
| F_R | 0.633 | 0.618 | 0.580 | 0.669 |
| F_L | 0.647 | 0.631 | 0.592 | 0.687 |
| shuf_M_R | 0.609 | 0.595 | 0.557 | 0.648 |
| shuf_F_R | 0.611 | 0.595 | 0.562 | 0.650 |
| marg_M_R | 0.626 | 0.611 | 0.571 | 0.662 |
| marg_F_R | 0.629 | 0.613 | 0.577 | 0.666 |
| random | 0.609 | 0.603 | 0.557 | 0.649 |

配对差（auc；A − B；学习率 0.05）：
- M_R − M_L: +0.004 [+0.002, +0.006] → **small-real**（学习率 0.15: +0.002 → small-real）
- F_R − F_L: -0.014 [-0.016, -0.012] → **small-real**（学习率 0.15: -0.013 → small-real）
- M_R − F_R: -0.009 [-0.012, -0.007] → **small-real**（学习率 0.15: -0.009 → small-real）
- M_L − F_L: -0.027 [-0.030, -0.025] → **small-real**（学习率 0.15: -0.023 → small-real）
- M_R − random: +0.015 [+0.012, +0.018] → **small-real**（学习率 0.15: +0.006 → small-real）
- F_R − random: +0.024 [+0.021, +0.027] → **small-real**（学习率 0.15: +0.015 → small-real）
- M_L − random: +0.011 [+0.007, +0.014] → **small-real**（学习率 0.15: +0.005 → small-real）
- F_L − random: +0.038 [+0.035, +0.041] → **meaningful-strict**（学习率 0.15: +0.028 → small-real）
- marg_M_R − random: +0.017 [+0.014, +0.020] → **small-real**（学习率 0.15: +0.008 → small-real）
- marg_F_R − random: +0.020 [+0.017, +0.023] → **small-real**（学习率 0.15: +0.010 → small-real）
- M_R − marg_M_R: -0.002 [-0.004, -0.000] → **small-real**（学习率 0.15: -0.002 → equivalent）
- F_R − marg_F_R: +0.004 [+0.002, +0.006] → **small-real**（学习率 0.15: +0.005 → small-real）
- M_R − shuf_M_R: +0.014 [+0.011, +0.017] → **small-real**（学习率 0.15: +0.015 → small-real）
- F_R − shuf_F_R: +0.022 [+0.019, +0.025] → **small-real**（学习率 0.15: +0.023 → small-real）

## door_class
| 学习器 | auc（学习率 0.05） | auc（0.15） | 50 次后（0.05） | 最终（0.05） |
|---|---|---|---|---|
| M_R | 0.675 | 0.669 | 0.649 | 0.696 |
| M_L | 0.674 | 0.669 | 0.651 | 0.695 |
| F_R | 0.675 | 0.668 | 0.652 | 0.692 |
| F_L | 0.672 | 0.666 | 0.652 | 0.689 |
| shuf_M_R | 0.666 | 0.660 | 0.644 | 0.686 |
| shuf_F_R | 0.666 | 0.660 | 0.645 | 0.687 |
| marg_M_R | 0.669 | 0.663 | 0.649 | 0.689 |
| marg_F_R | 0.671 | 0.664 | 0.645 | 0.690 |
| random | 0.675 | 0.674 | 0.654 | 0.694 |

配对差（auc；A − B；学习率 0.05）：
- ★M_R − F_R: +0.000 [-0.004, +0.005] → **equivalent**（学习率 0.15: +0.002 → equivalent）
- ★M_R − random: +0.000 [-0.005, +0.005] → **equivalent**（学习率 0.15: -0.004 → small-real）
- M_R − M_L: +0.001 [-0.002, +0.004] → **equivalent**（学习率 0.15: +0.001 → equivalent）
- F_R − F_L: +0.003 [+0.000, +0.005] → **small-real**（学习率 0.15: +0.002 → equivalent）
- M_L − F_L: +0.002 [-0.000, +0.004] → **equivalent**（学习率 0.15: +0.003 → small-real）
- F_R − random: -0.000 [-0.004, +0.004] → **equivalent**（学习率 0.15: -0.006 → small-real）
- M_L − random: -0.001 [-0.004, +0.003] → **equivalent**（学习率 0.15: -0.005 → small-real）
- F_L − random: -0.003 [-0.006, +0.001] → **equivalent**（学习率 0.15: -0.008 → small-real）
- marg_M_R − random: -0.006 [-0.009, -0.003] → **small-real**（学习率 0.15: -0.011 → small-real）
- marg_F_R − random: -0.004 [-0.008, -0.001] → **small-real**（学习率 0.15: -0.010 → small-real）
- M_R − marg_M_R: +0.006 [+0.004, +0.009] → **small-real**（学习率 0.15: +0.007 → small-real）
- F_R − marg_F_R: +0.004 [+0.002, +0.007] → **small-real**（学习率 0.15: +0.004 → small-real）
- M_R − shuf_M_R: +0.009 [+0.007, +0.012] → **small-real**（学习率 0.15: +0.009 → small-real）
- F_R − shuf_F_R: +0.009 [+0.005, +0.013] → **small-real**（学习率 0.15: +0.007 → small-real）

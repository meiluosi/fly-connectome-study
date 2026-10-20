# 结果（第四阶段 0，自动生成）

三档判定，s = 0.03（准确率点）；主结论族（★）99.3% 区间，其余 95%。每个任务 100 个测试世界（种子 5000–5099）。


## teacher_real
| 学习器 | auc（样本效率） | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |
|---|---|---|---|---|---|---|
| real | 0.764 | 0.680 | 0.826 | 0.789 | 0.741 | 0.029 |
| shuffled | 0.683 | 0.594 | 0.743 | 0.719 | 0.599 | 0.030 |
| random | 0.681 | 0.589 | 0.748 | 0.726 | 0.643 | 0.033 |
| real_binary | 0.728 | 0.647 | 0.780 | 0.753 | 0.705 | 0.025 |
| real_wshuf | 0.746 | 0.646 | 0.812 | 0.780 | 0.725 | 0.030 |
| linear | 0.756 | 0.651 | 0.828 | 0.789 | 0.828 | 0.020 |
| real+ad | 0.758 | 0.681 | 0.819 | 0.786 | 0.760 | 0.025 |
| shuffled+ad | 0.697 | 0.610 | 0.761 | 0.736 | 0.649 | 0.028 |
| random+ad | 0.688 | 0.606 | 0.751 | 0.722 | 0.675 | 0.029 |

配对差（auc；A − B）：
- ★real − shuffled: +0.081 [+0.073, +0.089] → **meaningful**
- ★real − random: +0.083 [+0.076, +0.092] → **meaningful**
- real − real_binary: +0.036 [+0.033, +0.039] → **meaningful**
- real − real_wshuf: +0.018 [+0.016, +0.021] → **small-real**
- real − linear: +0.008 [+0.003, +0.013] → **small-real**
- linear − random: +0.075 [+0.070, +0.080] → **meaningful**
- real+ad − random+ad: +0.069 [+0.065, +0.074] → **meaningful**
- real+ad − shuffled+ad: +0.061 [+0.056, +0.066] → **meaningful**
- real+ad − real: -0.006 [-0.008, -0.004] → **small-real**
- random+ad − random: +0.007 [+0.004, +0.010] → **small-real**
- shuffled+ad − shuffled: +0.014 [+0.012, +0.016] → **small-real**
- （acc50）real − random: +0.091 [+0.081, +0.101] → meaningful
- （noisy）real − random: +0.063 [+0.054, +0.072] → meaningful
- （silenced）real − random: +0.098 [+0.089, +0.107] → meaningful

## teacher_random
| 学习器 | auc（样本效率） | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |
|---|---|---|---|---|---|---|
| real | 0.556 | 0.523 | 0.573 | 0.569 | 0.535 | 0.018 |
| shuffled | 0.565 | 0.527 | 0.589 | 0.582 | 0.538 | 0.019 |
| random | 0.566 | 0.527 | 0.597 | 0.589 | 0.556 | 0.021 |
| real_binary | 0.553 | 0.523 | 0.574 | 0.569 | 0.530 | 0.020 |
| real_wshuf | 0.560 | 0.528 | 0.581 | 0.578 | 0.549 | 0.019 |
| linear | 0.593 | 0.543 | 0.626 | 0.616 | 0.626 | 0.022 |
| real+ad | 0.566 | 0.532 | 0.585 | 0.576 | 0.551 | 0.020 |
| shuffled+ad | 0.575 | 0.536 | 0.597 | 0.593 | 0.558 | 0.021 |
| random+ad | 0.576 | 0.534 | 0.603 | 0.596 | 0.569 | 0.023 |

配对差（auc；A − B）：
- real − shuffled: -0.009 [-0.012, -0.006] → **small-real**
- real − random: -0.011 [-0.013, -0.008] → **small-real**
- real − real_binary: +0.003 [+0.001, +0.005] → **small-real**
- real − real_wshuf: -0.004 [-0.006, -0.002] → **small-real**
- real − linear: -0.037 [-0.040, -0.035] → **meaningful**
- linear − random: +0.027 [+0.024, +0.029] → **small-real**
- real+ad − random+ad: -0.010 [-0.013, -0.007] → **small-real**
- real+ad − shuffled+ad: -0.009 [-0.012, -0.006] → **small-real**
- real+ad − real: +0.010 [+0.008, +0.011] → **small-real**
- random+ad − random: +0.009 [+0.007, +0.011] → **small-real**
- shuffled+ad − shuffled: +0.010 [+0.008, +0.011] → **small-real**
- （acc50）real − random: -0.004 [-0.010, +0.001] → equivalent
- （noisy）real − random: -0.020 [-0.026, -0.014] → small-real
- （silenced）real − random: -0.020 [-0.026, -0.015] → small-real

## linear_teacher
| 学习器 | auc（样本效率） | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |
|---|---|---|---|---|---|---|
| real | 0.664 | 0.600 | 0.716 | 0.697 | 0.618 | 0.029 |
| shuffled | 0.699 | 0.616 | 0.770 | 0.741 | 0.634 | 0.029 |
| random | 0.697 | 0.613 | 0.772 | 0.747 | 0.671 | 0.032 |
| real_binary | 0.659 | 0.585 | 0.722 | 0.702 | 0.600 | 0.035 |
| real_wshuf | 0.679 | 0.603 | 0.737 | 0.716 | 0.651 | 0.032 |
| linear | 0.790 | 0.677 | 0.879 | 0.834 | 0.879 | 0.016 |
| real+ad | 0.681 | 0.612 | 0.737 | 0.711 | 0.664 | 0.026 |
| shuffled+ad | 0.716 | 0.631 | 0.781 | 0.756 | 0.688 | 0.026 |
| random+ad | 0.708 | 0.626 | 0.771 | 0.743 | 0.702 | 0.026 |

配对差（auc；A − B）：
- real − shuffled: -0.034 [-0.039, -0.030] → **meaningful**
- real − random: -0.033 [-0.038, -0.028] → **meaningful**
- real − real_binary: +0.006 [+0.002, +0.009] → **small-real**
- real − real_wshuf: -0.015 [-0.018, -0.012] → **small-real**
- real − linear: -0.126 [-0.131, -0.120] → **meaningful**
- linear − random: +0.092 [+0.087, +0.098] → **meaningful**
- real+ad − random+ad: -0.026 [-0.031, -0.022] → **small-real**
- real+ad − shuffled+ad: -0.035 [-0.039, -0.031] → **meaningful**
- real+ad − real: +0.017 [+0.015, +0.019] → **small-real**
- random+ad − random: +0.010 [+0.007, +0.014] → **small-real**
- shuffled+ad − shuffled: +0.018 [+0.015, +0.020] → **small-real**
- （acc50）real − random: -0.013 [-0.019, -0.007] → small-real
- （noisy）real − random: -0.050 [-0.058, -0.042] → meaningful
- （silenced）real − random: -0.053 [-0.062, -0.045] → meaningful

## family
| 学习器 | auc（样本效率） | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |
|---|---|---|---|---|---|---|
| real | 0.968 | 0.987 | 0.992 | 0.980 | 0.990 | 0.010 |
| shuffled | 0.976 | 0.999 | 1.000 | 0.996 | 0.999 | 0.002 |
| random | 0.976 | 0.998 | 1.000 | 0.997 | 1.000 | 0.002 |
| real_binary | 0.973 | 0.994 | 0.998 | 0.990 | 0.996 | 0.005 |
| real_wshuf | 0.973 | 0.995 | 0.997 | 0.989 | 0.996 | 0.005 |
| linear | 0.976 | 1.000 | 1.000 | 0.998 | 1.000 | 0.001 |
| real+ad | 0.976 | 1.000 | 1.000 | 0.997 | 1.000 | 0.001 |
| shuffled+ad | 0.976 | 1.000 | 1.000 | 0.997 | 1.000 | 0.001 |
| random+ad | 0.976 | 1.000 | 1.000 | 0.997 | 1.000 | 0.001 |

配对差（auc；A − B）：
- real − shuffled: -0.008 [-0.010, -0.006] → **small-real**
- real − random: -0.008 [-0.010, -0.006] → **small-real**
- real − real_binary: -0.005 [-0.006, -0.004] → **small-real**
- real − real_wshuf: -0.005 [-0.006, -0.004] → **small-real**
- real − linear: -0.008 [-0.010, -0.006] → **small-real**
- linear − random: +0.001 [+0.000, +0.001] → **small-real**
- real+ad − random+ad: +0.000 [-0.000, +0.000] → **equivalent**
- real+ad − shuffled+ad: +0.000 [-0.000, +0.000] → **equivalent**
- real+ad − real: +0.008 [+0.006, +0.010] → **small-real**
- random+ad − random: +0.001 [+0.000, +0.001] → **small-real**
- shuffled+ad − shuffled: +0.000 [+0.000, +0.001] → **small-real**
- （acc50）real − random: -0.011 [-0.015, -0.008] → small-real
- （noisy）real − random: -0.017 [-0.021, -0.013] → small-real
- （silenced）real − random: -0.010 [-0.013, -0.007] → small-real

## door_class
| 学习器 | auc（样本效率） | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |
|---|---|---|---|---|---|---|
| real | 0.672 | 0.646 | 0.694 | 0.684 | 0.671 | 0.058 |
| shuffled | 0.664 | 0.641 | 0.686 | 0.681 | 0.664 | 0.060 |
| random | 0.673 | 0.654 | 0.691 | 0.683 | 0.685 | 0.059 |
| real_binary | 0.669 | 0.648 | 0.690 | 0.680 | 0.670 | 0.061 |
| real_wshuf | 0.666 | 0.639 | 0.686 | 0.681 | 0.674 | 0.060 |
| linear | 0.672 | 0.645 | 0.702 | 0.693 | 0.702 | 0.056 |
| real+ad | 0.660 | 0.634 | 0.684 | 0.679 | 0.665 | 0.058 |
| shuffled+ad | 0.658 | 0.638 | 0.679 | 0.672 | 0.658 | 0.060 |
| random+ad | 0.657 | 0.633 | 0.672 | 0.666 | 0.664 | 0.062 |

配对差（auc；A − B）：
- real − shuffled: +0.008 [+0.005, +0.011] → **small-real**
- ★real − random: -0.001 [-0.006, +0.004] → **equivalent**
- real − real_binary: +0.003 [-0.000, +0.007] → **equivalent**
- real − real_wshuf: +0.006 [+0.004, +0.009] → **small-real**
- real − linear: -0.000 [-0.005, +0.004] → **equivalent**
- linear − random: -0.001 [-0.005, +0.005] → **equivalent**
- ★real+ad − random+ad: +0.003 [-0.003, +0.009] → **equivalent**
- real+ad − shuffled+ad: +0.002 [-0.000, +0.005] → **equivalent**
- real+ad − real: -0.012 [-0.017, -0.007] → **small-real**
- random+ad − random: -0.016 [-0.021, -0.011] → **small-real**
- shuffled+ad − shuffled: -0.006 [-0.010, -0.002] → **small-real**
- （acc50）real − random: -0.008 [-0.016, +0.000] → equivalent
- （noisy）real − random: +0.001 [-0.007, +0.009] → equivalent
- （silenced）real − random: -0.014 [-0.022, -0.007] → small-real

## door_teacher_real
| 学习器 | auc（样本效率） | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |
|---|---|---|---|---|---|---|
| real | 0.764 | 0.722 | 0.809 | 0.778 | 0.762 | 0.032 |
| shuffled | 0.736 | 0.695 | 0.770 | 0.755 | 0.725 | 0.036 |
| random | 0.731 | 0.701 | 0.761 | 0.745 | 0.743 | 0.033 |
| real_binary | 0.743 | 0.706 | 0.783 | 0.752 | 0.737 | 0.036 |
| real_wshuf | 0.751 | 0.715 | 0.791 | 0.765 | 0.755 | 0.034 |
| linear | 0.732 | 0.688 | 0.773 | 0.731 | 0.773 | 0.033 |
| real+ad | 0.700 | 0.670 | 0.730 | 0.718 | 0.692 | 0.039 |
| shuffled+ad | 0.695 | 0.663 | 0.729 | 0.710 | 0.687 | 0.038 |
| random+ad | 0.702 | 0.683 | 0.727 | 0.710 | 0.717 | 0.037 |

配对差（auc；A − B）：
- real − shuffled: +0.028 [+0.024, +0.032] → **small-real**
- ★real − random: +0.033 [+0.027, +0.039] → **meaningful**
- real − real_binary: +0.021 [+0.017, +0.024] → **small-real**
- real − real_wshuf: +0.013 [+0.011, +0.016] → **small-real**
- real − linear: +0.032 [+0.027, +0.037] → **meaningful**
- linear − random: +0.001 [-0.003, +0.005] → **equivalent**
- ★real+ad − random+ad: -0.002 [-0.008, +0.005] → **equivalent**
- real+ad − shuffled+ad: +0.005 [+0.003, +0.007] → **small-real**
- real+ad − real: -0.064 [-0.069, -0.058] → **meaningful**
- random+ad − random: -0.029 [-0.033, -0.025] → **small-real**
- shuffled+ad − shuffled: -0.041 [-0.045, -0.037] → **meaningful**
- （acc50）real − random: +0.021 [+0.010, +0.032] → small-real
- （noisy）real − random: +0.033 [+0.025, +0.042] → meaningful
- （silenced）real − random: +0.018 [+0.011, +0.026] → small-real

## 门槛（阳性对照）
- teacher_real: real − shuffled → meaningful（+0.081）；real − random → meaningful（+0.083）
- linear_teacher: linear − real → meaningful（+0.126）
- teacher_random（阴性）: real − random → small-real（-0.011）；不应为 real 更好 meaningful
- **门槛：通过**

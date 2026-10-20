# 结果（第四阶段 0b，自动生成）

三档判定，s = 0.03；主结论族（★，6 个）99.2% 区间，其余 95%；100 个测试世界（种子 5000–5099）。


## teacher_pert
| 学习器 | auc | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |
|---|---|---|---|---|---|---|
| real | 0.733 | 0.676 | 0.786 | 0.756 | 0.783 | 0.027 |
| shuffled | 0.669 | 0.607 | 0.728 | 0.707 | 0.722 | 0.027 |
| random | 0.667 | 0.602 | 0.732 | 0.708 | 0.727 | 0.030 |
| real_binary | 0.698 | 0.645 | 0.744 | 0.721 | 0.745 | 0.024 |
| real_wshuf | 0.717 | 0.651 | 0.777 | 0.749 | 0.775 | 0.028 |
| linear | 0.737 | 0.659 | 0.802 | 0.768 | — | 0.021 |

配对差（auc；A − B）：
- ★real − shuffled: +0.064 [+0.058, +0.071] → **meaningful-strict**
- ★real − random: +0.066 [+0.059, +0.074] → **meaningful-strict**
- shuffled − random: +0.002 [-0.001, +0.005] → **equivalent**
- real − real_binary: +0.036 [+0.033, +0.039] → **meaningful-strict**
- real − real_wshuf: +0.016 [+0.013, +0.019] → **small-real**
- real − linear: -0.004 [-0.008, +0.001] → **equivalent**
- linear − random: +0.070 [+0.065, +0.076] → **meaningful-strict**
- （acc50）real − random: +0.074 [+0.067, +0.082] → meaningful-strict
- （noisy）real − random: +0.048 [+0.040, +0.057] → meaningful-strict
- （silenced）real − random: +0.057 [+0.048, +0.066] → meaningful-strict

## teacher_shuf
| 学习器 | auc | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |
|---|---|---|---|---|---|---|
| real | 0.606 | 0.558 | 0.649 | 0.637 | 0.647 | 0.028 |
| shuffled | 0.624 | 0.564 | 0.670 | 0.654 | 0.667 | 0.023 |
| random | 0.623 | 0.562 | 0.675 | 0.664 | 0.676 | 0.027 |
| real_binary | 0.601 | 0.552 | 0.644 | 0.637 | 0.646 | 0.024 |
| real_wshuf | 0.614 | 0.561 | 0.656 | 0.645 | 0.653 | 0.023 |
| linear | 0.668 | 0.602 | 0.725 | 0.705 | — | 0.022 |

配对差（auc；A − B）：
- real − shuffled: -0.018 [-0.022, -0.014] → **small-real**
- real − random: -0.016 [-0.021, -0.012] → **small-real**
- ★shuffled − random: +0.001 [-0.002, +0.005] → **equivalent**
- real − real_binary: +0.005 [+0.002, +0.008] → **small-real**
- real − real_wshuf: -0.007 [-0.010, -0.004] → **small-real**
- real − linear: -0.061 [-0.067, -0.056] → **meaningful-strict**
- linear − random: +0.045 [+0.041, +0.049] → **meaningful-strict**
- （acc50）real − random: -0.004 [-0.009, +0.001] → equivalent
- （noisy）real − random: -0.026 [-0.034, -0.020] → small-real
- （silenced）real − random: -0.028 [-0.035, -0.021] → small-real

## teacher_real
| 学习器 | auc | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |
|---|---|---|---|---|---|---|
| real | 0.766 | 0.716 | 0.810 | 0.776 | 0.806 | 0.023 |
| shuffled | 0.684 | 0.611 | 0.743 | 0.719 | 0.741 | 0.030 |
| random | 0.683 | 0.605 | 0.748 | 0.726 | 0.746 | 0.034 |
| real_binary | 0.731 | 0.667 | 0.780 | 0.753 | 0.781 | 0.025 |
| real_wshuf | 0.748 | 0.673 | 0.812 | 0.780 | 0.811 | 0.031 |
| linear | 0.759 | 0.675 | 0.828 | 0.789 | — | 0.020 |

配对差（auc；A − B）：
- real − shuffled: +0.082 [+0.077, +0.087] → **meaningful-strict**
- real − random: +0.084 [+0.078, +0.089] → **meaningful-strict**
- shuffled − random: +0.001 [-0.002, +0.005] → **equivalent**
- real − real_binary: +0.036 [+0.033, +0.038] → **meaningful-strict**
- real − real_wshuf: +0.018 [+0.015, +0.021] → **small-real**
- real − linear: +0.007 [+0.004, +0.011] → **small-real**
- linear − random: +0.076 [+0.071, +0.082] → **meaningful-strict**
- （acc50）real − random: +0.110 [+0.101, +0.120] → meaningful-strict
- （noisy）real − random: +0.050 [+0.041, +0.058] → meaningful-strict
- （silenced）real − random: +0.060 [+0.052, +0.069] → meaningful-strict

## teacher_random
| 学习器 | auc | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |
|---|---|---|---|---|---|---|
| real | 0.557 | 0.532 | 0.573 | 0.569 | 0.568 | 0.018 |
| shuffled | 0.566 | 0.535 | 0.589 | 0.582 | 0.588 | 0.019 |
| random | 0.567 | 0.533 | 0.597 | 0.589 | 0.594 | 0.022 |
| real_binary | 0.554 | 0.527 | 0.574 | 0.569 | 0.569 | 0.020 |
| real_wshuf | 0.560 | 0.532 | 0.581 | 0.578 | 0.580 | 0.019 |
| linear | 0.594 | 0.549 | 0.626 | 0.616 | — | 0.022 |

配对差（auc；A − B）：
- real − shuffled: -0.009 [-0.011, -0.006] → **small-real**
- real − random: -0.010 [-0.013, -0.007] → **small-real**
- shuffled − random: -0.001 [-0.003, +0.001] → **equivalent**
- real − real_binary: +0.003 [+0.001, +0.005] → **small-real**
- real − real_wshuf: -0.004 [-0.006, -0.002] → **small-real**
- real − linear: -0.038 [-0.040, -0.035] → **meaningful-strict**
- linear − random: +0.027 [+0.024, +0.030] → **small-real**
- （acc50）real − random: -0.001 [-0.006, +0.004] → equivalent
- （noisy）real − random: -0.020 [-0.026, -0.013] → small-real
- （silenced）real − random: -0.025 [-0.032, -0.019] → small-real

## linear_teacher
| 学习器 | auc | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |
|---|---|---|---|---|---|---|
| real | 0.666 | 0.612 | 0.716 | 0.697 | 0.714 | 0.029 |
| shuffled | 0.701 | 0.628 | 0.770 | 0.741 | 0.761 | 0.030 |
| random | 0.699 | 0.625 | 0.772 | 0.747 | 0.768 | 0.033 |
| real_binary | 0.661 | 0.599 | 0.722 | 0.702 | 0.719 | 0.035 |
| real_wshuf | 0.682 | 0.617 | 0.737 | 0.716 | 0.736 | 0.033 |
| linear | 0.793 | 0.697 | 0.879 | 0.834 | — | 0.016 |

配对差（auc；A − B）：
- real − shuffled: -0.035 [-0.040, -0.030] → **meaningful-strict**
- real − random: -0.033 [-0.038, -0.028] → **meaningful (边缘)**
- shuffled − random: +0.002 [-0.002, +0.005] → **equivalent**
- real − real_binary: +0.005 [+0.002, +0.009] → **small-real**
- real − real_wshuf: -0.015 [-0.019, -0.012] → **small-real**
- real − linear: -0.127 [-0.132, -0.121] → **meaningful-strict**
- linear − random: +0.093 [+0.088, +0.099] → **meaningful-strict**
- （acc50）real − random: -0.014 [-0.021, -0.007] → small-real
- （noisy）real − random: -0.050 [-0.058, -0.042] → meaningful-strict
- （silenced）real − random: -0.054 [-0.062, -0.045] → meaningful-strict

## door_class
| 学习器 | auc | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |
|---|---|---|---|---|---|---|
| real | 0.674 | 0.647 | 0.694 | 0.684 | 0.691 | 0.058 |
| shuffled | 0.665 | 0.645 | 0.686 | 0.681 | 0.683 | 0.060 |
| random | 0.675 | 0.655 | 0.691 | 0.683 | 0.688 | 0.059 |
| real_binary | 0.670 | 0.649 | 0.690 | 0.680 | 0.683 | 0.061 |
| real_wshuf | 0.667 | 0.642 | 0.686 | 0.681 | 0.685 | 0.060 |
| linear | 0.674 | 0.644 | 0.702 | 0.693 | — | 0.056 |

配对差（auc；A − B）：
- ★real − shuffled: +0.008 [+0.005, +0.012] → **small-real**
- ★real − random: -0.001 [-0.006, +0.004] → **equivalent**
- shuffled − random: -0.009 [-0.013, -0.006] → **small-real**
- real − real_binary: +0.003 [-0.000, +0.007] → **equivalent**
- real − real_wshuf: +0.007 [+0.004, +0.009] → **small-real**
- real − linear: -0.000 [-0.005, +0.005] → **equivalent**
- linear − random: -0.001 [-0.006, +0.004] → **equivalent**
- （acc50）real − random: -0.008 [-0.015, -0.001] → small-real
- （noisy）real − random: +0.001 [-0.007, +0.009] → equivalent
- （silenced）real − random: +0.003 [-0.004, +0.010] → equivalent

## door_teacher_real
| 学习器 | auc | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |
|---|---|---|---|---|---|---|
| real | 0.768 | 0.727 | 0.809 | 0.778 | 0.805 | 0.033 |
| shuffled | 0.740 | 0.706 | 0.770 | 0.755 | 0.768 | 0.036 |
| random | 0.734 | 0.707 | 0.761 | 0.745 | 0.762 | 0.033 |
| real_binary | 0.747 | 0.710 | 0.783 | 0.752 | 0.785 | 0.038 |
| real_wshuf | 0.754 | 0.719 | 0.791 | 0.765 | 0.786 | 0.035 |
| linear | 0.735 | 0.697 | 0.773 | 0.731 | — | 0.033 |

配对差（auc；A − B）：
- real − shuffled: +0.028 [+0.024, +0.032] → **small-real**
- real − random: +0.034 [+0.029, +0.038] → **meaningful (边缘)**
- shuffled − random: +0.006 [+0.003, +0.009] → **small-real**
- real − real_binary: +0.021 [+0.018, +0.025] → **small-real**
- real − real_wshuf: +0.013 [+0.011, +0.016] → **small-real**
- real − linear: +0.033 [+0.027, +0.038] → **meaningful (边缘)**
- linear − random: +0.001 [-0.003, +0.005] → **equivalent**
- （acc50）real − random: +0.021 [+0.010, +0.031] → small-real
- （noisy）real − random: +0.033 [+0.025, +0.042] → meaningful (边缘)
- （silenced）real − random: +0.044 [+0.035, +0.051] → meaningful-strict

## 门槛（非循环阳性对照）
- 对比 1 teacher_pert real − shuffled: +0.064 [+0.058, +0.071] → meaningful-strict
- 对比 2 teacher_pert real − random: +0.066 [+0.059, +0.074] → meaningful-strict
- 对比 3 teacher_shuf shuffled − random: +0.001 [-0.002, +0.005] → equivalent
- 对比 4 teacher_shuf shuffled − real: +0.018 [+0.013, +0.023] → small-real
- **门槛 A（连线实例检出）：通过；门槛 B（统计类别检出）：未通过**
- door_class 解读规则见 PREREG：A、B 都通过→等价可解读为无优势；A 通过 B 不通过→只说无实例层面优势；A 不通过→不解读。

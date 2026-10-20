# 结果（第四阶段 5：KC 类别的定向病变，自动生成）

学习率固定 0.05；剂量 = 沉默的 KC 数（102 / 409 / 818 ≈ 5% / 20% / 40%）；“损失”= 完整时准确率 − 病变后准确率；“超额”= 排序病变的损失 − 同样数量随机病变的损失。三档判定，s = 0.03；主结论族（★，8 个）99.4% 区间，其余 95%；100 个测试世界（种子 5000–5099）。

## 主结论族

- ★1. door_teacher_real real：post-hoc，active 409 的超额损失: +0.045 [+0.027, +0.065] → **meaningful (边缘)**
- ★2. door_teacher_real real：post-hoc，active 818 的超额损失: +0.124 [+0.103, +0.147] → **meaningful-strict**
- ★3. door_teacher_real real：post-hoc，hub 818 的超额损失: +0.052 [+0.033, +0.071] → **meaningful-strict**
- ★4. door_teacher_real：active 409 超额损失，real − shuffled: +0.009 [-0.005, +0.024] → **equivalent**
- ★5. door_teacher_real：active 409 超额损失，real − random 连线: +0.035 [+0.018, +0.052] → **meaningful (边缘)**
- ★6. door_class real：post-hoc，active 409 的超额损失: +0.003 [-0.011, +0.017] → **equivalent**
- ★7. door_class real：post-hoc，active 818 的超额损失: +0.043 [+0.026, +0.060] → **meaningful (边缘)**
- ★8. door_teacher_real real：训练前移除，active 409 的超额损失: -0.010 [-0.020, -0.000] → **small-real**

## door_class

完整准确率：real 0.694，shuffled 0.686，random 0.691

| 连线 | 时机 | 排序 | 损失（102） | 损失（409） | 损失（818） |
|---|---|---|---|---|---|
| real | 测试时沉默 | hub | +0.001 | -0.001 | +0.004 |
| real | 测试时沉默 | active | -0.003 | +0.006 | +0.053 |
| real | 测试时沉默 | random | +0.002 | +0.003 | +0.010 |
| real | 训练前移除 | hub | +0.002 | +0.002 | +0.002 |
| real | 训练前移除 | active | -0.002 | -0.006 | +0.003 |
| real | 训练前移除 | random | +0.001 | +0.003 | +0.008 |
| shuffled | 测试时沉默 | hub | -0.000 | +0.000 | +0.007 |
| shuffled | 测试时沉默 | active | +0.001 | +0.007 | +0.034 |
| shuffled | 测试时沉默 | random | +0.001 | +0.002 | +0.006 |
| shuffled | 训练前移除 | hub | +0.000 | +0.002 | +0.005 |
| shuffled | 训练前移除 | active | -0.001 | -0.009 | -0.010 |
| shuffled | 训练前移除 | random | +0.001 | +0.002 | +0.008 |
| random | 测试时沉默 | hub | +0.001 | +0.010 | +0.007 |
| random | 测试时沉默 | active | -0.001 | +0.009 | +0.018 |
| random | 测试时沉默 | random | -0.000 | +0.005 | +0.012 |
| random | 训练前移除 | hub | +0.001 | +0.007 | +0.014 |
| random | 训练前移除 | active | +0.001 | +0.011 | +0.003 |
| random | 训练前移除 | random | +0.004 | +0.007 | +0.016 |

超额损失（排序 − 随机，95% 区间）：
- real / post / hub / 102: -0.001 [-0.003, +0.002] → equivalent
- real / post / hub / 409: -0.004 [-0.008, +0.001] → equivalent
- real / post / hub / 818: -0.007 [-0.015, +0.002] → equivalent
- real / post / active / 102: -0.005 [-0.011, +0.001] → equivalent
- real / post / active / 409: +0.003 [-0.007, +0.013] → equivalent
- real / post / active / 818: +0.043 [+0.030, +0.055] → meaningful-strict
- real / pre / hub / 102: +0.000 [-0.002, +0.003] → equivalent
- real / pre / hub / 409: -0.001 [-0.005, +0.003] → equivalent
- real / pre / hub / 818: -0.006 [-0.012, -0.001] → small-real
- real / pre / active / 102: -0.003 [-0.008, +0.002] → equivalent
- real / pre / active / 409: -0.009 [-0.015, -0.003] → small-real
- real / pre / active / 818: -0.004 [-0.011, +0.002] → equivalent
- shuffled / post / hub / 102: -0.001 [-0.004, +0.001] → equivalent
- shuffled / post / hub / 409: -0.002 [-0.005, +0.002] → equivalent
- shuffled / post / hub / 818: +0.002 [-0.005, +0.008] → equivalent
- shuffled / post / active / 102: -0.000 [-0.007, +0.006] → equivalent
- shuffled / post / active / 409: +0.005 [-0.006, +0.015] → equivalent
- shuffled / post / active / 818: +0.028 [+0.015, +0.040] → small-real
- shuffled / pre / hub / 102: -0.001 [-0.003, +0.001] → equivalent
- shuffled / pre / hub / 409: +0.000 [-0.003, +0.004] → equivalent
- shuffled / pre / hub / 818: -0.002 [-0.008, +0.003] → equivalent
- shuffled / pre / active / 102: -0.002 [-0.006, +0.003] → equivalent
- shuffled / pre / active / 409: -0.012 [-0.017, -0.006] → small-real
- shuffled / pre / active / 818: -0.017 [-0.024, -0.011] → small-real
- random / post / hub / 102: +0.001 [-0.002, +0.004] → equivalent
- random / post / hub / 409: +0.005 [+0.000, +0.009] → small-real
- random / post / hub / 818: -0.005 [-0.011, +0.000] → equivalent
- random / post / active / 102: -0.001 [-0.006, +0.004] → equivalent
- random / post / active / 409: +0.004 [-0.003, +0.011] → equivalent
- random / post / active / 818: +0.006 [-0.003, +0.016] → equivalent
- random / pre / hub / 102: -0.002 [-0.005, +0.001] → equivalent
- random / pre / hub / 409: -0.000 [-0.004, +0.004] → equivalent
- random / pre / hub / 818: -0.002 [-0.006, +0.002] → equivalent
- random / pre / active / 102: -0.003 [-0.007, +0.002] → equivalent
- random / pre / active / 409: +0.004 [-0.002, +0.009] → equivalent
- random / pre / active / 818: -0.012 [-0.021, -0.004] → small-real

## door_teacher_real

完整准确率：real 0.809，shuffled 0.770，random 0.767

| 连线 | 时机 | 排序 | 损失（102） | 损失（409） | 损失（818） |
|---|---|---|---|---|---|
| real | 测试时沉默 | hub | +0.002 | -0.003 | +0.066 |
| real | 测试时沉默 | active | -0.001 | +0.050 | +0.138 |
| real | 测试时沉默 | random | +0.003 | +0.005 | +0.014 |
| real | 训练前移除 | hub | +0.004 | -0.005 | +0.001 |
| real | 训练前移除 | active | -0.006 | -0.005 | +0.008 |
| real | 训练前移除 | random | +0.003 | +0.005 | +0.010 |
| shuffled | 测试时沉默 | hub | -0.001 | -0.002 | +0.010 |
| shuffled | 测试时沉默 | active | +0.004 | +0.036 | +0.107 |
| shuffled | 测试时沉默 | random | -0.002 | +0.000 | +0.009 |
| shuffled | 训练前移除 | hub | -0.002 | -0.000 | +0.003 |
| shuffled | 训练前移除 | active | -0.004 | -0.003 | +0.019 |
| shuffled | 训练前移除 | random | -0.002 | -0.000 | +0.009 |
| random | 测试时沉默 | hub | +0.001 | +0.006 | +0.009 |
| random | 测试时沉默 | active | +0.001 | +0.013 | +0.044 |
| random | 测试时沉默 | random | -0.000 | +0.002 | +0.005 |
| random | 训练前移除 | hub | +0.001 | +0.010 | +0.008 |
| random | 训练前移除 | active | -0.003 | -0.002 | +0.013 |
| random | 训练前移除 | random | +0.001 | +0.003 | +0.010 |

超额损失（排序 − 随机，95% 区间）：
- real / post / hub / 102: -0.001 [-0.003, +0.001] → equivalent
- real / post / hub / 409: -0.008 [-0.013, -0.003] → small-real
- real / post / hub / 818: +0.052 [+0.039, +0.066] → meaningful-strict
- real / post / active / 102: -0.004 [-0.009, +0.001] → equivalent
- real / post / active / 409: +0.045 [+0.032, +0.059] → meaningful-strict
- real / post / active / 818: +0.124 [+0.108, +0.140] → meaningful-strict
- real / pre / hub / 102: +0.001 [-0.001, +0.003] → equivalent
- real / pre / hub / 409: -0.010 [-0.014, -0.006] → small-real
- real / pre / hub / 818: -0.009 [-0.015, -0.003] → small-real
- real / pre / active / 102: -0.008 [-0.013, -0.004] → small-real
- real / pre / active / 409: -0.010 [-0.017, -0.003] → small-real
- real / pre / active / 818: -0.002 [-0.009, +0.005] → equivalent
- shuffled / post / hub / 102: +0.001 [-0.002, +0.003] → equivalent
- shuffled / post / hub / 409: -0.002 [-0.006, +0.002] → equivalent
- shuffled / post / hub / 818: +0.001 [-0.006, +0.008] → equivalent
- shuffled / post / active / 102: +0.006 [-0.000, +0.012] → equivalent
- shuffled / post / active / 409: +0.036 [+0.026, +0.046] → meaningful (边缘)
- shuffled / post / active / 818: +0.098 [+0.082, +0.114] → meaningful-strict
- shuffled / pre / hub / 102: +0.000 [-0.003, +0.003] → equivalent
- shuffled / pre / hub / 409: -0.000 [-0.004, +0.003] → equivalent
- shuffled / pre / hub / 818: -0.006 [-0.011, -0.001] → small-real
- shuffled / pre / active / 102: -0.002 [-0.007, +0.003] → equivalent
- shuffled / pre / active / 409: -0.003 [-0.010, +0.003] → equivalent
- shuffled / pre / active / 818: +0.010 [+0.002, +0.017] → small-real
- random / post / hub / 102: +0.002 [-0.002, +0.005] → equivalent
- random / post / hub / 409: +0.004 [-0.001, +0.009] → equivalent
- random / post / hub / 818: +0.004 [-0.002, +0.009] → equivalent
- random / post / active / 102: +0.001 [-0.005, +0.006] → equivalent
- random / post / active / 409: +0.011 [+0.004, +0.018] → small-real
- random / post / active / 818: +0.039 [+0.028, +0.050] → meaningful (边缘)
- random / pre / hub / 102: -0.000 [-0.004, +0.004] → equivalent
- random / pre / hub / 409: +0.006 [+0.002, +0.010] → small-real
- random / pre / hub / 818: -0.002 [-0.006, +0.002] → equivalent
- random / pre / active / 102: -0.004 [-0.008, +0.001] → equivalent
- random / pre / active / 409: -0.005 [-0.011, +0.001] → equivalent
- random / pre / active / 818: +0.003 [-0.005, +0.010] → equivalent

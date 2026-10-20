# 结果（第四阶段 5b：嗅小球通道的定向病变，自动生成）

学习率 0.05；剂量 = 沉默的嗅小球通道数（3 / 7 / 13，约 5% / 10% / 20%）；超额 = 排序病变的损失 − 同样数量随机通道的损失。三档判定，s = 0.03；主结论族（★，7 个）99.3% 区间，其余 95%；100 个测试世界。

## 主结论族

- ★1. door_class real：post，hub 13 个通道的超额损失: +0.019 [+0.002, +0.035] → **small-real**
- ★2. door_class real：post，bridger 13 个通道的超额损失: +0.003 [-0.009, +0.015] → **equivalent**
- ★3. door_class real：pre，hub 13 个通道的超额损失: +0.012 [-0.001, +0.026] → **equivalent**
- ★4. door_teacher_real real：pre，hub 13 个通道的超额损失（教师用同一连线，循环，见登记）: +0.068 [+0.054, +0.083] → **meaningful-strict**
- ★5. door_teacher_real real：pre，bridger 13 个通道的超额损失: -0.009 [-0.021, +0.001] → **equivalent**
- ★6. door_teacher_real：post，hub 13 的超额损失，real − shuffled: +0.059 [+0.038, +0.081] → **meaningful-strict**
- ★7. door_class：post，hub 13 的超额损失，real − shuffled: +0.017 [-0.004, +0.037] → **uncertain**

## door_class

完整准确率：real 0.693，shuffled 0.686，random 0.692；hub 与 bridger 前 7 名的重叠个数：real 1.0，shuffled 1.4，random 1.5

超额损失（95% 区间）：
- real / post / hub / 3: -0.003 [-0.010, +0.004] → equivalent
- real / post / hub / 7: +0.024 [+0.013, +0.034] → small-real
- real / post / hub / 13: +0.019 [+0.007, +0.031] → small-real
- real / post / bridger / 3: +0.004 [-0.001, +0.010] → equivalent
- real / post / bridger / 7: -0.000 [-0.008, +0.008] → equivalent
- real / post / bridger / 13: +0.003 [-0.006, +0.012] → equivalent
- real / pre / hub / 3: -0.004 [-0.011, +0.003] → equivalent
- real / pre / hub / 7: +0.015 [+0.008, +0.023] → small-real
- real / pre / hub / 13: +0.012 [+0.003, +0.022] → small-real
- real / pre / bridger / 3: -0.000 [-0.005, +0.005] → equivalent
- real / pre / bridger / 7: -0.004 [-0.010, +0.002] → equivalent
- real / pre / bridger / 13: -0.007 [-0.015, +0.000] → equivalent
- shuffled / post / hub / 3: -0.001 [-0.005, +0.002] → equivalent
- shuffled / post / hub / 7: +0.001 [-0.006, +0.007] → equivalent
- shuffled / post / hub / 13: +0.002 [-0.008, +0.012] → equivalent
- shuffled / post / bridger / 3: +0.001 [-0.003, +0.004] → equivalent
- shuffled / post / bridger / 7: +0.001 [-0.005, +0.006] → equivalent
- shuffled / post / bridger / 13: +0.001 [-0.007, +0.009] → equivalent
- shuffled / pre / hub / 3: +0.001 [-0.003, +0.005] → equivalent
- shuffled / pre / hub / 7: +0.000 [-0.007, +0.007] → equivalent
- shuffled / pre / hub / 13: +0.001 [-0.007, +0.009] → equivalent
- shuffled / pre / bridger / 3: +0.001 [-0.004, +0.005] → equivalent
- shuffled / pre / bridger / 7: +0.003 [-0.003, +0.009] → equivalent
- shuffled / pre / bridger / 13: -0.001 [-0.009, +0.008] → equivalent
- random / post / hub / 3: -0.002 [-0.008, +0.005] → equivalent
- random / post / hub / 7: +0.001 [-0.006, +0.008] → equivalent
- random / post / hub / 13: +0.000 [-0.007, +0.008] → equivalent
- random / post / bridger / 3: +0.003 [-0.003, +0.010] → equivalent
- random / post / bridger / 7: +0.001 [-0.008, +0.009] → equivalent
- random / post / bridger / 13: -0.002 [-0.011, +0.008] → equivalent
- random / pre / hub / 3: +0.000 [-0.005, +0.005] → equivalent
- random / pre / hub / 7: +0.004 [-0.002, +0.011] → equivalent
- random / pre / hub / 13: -0.001 [-0.009, +0.007] → equivalent
- random / pre / bridger / 3: +0.002 [-0.004, +0.008] → equivalent
- random / pre / bridger / 7: +0.004 [-0.004, +0.010] → equivalent
- random / pre / bridger / 13: -0.001 [-0.009, +0.007] → equivalent

## door_teacher_real

完整准确率：real 0.809，shuffled 0.770，random 0.766；hub 与 bridger 前 7 名的重叠个数：real 1.0，shuffled 1.4，random 1.5

超额损失（95% 区间）：
- real / post / hub / 3: +0.011 [+0.004, +0.017] → small-real
- real / post / hub / 7: +0.066 [+0.055, +0.076] → meaningful-strict
- real / post / hub / 13: +0.060 [+0.047, +0.073] → meaningful-strict
- real / post / bridger / 3: +0.023 [+0.017, +0.028] → small-real
- real / post / bridger / 7: +0.005 [-0.002, +0.013] → equivalent
- real / post / bridger / 13: -0.023 [-0.032, -0.014] → small-real
- real / pre / hub / 3: +0.006 [-0.001, +0.013] → equivalent
- real / pre / hub / 7: +0.059 [+0.050, +0.069] → meaningful-strict
- real / pre / hub / 13: +0.068 [+0.058, +0.078] → meaningful-strict
- real / pre / bridger / 3: +0.022 [+0.018, +0.027] → small-real
- real / pre / bridger / 7: +0.010 [+0.004, +0.017] → small-real
- real / pre / bridger / 13: -0.009 [-0.017, -0.002] → small-real
- shuffled / post / hub / 3: -0.004 [-0.009, +0.002] → equivalent
- shuffled / post / hub / 7: -0.003 [-0.011, +0.005] → equivalent
- shuffled / post / hub / 13: +0.000 [-0.010, +0.010] → equivalent
- shuffled / post / bridger / 3: -0.002 [-0.008, +0.004] → equivalent
- shuffled / post / bridger / 7: +0.002 [-0.005, +0.010] → equivalent
- shuffled / post / bridger / 13: +0.006 [-0.004, +0.016] → equivalent
- shuffled / pre / hub / 3: -0.001 [-0.006, +0.004] → equivalent
- shuffled / pre / hub / 7: -0.001 [-0.008, +0.007] → equivalent
- shuffled / pre / hub / 13: +0.001 [-0.008, +0.011] → equivalent
- shuffled / pre / bridger / 3: +0.000 [-0.006, +0.006] → equivalent
- shuffled / pre / bridger / 7: +0.001 [-0.006, +0.007] → equivalent
- shuffled / pre / bridger / 13: +0.010 [+0.002, +0.018] → small-real
- random / post / hub / 3: -0.003 [-0.008, +0.003] → equivalent
- random / post / hub / 7: -0.000 [-0.009, +0.008] → equivalent
- random / post / hub / 13: +0.000 [-0.010, +0.011] → equivalent
- random / post / bridger / 3: +0.001 [-0.005, +0.007] → equivalent
- random / post / bridger / 7: -0.001 [-0.009, +0.006] → equivalent
- random / post / bridger / 13: +0.002 [-0.009, +0.013] → equivalent
- random / pre / hub / 3: -0.004 [-0.009, +0.002] → equivalent
- random / pre / hub / 7: -0.000 [-0.007, +0.007] → equivalent
- random / pre / hub / 13: +0.002 [-0.006, +0.010] → equivalent
- random / pre / bridger / 3: -0.002 [-0.007, +0.004] → equivalent
- random / pre / bridger / 7: -0.000 [-0.007, +0.007] → equivalent
- random / pre / bridger / 13: +0.003 [-0.006, +0.012] → equivalent

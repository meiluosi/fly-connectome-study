# 预先登记：第四阶段 0b（非循环阳性对照 + 指标修正）

写于运行 0b 测试之前。0b 是对阶段 0 的登记偏离重跑，原因见 `NOTES_v4_stage0.md` 与 `verification/review_stage0.md`。冻结文件与哈希：`PREREG_v4_stage0b.sha256`（含调参结果，调参先于冻结）。阶段 0 的代码与结果保持不变。

## 与阶段 0 的差别
1. **阳性对照改为非循环：** 教师连线不再是学生能“拿到”的同一实例。
   - `teacher_pert`：教师 = 真实连线，但每个 KC 30% 的输入边被挪到别的 PN 行（保持每个 KC 的突触数）。真实学生只拿到“大部分一致”的连线；打乱、随机学生没有。检验：真实连线的优势在教师连线不完全一致时是否还在。
   - `teacher_shuf`：教师 = 一个新抽的“打乱（保度数）”连线。学生里的打乱连线是另一个实例，只有统计类别相同。检验：连线的**统计类别**匹配能否被检出。
   - 保留 `teacher_real`、`teacher_random`、`linear_teacher`、`door_class`、`door_teacher_real`（沿用阶段 0 的定义，仅供对照；teacher_real 与 door_teacher_real 的优势按阶段 0 的审查视为循环，不当作独立证据）。`family` 不再运行（饱和）。
2. **指标修正：** KC 沉默改为真正移除（被沉默的 KC 不能发放，编码取其余 KC 的前 5%，b0 与 sc 重算）；线性学习器的沉默指标不定义。acc50 在第 50 次试验读取（每 10 次评估一次，auc 由此计算，与阶段 0 的 auc 不可直接比数值）。
3. 学习率网格加入 0.02：MB {0.02, 0.05, 0.15, 0.4, 1.0}，线性 {0.1, 0.3, 1.0, 3.0}。其余（调参种子 1000–1019、测试种子 5000–5099、前 5% KC、s = 0.03）不变。
4. 不再运行“+ad”：阶段 0 显示该规则冲掉连线（约 15 次激活后只剩 46%），无法检验“连线作初始化”。留给之后换成保守的适应规则再做。
5. 勘误：阶段 0 登记写“300 个测试气味”“47 个小球”，实际 door 任务的测试集为 91 个留出气味，odours.npz 覆盖 46 个小球。

## 学习器与评估
MB 学生 ∈ {real, shuffled, random, real_binary, real_wshuf}，线性学生；评估同阶段 0（配对差、对世界自助法 4000 次）。三档判定同阶段 0（s = 0.03）。另报“严格”标记：区间下界也 ≥ s 才写 meaningful-strict；表里 meaningful 但下界 < s 的写为 meaningful（边缘）。

**主结论族（6 个，99.2% 区间，auc）：**
1. teacher_pert：real − shuffled
2. teacher_pert：real − random
3. teacher_shuf：shuffled − random
4. teacher_shuf：shuffled − real
5. door_class：real − random
6. door_class：real − shuffled

其余（其他任务与学习器对、acc50、final、noisy、silenced）为描述性，95% 区间。

## 门槛与解读规则（预测不是判据）
- **连线实例检出（门槛 A）：** 对比 1 与 2 都为 real 更好的 meaningful。通过则认为流程能检出“连线与任务大体一致”的优势。
- **统计类别检出（门槛 B）：** 对比 3 或 4 为 shuffled 更好的 meaningful。通过则认为流程能检出连线统计类别的优势。
- door_class 的结论按门槛写：A 与 B 都通过——“等价”可解读为这个任务上没有连线优势；A 通过、B 不通过——只能说没有实例层面的优势，类别层面检不出；A 不通过——写“设计未通过非循环阳性对照”，不解读 door 任务。
- 预测：A 通过（real 优势缩小但存在）；B 不通过（阶段 0 的 teacher_random 已显示类别匹配没有优势）；door_class 等价。

## 已知局限（接受）
教师—学生任务衡量的是与教师连线的一致程度，不是自然适应性；30% 重连是任选的扰动强度，只测一档；door 的类别标签是随机分配；适应（+ad）与行为验证不在 0b 内。

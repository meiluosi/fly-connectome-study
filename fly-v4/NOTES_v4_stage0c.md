# 第四阶段 0c：保守的无监督适应（登记：`PREREG_v4_stage0c.md`，数字：`RESULTS_v4_stage0c.md`）

这一阶段没有做独立审查（共用代码已在阶段 0 审查中看过；0c 新增的只有 `v4core_c.py` 的适应包装）。

## 结果（eta_p = 0.01，99.2% 区间，auc）
| 任务 | real+ad − random+ad | 适应对 real 的效果（real+ad − real） |
|---|---|---|
| door_class | −0.004，等价 | −0.001，等价 |
| door_teacher_real | +0.013，small-real | −0.021，small-real（变差） |
| teacher_pert | +0.062，meaningful-strict | +0.004，small-real |

## 怎么读
- 温和的适应（柱的余弦保留约 0.93）没有提高样本效率：三个任务上适应的效果要么等价，要么是 small-real，door_teacher_real 上还略变差。“把连线当初始化”在这套规则里没有测出好处。
- teacher_pert 上 real 的优势在适应后还在（+0.062，与不适应的 +0.066 相当），说明适应不是把优势抹掉的原因；door_teacher_real 上 real − random 从 +0.034 缩到 +0.013，是适应让真实连线自己变差，不是随机稀疏变好。
- door_class 在所有设置下都是等价：真实气味 + 随机类别标签，无论适应与否，没有测出连线优势。
- 局限：规则是任选的一种 Hebbian 形式；只测三档强度；教师相关任务的优势来自教师本身用了真实连线（阶段 0 审查的循环性）。

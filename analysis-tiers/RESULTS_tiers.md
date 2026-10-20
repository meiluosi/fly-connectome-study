# 三档判定的重新分析（旧规则 vs 新规则；不重跑任何实验）

s = 各任务登记的最小有意义效应（TSP 0.5 个百分点，R4 0.25；觅食与元学习 6；遗忘 4）。区间均为 95%。

旧规则：区间整体在 ±s 内 = 等价；区间不含 0 且|均值|≥s = 更好/更差；否则不确定。新规则增加“小而可检出”：区间不含 0 但|均值|<s。

共 147 个对比。旧→新 的转移计数：

- 旧“better/worse” → 新“meaningful”：55
- 旧“equivalent” → 新“equivalent”：57
- 旧“equivalent” → 新“small-real”：15
- 旧“uncertain” → 新“small-real”：10
- 旧“uncertain” → 新“uncertain”：10

## 判定发生变化的对比（旧≠新）
| 任务 | 对比 | 差 [95% 区间] | s | 旧 | 新 |
|---|---|---|---|---|---|
| TSP v2 R3 | ON-real - ACO | -0.26 [-0.38, -0.13] | 0.5 | equivalent | **small-real** |
| TSP v2 R3 | ON-random - ACO | -0.25 [-0.37, -0.12] | 0.5 | equivalent | **small-real** |
| TSP v2 R3 | ON-real - ON-linear | -0.15 [-0.27, -0.03] | 0.5 | equivalent | **small-real** |
| TSP v2 R3 | HET4-real - ACO | -0.19 [-0.32, -0.07] | 0.5 | equivalent | **small-real** |
| TSP v2 R3 | ISL4x - ACO | -0.33 [-0.46, -0.21] | 0.5 | equivalent | **small-real** |
| TSP v2 R4 | ISL4x - ACO | +0.14 [+0.07, +0.21] | 0.25 | equivalent | **small-real** |
| TSP v3 R2 | HAND-turn - ACO | +0.32 [+0.16, +0.47] | 0.5 | equivalent | **small-real** |
| TSP v3 R2 | TURN-real - HAND-turn | -0.28 [-0.44, -0.13] | 0.5 | equivalent | **small-real** |
| TSP v3 R3 | TURN-real - ACO | -0.18 [-0.32, -0.05] | 0.5 | equivalent | **small-real** |
| TSP v3 R3 | TURN-random - ACO | -0.33 [-0.46, -0.19] | 0.5 | equivalent | **small-real** |
| TSP v3 R3 | TURN-linear - ACO | -0.18 [-0.33, -0.04] | 0.5 | equivalent | **small-real** |
| TSP v3 R3 | HAND-turn - ACO | -0.13 [-0.26, -0.01] | 0.5 | equivalent | **small-real** |
| TSP v3 R3 | TURN-real - TURN-random | +0.14 [+0.00, +0.29] | 0.5 | equivalent | **small-real** |
| TSP v3 R3 | ON-real - ACO | -0.28 [-0.42, -0.14] | 0.5 | equivalent | **small-real** |
| TSP v3 R3 | ON-random - ACO | -0.35 [-0.49, -0.21] | 0.5 | equivalent | **small-real** |
| foraging consistent | MB_real_binary - MB_real | +3.29 [+0.07, +6.45] | 6 | uncertain | **small-real** |
| foraging conflict | MB_real - linear_valence | +4.34 [+0.90, +7.76] | 6 | uncertain | **small-real** |
| meta (first run) indist | shuffled es0: evolved - default | +4.76 [+0.85, +8.76] | 6 | uncertain | **small-real** |
| meta (first run) indist | shuffled es1: evolved - default | +5.24 [+1.13, +9.44] | 6 | uncertain | **small-real** |
| meta (first run) indist | shuffled es2: evolved - default | +4.91 [+0.59, +9.20] | 6 | uncertain | **small-real** |
| forget fast | decay=0.001 - decay=0 | +3.52 [+1.91, +5.18] | 4 | uncertain | **small-real** |
| forget fast | decay=0.03 - decay=0 | +3.24 [+1.37, +5.04] | 4 | uncertain | **small-real** |
| forget fast | lrx0.5 - decay=0 | -2.88 [-4.45, -1.36] | 4 | uncertain | **small-real** |
| forget indist | lrx0.5 - decay=0 | -3.64 [-7.42, -0.09] | 4 | uncertain | **small-real** |
| forget stationary | decay=0.0001 - decay=0 | -3.82 [-6.34, -1.19] | 4 | uncertain | **small-real** |

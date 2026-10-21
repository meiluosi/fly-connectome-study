# 结果（第四阶段 7：自然气味统计上的表示层检验，自动生成）

DoOR 2.0 的 301 个气味分子 × 65 个嗅小球响应；T1 = 9 个化学类别的少样本最近质心分类（平衡准确率），T2 = 150 个气味的 5 近邻在 KC 编码与 DoOR 空间之间的重合比例。三档判定 s = 0.03；主结论族（★，6 个）99.2% 区间，其余 95%；100 个世界（种子 5000–5099）。随机水平约 0.11（T1）。

| 表示 | 2-shot 准确率 | 5-shot 准确率 | 近邻重合 |
|---|---|---|---|
| real | 0.262 | 0.349 | 0.669 |
| shuffled | 0.256 | 0.332 | 0.695 |
| random | 0.252 | 0.329 | 0.670 |
| real_binary | 0.258 | 0.345 | 0.684 |
| real_wshuf | 0.262 | 0.326 | 0.696 |
| raw | 0.280 | 0.351 | 1.000 |

配对差：
- ★acc_2shot: real − shuffled = +0.006 [-0.010, +0.021] → **equivalent**
- ★acc_2shot: real − random = +0.010 [-0.006, +0.024] → **equivalent**
- acc_2shot: real − real_binary = +0.003 [-0.003, +0.010] → **equivalent**
- acc_2shot: real − real_wshuf = +0.000 [-0.012, +0.012] → **equivalent**
- acc_2shot: real − raw = -0.019 [-0.030, -0.008] → **small-real**
- acc_2shot: random − shuffled = -0.004 [-0.016, +0.008] → **equivalent**
- ★acc_5shot: real − shuffled = +0.017 [-0.001, +0.036] → **uncertain**
- ★acc_5shot: real − random = +0.020 [+0.002, +0.040] → **small-real**
- acc_5shot: real − real_binary = +0.004 [-0.005, +0.012] → **equivalent**
- acc_5shot: real − real_wshuf = +0.023 [+0.009, +0.037] → **small-real**
- acc_5shot: real − raw = -0.002 [-0.016, +0.012] → **equivalent**
- acc_5shot: random − shuffled = -0.003 [-0.017, +0.010] → **equivalent**
- ★retrieval: real − shuffled = -0.026 [-0.033, -0.019] → **small-real**
- ★retrieval: real − random = -0.001 [-0.008, +0.006] → **equivalent**
- retrieval: real − real_binary = -0.016 [-0.020, -0.012] → **small-real**
- retrieval: real − real_wshuf = -0.027 [-0.032, -0.022] → **small-real**
- retrieval: real − raw = -0.331 [-0.335, -0.328] → **meaningful-strict**
- retrieval: random − shuffled = -0.025 [-0.030, -0.019] → **small-real**

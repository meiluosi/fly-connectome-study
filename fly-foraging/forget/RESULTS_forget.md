# 结果（forget 实验，自动生成）

平均净奖励（100 个新世界，种子 6000–6099）：

| 配置 | fast | in-dist | stationary |
|---|---|---|---|
| decay=0 | +5.2 | +28.0 | +68.6 |
| decay=0.0001 | +4.9 | +25.6 | +64.7 |
| decay=0.001 | +8.8 | +38.2 | +55.7 |
| decay=0.003 | +17.4 | +37.4 | +44.6 |
| decay=0.01 | +17.7 | +25.9 | +27.9 |
| decay=0.03 | +8.5 | +10.8 | +13.8 |
| lrx0.25 | -0.4 | +16.5 | +55.1 |
| lrx0.5 | +2.4 | +24.4 | +63.0 |
| lrx2 | +5.0 | +25.1 | +65.8 |
| lrx4 | +4.0 | +23.6 | +60.0 |
| asym(0.4,0.8) | +5.2 | +26.1 | +62.7 |
| asym(0.8,0.4) | +5.2 | +27.8 | +65.7 |
| asym(0.4,1.6) | +4.2 | +25.6 | +62.6 |
| evo0 | +7.7 | +35.0 | +71.6 |
| evo0+decay=0.001 | +10.6 | +44.2 | +58.7 |
| evo0+decay=0.01 | +17.1 | +24.2 | +26.8 |
| evo1 | +6.4 | +31.8 | +73.8 |
| evo1+decay=0.001 | +7.8 | +39.8 | +59.5 |
| evo1+decay=0.01 | +19.7 | +26.8 | +29.7 |
| evo2 | +6.0 | +30.7 | +75.2 |
| evo2+decay=0.001 | +11.0 | +40.9 | +62.0 |
| evo2+decay=0.01 | +20.0 | +27.9 | +31.1 |

配对差（净奖励；等价边界 ±4；★ 主结论族，97.5% 区间；其余 95% 描述性）：

### 遗忘扫描（对 decay=0）
- [fast] decay=0.0001 − decay=0: -0.3 [-1.8, +1.2] → **equivalent**
- [fast] ★decay=0.001 − decay=0: +3.5 [+1.6, +5.4] → **uncertain**
- [fast] decay=0.003 − decay=0: +12.1 [+9.9, +14.4] → **A better**
- [fast] ★decay=0.01 − decay=0: +12.4 [+9.8, +15.0] → **A better**
- [fast] decay=0.03 − decay=0: +3.2 [+1.4, +5.0] → **uncertain**
- [indist] decay=0.0001 − decay=0: -2.4 [-6.6, +1.8] → **uncertain**
- [indist] decay=0.001 − decay=0: +10.2 [+6.8, +13.5] → **A better**
- [indist] decay=0.003 − decay=0: +9.4 [+5.7, +12.9] → **A better**
- [indist] decay=0.01 − decay=0: -2.2 [-6.1, +1.5] → **uncertain**
- [indist] decay=0.03 − decay=0: -17.2 [-21.1, -13.5] → **A worse**
- [stationary] decay=0.0001 − decay=0: -3.8 [-6.4, -1.2] → **uncertain**
- [stationary] decay=0.001 − decay=0: -12.8 [-15.8, -9.6] → **A worse**
- [stationary] decay=0.003 − decay=0: -23.9 [-27.2, -20.4] → **A worse**
- [stationary] decay=0.01 − decay=0: -40.7 [-44.0, -37.3] → **A worse**
- [stationary] decay=0.03 − decay=0: -54.8 [-58.4, -51.0] → **A worse**

### 学习速度（对默认学习率）
- [fast] lrx0.25 − decay=0: -5.6 [-7.1, -4.0] → **A worse**
- [fast] lrx0.5 − decay=0: -2.9 [-4.4, -1.3] → **uncertain**
- [fast] lrx2 − decay=0: -0.2 [-1.8, +1.3] → **equivalent**
- [fast] lrx4 − decay=0: -1.2 [-3.0, +0.5] → **equivalent**
- [indist] lrx0.25 − decay=0: -11.6 [-15.5, -7.9] → **A worse**
- [indist] lrx0.5 − decay=0: -3.6 [-7.5, +0.1] → **uncertain**
- [indist] lrx2 − decay=0: -2.9 [-6.6, +0.7] → **uncertain**
- [indist] lrx4 − decay=0: -4.4 [-9.5, +0.3] → **uncertain**
- [stationary] lrx0.25 − decay=0: -13.4 [-16.6, -10.0] → **A worse**
- [stationary] lrx0.5 − decay=0: -5.5 [-8.7, -2.2] → **A worse**
- [stationary] lrx2 − decay=0: -2.8 [-8.3, +2.6] → **uncertain**
- [stationary] lrx4 − decay=0: -8.6 [-16.1, -0.9] → **A worse**

### 不对称（对对称默认）
- [fast] asym(0.4,0.8) − decay=0: -0.0 [-1.6, +1.6] → **equivalent**
- [fast] asym(0.8,0.4) − decay=0: -0.1 [-1.6, +1.5] → **equivalent**
- [fast] asym(0.4,1.6) − decay=0: -1.1 [-2.6, +0.6] → **equivalent**
- [indist] asym(0.4,0.8) − decay=0: -2.0 [-5.9, +1.8] → **uncertain**
- [indist] asym(0.8,0.4) − decay=0: -0.2 [-4.1, +3.7] → **uncertain**
- [indist] asym(0.4,1.6) − decay=0: -2.5 [-7.0, +2.3] → **uncertain**
- [stationary] asym(0.4,0.8) − decay=0: -5.9 [-11.7, -0.0] → **A worse**
- [stationary] asym(0.8,0.4) − decay=0: -2.8 [-4.7, -0.8] → **uncertain**
- [stationary] asym(0.4,1.6) − decay=0: -6.0 [-13.3, +1.2] → **uncertain**

### 进化结果上强制遗忘（对原进化结果）
- [fast] evo0+decay=0.001 − evo0: +2.9 [+1.0, +4.9] → **uncertain**
- [fast] evo0+decay=0.01 − evo0: +9.4 [+7.0, +11.8] → **A better**
- [fast] evo1+decay=0.001 − evo1: +1.4 [-0.5, +3.3] → **equivalent**
- [fast] evo1+decay=0.01 − evo1: +13.2 [+11.2, +15.2] → **A better**
- [fast] evo2+decay=0.001 − evo2: +5.1 [+3.1, +7.0] → **A better**
- [fast] evo2+decay=0.01 − evo2: +14.1 [+11.8, +16.3] → **A better**
- [indist] evo0+decay=0.001 − evo0: +9.2 [+5.1, +13.3] → **A better**
- [indist] evo0+decay=0.01 − evo0: -10.8 [-15.8, -6.1] → **A worse**
- [indist] evo1+decay=0.001 − evo1: +8.0 [+3.5, +12.3] → **A better**
- [indist] evo1+decay=0.01 − evo1: -5.0 [-10.0, -0.3] → **A worse**
- [indist] evo2+decay=0.001 − evo2: +10.1 [+6.1, +14.1] → **A better**
- [indist] evo2+decay=0.01 − evo2: -2.9 [-7.3, +1.3] → **uncertain**
- [stationary] evo0+decay=0.001 − evo0: -13.0 [-16.0, -9.7] → **A worse**
- [stationary] evo0+decay=0.01 − evo0: -44.9 [-48.1, -41.6] → **A worse**
- [stationary] evo1+decay=0.001 − evo1: -14.2 [-17.6, -10.7] → **A worse**
- [stationary] evo1+decay=0.01 − evo1: -44.1 [-48.5, -39.4] → **A worse**
- [stationary] evo2+decay=0.001 − evo2: -13.2 [-16.7, -9.5] → **A worse**
- [stationary] evo2+decay=0.01 − evo2: -44.1 [-47.9, -40.1] → **A worse**

### 学习速度的交互：fast 的提升 − stationary 的提升（lrx2 − 默认）
- +2.5 [-2.8, +8.2]

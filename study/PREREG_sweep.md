# 预先登记：real vs shuffled 扫描（写于运行之前）
主要问题：在 forgetting 上，真实隔间 vs 打乱隔间有无差异？
- 主检验网格（rho=0, coding=pn）：T ∈ {6,12,24,48} × 分配 ∈ {random, concentrated, roundrobin} = 12 格，每格 60 个配对种子。
- 指标：配对差 forgetting(real) − forgetting(shuffled)，4000 次自助法 95% 区间；12 个检验用 Holm 校正（用自助法 p 值：双侧）。
- 等价边界 δ = 0.02（绝对 forgetting 量）：区间完全落在 [−δ,+δ] 内，判为"本设定下无实质差异"。
- 稳健性（不进入 Holm）：coding ∈ {random, pn_norm}，rho ∈ {0, 0.1}，T ∈ {12,48}，分配 random。
- 结论规则：若 12 格校正后均不显著，且多数格落在等价边界内 → 空结果成立；若某格校正后显著 → 单独报告方向与条件。
- 不做事后换指标。

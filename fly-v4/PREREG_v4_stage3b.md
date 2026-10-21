# 预先登记：第四阶段 3b（个体差异：加入第三只果蝇，hemibrain）

写于运行测试之前。冻结文件与哈希：`PREREG_v4_stage3b.sha256`。无调参（学习率固定 0.05）。设计沿用 `PREREG_v4_stage3.md`，只在下面几点不同。

## 数据
hemibrain v1.2（雌性，右半球 MB；Janelia FlyEM，CC BY 4.0）。经用户同意下载：`https://storage.googleapis.com/hemibrain/v1.2/exported-traced-adjacencies-v1.2.tar.gz`，45,872,577 字节，sha256 `07d8946eb0c4e3a5cb23d5769c9817847494f9fcadbc0ca239eed7bbd5555cf7`（原始文件放在 `data_hemibrain/`，不入库）。`build_hemibrain.py` 取 traced-neurons.csv 与 traced-total-connections.csv，嗅小球 = PN 类型名在下划线之前的前缀，KC = 类型名以 KC 开头；得到 1927 个 KC（1801 个有 PN 输入）、12426 条 PN→KC 连接，覆盖参考的 65 个嗅小球中的 62 个，每个 KC 平均 5.73 个嗅小球、总权重 91.1（MaleCNS 约 97，FlyWire 约 57–69）。

## 与阶段 3 的差别
- 五个半球：M_R、M_L（MaleCNS）、F_R、F_L（FlyWire）、H_R（hemibrain）。每个半球随机抽 K = 1801 个 KC（hemibrain 有输入的 KC 只有 1801 个，是限制），KC→MBON 矩阵取固定随机子集的 1801 行；因此阶段 3b 的数值与阶段 3（K = 2018）不能直接比。
- 任务：teacher_H_R、teacher_M_R、teacher_F_R、door_class（定义同阶段 3）。学习器：M_R、M_L、F_R、F_L、H_R、shuf_H_R、marg_M_R、marg_F_R、marg_H_R、random。
- 学习率固定 0.05（不再做 0.15 的描述性）。测试种子 5000–5099。

## 主结论族（9 个，99.4% 区间，auc，三档 s = 0.03，meaningful-strict 要求区间下界也 ≥ s）
1. teacher_H_R：M_R − random；2. teacher_H_R：F_R − random；3. teacher_H_R：M_R − marg_M_R；4. teacher_H_R：F_R − marg_F_R；
5. teacher_M_R：H_R − random；6. teacher_M_R：H_R − marg_H_R；7. teacher_F_R：H_R − random；8. teacher_F_R：H_R − marg_H_R；
9. door_class：H_R − M_R（个体差异）。
其余为描述性（95%）。teacher_X 上学生 X 本身是自指的上限，只作参照。

## 解读规则与预测（预测不是判据）
- 同阶段 3：与 random 的差为 meaningful，说明跨个体共享可用结构；与 marg 的差为等价或 small-real，说明优势主要来自嗅小球层面的输入总量。
- 预测（来自调参种子 1000–1003 的预试，不是测试）：teacher_H_R 上自指的 H_R 最好（0.652），其余约 0.617–0.620，比 random（0.607）高约 +0.01；跨个体优势比阶段 3 的更小。

## 已知局限
同阶段 3；三只果蝇（两只雌、一只雄）仍然很少；hemibrain 和 FlyWire 是同一性别但不同个体，突触检测方法不同；hemibrain 的 KC 数量限制了 K。

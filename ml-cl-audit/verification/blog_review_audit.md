# Blog review (BLOG.md vs results files), ranked

Numbers: all headline figures match RESULTS_audit(.md/_auto.md): H1 gaps 0.054/0.060/0.131 and 0.046/0.060/0.099, NCM, ER-1000 0.76, EWC 0.05-0.10, replication numbers. No transcription errors found. Problems are framing.

## A. Claims stronger than evidence / misleading
1. **Title and one-liner: "更简单的方法" / "更标准的统计方法（SLDA）".** SLDA needs a d x d covariance and inversion; the post concedes this only later (H1). The genuinely simpler method (NCM) does NOT beat FlyModel on MNIST/CIFAR-A, and beats F0 only on strong features (0.533/0.541 vs 0.508; ties F1 0.540). Rewrite title: "...被一个同样免回放、但需要估计协方差的方法（SLDA）超过".
2. **H2 "论文的对照" is mislabeled.** The +0.56/+0.13/+0.07 are the registered F2 (my own L2-normalised class-sum-dot dense control, no beta tuning; review item 7). The paper-style dense control F2b is chance (gap +0.66/+0.33/+0.50). Quote: "论文的对照是在稠密特征上用同一个 Hebbian 类和点积规则，稀疏的优势是 +0.56". Rewrite: "我登记的稠密对照（L2 归一化的 Hebbian 类和点积，未调 beta）下优势为 +0.56…；论文式 min-max 版本直接是随机水平。"
3. **"约 17 倍 / 约 7 倍" appears in the opening summary as a flat result, but it is exploratory** (post hoc, flagged only in a parenthesis at the end of H2). The ratio compares gaps under two different classifiers; euclid vs cosine gives 17-19x and 5.5-7.5x. Rewrite summary: "（探索性，看到结果后加入）…约 17 倍…". Also the "-0.01" strong-feature gap has CI [-0.011,-0.005] but is tiny; "符号反过来" is fine, but don't over-read.
4. **Registered vs not (H1).** "我先登记判据…发现…被超过" implies the registered H1 was tested and failed. Registered H1 was "prototype equivalence" with only a "no advantage / beats / mixed" labelling; "被超过" is a post hoc relabel (disclosed only deep in the mistakes list). Also "三个基准一致": two of three are the same dataset with different features, and SLDA/NCM are single deterministic runs. Add: "H1 的登记标签后来改了；方向（SLDA>FlyModel）不依赖标签。"
5. **H3 interleaved stream and extended grid are post-review additions** (declared before running, but after seeing the review). Blog says "我据此加了" (ok) but the H3 heading and "ER-200: 0.61" use the interleaved result without saying the registered stream gave 0.62 and that H3's registered criterion required all three benchmarks (so it is "未完成", not "成立"). Heading currently says FlyModel beats EWC/ER-200; keep but append "（按登记判据整体未完成）".
6. **"追平" for NCM on strong features** understates: NCM > F0 by 0.025-0.033.

## B. Missing caveats from the results files
- Backprop hyper-parameters tuned on 1 seed; tuning budget asymmetric (FlyModel 12 configs vs ER 3 before extension).
- Hidden width 3360/20480 vs stated 3200/20000 (unlisted deviation); 5-pass sensitivity run not done.
- Offline upper bound for CIFAR-B has 3 seeds; SLDA/NCM have no intervals.
- "学习时准确率 0.98" (interleaved) and "恰好 0.5039 / 0.0500" (validation, lr>=1e-3 configs; registered test values 0.516/0.0523) are mixed in adjacent paragraphs without stream labels.
- Memory loss (0.089 vs paper 0.07, replicated) and H4 dropped; "遗忘" is defined but never reported, and the post says FlyModel "不遗忘" while its memory loss is ~0.09. Explain: loss comes from class competition, not overwriting.
- CIFAR-100 replication switched to 224x224 features after seeing results (REPLICATION_NOTES appendix A, post hoc).

## C. Clarity
- Undefined: k-WTA ("5%" is 1/20 for MNIST but 1% for CIFAR-100 default), beta, min-max, "学习时准确率", "交错流" vs "类内顺序流" (never defined in the post), F0/F1 (the post never names them; say "FlyModel(论文默认)" each time), "弱/强特征" (32x32 vs upsampled 224x224).
- Logic gap: "构造性不遗忘" holds also with clip only because increments are non-negative (verified in review); one sentence would help.

## D. Tone
Mostly honest. "我自己犯的错" mixes engineering bugs (cache race, irrelevant to conclusions) with design flaws (matter). Compress the bugs to one line; keep the unfair-stream flaw prominent. "先登记不能防止设计缺陷" is good. One-liner should add: "EWC/回放的对比只在 MNIST-20 完成。"

## E. Figures
- fig1: supports H1/H3 text; numbers correct. Misses: no error bars (SLDA/NCM single run), does not mark registered vs post-hoc stream, "EWC/微调" are interleaved-stream values (only in title), FlyModel bars mix F0/F1 (labelled, fine). "未完成" cells are honest.
- fig2: numbers match, but legend "论文式对照" is the mislabel in A2; blue points use euclid NCM only; no CIs; title omits "探索性". Add that tag to title/legend.

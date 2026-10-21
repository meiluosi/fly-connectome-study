"""Global multiplicity re-analysis of the starred (headline) contrasts of all fly-v4 stages.
Each RESULTS_v4_stage*.md line marked with a star carries (mean, [lo, hi]) at the stage's family-wise level. We back out a normal-approximation SE from the interval
(SE = (hi - lo) / (2 z_level)), compute a two-sided p, and apply Holm and Benjamini-Hochberg across ALL starred contrasts of all stages (one global family).
Normal approximation to a bootstrap interval: approximate, intended to show which headlines survive a global correction, not as a replacement for the per-stage analyses."""
import re, os, math
from statistics import NormalDist
HERE=os.path.dirname(os.path.abspath(__file__)); N=NormalDist()
STAGES=[("0","RESULTS_v4_stage0.md",99.3,0.03),("0b","RESULTS_v4_stage0b.md",99.2,0.03),("0c","RESULTS_v4_stage0c.md",99.2,0.03),("2","RESULTS_v4_stage2.md",99.4,None),
        ("3","RESULTS_v4_stage3.md",99.4,0.03),("4","RESULTS_v4_stage4.md",99.3,0.03),("5","RESULTS_v4_stage5.md",99.4,0.03),("5b","RESULTS_v4_stage5b.md",99.3,0.03),
        ("6b","RESULTS_v4_stage6b.md",98.8,6.0),("6c","RESULTS_v4_stage6c.md",98.8,6.0),("6d","RESULTS_v4_stage6d.md",98.8,6.0)]
pat=re.compile(r"★\s*(.*?)[:：=]\s*([+-]?\d+\.\d+)\s*\[([+-]?\d+\.\d+),\s*([+-]?\d+\.\d+)\]\s*→\s*\**([^*\n（(]+)")
rows=[]
for st,fn,lev,s in STAGES:
    ctx=""
    for line in open(os.path.join(HERE,fn),encoding="utf-8"):
        h=re.match(r"#{2,3}\s+(\S+)",line)
        if h: ctx=h.group(1)
        if "★" not in line: continue
        m=pat.search(line)
        if not m: continue
        lab,mean,lo,hi,tier=m.group(1).strip("- ").strip(),float(m.group(2)),float(m.group(3)),float(m.group(4)),m.group(5).strip()
        z=N.inv_cdf(1-(1-lev/100)/2); se=(hi-lo)/(2*z)
        p=2*(1-N.cdf(abs(mean)/se)) if se>0 else 0.0
        rows.append(dict(stage=st,label=((ctx+'：') if ctx and not lab.startswith(ctx) and len(ctx)<28 else '')+lab[:90],mean=mean,lo=lo,hi=hi,tier=tier,p=p))
n=len(rows); idx=sorted(range(n),key=lambda i:rows[i]["p"])
holm=[None]*n; run=0.0
for rank,i in enumerate(idx):
    run=max(run,min(1.0,(n-rank)*rows[i]["p"])); holm[i]=run
bh=[None]*n; prev=1.0
for rank in range(n-1,-1,-1):
    i=idx[rank]; prev=min(prev,rows[i]["p"]*n/(rank+1)); bh[i]=prev
out=[f"# 全局多重比较再分析（{n} 个主结论对比，fly-v4 阶段 0–6d）\n",
 "各阶段的区间已按阶段内的主结论族校正（见各 PREREG）。这里把所有阶段的星标对比放进**一个**族，从区间反推正态近似的标准误和双侧 p 值，做 Holm 与 Benjamini–Hochberg 校正（α = 0.05）。这是近似，目的是看哪些头条结论在全局校正下还成立，不替代各阶段的分析。同一假设在多个阶段被检验（例如“真实 vs 随机稀疏”），所以实际独立的检验比 {n} 个少，但相关性使得校正偏保守的方向未知，这里不做依赖修正。\n".replace("{n}",str(n)),
 "| 阶段 | 对比 | 均值 [阶段区间] | 阶段判定 | p（近似） | Holm 调整 p | BH 调整 p | 全局 Holm 下显著 |\n|---|---|---|---|---|---|---|---|"]
for i,r in enumerate(rows): out.append(f"| {r['stage']} | {r['label']} | {r['mean']:+.3f} [{r['lo']:+.3f}, {r['hi']:+.3f}] | {r['tier']} | {r['p']:.2g} | {holm[i]:.2g} | {bh[i]:.2g} | {'是' if holm[i]<0.05 else '否'} |")
sig=[i for i in range(n) if holm[i]<0.05]; strict=[i for i in sig if "strict" in rows[i]["tier"]]
out.append(f"\n全局 Holm 下 {len(sig)}/{n} 个显著；其中阶段内判定为 meaningful-strict 的有 {len(strict)} 个。阶段内判定为“meaningful（边缘）”或 small-real 的结果，在全局校正后是否仍显著，见表中最后一列；显著只表示区间不含 0，不表示效应超过最小有意义效应。")
open(os.path.join(HERE,"MULTIPLICITY.md"),"w",encoding="utf-8").write("\n".join(out)+"\n"); print("\n".join(out[:3])[:200]); print(n,"contrasts;",len(sig),"significant under global Holm;",len(strict),"of them strict")
for st in sorted({r['stage'] for r in rows}): print(st,sum(1 for r in rows if r['stage']==st))

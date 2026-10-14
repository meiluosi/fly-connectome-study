import sys, json, numpy as np; sys.path.insert(0,'../../skills/preregistered-experiment/scripts')
from verdict import boot_ci, verdict
from forget_exp import CFG, RES
import os
M=4.0; L=[]
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def load(n,c): return np.array([json.load(open(os.path.join(RES,f"{n}__{c}__{s}.json"))) for s in range(6000,6100)])
def con(a,b,c,lev=95):
    d=load(a,c)-load(b,c); m,lo,hi=boot_ci(d,lev); return m,lo,hi,verdict(m,lo,hi,M,"high")
HEAD={("decay=0.001","decay=0","fast"),("decay=0.01","decay=0","fast")}
conds={"fast":"fast（反转周期 500）","indist":"in-dist（反转 1000/2000/3000）","stationary":"stationary（不反转）"}
P("# 结果（forget 实验，自动生成）\n\n平均净奖励（100 个新世界，种子 6000–6099）：\n\n| 配置 | fast | in-dist | stationary |\n|---|---|---|---|")
for n in CFG: P(f"| {n} | "+" | ".join(f"{load(n,c).mean():+.1f}" for c in conds)+" |")
P(f"\n配对差（净奖励；等价边界 ±{M:g}；★ 主结论族，97.5% 区间；其余 95% 描述性）：")
sets=[("遗忘扫描（对 decay=0）",[(f"decay={d:g}","decay=0") for d in (1e-4,1e-3,3e-3,1e-2,3e-2)]),
      ("学习速度（对默认学习率）",[(f"lrx{s:g}","decay=0") for s in (0.25,0.5,2,4)]),
      ("不对称（对对称默认）",[(f"asym({p:g},{n:g})","decay=0") for p,n in ((0.4,0.8),(0.8,0.4),(0.4,1.6))]),
      ("进化结果上强制遗忘（对原进化结果）",[(f"evo{e}+decay={d:g}",f"evo{e}") for e in (0,1,2) for d in (1e-3,1e-2)])]
for title,pairs in sets:
    P(f"\n### {title}")
    for c in conds:
        for a,b in pairs:
            head=(a,b,c) in HEAD; m,lo,hi,v=con(a,b,c,97.5 if head else 95); P(f"- [{c}] {'★' if head else ''}{a} − {b}: {m:+.1f} [{lo:+.1f}, {hi:+.1f}] → **{v}**")
P("\n### 学习速度的交互：fast 的提升 − stationary 的提升（lrx2 − 默认）")
d=(load("lrx2","fast")-load("decay=0","fast"))-(load("lrx2","stationary")-load("decay=0","stationary")); m,lo,hi=boot_ci(d,95); P(f"- {m:+.1f} [{lo:+.1f}, {hi:+.1f}]")
open(os.path.join(RES,"..","RESULTS_forget.md"),"w").write("\n".join(L)+"\n")

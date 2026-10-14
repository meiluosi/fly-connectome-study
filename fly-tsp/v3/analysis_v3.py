"""Registered analysis of v3. Same rules as v2: gap % vs reference; instance means over 3 reps; bootstrap over instances; equivalence margin +-0.5pp; headline family (TURN-real - ACO in R1,R2,R3; 3 contrasts) uses 99.2% CIs, the rest 95% descriptive."""
import sys, os, json, pickle, numpy as np; sys.path.insert(0,'.')
import arms3 as A
rng=np.random.default_rng(47); M=0.5; L=[]
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def load(reg,arm):
    out=np.zeros((A.NTEST,A.NREP))
    for r in range(A.NREP):
        for c in range(A.NTEST//A.CH): out[c*A.CH:(c+1)*A.CH,r]=json.load(open(f"results/{reg}/{arm}__r{r}__c{c}.json"))
    return out
def ci(d,lev,n=4000):
    d=np.asarray(d,float); m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); a=(100-lev)/2; return float(d.mean()),*[float(x) for x in np.percentile(m,[a,100-a])]
def verdict(m,lo,hi): return "等价" if (lo>-M and hi<M) else "A 更好" if (hi<0 and m<=-M) else "A 更差" if (lo>0 and m>=M) else "不确定"
HEAD={("TURN-real","ACO")}
CON=[("TURN-real","ACO"),("TURN-random","ACO"),("TURN-linear","ACO"),("HAND-turn","ACO"),("TURN-real","TURN-random"),("TURN-real","TURN-linear"),("TURN-real","HAND-turn"),("TURN-real","ON-real"),("ON-real","ACO"),("ON-random","ACO"),("NOTAU-none","ACO")]
names={"R1":"R1：均匀 n=50，500 次构造","R2":"R2：均匀 n=100，1000 次构造","R3":"R3：聚类 n=50，500 次构造"}
for reg in A.REGS:
    ref=np.array(pickle.load(open(f"cache/ref_test_{reg}.pkl","rb"))); G={}; R={}
    for a in A.ARMS:
        x=100*(load(reg,a)/ref[:,None]-1); G[a]=x.mean(1); R[a]=x.mean(0)
    assert len(G)==len(A.ARMS)
    P(f"\n## {names[reg]}（{A.NTEST} 个新测试实例；差距 %）\n| 算法 | 平均差距 [95% 区间] | 三个重复间的范围 |\n|---|---|---|")
    for a,v in G.items(): m,lo,hi=ci(v,95); P(f"| {a} | {m:.2f} [{lo:.2f}, {hi:.2f}] | {R[a].min():.2f} 到 {R[a].max():.2f} |")
    P(f"\n配对差（百分点，负 = A 更好；等价边界 ±{M}；★ = 主结论，99.2% 区间）：")
    for a,b in CON:
        lev=99.2 if (a,b) in HEAD else 95; m,lo,hi=ci(G[a]-G[b],lev); P(f"- {'★' if (a,b) in HEAD else ''}{a} − {b}: {m:+.2f} [{lo:+.2f}, {hi:+.2f}] → **{verdict(m,lo,hi)}**")
open("RESULTS_v3.md","w").write("# 结果（v3，自动生成）\n"+"\n".join(L)+"\n")

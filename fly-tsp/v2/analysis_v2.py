"""Registered analysis of the v2 evaluation. Gap = 100*(len/ref-1) vs the 30-restart 2-opt+Or-opt reference; instance-level mean over 3 replicates; bootstrap over instances.
Verdict (as v1): equivalent if CI within +-0.5pp; A better/worse if CI excludes 0 and |mean|>=0.5; otherwise uncertain. Headline family (8 contrasts) uses 99.4% CIs (Bonferroni), all others 95% and are descriptive."""
import sys, os, glob, json, pickle, numpy as np; sys.path.insert(0,'.')
import arms as A
rng=np.random.default_rng(43); M=0.5; L=[]
MARG={'R1':0.5,'R2':0.5,'R3':0.5,'R4':0.25}
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def load(reg,arm):
    nc=A.REG[reg]["ntest"]//10; out=np.zeros((A.REG[reg]["ntest"],A.NREP))
    for r in range(A.NREP):
        for c in range(nc): out[c*10:(c+1)*10,r]=json.load(open(f"results/{reg}/{arm}__r{r}__c{c}.json"))
    return out
def ci(d,lev,n=4000):
    d=np.asarray(d,float); m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); a=(100-lev)/2; return float(d.mean()),*[float(x) for x in np.percentile(m,[a,100-a])]
def verdict(m,lo,hi): return "等价" if (lo>-M and hi<M) else "A 更好" if (hi<0 and m<=-M) else "A 更差" if (lo>0 and m>=M) else "不确定"
HEAD={("ON-real","ACO"),("HET4-real","ONd-real")}
CON=[("ON-real","ACO"),("ON-linear","ACO"),("ON-random","ACO"),("ON-real","ON-random"),("ON-real","ON-shuffled"),("ON-real","ON-linear"),("NOTAU-real","ACO"),("NOTAU-real","ON-real"),("NOTAU-linear","ACO"),
     ("FROZEN-real","ACO"),("PRE-real","ACO"),("PRE-real","FROZEN-real"),("ON-real","FROZEN-real"),
     ("HET4-real","ONd-real"),("HET4-random","ONd-random"),("HET4-real","ON-real"),("HET4-real","HET4-random"),("HET4-real","HET4-shuffled"),("HET4-real","ACO"),
     ("HET4-real","HET4P-real"),("ISL4x","ACO"),("ISL4x","ISL4"),("ISL4","ACO")]
names={"R1":"R1：均匀 n=50，500 次构造","R2":"R2：均匀 n=100，1000 次构造","R3":"R3：聚类 n=50，500 次构造","R4":"R4：均匀 n=100，每条路线做 2-opt，30 次构造"}
for reg in A.REG:
    M=MARG[reg]
    arms=A.ARMS_R4 if reg=="R4" else A.ARMS
    try: ref=np.array(pickle.load(open(f"cache/ref_test_{reg}.pkl","rb")))
    except Exception: continue
    G={}; R={}
    for a in arms:
        try: x=100*(load(reg,a)/ref[:,None]-1); G[a]=x.mean(1); R[a]=x.mean(0)
        except Exception: pass
    if not G: continue
    P(f"\n## {names[reg]}（{A.REG[reg]['ntest']} 个测试实例；差距 %，相对参考解）\n| 算法 | 平均差距 [95% 区间] | 三个重复间的范围 |\n|---|---|---|")
    for a,v in G.items(): m,lo,hi=ci(v,95); P(f"| {a} | {m:.2f} [{lo:.2f}, {hi:.2f}] | {R[a].min():.2f} 到 {R[a].max():.2f} |")
    P(f"\n配对差（百分点，负 = A 更好；等价边界 ±{M}；★ = 主结论族，99.4% 区间）：")
    for a,b in CON:
        if a in G and b in G:
            lev=99.4 if (a,b) in HEAD else 95; m,lo,hi=ci(G[a]-G[b],lev); P(f"- {'★' if (a,b) in HEAD else ''}{a} − {b}: {m:+.2f} [{lo:+.2f}, {hi:+.2f}] → **{verdict(m,lo,hi)}**")
    if all(k in G for k in ("HET4-real","ONd-real","HET4-random","ONd-random")):
        m,lo,hi=ci((G["HET4-real"]-G["ONd-real"])-(G["HET4-random"]-G["ONd-random"]),95); P(f"- 差中差 [(HET4-real − ONd-real) − (HET4-random − ONd-random)]: {m:+.2f} [{lo:+.2f}, {hi:+.2f}] → **{verdict(m,lo,hi)}**")
open("RESULTS_v2.md","w").write("# 结果（v2，自动生成）\n"+"\n".join(L)+"\n")

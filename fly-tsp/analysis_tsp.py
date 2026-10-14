import json, numpy as np
rng=np.random.default_rng(41); R=json.load(open("eval_tsp.json")); L=[]; M=0.5
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def ci(d,n=4000): d=np.asarray(d,float); m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return float(d.mean()),*[float(x) for x in np.percentile(m,[2.5,97.5])]
def verdict(m,lo,hi): return "等价" if (lo>-M and hi<M) else "A 更好" if (hi<0 and m<=-M) else "A 更差" if (lo>0 and m>=M) else "不确定"
names={"R1":"R1：均匀 n=50，500 次构造","R2":"R2：均匀 n=100（规模迁移），1000 次构造","R3":"R3：聚类 n=50（分布迁移），500 次构造"}
for reg in ("R1","R2","R3"):
    ref=np.array(R["ref"][reg]); G={"ACO":100*(np.array(R["aco"][reg])/ref-1)}
    for kind in ("real","shuffled","random","linear"):
        runs=R["learners"][f"{kind}|{reg}"]; G[f"MB-{kind}" if kind!="linear" else "Linear"]=100*(np.mean([np.array(v) for v in runs.values()],axis=0)/ref-1)
    P(f"\n## {names[reg]}（100 个测试实例；相对参考解的差距，%）\n| 算法 | 平均差距 [95% 区间] | 训练种子间的离散（差距均值的范围） |\n|---|---|---|")
    for k,v in G.items():
        m,lo,hi=ci(v); sp=""
        if k!="ACO":
            kind=k.replace("MB-","").replace("Linear","linear"); per=[100*np.mean(np.array(x)/ref-1) for x in R["learners"][f"{kind}|{reg}"].values()]; sp=f"{min(per):.2f} 到 {max(per):.2f}"
        P(f"| {k} | {m:.2f} [{lo:.2f}, {hi:.2f}] | {sp} |")
    P("\n配对差（百分点，负 = A 更好；等价边界 ±0.5）：")
    for name,a,b in [("T1 MB-real − ACO","MB-real","ACO"),("T2 MB-real − MB-random","MB-real","MB-random"),("T3 MB-real − MB-shuffled","MB-real","MB-shuffled"),("T4 MB-real − Linear","MB-real","Linear")]:
        m,lo,hi=ci(G[a]-G[b]); P(f"- {name}: {m:+.2f} [{lo:+.2f}, {hi:+.2f}] → **{verdict(m,lo,hi)}**")
open("RESULTS_tsp.md","w").write("\n".join(L)); print("written")

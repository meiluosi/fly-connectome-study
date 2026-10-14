import json, numpy as np
rng=np.random.default_rng(21); R=json.load(open("eval_swarm.json")); L=[]; M=20.0
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def ci(d,n=4000): d=np.asarray(d,float); m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return float(d.mean()),*[float(x) for x in np.percentile(m,[2.5,97.5])]
def verdict(m,lo,hi): return "等价" if (lo>-M and hi<M) else "A 更好" if (lo>0 and m>=M) else "A 更差" if (hi<0 and m<=-M) else "不确定"
for cond in ("consistent","conflict"):
    rows=R[cond]; P(f"\n## {cond}（100 个新世界，20 个个体）\n| 群体 | 总净奖励 | 每个个体 |\n|---|---|---|")
    for k in ["independent","attract","observe","broadcast","ants","single"]:
        v=np.array([r[k] for r in rows]); n=1 if k=="single" else 20; P(f"| {k} | {v.mean():+.1f} | {v.mean()/n:+.1f} |")
    P("\n配对差（总量；等价边界 ±20）：")
    for name,a,b in [("S1 独立果蝇群 − 蚁群","independent","ants"),("S2 观察学习 − 独立","observe","independent"),("S3 广播 − 观察学习","broadcast","observe"),("S4 社交吸引 − 独立","attract","independent")]:
        m,lo,hi=ci(np.array([r[a] for r in rows])-np.array([r[b] for r in rows])); P(f"- {name}: {m:+.1f} [{lo:+.1f}, {hi:+.1f}] → **{verdict(m,lo,hi)}**")
    ind=np.array([r["independent"] for r in rows])/20; sg=np.array([r["single"] for r in rows]); m,lo,hi=ci(sg-ind); P(f"- S5（描述性）每个个体：单只 − 独立群体中的一只: {m:+.1f} [{lo:+.1f}, {hi:+.1f}]（拥挤成本）")
P("\n## 拥挤曲线（independent 模式，30 个 consistent 世界，种子 100–129）\n| 群体大小 | 每个个体净奖励 | 总量 |\n|---|---|---|")
c=R["crowd"]; base={n:[r["independent"] for r in R["consistent"][:30]] for n in (20,)}; single=[r["single"] for r in R["consistent"][:30]]
for n,v in [(1,single),(5,c["5"]),(10,c["10"]),(20,base[20]),(40,c["40"])]: P(f"| {n} | {np.mean(v)/n:+.1f} | {np.mean(v):+.1f} |")
open("RESULTS_swarm_eval.md","w").write("\n".join(L)); print("written")

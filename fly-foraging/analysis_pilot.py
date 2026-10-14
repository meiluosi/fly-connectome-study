import json, numpy as np
rng=np.random.default_rng(1); R=json.load(open("pilot_results.json")); L=[]
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def ci(d,n=4000): d=np.asarray(d,float); m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return d.mean(),*np.percentile(m,[2.5,97.5])
for cond,res in R.items():
    P(f"\n## 世界类型：{cond}（20 个测试世界，6000 步，第 3000 步奖励反转）")
    P("| 智能体 | 总净奖励 [95% 区间] | 每个个体 | 反转前 500 步 | 反转后 500 步 | 第一阶段 | 第二阶段 |\n|---|---|---|---|---|---|---|")
    for k,v in res.items():
        tot=[x["total"] for x in v]; m,lo,hi=ci(tot); n=20 if k=="ants20" else 1
        P(f"| {k} | {m:+.1f} [{lo:+.1f}, {hi:+.1f}] | {m/n:+.1f} | {np.mean([x['pre'] for x in v]):+.1f} | {np.mean([x['post'] for x in v]):+.1f} | {np.mean([x['p1'] for x in v]):+.1f} | {np.mean([x['p2'] for x in v]):+.1f} |")
    P("\n配对差（同一世界同一种子）：蘑菇体（真实连线）− 对照")
    for k in ["MB_shuffled","MB_random","linear_valence","no_learning","q_learner"]:
        d=[a["total"]-b["total"] for a,b in zip(res["MB_real"],res[k])]; m,lo,hi=ci(d); P(f"- 真实 − {k}: {m:+.1f} [{lo:+.1f}, {hi:+.1f}]")
    d=[a["total"]-b["total"]/20 for a,b in zip(res["MB_real"],res["ants20"])]; m,lo,hi=ci(d); P(f"- 真实 − 蚁群每只个体: {m:+.1f} [{lo:+.1f}, {hi:+.1f}]")
open("RESULTS_pilot.md","w").write("\n".join(L)); print("written")

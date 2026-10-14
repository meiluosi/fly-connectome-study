import json, numpy as np
rng=np.random.default_rng(31); D=json.load(open("eval_meta.json")); R=D["results"]; PR=D["params"]; L=[]; M=6.0
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def ci(d,n=4000): d=np.asarray(d,float); m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return float(d.mean()),*[float(x) for x in np.percentile(m,[2.5,97.5])]
def better(m,lo): return lo>0 and m>=M
P("## 进化参数（9 次进化的最终中心点）与默认\n| 连线 | 进化种子 | eta+ | eta− | 遗忘速率 | KC 稀疏度 | g_learn |\n|---|---|---|---|---|---|---|")
P("| 默认 | - | 0.40 | 0.40 | ≈0 | 0.050 | 2.0 |")
for kind in ("real","shuffled","random"):
    for es in (0,1,2): p=PR[f"{kind}|{es}"]; P(f"| {kind} | {es} | {p['eta_pos']:.2f} | {p['eta_neg']:.2f} | {p['decay']:.1e} | {p['kc_frac']:.3f} | {p['g_learn']:.2f} |")
P("\n## H1/H2：进化结果 − 默认（配对，100 个留出世界）；每格 = 3 个进化种子的差值 [95% 区间]；满足判据（区间下界>0 且均值≥6）的种子数")
verd={}
for cond,lab in (("indist","in-dist"),("fast","fast（更波动）"),("stationary","stationary（不反转）")):
    P(f"\n### {lab}")
    for kind in ("real","shuffled","random"):
        row=[];n=0; dm=[]
        for es in (0,1,2):
            d=np.array(R[f"{kind}|{es}|evolved|{cond}"])-np.array(R[f"{kind}|{es}|default|{cond}"]); m,lo,hi=ci(d); row.append(f"{m:+.1f} [{lo:+.1f},{hi:+.1f}]"); n+=better(m,lo); dm.append(m)
        verd[(cond,kind)]=n; P(f"- {kind}: "+" ; ".join(row)+f" → 满足 {n}/3 → "+("**成立**" if n>=2 else "不成立"))
P("\n## H3：进化的 real − 进化的 shuffled / random（in-dist，按进化种子配对）")
for other in ("shuffled","random"):
    row=[]
    for es in (0,1,2):
        d=np.array(R[f"real|{es}|evolved|indist"])-np.array(R[f"{other}|{es}|evolved|indist"]); m,lo,hi=ci(d); v="等价" if (lo>-M and hi<M) else ("real 更好" if (lo>0 and m>=M) else ("real 更差" if (hi<0 and m<=-M) else "不确定")); row.append(f"{m:+.1f} [{lo:+.1f},{hi:+.1f}] {v}")
    P(f"- real − {other}: "+" ; ".join(row))
P("\n## 各条件下的平均总净奖励（3 个进化种子的均值）\n| 连线 | 参数 | in-dist | fast | stationary |\n|---|---|---|---|---|")
for kind in ("real","shuffled","random"):
    for which in ("default","evolved"):
        P(f"| {kind} | {which} | "+" | ".join(f"{np.mean([np.mean(R[f'{kind}|{es}|{which}|{c}']) for es in (0,1,2)]):+.1f}" for c in ('indist','fast','stationary'))+" |")
open("RESULTS_meta.md","w").write("\n".join(L)); print("written")

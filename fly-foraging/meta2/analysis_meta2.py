import json, numpy as np
R=json.load(open("eval_meta2.json")); res=R["results"]; rng=np.random.default_rng(53); M=6.0; L=[]
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def ci(d,n=4000): d=np.asarray(d,float); m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return float(d.mean()),*[float(x) for x in np.percentile(m,[2.5,97.5])]
def get(k,w,c): return np.array(res[f"{k}|{w}|{c}"]) if False else np.array(res[f"{k}|{w}|{c}"])
def key(kind,es,which,cond): return np.array(res[f"{kind}|{es}|{which}|{cond}"])
def ok(m,lo): return lo>0 and m>=M
P("# 结果（元学习重跑 meta2，自动生成）\n\n评估世界 6100–6199（100 个），三种条件；判据：区间下界>0 且均值≥6。\n")
P("## H2：9 次进化的最终遗忘速率（初始 5.6e-4）\n| 连线 | 种子 | decay | eta+ | eta− | KC 稀疏度 | g_learn |\n|---|---|---|---|---|---|---|")
dec=[]
for kind in ("real","shuffled","random"):
    for es in (0,1,2):
        p=R["params"][f"{kind}|{es}"]["evo2"]; dec.append(p["decay"]); P(f"| {kind} | {es} | {p['decay']:.2e} | {p['eta_pos']:.2f} | {p['eta_neg']:.2f} | {p['kc_frac']:.3f} | {p['g_learn']:.2f} |")
P(f"\n≥1e-3 的进化数：{sum(d>=1e-3 for d in dec)}/9；范围 {min(dec):.1e} 到 {max(dec):.1e}")
for cond in ("indist","fast","stationary"):
    P(f"\n## {cond}：平均净奖励与配对差")
    P("| 连线 | default | evo1(第一次) | evo2(重跑) | evo2−default（各进化种子） | evo2−evo1（各进化种子） |\n|---|---|---|---|---|---|")
    for kind in ("real","shuffled","random"):
        d0=[key(kind,es,"default",cond) for es in (0,1,2)]; e1=[key(kind,es,"evo1",cond) for es in (0,1,2)]; e2=[key(kind,es,"evo2",cond) for es in (0,1,2)]
        a=[ci(e2[i]-d0[i]) for i in range(3)]; b=[ci(e2[i]-e1[i]) for i in range(3)]
        f=lambda t:f"{t[0]:+.1f} [{t[1]:+.1f},{t[2]:+.1f}]"
        P(f"| {kind} | {np.mean(d0):+.1f} | {np.mean(e1):+.1f} | {np.mean(e2):+.1f} | "+" ; ".join(f(t) for t in a)+" | "+" ; ".join(f(t) for t in b)+" |")
        if cond=="indist": P(f"|  | | | | H1 满足 {sum(ok(t[0],t[1]) for t in a)}/3 | H3 满足 {sum(ok(t[0],t[1]) for t in b)}/3 |")
P("\n## H5：in-dist 上 evo2 的 real − shuffled / random（按进化种子配对）")
for other in ("shuffled","random"):
    out=[]
    for es in (0,1,2):
        d=key("real",es,"evo2","indist")-key(other,es,"evo2","indist"); m,lo,hi=ci(d); out.append(f"{m:+.1f} [{lo:+.1f},{hi:+.1f}]")
    P(f"- real − {other}: "+" ; ".join(out))
open("RESULTS_meta2.md","w").write("\n".join(L)+"\n")

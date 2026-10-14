import json, numpy as np
rng=np.random.default_rng(11); R=json.load(open("eval_forage.json")); L=[]; MARGIN=6.0
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def ci(d,n=4000): d=np.asarray(d,float); m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return float(d.mean()),*[float(x) for x in np.percentile(m,[2.5,97.5])]
def verdict(m,lo,hi): return "等价" if (lo>-MARGIN and hi<MARGIN) else "A 更好" if (lo>0 and m>=MARGIN) else "A 更差" if (hi<0 and m<=-MARGIN) else "不确定"
for cond,res in R.items():
    P(f"\n## {cond}（200 个新世界）")
    P("| 智能体 | 平均总净奖励 | 标准差（世界间） |\n|---|---|---|")
    for k,v in res.items(): P(f"| {k} | {np.mean(v):+.1f} | {np.std(v):.1f} |")
    P("\n配对差（A − B），登记判据（等价边界 ±6）：")
    for name,a,b in [("C1 真实 − 打乱","MB_real","MB_shuffled"),("C2 真实 − 随机稀疏","MB_real","MB_random"),("C3 真实 − 线性价值","MB_real","linear_valence"),("C4 真实二值 − 真实","MB_real_binary","MB_real"),("C5 真实 − 不学习（健全性）","MB_real","no_learning")]:
        m,lo,hi=ci(np.array(res[a])-np.array(res[b])); P(f"- {name}: {m:+.1f} [{lo:+.1f}, {hi:+.1f}] → **{verdict(m,lo,hi)}**")
open("RESULTS_forage_eval.md","w").write("\n".join(L)); print("written")

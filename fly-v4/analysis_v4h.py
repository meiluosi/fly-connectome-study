"""Registered analysis of stage 6b (PREREG_v4_stage6b.md): foraging with the compartment learner. Equivalence bound +-6 net reward (as in fly-foraging/PREREG_forage.md)."""
import json, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); rng=np.random.default_rng(78); S=6.0; L=[]
ARMS=["global","comp_real","comp_shuf","comp_shufbal","no_learning"]; CONDS=["consistent","conflict"]
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def load(c,a): return np.array([json.load(open(os.path.join(HERE,"results_h",f"{c}__{a}__{s}.json")))["net"] for s in range(400,600)])
def ci(d,lev,n=10000):
    d=np.asarray(d,float); b=d[rng.integers(0,len(d),(n,len(d)))].mean(1); a=(100-lev)/2; return float(d.mean()),*[float(x) for x in np.percentile(b,[a,100-a])]
def tier(m,lo,hi):
    if lo>0 or hi<0: return "small-real" if abs(m)<S else ("meaningful-strict" if min(abs(lo),abs(hi))>=S else "meaningful (边缘)")
    return "equivalent" if (lo>-S and hi<S) else "uncertain"
B=json.load(open(os.path.join(HERE,"tuning_v4h.json")))
HEAD=[("consistent","comp_real","global"),("consistent","comp_real","comp_shufbal"),("conflict","comp_real","global"),("conflict","comp_real","comp_shufbal")]
P("# 结果（第四阶段 6b：觅食环境里的隔间学习器，自动生成）\n\n200 个全新世界（种子 400–599），T = 6000，第 3000 步奖励反转；指标 = 总净奖励；等价边界 ±6；主结论族（★，4 个）98.8% 区间，其余 95%。\n")
for c in CONDS:
    P(f"\n## {c}\n| 学习器 | 学习率 / g_learn | 净奖励 |\n|---|---|---|")
    for a in ARMS: P(f"| {a} | "+("—" if a=="no_learning" else f"{B[f'{c}|{a}']['prm']['eta']} / {B[f'{c}|{a}']['prm']['g_learn']}")+f" | {load(c,a).mean():+.1f} |")
    P("\n配对差：")
    for a,b in (("comp_real","global"),("comp_real","comp_shufbal"),("comp_real","comp_shuf"),("comp_real","no_learning"),("global","no_learning"),("global","comp_shufbal")):
        h=(c,a,b) in HEAD; m,lo,hi=ci(load(c,a)-load(c,b),98.8 if h else 95); P(f"- {'★' if h else ''}{a} − {b}: {m:+.1f} [{lo:+.1f}, {hi:+.1f}] → **{tier(m,lo,hi)}**")
open(os.path.join(HERE,"RESULTS_v4_stage6b.md"),"w").write("\n".join(L)+"\n")

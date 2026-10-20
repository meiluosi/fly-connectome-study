"""Registered analysis of stage 0c (PREREG_v4_stage0c.md)."""
import json, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); rng=np.random.default_rng(73); S=0.03; L=[]
TASKS=["door_class","door_teacher_real","teacher_pert"]; EP=(0.0,0.003,0.01,0.03); HE=0.01
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def load(t,k,e,m="auc"): return np.array([json.load(open(os.path.join(HERE,"results_c",f"{t}__{k}__{e}__{s}.json")))[m] for s in range(5000,5100)])
def ci(d,lev,n=10000):
    d=np.asarray(d,float); m=d[rng.integers(0,len(d),(n,len(d)))].mean(1); a=(100-lev)/2; return float(d.mean()),*[float(x) for x in np.percentile(m,[a,100-a])]
def tier(m,lo,hi):
    if lo>0 or hi<0: return "small-real" if abs(m)<S else ("meaningful-strict" if min(abs(lo),abs(hi))>=S else "meaningful (边缘)")
    return "equivalent" if (lo>-S and hi<S) else "uncertain"
P("# 结果（第四阶段 0c：保守的无监督适应，自动生成）\n\n三档判定，s = 0.03；主结论族（★，6 个）99.2% 区间，其余 95%；100 个测试世界。headline 适应强度 eta_p = 0.01。\n")
for t in TASKS:
    P(f"\n## {t}\n| 学习器 | "+" | ".join(f"eta_p={e} auc" for e in EP)+" | eta_p=0.01 的柱保留（余弦） |\n|---|---|---|---|---|---|")
    for k in ("real","shuffled","random"): P(f"| {k} | "+" | ".join(f"{load(t,k,e).mean():.3f}" for e in EP)+f" | {load(t,k,HE,'retention').mean():.2f} |")
    P("\n配对差（auc）：")
    for e in EP[1:]:
        for a,b,ea,eb in (("real","random",e,e),("real","shuffled",e,e)):
            h=(e==HE and b=="random"); m,lo,hi=ci(load(t,a,ea)-load(t,b,eb),99.2 if h else 95); P(f"- {'★' if h else ''}eta_p={e}: {a}+ad − {b}+ad = {m:+.3f} [{lo:+.3f}, {hi:+.3f}] → **{tier(m,lo,hi)}**")
    for e in EP[1:]:
        for k in ("real","random"):
            h=(e==HE and k=="real"); m,lo,hi=ci(load(t,k,e)-load(t,k,0.0),99.2 if h else 95); P(f"- {'★' if h else ''}eta_p={e}: {k}+ad − {k}（适应的效果）= {m:+.3f} [{lo:+.3f}, {hi:+.3f}] → **{tier(m,lo,hi)}**")
    m0,lo0,hi0=ci(load(t,"real",0.0)-load(t,"random",0.0),95); P(f"- 参照 eta_p=0: real − random = {m0:+.3f} [{lo0:+.3f}, {hi0:+.3f}] → {tier(m0,lo0,hi0)}")
open(os.path.join(HERE,"RESULTS_v4_stage0c.md"),"w").write("\n".join(L)+"\n")

"""Registered analysis of stage 3 (PREREG_v4_stage3.md)."""
import json, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); rng=np.random.default_rng(74); S=0.03; L=[]
TASKS=["teacher_M_R","teacher_F_R","teacher_M_L","teacher_F_L","door_class"]; KINDS=["M_R","M_L","F_R","F_L","shuf_M_R","shuf_F_R","marg_M_R","marg_F_R","random"]
HEAD=[("teacher_M_R","M_L","random"),("teacher_M_R","F_R","random"),("teacher_M_R","F_R","marg_F_R"),("teacher_F_R","F_L","random"),("teacher_F_R","M_R","random"),("teacher_F_R","M_R","marg_M_R"),("door_class","M_R","F_R"),("door_class","M_R","random")]
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def load(t,k,e=0.05,m="auc"): return np.array([json.load(open(os.path.join(HERE,"results_d",f"{t}__{k}__{e}__{s}.json")))[m] for s in range(5000,5100)])
def ci(d,lev,n=10000):
    d=np.asarray(d,float); m=d[rng.integers(0,len(d),(n,len(d)))].mean(1); a=(100-lev)/2; return float(d.mean()),*[float(x) for x in np.percentile(m,[a,100-a])]
def tier(m,lo,hi):
    if lo>0 or hi<0: return "small-real" if abs(m)<S else ("meaningful-strict" if min(abs(lo),abs(hi))>=S else "meaningful (边缘)")
    return "equivalent" if (lo>-S and hi<S) else "uncertain"
P("# 结果（第四阶段 3：个体差异，自动生成）\n\n三档判定，s = 0.03；主结论族（★，8 个）99.4% 区间，其余 95%；100 个测试世界（种子 5000–5099）；headline 学习率 0.05，0.15 为描述性。\n")
for t in TASKS:
    P(f"\n## {t}\n| 学习器 | auc（学习率 0.05） | auc（0.15） | 50 次后（0.05） | 最终（0.05） |\n|---|---|---|---|---|")
    for k in KINDS: P(f"| {k} | {load(t,k).mean():.3f} | {load(t,k,0.15).mean():.3f} | {load(t,k,0.05,'acc50').mean():.3f} | {load(t,k,0.05,'final').mean():.3f} |")
    P("\n配对差（auc；A − B；学习率 0.05）：")
    pairs=[(a,b) for (tt,a,b) in HEAD if tt==t]+[(a,b) for a,b in (("M_R","M_L"),("F_R","F_L"),("M_R","F_R"),("M_L","F_L"),("M_R","random"),("F_R","random"),("M_L","random"),("F_L","random"),("marg_M_R","random"),("marg_F_R","random"),("M_R","marg_M_R"),("F_R","marg_F_R"),("M_R","shuf_M_R"),("F_R","shuf_F_R")) if (t,a,b) not in HEAD]
    for a,b in pairs:
        h=(t,a,b) in HEAD; m,lo,hi=ci(load(t,a)-load(t,b),99.4 if h else 95); m2=ci(load(t,a,0.15)-load(t,b,0.15),95)
        P(f"- {'★' if h else ''}{a} − {b}: {m:+.3f} [{lo:+.3f}, {hi:+.3f}] → **{tier(m,lo,hi)}**（学习率 0.15: {m2[0]:+.3f} → {tier(*m2)}）")
open(os.path.join(HERE,"RESULTS_v4_stage3.md"),"w").write("\n".join(L)+"\n")

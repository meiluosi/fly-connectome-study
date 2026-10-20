"""Registered analysis of stage 2 (PREREG_v4_stage2.md)."""
import json, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); rng=np.random.default_rng(72); L=[]
KINDS=["real","shuffled","random","real_binary","real_wshuf"]; OV=(6,5,4,3,2,0)
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
R={k:[json.load(open(os.path.join(HERE,"results_phen",f"{k}__{s}.json"))) for s in range(5000,5100)] for k in KINDS}
def col(k,n): return np.array([r[n] for r in R[k]],float)
def G(k): return np.array([r["G"] for r in R[k]])
def boot(fun,lev,n=10000):
    w=rng.integers(0,100,(n,100)); v=np.array([fun(i) for i in w]); a=(100-lev)/2; return float(fun(np.arange(100))),*[float(x) for x in np.percentile(v,[a,100-a])]
def reldrop(k,tag,i): s=col(k,f"sep_{tag}_s")[i].mean(); d=col(k,f"sep_{tag}_d")[i].mean(); return 1-d/s
# metrics (per learner): spec = G6-G0 ; aplsel = reldrop_sim - reldrop_dis ; flip ; ratio
def M(k,name):
    return {"spec":lambda i:(G(k)[i,0]-G(k)[i,-1]).mean(),
            "aplsel":lambda i:reldrop(k,"sim",i)-reldrop(k,"dis",i),
            "flip":lambda i:col(k,"flip")[i].mean(),
            "ratio":lambda i:np.nanmean(col(k,"ratio")[i])}[name]
S={"spec":0.05,"aplsel":0.10,"flip":5.0,"ratio":0.10}
def tier(m,lo,hi,s):
    if lo>0 or hi<0: return "meaningful" if abs(m)>=s else "small-real"
    return "equivalent" if (lo>-s and hi<s) else "uncertain"
P("# 结果（第四阶段 2：行为现象复现，自动生成）\n\n每个学习器 100 个世界（种子 5000–5099），固定学习率 0.05，不调参。\n")
P("## 判据 C1–C4（每个学习器）\n")
P("| 学习器 | C1 梯度：各重叠度的平均响应（6,5,4,3,2,0） | C1 通过 | C2 稀疏→稠密的相对下降：相似 / 不相似 | C2 通过 | C3 反转：翻转所需试验数（中位数）/ 30 次内翻转比例 | C3 通过 | C4 消退：末值/峰值 | C4 通过 |\n|---|---|---|---|---|---|---|---|---|")
for k in KINDS:
    g=G(k).mean(0); c1=bool(np.all(np.diff(g)<0) and g[-1]<=0.25*g[0]); _,lo1,_=boot(M(k,"spec"),95)
    c1=c1 and lo1>0
    rs=reldrop(k,"sim",np.arange(100)); rd=reldrop(k,"dis",np.arange(100)); m2,lo2,hi2=boot(M(k,"aplsel"),95); c2=lo2>0 and m2>=S["aplsel"]
    fl=col(k,"flip"); c3=bool(np.median(fl)<=20 and (fl<30).mean()>=0.9)
    ra=np.nanmean(col(k,"ratio")); c4=bool(ra<=0.25)
    P(f"| {k} | "+", ".join(f"{x:.2f}" for x in g)+f" | {'是' if c1 else '否'} | {rs:.2f} / {rd:.2f}（差 {m2:+.2f} [{lo2:+.2f}, {hi2:+.2f}]） | {'是' if c2 else '否'} | {np.median(fl):.0f} / {(fl<30).mean():.2f} | {'是' if c3 else '否'} | {ra:.2f} | {'是' if c4 else '否'} |")
P("\n## 连线对比（主结论族 8 个，99.4% 区间；A − B，三档，s：spec 0.05、aplsel 0.10、flip 5 次、ratio 0.10）\n")
for name in ("spec","aplsel","flip","ratio"):
    for b in ("shuffled","random"):
        fa,fb=M("real",name),M(b,name); m,lo,hi=boot(lambda i:fa(i)-fb(i),99.4)
        P(f"- ★{name}: real − {b} = {m:+.3f} [{lo:+.3f}, {hi:+.3f}] → **{tier(m,lo,hi,S[name])}**")
P("\n描述性（95% 区间）：real − real_binary / real_wshuf\n")
for name in ("spec","aplsel","flip","ratio"):
    for b in ("real_binary","real_wshuf"):
        fa,fb=M("real",name),M(b,name); m,lo,hi=boot(lambda i:fa(i)-fb(i),95); P(f"- {name}: real − {b} = {m:+.3f} [{lo:+.3f}, {hi:+.3f}] → {tier(m,lo,hi,S[name])}")
open(os.path.join(HERE,"RESULTS_v4_stage2.md"),"w").write("\n".join(L)+"\n")

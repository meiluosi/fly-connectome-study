"""Applies PREREG_ablation.md: forgetting interpolated at matched learned accuracy, paired over seeds."""
import json, numpy as np
rng=np.random.default_rng(11); L=[]; P=lambda *a:(print(*a),L.append(" ".join(str(x) for x in a)))
D={r:json.load(open(f"ablate_{r}.json")) for r in ["bounded","additive0","multup","delta"]}
import os
for r in ["bounded","additive0","multup"]:
    if os.path.exists(f"ablate_ext_{r}.json"): D[r].update(json.load(open(f"ablate_ext_{r}.json")))
def curves(rule,task,cond):
    keys=sorted([k for k in D[rule] if k.startswith(f"{task}|{cond}|")],key=lambda k:float(k.split("|")[2])); n=len(D[rule][keys[0]])
    la=np.array([[r["learn_acc"] for r in D[rule][k]] for k in keys]); fo=np.array([[r["forg_acc"] for r in D[rule][k]] for k in keys]); return la,fo   # (eta, seed)
def at(la,fo,target):
    out=[]
    for s in range(la.shape[1]):
        o=np.argsort(la[:,s]); x,y=la[o,s],fo[o,s]
        out.append(np.interp(target,x,y) if x[0]<=target<=x[-1] else np.nan)
    return np.array(out)
def boot(d):
    d=d[~np.isnan(d)]; m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(4000)]); return d.mean(),*np.percentile(m,[2.5,97.5]),len(d)
for task in ["random","similar"]:
    P(f"\n## {task} 任务，T=48，MR，30 配对种子")
    P("各规则/条件的学习准确率范围（η 扫描覆盖）：")
    for r in ["bounded","additive0","multup"]:
        for cond in ["real","none"]:
            la,fo=curves(r,task,cond); P(f"- {r:9s} {cond:5s} 学习准确率均值 {la.mean(1).min():.3f}–{la.mean(1).max():.3f}；对应遗忘 {fo.mean(1).min():.3f}–{fo.mean(1).max():.3f}")
    la,fo=curves("delta",task,"delta"); P(f"- delta     学习准确率 {la.mean(1).min():.3f}–{la.mean(1).max():.3f}；遗忘 {fo.mean(1).min():.3f}–{fo.mean(1).max():.3f}")
    P("\n匹配学习量下的遗忘（real 条件）：差值 = 无界规则 − bounded，[95% 区间]，n=可插值种子数")
    for tg in [0.70,0.75,0.80,0.90]:
        lb,fb=curves("bounded",task,"real"); b=at(lb,fb,tg); row=f"- 目标 {tg:.2f}: bounded {np.nanmean(b):.3f}" if (~np.isnan(b)).any() else f"- 目标 {tg:.2f}: bounded 不可比"
        for r in ["additive0","multup"]:
            lu,fu=curves(r,task,"real"); u=at(lu,fu,tg); ok=~np.isnan(b)&~np.isnan(u)
            row+=f" | {r}: "+("不可比" if ok.sum()<10 else "%.3f 差值 %+.3f [%+.3f,%+.3f] n=%d"%(np.nanmean(u),*boot((u-b)[ok])[:3],ok.sum()))
        P(row)
    P("\nnone − real 在匹配学习量下（同一规则内，次要）：")
    for r in ["bounded","additive0","multup"]:
        lr_,fr_=curves(r,task,"real"); ln,fn=curves(r,task,"none"); row=f"- {r}:"
        for tg in [0.75,0.80,0.90,0.95]:
            a,b=at(lr_,fr_,tg),at(ln,fn,tg); ok=~np.isnan(a)&~np.isnan(b); row+=f" [{tg:.2f}] "+("n/a" if ok.sum()<10 else "%+.3f"%np.mean((b-a)[ok]))
        P(row)
    P("\ndelta 在匹配学习量下的遗忘（与回路 bounded-real 比较）：")
    ld,fd=curves("delta",task,"delta")
    for tg in [0.75,0.80,0.90]:
        a=at(ld,fd,tg); lb,fb=curves("bounded",task,"real"); b=at(lb,fb,tg); ok=~np.isnan(a)&~np.isnan(b); P(f"- 目标 {tg:.2f}: "+("delta 不可比" if ok.sum()<10 else "delta−bounded %+.3f [%+.3f,%+.3f] n=%d"%tuple(boot((a-b)[ok]))))
open("RESULTS_ablation_auto.md","w").write("\n".join(L)); print("written")

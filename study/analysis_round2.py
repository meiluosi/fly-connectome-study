"""Applies PREREG_round2.md verbatim. Writes RESULTS_round2_auto.md"""
import json, numpy as np, os
rng=np.random.default_rng(77); L=[]; P=lambda *a:(print(*a),L.append(" ".join(str(x) for x in a)))
def bci(d,n=4000): m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return float(d.mean()),*[float(x) for x in np.percentile(m,[2.5,97.5])]
P("## A. 修正后的因果剂量反应（入度分层划分，准确率遗忘，种子 4000–4029）")
for circ in ["MR","FR"]:
    d=json.load(open(f"round2_A_{circ}.json")); pr=d["parts"]; ov=np.array([p["overlap"] for p in pr]); dv=np.array([p["degvar"] for p in pr]); ln=np.array([np.mean(p["learn"]) for p in pr]); fg=np.array([np.mean(p["forg"]) for p in pr])
    X=np.c_[np.ones(len(ov)),ov,dv,ln]
    def coef(idx): return np.linalg.lstsq(X[idx],fg[idx],rcond=None)[0]
    cf=coef(np.arange(len(ov))); bs=np.array([coef(rng.integers(0,len(ov),len(ov))) for _ in range(4000)]); lo,hi=np.percentile(bs[:,1],[2.5,97.5])
    sl=np.polyfit(ov,fg,1)[0]; bsl=[np.polyfit(ov[i],fg[i],1)[0] for i in (rng.integers(0,len(ov),len(ov)) for _ in range(4000))]
    P(f"- {circ}: 重叠度范围 {d['lo']:.3f}–{d['hi']:.3f}（真实 {d['real']:.3f}）；重叠度与 degvar 相关 r={np.corrcoef(ov,dv)[0,1]:.2f}；")
    P(f"  **P-A1 偏回归系数（重叠度）{cf[1]:.4f} [{lo:.4f},{hi:.4f}] → {'通过' if lo>0 else '未通过'}**；P-A2 简单斜率 {sl:.4f} [{np.percentile(bsl,2.5):.4f},{np.percentile(bsl,97.5):.4f}] → {'通过' if np.percentile(bsl,2.5)>0 else '未通过'}；学习准确率范围 {ln.min():.3f}–{ln.max():.3f}；遗忘范围 {fg.min():.3f}–{fg.max():.3f}")
P("\n## B. 修正后的基线（种子：选择集 5000–5009，测试集 5010–5039）")
for circ in ["MR","FR"]:
    if not os.path.exists(f"round2_B_{circ}.json"): P(circ,"缺失"); continue
    R=json.load(open(f"round2_B_{circ}.json"))
    if os.path.exists(f"round2_B_ext_{circ}.json"):
        E=json.load(open(f"round2_B_ext_{circ}.json"))
        for key in R:
            for k,v in E[key].items(): R[key][k]=[v[0]]*10+v
    P(f"\n### {circ}\n| 任务 | T | fly-real(η=0.3) 学/终/忘 | delta(lr=.5) 终/忘 | EWC(λ*) 终/忘 | EWC−delta 遗忘降低 [95%] | 多头 终/忘 | delta 在 fly 学习量处的遗忘 | fly−delta(匹配学习量) [95%] |\n|---|---|---|---|---|---|---|---|---|")
    for key,res in R.items():
        task,T=key.split("_T"); g=lambda k,f,sl:np.array([x[f] for x in res[k]])[sl]; sel,tst=slice(0,10),slice(10,40)
        lam=max([1,10,100,1000],key=lambda l:g(f"ewc_{l}","final_acc",sel).mean())
        d_ew=g("delta_0.5","forg_acc",tst)-g(f"ewc_{lam}","forg_acc",tst); m,lo,hi=bci(d_ew)
        # matched learning: per-seed interpolation of delta forgetting at fly-real learned accuracy
        lrs=[0.0005,0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.25,0.5]; la=np.array([g(f"delta_{l}","learn_acc",tst) for l in lrs]); fo=np.array([g(f"delta_{l}","forg_acc",tst) for l in lrs]); fl=g("fly_real_0.3","learn_acc",tst); ff=g("fly_real_0.3","forg_acc",tst)
        dm=[]
        for sd in range(la.shape[1]):
            o=np.argsort(la[:,sd]); x,y=la[o,sd],fo[o,sd]
            dm.append(np.interp(fl[sd],x,y) if x[0]<=fl[sd]<=x[-1] else np.nan)
        dm=np.array(dm); ok=~np.isnan(dm); mm=bci((ff-dm)[ok]) if ok.sum()>=10 else None
        P(f"| {task} | {T} | {fl.mean():.2f}/{g('fly_real_0.3','final_acc',tst).mean():.3f}/{ff.mean():.3f} | {g('delta_0.5','final_acc',tst).mean():.3f}/{g('delta_0.5','forg_acc',tst).mean():.3f} | λ={lam}: {g(f'ewc_{lam}','final_acc',tst).mean():.3f}/{g(f'ewc_{lam}','forg_acc',tst).mean():.3f} | {m:+.3f} [{lo:+.3f},{hi:+.3f}] | {g('mh','final_acc',tst).mean():.3f}/{g('mh','forg_acc',tst).mean():.3f} | {np.nanmean(dm):.3f} (n={ok.sum()}) | "+(f"{mm[0]:+.3f} [{mm[1]:+.3f},{mm[2]:+.3f}]" if mm else "不可比")+" |")
open("RESULTS_round2_auto.md","w").write("\n".join(L)); print("written")

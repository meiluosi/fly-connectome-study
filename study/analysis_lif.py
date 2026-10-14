"""Applies PREREG_lif.md -> RESULTS_lif_auto.md"""
import json, os, numpy as np
rng=np.random.default_rng(5); L=[]; P=lambda *a:(print(*a),L.append(" ".join(str(x) for x in a))); TARGETS=[0.65,0.70,0.75,0.80]; MINN=24
def curves(D,cond):
    ks=sorted([k for k in D if k.startswith(f"bounded|{cond}|")],key=lambda k:float(k.split("|")[2])); return np.array([[x["learn_acc"] for x in D[k]] for k in ks]),np.array([[x["forg_acc"] for x in D[k]] for k in ks])
def at(la,fo,t):
    o=[]
    for s in range(la.shape[1]):
        i=np.argsort(la[:,s]); x,y=la[i,s],fo[i,s]; o.append(np.interp(t,x,y) if x[0]<=t<=x[-1] else np.nan)
    return np.array(o)
def ci(d): m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(4000)]); return d.mean(),*np.percentile(m,[2.5,97.5])
res={}; P("## H-L1 匹配学习量下 none−real（LIF 编码，MR，30 种子）")
for b in ["raw","top5"]:
    cells=[]
    for task in ["random","similar"]:
        for T in [12,48]:
            f=f"lif_{b}_{task}_{T}.json"
            if not os.path.exists(f): continue
            D=json.load(open(f)); r,n_=curves(D,"real"),curves(D,"none")
            P(f"- [{b}] {task} T={T}: 学习准确率范围 real {r[0].mean(1).min():.3f}–{r[0].mean(1).max():.3f}，none {n_[0].mean(1).min():.3f}–{n_[0].mean(1).max():.3f}")
            for t in TARGETS:
                x,y=at(*n_,t),at(*r,t); ok=~np.isnan(x)&~np.isnan(y); n=int(ok.sum())
                if n<MINN: cells.append("不可比"); P(f"    目标{t:.2f}: 不可比 (n={n})"); continue
                m,lo,hi=ci((x-y)[ok]); st="等价" if lo>-0.02 and hi<0.02 else "高于+0.02" if lo>0.02 else "低于-0.02" if hi<-0.02 else "其他"; cells.append(st); P(f"    目标{t:.2f}: {m:+.4f} [{lo:+.4f},{hi:+.4f}] n={n} → {st}")
    cc=[c for c in cells if c!="不可比"]
    if cc:
        eq=cc.count("等价")/len(cc); hi_=cc.count("高于+0.02")/len(cc); P(f"H-L1 [{b}]: 可比格子 {len(cc)}（不可比 {len(cells)-len(cc)}）；等价 {eq:.0%}；整体高于+0.02 {hi_:.0%} → "+("结论不变（无实质差异）" if eq>=0.75 else "结论改变（隔间化有优势）" if hi_>=0.25 else "证据不足"))
P("\n## H-L2 基线排序（fly-real η=0.3 对 delta / EWC(λ=10)；30 种子均值 学习/最终准确率/遗忘）\n| 编码 | 任务 | T | fly-real | delta | EWC | fly 最终准确率 < EWC |\n|---|---|---|---|---|---|---|")
flags=[]
for b in ["raw","top5"]:
    for task in ["random","similar"]:
        for T in [12,48]:
            f=f"lif_{b}_{task}_{T}.json"
            if not os.path.exists(f): continue
            D=json.load(open(f)); g=lambda k,m:np.mean([x[m] for x in D[k]]); fr="bounded|real|0.3"
            lt=lambda k:f"{g(k,'learn_acc'):.2f}/{g(k,'final_acc'):.3f}/{g(k,'forg_acc'):.3f}"
            fl=g(fr,"final_acc")<g("ewc10","final_acc"); flags.append(fl); P(f"| {b} | {task} | {T} | {lt(fr)} | {lt('delta')} | {lt('ewc10')} | {'是' if fl else '否'} |")
if len(flags)==8: P(f"\nH-L2: fly-real 最终准确率低于 EWC 的设定 {sum(flags)}/8 → {'通过' if all(flags) else '未通过'}")
open("RESULTS_lif_auto.md","w").write("\n".join(L)); print("written")

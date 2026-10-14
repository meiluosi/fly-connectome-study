"""Applies PREREG_matched.md verbatim -> RESULTS_matched_auto.md"""
import json, os, numpy as np
rng=np.random.default_rng(99); L=[]; P=lambda *a:(print(*a),L.append(" ".join(str(x) for x in a)))
TARGETS=[0.65,0.70,0.75,0.80]; MINN=30
def curves(D,rule,cond):
    ks=sorted([k for k in D if k.startswith(f"{rule}|{cond}|")],key=lambda k:float(k.split("|")[2]))
    return np.array([[x["learn_acc"] for x in D[k]] for k in ks]),np.array([[x["forg_acc"] for x in D[k]] for k in ks])
def at(la,fo,t):
    o=[]
    for s in range(la.shape[1]):
        i=np.argsort(la[:,s]); x,y=la[i,s],fo[i,s]; o.append(np.interp(t,x,y) if x[0]<=t<=x[-1] else np.nan)
    return np.array(o)
def ci(d): m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(4000)]); return d.mean(),*np.percentile(m,[2.5,97.5])
cells={"M1":[],"M2":[]}
P("## 逐格结果（遗忘差；n=可比种子数；区间为自助法 95%）")
for circ in ["MR","FR"]:
    for task in ["random","similar"]:
        for T in [12,48]:
            f=f"matched_{circ}_{task}_{T}.json"
            if not os.path.exists(f): continue
            D=json.load(open(f)); br=curves(D,"bounded","real"); bn=curves(D,"bounded","none"); ar=curves(D,"additive0","real")
            for t in TARGETS:
                a,b,c_=at(*br,t),at(*bn,t),at(*ar,t)
                for name,x,y,lab in [("M1",b,a,"none−real(bounded)"),("M2",c_,a,"additive0−bounded(real)")]:
                    ok=~np.isnan(x)&~np.isnan(y); n=int(ok.sum())
                    if n<MINN: cells[name].append(dict(circ=circ,task=task,T=T,t=t,n=n,status="不可比")); P(f"- {name} {circ} {task} T={T} 目标{t:.2f}: 不可比 (n={n})"); continue
                    m,lo,hi=ci((x-y)[ok]); st=("等价" if lo>-0.02 and hi<0.02 else "高于+0.02" if lo>0.02 else "低于-0.02" if hi<-0.02 else "其他")
                    cells[name].append(dict(circ=circ,task=task,T=T,t=t,n=n,mean=float(m),lo=float(lo),hi=float(hi),status=st)); P(f"- {name} {circ} {task} T={T} 目标{t:.2f}: {m:+.4f} [{lo:+.4f},{hi:+.4f}] n={n} → {st}")
P("\n## 判定")
c1=[c for c in cells["M1"] if c["status"]!="不可比"]
if c1:
    eq=sum(c["status"]=="等价" for c in c1); hi_=sum(c["status"]=="高于+0.02" for c in c1)
    P(f"H-M1: 可比格子 {len(c1)}（不可比 {len(cells['M1'])-len(c1)}）；等价 {eq} ({eq/len(c1):.0%})；整体高于+0.02 {hi_} ({hi_/len(c1):.0%}) → "+("匹配学习量下无实质差异" if eq/len(c1)>=0.75 else "匹配学习量下仍有隔间化优势" if hi_/len(c1)>=0.25 else "证据不足"))
    for circ in ["MR","FR"]:
        cc=[c for c in c1 if c["circ"]==circ]
        if cc: P(f"  {circ}: 可比 {len(cc)}，等价 {sum(c['status']=='等价' for c in cc)}，高于+0.02 {sum(c['status']=='高于+0.02' for c in cc)}，低于−0.02 {sum(c['status']=='低于-0.02' for c in cc)}")
for circ in ["MR","FR"]:
    c2=[c for c in cells["M2"] if c["circ"]==circ and c["status"]!="不可比"]
    if c2:
        lowc=sum(c["hi"]<0 and c["mean"]<=-0.02 for c in c2); highc=sum(c["lo"]>0.02 for c in c2)
        P(f"H-M2 {circ}: 可比格子 {len(c2)}；整体低于0且均值≤−0.02: {lowc} ({lowc/len(c2):.0%})；整体高于+0.02: {highc} ({highc/len(c2):.0%}) → "+("无界加法同学习量下遗忘更少" if lowc/len(c2)>=0.5 else "有界规则有保护作用" if highc/len(c2)>=0.5 else "证据不足"))
open("RESULTS_matched_auto.md","w").write("\n".join(L)); json.dump(cells,open("matched_cells.json","w"),indent=1); print("written")

"""Applies the verdict rules of PREREG_confirm.md verbatim. Writes RESULTS_confirm_auto.md."""
import json, numpy as np
rng=np.random.default_rng(2026); L=[]; P=lambda *a:(print(*a),L.append(" ".join(str(x) for x in a)))
def boot(d,n=4000):
    m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); p=min(1.0,2*min((m<=0).mean(),(m>=0).mean())); return d.mean(),*np.percentile(m,[2.5,97.5]),max(p,1/n)
CIR=["MR","ML","FR","FL"]
P("## P1 因果剂量反应（v2 规则，T=24，种子 1000–1029）")
for circ in ["MR","FR"]:
    try: d=json.load(open(f"confirm_p1_{circ}.json"))
    except Exception as e: P(circ,"缺失",e); continue
    parts=d["parts"]; ok=[p for p in parts if not (np.isnan(p["forg"]).any() or np.isnan(p["learned"]).any())]
    x=np.array([p["overlap"] for p in ok]); y=np.array([np.mean(p["forg"]) for p in ok]); l=np.array([np.mean(p["learned"]) for p in ok])
    sl=np.polyfit(x,y,1)[0]; bs=[np.polyfit(x[i],y[i],1)[0] for i in (rng.integers(0,len(x),len(x)) for _ in range(4000))]; lo,hi=np.percentile(bs,[2.5,97.5])
    xa=np.array([p["overlap"] for p in parts]); ya=np.array([np.nanmean(p["forg"]) for p in parts]); sla=np.polyfit(xa,ya,1)[0]
    lv={}
    for p in ok: lv.setdefault(round(p["target"],2),[]).append(np.mean(p["learned"]))
    rngL=max(np.mean(v) for v in lv.values())-min(np.mean(v) for v in lv.values())
    P(f"- {circ}: 无NaN划分 {len(ok)}/{len(parts)}；斜率 {sl:.4f} [{lo:.4f},{hi:.4f}]；全部划分(NaN种子丢弃)斜率 {sla:.4f}；学习得分各档范围 {rngL:.3f}；真实重叠 {d['real_overlap']:.3f}")
    P(f"  P1a(下界>0): {'通过' if lo>0 else '未通过'}；P1b(学习变化<0.03): {'通过' if rngL<0.03 else '未通过'}")
    ref={k:np.array(v) for k,v in d["ref"].items()}; P("  参照遗忘:",{k:round(float(np.nanmean(v[:,1])),4) for k,v in ref.items()})
P("\n## P2 / P3 行为读出（随机气味任务，60 配对种子）")
data={c:json.load(open(f"confirm_p24_{c}.json")) for c in CIR if __import__("os").path.exists(f"confirm_p24_{c}.json")}
rows=[]
for c,dd in data.items():
    for T in [12,48]:
        r=dd[f"random_T{T}"]; g=lambda m,k:np.array([x[k] for x in r[m]])
        d=g("real","forg_acc")-g("shuffled","forg_acc"); m,lo,hi,p=boot(d); rows.append((c,T,m,lo,hi,p,g("none","forg_acc").mean()-g("real","forg_acc").mean(),g("real","forg_acc").mean(),g("shuffled","forg_acc").mean()))
ps=np.array([r[5] for r in rows]); o=np.argsort(ps); holm=np.empty(len(rows)); run_=0
for rank,i in enumerate(o): run_=max(run_,min(1,(len(rows)-rank)*ps[i])); holm[i]=run_
P("| 电路 | T | real遗忘 | shuffled遗忘 | 差值 | 95%区间 | Holm p | 区间在±0.01内 | none−real |\n|---|---|---|---|---|---|---|---|---|")
for r,h in zip(rows,holm): P(f"| {r[0]} | {r[1]} | {r[7]:.3f} | {r[8]:.3f} | {r[2]:+.4f} | [{r[3]:+.4f},{r[4]:+.4f}] | {h:.3f} | {'是' if r[3]>-0.01 and r[4]<0.01 else '否'} | {r[6]:.3f} |")
if len(rows)==8:
    npos=sum(r[2]>0 for r in rows); nsig=sum((h<0.05 and r[2]>0) for r,h in zip(rows,holm))
    P(f"\nP2a: 差值为正 {npos}/8（要求≥7），Holm后显著为正 {nsig}/8（要求≥6）→ {'通过' if npos>=7 and nsig>=6 else '未通过'}")
    P(f"P3: none−real 全部 >0.05: {'通过' if all(r[6]>0.05 for r in rows) else '未通过'}（最小 {min(r[6] for r in rows):.3f}）")
P("\n## P4 相似气味任务与基线（60 配对种子）")
for task in ["random","similar"]:
    P(f"\n### {task} 任务\n| 电路 | T | fly-real 学/终/忘 | fly-shuf 终/忘 | none 终/忘 | delta 终/忘 | 最优EWC(λ) 终/忘 | multi-head 终/忘 |\n|---|---|---|---|---|---|---|---|")
    chk=[]
    for c,dd in data.items():
        for T in [12,48]:
            r=dd[f"{task}_T{T}"]; mu=lambda m,k:float(np.mean([x[k] for x in r[m]]))
            best=max(["ewc10","ewc100","ewc1000"],key=lambda m:mu(m,"final_acc"))
            P(f"| {c} | {T} | {mu('real','learn_acc'):.2f}/{mu('real','final_acc'):.3f}/{mu('real','forg_acc'):.3f} | {mu('shuffled','final_acc'):.3f}/{mu('shuffled','forg_acc'):.3f} | {mu('none','final_acc'):.3f}/{mu('none','forg_acc'):.3f} | {mu('delta','final_acc'):.3f}/{mu('delta','forg_acc'):.3f} | {best[3:]}: {mu(best,'final_acc'):.3f}/{mu(best,'forg_acc'):.3f} | {mu('mh','final_acc'):.3f}/{mu('mh','forg_acc'):.3f} |")
            chk.append((mu("delta","forg_acc")-mu(best,"forg_acc"),mu("real","final_acc")<max(mu("delta","final_acc"),mu(best,"final_acc"))))
    if task=="similar" and len(chk)==8:
        P(f"\nP4a: EWC 相对 delta 的遗忘降低 ≥0.02 的设定数 {sum(a>=0.02 for a,_ in chk)}/8（各设定降低量：{[round(a,3) for a,_ in chk]}）")
        P(f"P4b: fly-real 最终准确率低于最强基线的设定数 {sum(b for _,b in chk)}/8 → {'通过' if all(b for _,b in chk) else '未通过'}")
open("RESULTS_confirm_auto.md","w").write("\n".join(L)); print("\nwritten")

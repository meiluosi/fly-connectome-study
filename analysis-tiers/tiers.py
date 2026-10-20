"""Re-analysis of existing results with a three-tier verdict, no new runs.
Old rule (registered): equivalent if the 95% CI lies within +-s; better/worse if the CI excludes 0 AND |mean| >= s; otherwise uncertain.
New tiers (s = the same smallest effect of interest as registered):
  meaningful   CI excludes 0 and |mean| >= s                    (= old better/worse)
  small-real   CI excludes 0 and |mean| <  s                    (old rule called this 'equivalent' when the CI stayed inside +-s)
  equivalent   CI contains 0 and lies inside (-s, +s)
  uncertain    otherwise
All CIs: paired bootstrap over units (4000 resamples), 95%."""
import json, pickle, os, sys, numpy as np
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); rng=np.random.default_rng(61); out=[]
def ci(d,n=4000):
    d=np.asarray(d,float); m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return float(d.mean()),*[float(x) for x in np.percentile(m,[2.5,97.5])]
def old(m,lo,hi,s): return "equivalent" if (lo>-s and hi<s) else ("better/worse" if ((lo>0 or hi<0) and abs(m)>=s) else "uncertain")
def new(m,lo,hi,s):
    if (lo>0 or hi<0): return "meaningful" if abs(m)>=s else "small-real"
    return "equivalent" if (lo>-s and hi<s) else "uncertain"
rows=[]
def add(task,name,d,s,unit=""):
    m,lo,hi=ci(d); o=old(m,lo,hi,s); n=new(m,lo,hi,s); rows.append((task,name,m,lo,hi,s,o,n))
# ---------------- TSP v2 / v3 (gap %, lower = A shorter)
def tsp(ver,regs,arms,CON,margins):
    R=json.load(open(f"{ROOT}/fly-tsp/{ver}/results_all.json"))
    for reg in regs:
        ref=np.array(pickle.load(open(f"{ROOT}/fly-tsp/{ver}/cache/ref_test_{reg}.pkl","rb"))); G={}
        for a in arms:
            ks=[k for k in R[reg] if k.startswith(a+"__")]
            if not ks: continue
            n=len(ref); X=np.zeros((n,3)); 
            for k in ks:
                _,r,c=k.split("__"); r=int(r[1:]); c=int(c[1:]); X[c*10:(c+1)*10,r]=R[reg][k]
            G[a]=100*(X/ref[:,None]-1).mean(1)
        for a,b in CON:
            if a in G and b in G: add(f"TSP {ver} {reg}",f"{a} - {b}",G[a]-G[b],margins.get(reg,0.5))
sys.path.insert(0,f"{ROOT}/fly-tsp/v2")
tsp("v2",["R1","R2","R3","R4"],["ACO","ISL4","ISL4x","FROZEN-real","PRE-real","ON-real","ON-shuffled","ON-random","ON-linear","NOTAU-real","HET4-real","HET4-shuffled","HET4-random","HET4P-real","ONd-real","ONd-random"],
    [("ON-real","ACO"),("ON-random","ACO"),("ON-linear","ACO"),("ON-real","ON-random"),("ON-real","ON-shuffled"),("ON-real","ON-linear"),("HET4-real","ONd-real"),("HET4-real","ACO"),("HET4-real","HET4P-real"),("ISL4x","ACO"),("ISL4x","ISL4"),("ISL4","ACO"),("PRE-real","FROZEN-real")],{"R4":0.25})
tsp("v3",["R1","R2","R3"],["ACO","NOTAU-none","ON-real","ON-random","HAND-turn","TURN-real","TURN-random","TURN-linear"],
    [("TURN-real","ACO"),("TURN-random","ACO"),("TURN-linear","ACO"),("HAND-turn","ACO"),("TURN-real","TURN-random"),("TURN-real","TURN-linear"),("TURN-real","HAND-turn"),("ON-real","ACO"),("ON-random","ACO")],{})
# ---------------- foraging single fly (net reward, higher = better), s = 6
F=json.load(open(f"{ROOT}/fly-foraging/eval_forage.json"))
for w in ("consistent","conflict"):
    for a,b in [("MB_real","MB_shuffled"),("MB_real","MB_random"),("MB_real","linear_valence"),("MB_real_binary","MB_real"),("MB_real","no_learning")]:
        add(f"foraging {w}",f"{a} - {b}",np.array(F[w][a])-np.array(F[w][b]),6.0)
# ---------------- meta-learning first run and rerun (net reward), s = 6
M=json.load(open(f"{ROOT}/fly-foraging/eval_meta.json"))["results"]
for kind in ("real","shuffled","random"):
    for es in (0,1,2):
        add("meta (first run) indist",f"{kind} es{es}: evolved - default",np.array(M[f"{kind}|{es}|evolved|indist"])-np.array(M[f"{kind}|{es}|default|indist"]),6.0)
M2=json.load(open(f"{ROOT}/fly-foraging/meta2/eval_meta2.json"))["results"]
for cond in ("indist","fast","stationary"):
    for kind in ("real","shuffled","random"):
        for es in (0,1,2):
            add(f"meta rerun {cond}",f"{kind} es{es}: evo2 - default",np.array(M2[f"{kind}|{es}|evo2|{cond}"])-np.array(M2[f"{kind}|{es}|default|{cond}"]),6.0)
# ---------------- forgetting sweep (net reward), s = 4
Z=json.load(open(f"{ROOT}/fly-foraging/forget/results_all.json"))
def zv(n,c): return np.array([Z[f"{n}__{c}__{s}"] for s in range(6000,6100)])
for c in ("fast","indist","stationary"):
    for d in ("1e-04","0.001","0.003","0.01","0.03"):
        n=f"decay={float(d):g}"; add(f"forget {c}",f"{n} - decay=0",zv(n,c)-zv("decay=0",c),4.0)
    for sc in ("0.25","0.5","2","4"): add(f"forget {c}",f"lrx{sc} - decay=0",zv(f"lrx{sc}",c)-zv("decay=0",c),4.0)
# ---------------- report
lines=["# 三档判定的重新分析（旧规则 vs 新规则；不重跑任何实验）\n","s = 各任务登记的最小有意义效应（TSP 0.5 个百分点，R4 0.25；觅食与元学习 6；遗忘 4）。区间均为 95%。\n","旧规则：区间整体在 ±s 内 = 等价；区间不含 0 且|均值|≥s = 更好/更差；否则不确定。新规则增加“小而可检出”：区间不含 0 但|均值|<s。\n"]
from collections import Counter
c=Counter((r[6],r[7]) for r in rows); lines.append(f"共 {len(rows)} 个对比。旧→新 的转移计数：\n"); lines+= [f"- 旧“{o}” → 新“{n}”：{k}" for (o,n),k in sorted(c.items())]
lines.append("\n## 判定发生变化的对比（旧≠新）\n| 任务 | 对比 | 差 [95% 区间] | s | 旧 | 新 |\n|---|---|---|---|---|---|")
for t,nm,m,lo,hi,s,o,n in rows:
    chg={"equivalent":"equivalent","better/worse":"meaningful","uncertain":"uncertain"}[o]!=n
    if chg: lines.append(f"| {t} | {nm} | {m:+.2f} [{lo:+.2f}, {hi:+.2f}] | {s:g} | {o} | **{n}** |")
open("RESULTS_tiers.md","w").write("\n".join(lines)+"\n"); print("\n".join(lines))

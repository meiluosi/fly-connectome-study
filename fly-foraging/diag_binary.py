import numpy as np, json, forage as F, params as Pm
kinds=["real","real_binary","shuffled","shuffled_binary","random"]; out={}
for cond,conflict in (("consistent",False),("conflict",True)):
    res={k:[] for k in kinds}
    for s in range(20):
        rng=np.random.default_rng(900+s)
        for k in kinds:
            P=F.make_P(k,rng); w=F.World(s,T=Pm.T,rev=Pm.REV,conflict=conflict); res[k].append(float(F.run_fly(w,F.MB(P,eta=Pm.FLY_MB["eta"]),P,seed=100+s,g_learn=Pm.FLY_MB["g_learn"],k_turn=Pm.FLY_MB["k_turn"])[0].sum()))
    out[cond]=res; print(cond,{k:round(float(np.mean(v)),1) for k,v in res.items()})
rng=np.random.default_rng(4)
def ci(d,n=4000): d=np.asarray(d); m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return d.mean(),*np.percentile(m,[2.5,97.5])
for cond,res in out.items():
    for a,b in [("real_binary","real"),("real_binary","random"),("shuffled_binary","shuffled"),("random","real")]:
        m,lo,hi=ci(np.array(res[a])-np.array(res[b])); print(f"{cond:10s} {a:16s} - {b:8s} {m:+.1f} [{lo:+.1f},{hi:+.1f}]")
json.dump(out,open("diag_binary.json","w"))

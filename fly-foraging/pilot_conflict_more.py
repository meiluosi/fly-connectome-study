import numpy as np, json, forage as F, params as Pm
P0=F.P0; res={k:[] for k in ["MB_real","MB_shuffled","MB_random","linear_valence"]}
for s in range(20,80):
    mk=lambda:F.World(s,T=Pm.T,rev=Pm.REV,conflict=True); rng=np.random.default_rng(500+s); Ps=F.make_P("shuffled",rng); Pr=F.make_P("random",rng); kw=dict(g_learn=Pm.FLY_MB["g_learn"],k_turn=Pm.FLY_MB["k_turn"])
    runs={"MB_real":F.run_fly(mk(),F.MB(P0,eta=Pm.FLY_MB["eta"]),P0,seed=100+s,**kw)[0],"MB_shuffled":F.run_fly(mk(),F.MB(Ps,eta=Pm.FLY_MB["eta"]),Ps,seed=100+s,**kw)[0],"MB_random":F.run_fly(mk(),F.MB(Pr,eta=Pm.FLY_MB["eta"]),Pr,seed=100+s,**kw)[0],
          "linear_valence":F.run_fly(mk(),F.LinearValence(Pm.FLY_LINEAR["eta"]),None,seed=100+s,g_learn=Pm.FLY_LINEAR["g_learn"],k_turn=Pm.FLY_LINEAR["k_turn"])[0]}
    for k,r in runs.items(): res[k].append(float(r.sum()))
rng=np.random.default_rng(3)
def ci(d,n=4000): d=np.asarray(d); m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return d.mean(),*np.percentile(m,[2.5,97.5])
print("conflict worlds 20-79 (n=60): mean net reward"); [print(f"  {k:15s} {np.mean(v):+.1f}") for k,v in res.items()]
for k in ["MB_shuffled","MB_random","linear_valence"]:
    d=np.array(res["MB_real"])-np.array(res[k]); m,lo,hi=ci(d); print(f"  MB_real - {k:14s} {m:+.1f} [{lo:+.1f}, {hi:+.1f}]")
json.dump(res,open("pilot_conflict_more.json","w"))

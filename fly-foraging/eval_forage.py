import numpy as np, json, forage as F, params as Pm
kinds=["MB_real","MB_shuffled","MB_random","MB_real_binary","linear_valence","no_learning"]; out={}
for cond,conflict in (("consistent",False),("conflict",True)):
    res={k:[] for k in kinds}
    for s in range(100,300):
        rng=np.random.default_rng(7000+s); mk=lambda:F.World(s,T=Pm.T,rev=Pm.REV,conflict=conflict); kw=dict(g_learn=Pm.FLY_MB["g_learn"],k_turn=Pm.FLY_MB["k_turn"]); sd=5000+s
        Pr=F.make_P("random",rng); Ps=F.make_P("shuffled",rng); Pb=F.make_P("real_binary",rng)
        runs={"MB_real":F.run_fly(mk(),F.MB(F.P0,eta=Pm.FLY_MB["eta"]),F.P0,seed=sd,**kw)[0],"MB_shuffled":F.run_fly(mk(),F.MB(Ps,eta=Pm.FLY_MB["eta"]),Ps,seed=sd,**kw)[0],
              "MB_random":F.run_fly(mk(),F.MB(Pr,eta=Pm.FLY_MB["eta"]),Pr,seed=sd,**kw)[0],"MB_real_binary":F.run_fly(mk(),F.MB(Pb,eta=Pm.FLY_MB["eta"]),Pb,seed=sd,**kw)[0],
              "linear_valence":F.run_fly(mk(),F.LinearValence(Pm.FLY_LINEAR["eta"]),None,seed=sd,g_learn=Pm.FLY_LINEAR["g_learn"],k_turn=Pm.FLY_LINEAR["k_turn"])[0],
              "no_learning":F.run_fly(mk(),F.NoLearning(),None,seed=sd,k_turn=Pm.FLY_NOLEARN["k_turn"])[0]}
        for k,r in runs.items(): res[k].append(float(r.sum()))
        if s%20==0: print(cond,s,flush=True)
    out[cond]=res
json.dump(out,open("eval_forage.json","w")); print("saved")

import numpy as np, json, forage as F, params as Pm
P0=F.P0; out={}; WORLDS=range(20)
for cond,conflict in (("consistent",False),("conflict",True)):
    res={k:[] for k in ["MB_real","MB_shuffled","MB_random","linear_valence","no_learning","ants20","q_learner"]}
    for s in WORLDS:
        mk=lambda:F.World(s,T=Pm.T,rev=Pm.REV,conflict=conflict); rng=np.random.default_rng(500+s)
        Ps=F.make_P("shuffled",rng); Pr=F.make_P("random",rng)
        runs={"MB_real":F.run_fly(mk(),F.MB(P0,eta=Pm.FLY_MB["eta"]),P0,seed=100+s,g_learn=Pm.FLY_MB["g_learn"],k_turn=Pm.FLY_MB["k_turn"])[0],
              "MB_shuffled":F.run_fly(mk(),F.MB(Ps,eta=Pm.FLY_MB["eta"]),Ps,seed=100+s,g_learn=Pm.FLY_MB["g_learn"],k_turn=Pm.FLY_MB["k_turn"])[0],
              "MB_random":F.run_fly(mk(),F.MB(Pr,eta=Pm.FLY_MB["eta"]),Pr,seed=100+s,g_learn=Pm.FLY_MB["g_learn"],k_turn=Pm.FLY_MB["k_turn"])[0],
              "linear_valence":F.run_fly(mk(),F.LinearValence(Pm.FLY_LINEAR["eta"]),None,seed=100+s,g_learn=Pm.FLY_LINEAR["g_learn"],k_turn=Pm.FLY_LINEAR["k_turn"])[0],
              "no_learning":F.run_fly(mk(),F.NoLearning(),None,seed=100+s,k_turn=Pm.FLY_NOLEARN["k_turn"])[0],
              "ants20":F.run_ants(mk(),rho=Pm.ANTS["rho"],alpha=Pm.ANTS["alpha"],seed=100+s),
              "q_learner":F.run_qlearner(mk(),alpha=Pm.QL["alpha"],eps=Pm.QL["eps"],seed=100+s)}
        for k,r in runs.items(): res[k].append(dict(total=float(r.sum()),p1=float(r[:Pm.REV].sum()),p2=float(r[Pm.REV:].sum()),post=float(r[Pm.REV:Pm.REV+500].sum()),pre=float(r[Pm.REV-500:Pm.REV].sum())))
        print(cond,"world",s,"done",flush=True)
    out[cond]=res
json.dump(out,open("pilot_results.json","w")); print("saved")

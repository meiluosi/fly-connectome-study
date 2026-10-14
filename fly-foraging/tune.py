"""Tune every agent on TUNING worlds (seeds 1000-1004), same task shape as the test (T=6000, reversal at 3000), objective = mean net reward per world. Test worlds use other seeds."""
import numpy as np, json, itertools, forage as F
P=F.P0; TUNE=range(1000,1005); T,REV=6000,3000
def score(fn): return float(np.mean([fn(F.World(s,T=T,rev=REV),s).sum() for s in TUNE]))
out={}
def best(name,grid,fn):
    res=[(score(lambda w,s,kw=kw:fn(w,s,**kw)),kw) for kw in grid]; res.sort(key=lambda x:-x[0]); out[name]=dict(best=res[0][1],score=res[0][0],all=[(round(a,2),b) for a,b in res]); print(f"{name:22s} best {res[0][1]}  net/world {res[0][0]:+.2f}  | worst {res[-1][0]:+.2f}",flush=True)
best("fly_MB_real",[dict(eta=e,g_learn=g,k_turn=k) for e in (0.15,0.4,0.8) for g in (1.0,2.0,3.0) for k in (0.45,0.9,1.4)],lambda w,s,eta,g_learn,k_turn:F.run_fly(w,F.MB(P,eta=eta),P,seed=7+s,g_learn=g_learn,k_turn=k_turn)[0])
best("fly_linear_valence",[dict(eta=e,g_learn=g,k_turn=k) for e in (0.1,0.3,0.6,1.0) for g in (1.0,2.0,3.0) for k in (0.9,1.4)],lambda w,s,eta,g_learn,k_turn:F.run_fly(w,F.LinearValence(eta),None,seed=7+s,g_learn=g_learn,k_turn=k_turn)[0])
best("fly_no_learning",[dict(k_turn=k) for k in (0.45,0.9,1.4)],lambda w,s,k_turn:F.run_fly(w,F.NoLearning(),None,seed=7+s,k_turn=k_turn)[0])
best("ants",[dict(rho=r,alpha=a) for r in (0.003,0.01,0.03) for a in (1.0,2.0,3.0)],lambda w,s,rho,alpha:F.run_ants(w,rho=rho,alpha=alpha,seed=7+s))
best("q_learner",[dict(alpha=a,eps=e) for a in (0.003,0.01,0.03) for e in (0.05,0.2)],lambda w,s,alpha,eps:F.run_qlearner(w,alpha=alpha,eps=eps,seed=7+s))
json.dump(out,open("tuning_results.json","w"),indent=1); print("saved")

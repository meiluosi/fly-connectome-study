import numpy as np, json, forage as F, params as Pm, swarm as S
from multiprocessing import Pool
MODES=["independent","attract","observe","broadcast"]
def main_world(args):
    s,conflict=args; out={}
    for mode in MODES:
        w=F.World(s,T=Pm.T,rev=Pm.REV,conflict=conflict); rew,per=S.run_swarm(w,mode,n=20,seed=8000+s); out[mode]=float(rew.sum())
    w=F.World(s,T=Pm.T,rev=Pm.REV,conflict=conflict); out["ants"]=float(F.run_ants(w,rho=Pm.ANTS["rho"],alpha=Pm.ANTS["alpha"],seed=8000+s).sum())
    w=F.World(s,T=Pm.T,rev=Pm.REV,conflict=conflict); out["single"]=float(F.run_fly(w,F.MB(F.P0,eta=Pm.FLY_MB["eta"]),F.P0,seed=8000+s,g_learn=Pm.FLY_MB["g_learn"],k_turn=Pm.FLY_MB["k_turn"])[0].sum())
    return out
def crowd(args):
    s,n=args; w=F.World(s,T=Pm.T,rev=Pm.REV); rew,per=S.run_swarm(w,"independent",n=n,seed=8000+s); return float(rew.sum())
if __name__=="__main__":
    res={}
    with Pool(8) as p:
        for cond,conflict in (("consistent",False),("conflict",True)): res[cond]=p.map(main_world,[(s,conflict) for s in range(100,200)]); print(cond,"done",flush=True)
        res["crowd"]={n:p.map(crowd,[(s,n) for s in range(100,130)]) for n in (1,5,10,40)}; print("crowd done",flush=True)
    json.dump(res,open("eval_swarm.json","w")); print("saved")

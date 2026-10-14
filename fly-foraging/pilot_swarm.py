import numpy as np, json, forage as F, params as Pm, swarm as S
from multiprocessing import Pool
MODES=["independent","attract","observe","broadcast"]
def one(args):
    s,conflict=args; out={}
    for mode in MODES:
        w=F.World(s,T=Pm.T,rev=Pm.REV,conflict=conflict); rew,per=S.run_swarm(w,mode,n=20,seed=100+s); out[mode]=dict(total=float(rew.sum()),p1=float(rew[:Pm.REV].sum()),p2=float(rew[Pm.REV:].sum()),post=float(rew[Pm.REV:Pm.REV+500].sum()),sd_per=float(per.std()))
    w=F.World(s,T=Pm.T,rev=Pm.REV,conflict=conflict); out["ants"]=dict(total=float(F.run_ants(w,rho=Pm.ANTS["rho"],alpha=Pm.ANTS["alpha"],seed=100+s).sum()))
    w=F.World(s,T=Pm.T,rev=Pm.REV,conflict=conflict); out["single"]=dict(total=float(F.run_fly(w,F.MB(F.P0,eta=Pm.FLY_MB["eta"]),F.P0,seed=100+s,g_learn=Pm.FLY_MB["g_learn"],k_turn=Pm.FLY_MB["k_turn"])[0].sum()))
    return out
if __name__=="__main__":
    res={}
    with Pool(8) as p:
        for cond,conflict in (("consistent",False),("conflict",True)):
            rows=p.map(one,[(s,conflict) for s in range(20)]); res[cond]=rows; print(cond,"done",flush=True)
    json.dump(res,open("pilot_swarm.json","w")); 
    for cond,rows in res.items():
        print("\n##",cond,"(20 test worlds, 20 agents each; total net reward over 6000 ticks)")
        for k in MODES+["ants","single"]:
            v=np.array([r[k]["total"] for r in rows]); n=1 if k=="single" else 20; print(f"  {k:12s} total {v.mean():+7.1f}   per agent {v.mean()/n:+6.1f}")

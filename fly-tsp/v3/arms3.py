import sys, os, json, pickle; HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); sys.path.insert(0,os.path.join(HERE,"..","v2"))
import numpy as np, v2core as V, v3core as V3, arms as A2, tsp as T
REGS=("R1","R2","R3"); TEST0={"R1":9000,"R2":9300,"R3":9600}; NTEST=300; CH=10; NREP=3
TUN=json.load(open(os.path.join(HERE,"..","v2","tuning_v2_final.json")))
def aco_p(reg): return tuple(TUN[reg]["aco"]["best"])
def on_p(reg,kind): return tuple(TUN[reg]["on"]["ON-"+kind]["best"])
def test_insts(reg): return [A2.REG[reg]["gen"](TEST0[reg]+i) for i in range(NTEST)]
def tune_insts(reg): return A2.tune_insts(reg)
ARMS=["ACO","NOTAU-none","ON-real","ON-random","HAND-turn","TURN-real","TURN-random","TURN-linear"]
def one(arm,reg,P,X,D,seed,rep):
    """P: dict(turn={'real':(lr,k),...}, gamma=g)."""
    c=A2.REG[reg]; al,be,rho=aco_p(reg); cfg=dict(alpha=al,beta=be,rho=rho,ants=c["ants"],iters=c["iters"],ls=False); sd=11+rep
    if arm=="ACO": return V.run(X,D,cfg,[],seed=seed)
    if arm=="NOTAU-none": return V.run(X,D,dict(cfg,alpha=0.0),[],seed=seed)
    if arm in("ON-real","ON-random"):
        k=arm.split("-")[1]; lr,ka=on_p(reg,k); return V.run(X,D,dict(cfg,kappa=ka),V.make_flock(k,1,lr,sd),seed=seed)
    if arm=="HAND-turn": return V3.run3(X,D,dict(cfg,kappa=0.0),None,hand_gamma=P["gamma"],seed=seed)
    k=arm.split("-")[1]; lr,ka=P["turn"][k]; return V3.run3(X,D,dict(cfg,kappa=ka),V3.Circuit3(k,lr,sd),seed=seed)
def run_arm(arm,reg,P,insts,reps,seed0=0):
    out=np.zeros((len(insts),len(reps)))
    for j,rep in enumerate(reps):
        for i,(X,D) in enumerate(insts): out[i,j]=one(arm,reg,P,X,D,3*(seed0+i)+rep,rep)
    return out
def ref_for(reg,which,insts):
    f=os.path.join(HERE,"cache",f"ref_{which}_{reg}.pkl")
    if os.path.exists(f): return pickle.load(open(f,"rb"))
    if which=="tune":                                    # same tuning instances as v2 -> reuse its references
        r=A2.ref_for(reg,"tune",insts); pickle.dump(r,open(f,"wb")); return r
    from multiprocessing import Pool
    with Pool(10) as p: r=p.map(A2._ref,[(D,i) for i,(X,D) in enumerate(insts)])
    pickle.dump(r,open(f,"wb")); return r

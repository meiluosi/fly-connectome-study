"""Arm definitions, regimes, instance seeds, pretraining cache and evaluation helpers for the v2 study."""
import sys, os, json, pickle, ast; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np, v2core as V, tsp as T, fly_heuristic as H, mbcore as M
HERE=os.path.dirname(os.path.abspath(__file__))
REG={"R1":dict(gen=lambda s:T.make_instance(50,s),ants=20,iters=25,ls=False,tune0=8000,test0=7000,ntest=300),
     "R2":dict(gen=lambda s:T.make_instance(100,s),ants=20,iters=50,ls=False,tune0=8100,test0=7300,ntest=300),
     "R3":dict(gen=lambda s:T.make_clustered(50,s),ants=20,iters=25,ls=False,tune0=8200,test0=7600,ntest=300),
     "R4":dict(gen=lambda s:T.make_instance(100,s),ants=10,iters=3,ls=True,tune0=8300,test0=7900,ntest=150)}
NTUNE=40; NREP=3; NREP_TUNE=2
def tune_insts(reg): return [REG[reg]["gen"](REG[reg]["tune0"]+i) for i in range(NTUNE)]
def test_insts(reg): return [REG[reg]["gen"](REG[reg]["test0"]+i) for i in range(REG[reg]["ntest"])]
TRAIN=lambda: [T.make_instance(50,2000+s) for s in range(100)]
V1=json.load(open(os.path.join(HERE,"..","tuning_tsp2.json")))
def v1_cfg(reg):                       # v1-tuned (lr,kappa) for the real learner; R4 uses R1's
    b=V1["learners"]["real"]["R1" if reg=="R4" else reg]["best"]; b=ast.literal_eval(b) if isinstance(b,str) else b; return b[1],b[2]
def pretrain(lr,kappa,tseed):
    f=os.path.join(HERE,"cache",f"pre_{lr}_{kappa}_{tseed}.pkl")
    if os.path.exists(f): return pickle.load(open(f,"rb"))
    tb=H.SigTable("real",tseed); tb.mb.eta=lr; H.train(tb,TRAIN(),iters=10,n_ants=20,kappa=kappa,beta=5.0,seed=tseed); q=tb.mb.q.copy(); pickle.dump(q,open(f,"wb")); return q
ON_KINDS=("real","shuffled","random","linear")
ARMS=["ACO","ISL4","ISL4x","FROZEN-real","PRE-real"]+[f"ON-{k}" for k in ON_KINDS]+[f"NOTAU-{k}" for k in ("real","random","linear")]+[f"HET4-{k}" for k in ("real","shuffled","random")]+["HET4P-real","ONd-real","ONd-random"]
ARMS_R4=["ACO","ISL4x","ON-real","ON-random","ON-linear","HET4-real","HET4-random","ONd-real","ONd-random"]
def base_of(arm):                     # which tuned base arm supplies (lr,kappa)
    if arm in("ACO","ISL4","ISL4x"): return None
    k=arm.split("-",1)[1]; return "ON-"+k
def build(arm,reg,P,rep):
    """P: dict(aco=(al,be,rho), on={'ON-real':(lr,kappa),...}). Returns (cfg, circuits) for a replicate rep."""
    c=REG[reg]; al,be,rho=P["aco"]; cfg=dict(alpha=al,beta=be,rho=rho,ants=c["ants"],iters=c["iters"],ls=c["ls"])
    if arm=="ACO": return cfg,[]
    if arm=="ISL4": return dict(cfg,islands=4,exch=None),[]
    if arm=="ISL4x": return dict(cfg,islands=4,exch=5),[]
    sd=11+rep
    if arm in("FROZEN-real","PRE-real"):
        lr,ka=v1_cfg(reg); q=pretrain(lr,ka,7+rep); return dict(cfg,kappa=ka),V.make_flock("real",1,lr,sd,q0=q,learn=(arm=="PRE-real"))
    lr,ka=P["on"][base_of(arm)]; cfg=dict(cfg,kappa=ka); head,k=arm.split("-",1)
    if head=="ON": return cfg,V.make_flock(k,1,lr,sd)
    if head=="NOTAU": return dict(cfg,alpha=0.0),V.make_flock(k,1,lr,sd)
    if head=="ONd": return cfg,V.make_flock(k,1,lr,sd,drop=0.3)
    if head=="HET4": return dict(cfg,broadcast=True),V.make_flock(k,4,lr,sd,drop=0.3)
    if head=="HET4P": return dict(cfg,broadcast=False),V.make_flock(k,4,lr,sd,drop=0.3)
    raise ValueError(arm)
def run_arm(arm,reg,P,insts,reps):
    """-> array (n_inst, len(reps)) of best tour lengths. search seed = 3*i+rep."""
    out=np.zeros((len(insts),len(reps)))
    for j,rep in enumerate(reps):
        for i,(X,D) in enumerate(insts):
            cfg,circ=build(arm,reg,P,rep); out[i,j]=V.run(X,D,cfg,circ,seed=3*i+rep)
    return out
def ref_for(reg,which,insts):
    f=os.path.join(HERE,"cache",f"ref_{which}_{reg}.pkl")
    if os.path.exists(f): return pickle.load(open(f,"rb"))
    from multiprocessing import Pool
    with Pool(10) as p: r=p.map(_ref,[(D,i) for i,(X,D) in enumerate(insts)])
    pickle.dump(r,open(f,"wb")); return r
def _ref(a): return T.reference_solver(a[0],restarts=30,seed=a[1])[1]

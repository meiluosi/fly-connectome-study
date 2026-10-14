"""Per-regime tuning on TUNING instances only (seeds 1000-1019). Regimes: R1 uniform n=50, 500 constructions; R2 uniform n=100, 1000; R3 clustered n=50, 500.
Learners are trained ONCE per (kind, lr, kappa) on uniform n=50 training instances (seeds 2000-2099, 10 iterations each) and then evaluated in every regime with that regime's tuned ACO parameters."""
import numpy as np, json, itertools, time, pickle, os, tsp as T, fly_heuristic as H
from multiprocessing import Pool
REG={"R1":dict(gen=lambda s:T.make_instance(50,s),ants=20,iters=25),"R2":dict(gen=lambda s:T.make_instance(100,s),ants=20,iters=50),"R3":dict(gen=lambda s:T.make_clustered(50,s),ants=20,iters=25)}
TUNE={k:[v["gen"](1000+s) for s in range(20)] for k,v in REG.items()}; TRAIN=[T.make_instance(50,2000+s) for s in range(100)]
def ref_for(insts,name,restarts=30):
    f=f"ref_{name}.pkl"
    if os.path.exists(f): return pickle.load(open(f,"rb"))
    r=[T.reference_solver(D,restarts=restarts,seed=i)[1] for i,(X,D) in enumerate(insts)]; pickle.dump(r,open(f,"wb")); return r
REF={k:ref_for(TUNE[k],"tune_"+k) for k in REG}
def gap(L,ref): return float(np.mean([l/r-1 for l,r in zip(L,ref)]))
def aco_job(a):
    reg,al,be,rho=a; c=REG[reg]; return (a,gap([H.aco_vec(D,n_ants=c["ants"],iters=c["iters"],alpha=al,beta=be,rho=rho,seed=i)[0] for i,(X,D) in enumerate(TUNE[reg])],REF[reg]))
def learner_job(a):
    kind,lr,kappa,acop=a; tb=H.SigTable(kind,7)
    if kind=="linear": tb.lin_eta=lr
    elif tb.mb is not None: tb.mb.eta=lr
    be=3.0; H.train(tb,TRAIN,iters=10,n_ants=20,kappa=kappa,beta=acop["R1"][1],seed=3); out={}
    for reg,c in REG.items():
        al,be,rho=acop[reg]; L=[]
        for i,(X,D) in enumerate(TUNE[reg]): sig=tb.ids_for(H.edge_signatures(X,D)); V=tb.valence(sig); L.append(H.aco_vec(D,V=V,kappa=kappa,n_ants=c["ants"],iters=c["iters"],alpha=al,beta=be,rho=rho,seed=i)[0])
        out[reg]=gap(L,REF[reg])
    return (a[:3],out)
if __name__=="__main__":
    t0=time.time(); res={}
    with Pool(8) as p:
        for reg in REG:
            rr=p.map(aco_job,[(reg,al,be,rho) for al in (0.5,1.0,2.0) for be in (2.0,3.0,5.0) for rho in (0.05,0.1,0.3)]); rr.sort(key=lambda x:x[1]); res[reg]=dict(best=rr[0][0][1:],gap=rr[0][1],grid=rr); print(reg,"ACO best",rr[0][0][1:],"gap %.2f%%"%(100*rr[0][1]),"worst %.2f%%"%(100*rr[-1][1]),round(time.time()-t0),"s",flush=True)
        acop={reg:res[reg]["best"] for reg in REG}; out={}
        for kind in ("real","shuffled","random","linear"):
            lrs=(0.1,0.3,1.0,3.0) if kind=="linear" else (0.01,0.03,0.1,0.3)
            rr=p.map(learner_job,[(kind,lr,k,acop) for lr in lrs for k in (1.0,2.0,4.0)]); out[kind]=dict(grid=rr)
            for reg in REG:
                b=min(rr,key=lambda x:x[1][reg]); out[kind][reg]=dict(best=b[0],gap=b[1][reg]); 
            print(f"{kind:9s} "+" | ".join(f"{reg}: (lr,kappa)={out[kind][reg]['best'][1:]} gap {100*out[kind][reg]['gap']:.2f}%" for reg in REG),round(time.time()-t0),"s",flush=True)
    json.dump(dict(aco={k:dict(best=v["best"],gap=v["gap"]) for k,v in res.items()},learners=out),open("tuning_tsp2.json","w"),default=str); print("saved")

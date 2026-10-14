"""Tuning on TUNING instances only (n=50, seeds 1000-1019). Budget: 20 ants x 100 iterations = 2000 constructions, no local search.
Training instances for the learners: seeds 2000-2099 (n=50), 10 construction iterations each. Test instances (5000+) are never touched here."""
import numpy as np, json, itertools, time, pickle, os, tsp as T, fly_heuristic as H
from multiprocessing import Pool
ANTS,ITERS=20,100; TUNE=[T.make_instance(50,1000+s) for s in range(20)]; TRAIN=[T.make_instance(50,2000+s) for s in range(100)]
def ref_for(insts,name,restarts=30):
    f=f"ref_{name}.pkl"
    if os.path.exists(f): return pickle.load(open(f,"rb"))
    r=[T.reference_solver(D,restarts=restarts,seed=i)[1] for i,(X,D) in enumerate(insts)]; pickle.dump(r,open(f,"wb")); return r
REF=ref_for(TUNE,"tune")
def gap(lens,ref): return float(np.mean([l/r-1 for l,r in zip(lens,ref)]))
def aco_job(a):
    al,be,rho=a; L=[H.aco_vec(D,n_ants=ANTS,iters=ITERS,alpha=al,beta=be,rho=rho,seed=i)[0] for i,(X,D) in enumerate(TUNE)]; return (a,gap(L,REF))
def learner_job(a):
    kind,lr,kappa,al,be,rho=a; tb=H.SigTable(kind,7)
    if kind=="linear": tb.lin_eta=lr
    elif tb.mb is not None: tb.mb.eta=lr
    H.train(tb,TRAIN,iters=10,n_ants=20,kappa=kappa,beta=be,seed=3); L=[]
    for i,(X,D) in enumerate(TUNE): sig=tb.ids_for(H.edge_signatures(X,D)); V=tb.valence(sig); L.append(H.aco_vec(D,V=V,kappa=kappa,n_ants=ANTS,iters=ITERS,alpha=al,beta=be,rho=rho,seed=i)[0])
    return (a,gap(L,REF))
if __name__=="__main__":
    t0=time.time()
    with Pool(8) as p:
        res=p.map(aco_job,list(itertools.product((0.5,1.0,2.0),(2.0,3.0,5.0),(0.05,0.1,0.3)))); res.sort(key=lambda x:x[1]); best=res[0][0]; print("ACO best (alpha,beta,rho)",best,"gap %.2f%%"%(100*res[0][1]),"| worst %.2f%%"%(100*res[-1][1]),round(time.time()-t0),"s",flush=True)
        out=dict(aco=dict(best=best,grid=res),learners={})
        for kind in ("real","shuffled","random","linear"):
            lrs=(0.1,0.3,1.0,3.0) if kind=="linear" else (0.01,0.03,0.1,0.3)
            rr=p.map(learner_job,[(kind,lr,k,*best) for lr in lrs for k in (1.0,2.0,4.0)]); rr.sort(key=lambda x:x[1]); out["learners"][kind]=dict(best=rr[0][0],gap=rr[0][1],grid=rr)
            print(f"{kind:9s} best (lr,kappa)=({rr[0][0][1]},{rr[0][0][2]}) gap {100*rr[0][1]:.2f}% | worst {100*rr[-1][1]:.2f}% | {round(time.time()-t0)}s",flush=True)
    json.dump(out,open("tuning_tsp.json","w"),default=str); print("saved")

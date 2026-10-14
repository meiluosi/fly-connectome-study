import numpy as np, json, pickle, os, time, tsp as T, fly_heuristic as H
from multiprocessing import Pool
TUN=json.load(open("tuning_tsp2.json")); import ast
REG={"R1":dict(gen=lambda s:T.make_instance(50,s),ants=20,iters=25),"R2":dict(gen=lambda s:T.make_instance(100,s),ants=20,iters=50),"R3":dict(gen=lambda s:T.make_clustered(50,s),ants=20,iters=25)}
TRAIN=[T.make_instance(50,2000+s) for s in range(100)]; TEST={k:[v["gen"](5000+s) for s in range(100)] for k,v in REG.items()}
def ref_for(insts,name):
    f=f"ref_{name}.pkl"
    if os.path.exists(f): return pickle.load(open(f,"rb"))
    r=[T.reference_solver(D,restarts=30,seed=i)[1] for i,(X,D) in enumerate(insts)]; pickle.dump(r,open(f,"wb")); return r
def cfg(kind,reg):
    b=TUN["learners"][kind][reg]["best"]; b=ast.literal_eval(b) if isinstance(b,str) else b; return b[1],b[2]
def aco_params(reg): b=TUN["aco"][reg]["best"]; return tuple(ast.literal_eval(b) if isinstance(b,str) else b)
def learner_job(a):
    kind,reg,tseed=a; lr,kappa=cfg(kind,reg); al,be,rho=aco_params(reg); c=REG[reg]; tb=H.SigTable(kind,tseed)
    if kind=="linear": tb.lin_eta=lr
    elif tb.mb is not None: tb.mb.eta=lr
    H.train(tb,TRAIN,iters=10,n_ants=20,kappa=kappa,beta=aco_params("R1")[1],seed=tseed); L=[]
    for i,(X,D) in enumerate(TEST[reg]): sig=tb.ids_for(H.edge_signatures(X,D)); V=tb.valence(sig); L.append(H.aco_vec(D,V=V,kappa=kappa,n_ants=c["ants"],iters=c["iters"],alpha=al,beta=be,rho=rho,seed=i)[0])
    return (kind,reg,tseed,L)
def aco_job(reg):
    al,be,rho=aco_params(reg); c=REG[reg]; return (reg,[H.aco_vec(D,n_ants=c["ants"],iters=c["iters"],alpha=al,beta=be,rho=rho,seed=i)[0] for i,(X,D) in enumerate(TEST[reg])])
if __name__=="__main__":
    t0=time.time(); REF={k:ref_for(TEST[k],"test_"+k) for k in REG}; print("references ready",round(time.time()-t0),"s",flush=True)
    out={"ref":REF,"aco":{},"learners":{}}
    with Pool(8) as p:
        for reg,L in p.map(aco_job,list(REG)): out["aco"][reg]=L
        print("aco done",round(time.time()-t0),"s",flush=True)
        for kind,reg,ts,L in p.imap_unordered(learner_job,[(k,r,ts) for k in ("real","shuffled","random","linear") for r in REG for ts in (7,8,9)]): out["learners"].setdefault(f"{kind}|{reg}",{})[ts]=L; print(kind,reg,ts,"done",round(time.time()-t0),"s",flush=True)
    json.dump(out,open("eval_tsp.json","w")); print("saved")

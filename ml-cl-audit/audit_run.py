"""usage: audit_run.py BENCH STAGE [THREADS]   BENCH in mnist20|cifar100|cifar100_224 ; STAGE in proto|backprop|offline|backprop_multi
Implements PREREG_audit.md. Results cached in results/BENCH.json so an interrupted run resumes."""
import sys, os, json, time, itertools, numpy as np, cl_bench as B, cl_baselines as C, cl_backprop as P
bench,stage=sys.argv[1],sys.argv[2]; threads=int(sys.argv[3]) if len(sys.argv)>3 else 3
CFG={"mnist20":dict(m=3200,k_inputs=10,l=160,beta=0.01,K=20,per=2),"cifar100":dict(m=20000,k_inputs=64,l=200,beta=0.2,K=100,per=4),"cifar100_224":dict(m=20000,k_inputs=64,l=200,beta=0.2,K=100,per=4)}[bench]
K,per=CFG["K"],CFG["per"]; tasks=B.task_classes(K,per); Xtr,ytr,Xte,yte=B.load(bench); d=Xtr.shape[1]
rng=np.random.default_rng(12345); val=np.zeros(len(ytr),bool)
for c in range(K): idx=np.where(ytr==c)[0]; val[rng.choice(idx,int(0.1*len(idx)),replace=False)]=True
Xs,ys,Xv,yv=Xtr[~val],ytr[~val],Xtr[val],ytr[val]
import hashlib, glob
RD=f"results/{bench}"; os.makedirs(RD,exist_ok=True)   # one file per result key: safe under concurrent processes (the earlier single-file cache lost updates)
def _fn(key): return f"{RD}/{hashlib.sha1(key.encode()).hexdigest()}.json"
def put(key,val):
    cache[key]=val; tmp=_fn(key)+f".tmp{os.getpid()}"; json.dump(dict(key=key,value=val),open(tmp,"w")); os.replace(tmp,_fn(key))
cache={}
for _f in glob.glob(f"{RD}/*.json"):
    _rec=json.load(open(_f)); cache[_rec["key"]]=_rec["value"]
def summ(R,al): T=R.shape[0]; return dict(final=float(al[-1]),learn=float(np.mean(np.diag(R))),memloss=float(np.mean([R[j][j]-R[T-1][j] for j in range(T)])),R=np.round(R,4).tolist())
def cached(key,fn):
    if key not in cache and os.path.exists(_fn(key)): _r=json.load(open(_fn(key))); cache[key]=_r['value']
    if key not in cache: t0=time.time(); v=fn(); v["secs"]=round(time.time()-t0,1); put(key,v); print(key,"final %.4f"%v["final"] if "final" in v else "",v["secs"],"s",flush=True)
    return cache[key]
def proto_run(name,hp,seed,phase):
    Xa,ya,Xb,yb=(Xs,ys,Xv,yv) if phase=="val" else (Xtr,ytr,Xte,yte); m=C.make(name,d,K,CFG,seed,hp); R,al=B.class_incremental_eval(m,Xa,ya,Xb,yb,tasks,seed); return summ(R,al)
STREAM=os.environ.get('AUDIT_STREAM','ordered')
def bp_run(method,hp,seed,phase,epochs):
    Xa,ya,Xb,yb=(Xs,ys,Xv,yv) if phase=="val" else (Xtr,ytr,Xte,yte); R,al=P.run_backprop(method,Xa,ya,Xb,yb,tasks,K,hp,seed,epochs=epochs,threads=threads,device=os.environ.get('AUDIT_DEVICE','cpu'),interleave=(STREAM=='inter')); return summ(R,al)
if stage=="proto":
    for name,grid in [("NCM_euclid",[{}]),("NCM_cos",[{}]),("ClassSumDot",[{}]),("SLDA",[{"shrink":s} for s in (1e-3,1e-2,1e-1,1.0)]),("Fly_dense_l2",[{}]),("Fly_dense_minmax",[{}])]:
        best=max(grid,key=lambda hp:cached(f"val|{name}|{json.dumps(hp)}|s0",lambda:proto_run(name,hp,0,"val"))["final"])
        for sd in (range(5) if name.startswith("Fly") else [0]): cached(f"test|{name}|{json.dumps(best)}|s{sd}",lambda:proto_run(name,best,sd,"test"))
        put(f"best|{name}",best)
    cached(f"test|Fly_F0|{{}}|s0",lambda:proto_run("Fly",{},0,"test")) if False else None
    for sd in range(5): cached(f"test|Fly_F0|{{}}|s{sd}",lambda:proto_run("Fly",{},sd,"test"))
    gridF=[{"l":int(f*CFG["m"]),"beta":b} for f in (0.01,0.025,0.05,0.10) for b in (0.01,0.05,0.2)]
    bestF=max(gridF,key=lambda hp:cached(f"val|Fly_F1|{json.dumps(hp)}|s0",lambda:proto_run("Fly",hp,0,"val"))["final"]); put("best|Fly_F1",bestF)
    for sd in range(5): cached(f"test|Fly_F1|{json.dumps(bestF)}|s{sd}",lambda:proto_run("Fly",bestF,sd,"test"))
elif stage in ("backprop","backprop_multi"):
    ep=1 if stage=="backprop" else 5; tag=("" if ep==1 else "|ep5")+("|inter" if STREAM=="inter" else "")
    lrs=(1e-5,1e-4,1e-3,1e-2); grids={"B1_vanilla":[dict(lr=l) for l in lrs],"B2_ewc":[dict(lr=l,lam=lam) for l in lrs for lam in (0.1,1,10,100,1e3,1e4)],"B3_er200":[dict(lr=l,buffer=200) for l in lrs],"B3_er1000":[dict(lr=l,buffer=1000) for l in lrs]}
    for name,grid in grids.items():
        meth=name.split("_")[1]
        best=max(grid,key=lambda hp:cached(f"val|{name}{tag}|{json.dumps(hp)}|s0",lambda:bp_run(meth,hp,0,"val",ep))["final"]); put(f"best|{name}{tag}",best)
        for sd in range(5): cached(f"test|{name}{tag}|{json.dumps(best)}|s{sd}",lambda:bp_run(meth,best,sd,"test",ep))
elif stage=="supp":
    for name in ("Fly_dense_l2_noclip","Fly_wta_noclip","ExpNCM_wta_euc","ExpNCM_wta_cos","ExpNCM_dense_euc","ExpNCM_dense_cos"):
        for sd in range(5): cached(f"test|{name}|{{}}|s{sd}",lambda:proto_run(name,{},sd,"test"))
elif stage=="offline":
    best_lr=1e-3; accs=P.run_offline(Xs,ys,Xv,yv,K,best_lr,15,0,threads=threads); ep=int(np.argmax(accs))+1; put("offline|val_accs",accs)
    for sd in range(5):
        a=P.run_offline(Xtr,ytr,Xte,yte,K,best_lr,ep,sd,threads=threads); put(f"test|B4_offline|ep{ep}|s{sd}",dict(final=a[-1],learn=float("nan"),memloss=float("nan"))); print("offline",sd,a[-1],flush=True)
print("stage done")

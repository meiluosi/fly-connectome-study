import numpy as np, json, time, cl_bench as B
Xtr,ytr,Xte,yte=B.load("cifar100_224"); tasks=B.task_classes(100,4); rows=[]; t0=time.time()
for seed in range(5):
    fm=B.FlyModel(512,20000,64,200,0.2,100,seed); R,al=B.class_incremental_eval(fm,Xtr,ytr,Xte,yte,tasks,seed); rows.append(B.summarize(R,al)); print("cifar100_224 seed",seed,{k:round(v,4) for k,v in rows[-1].items()},round(time.time()-t0),"s",flush=True)
r={k:(float(np.mean([x[k] for x in rows])),float(np.std([x[k] for x in rows]))) for k in rows[0]}; json.dump(r,open("replication_cifar224.json","w"),indent=1); print("MEAN",{k:"%.4f±%.4f"%v for k,v in r.items()},"| paper final ~0.41")

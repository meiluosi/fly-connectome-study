import numpy as np, json, time, cl_bench as B
res={}
CFG={"mnist20":dict(m=3200,k_inputs=10,l=160,beta=0.01,n_classes=20,per_task=2),"cifar100":dict(m=20000,k_inputs=64,l=200,beta=0.2,n_classes=100,per_task=4)}
for name,c in CFG.items():
    Xtr,ytr,Xte,yte=B.load(name); tasks=B.task_classes(c["n_classes"],c["per_task"]); rows=[]; t0=time.time()
    for seed in range(5):
        fm=B.FlyModel(Xtr.shape[1],c["m"],c["k_inputs"],c["l"],c["beta"],c["n_classes"],seed); R,al=B.class_incremental_eval(fm,Xtr,ytr,Xte,yte,tasks,seed); rows.append(B.summarize(R,al))
        print(name,"seed",seed,{k:round(v,4) for k,v in rows[-1].items()},round(time.time()-t0),"s",flush=True)
    res[name]={k:(float(np.mean([r[k] for r in rows])),float(np.std([r[k] for r in rows]))) for k in rows[0]}
json.dump(res,open("replication_flymodel.json","w"),indent=1)
print("\nPAPER TARGETS: MNIST-20 acc@10 classes 0.86; final ~0.75; mem loss 0.07 | CIFAR-100 final ~0.41")
for n,v in res.items(): print(n,{k:"%.4f±%.4f"%x for k,x in v.items()})

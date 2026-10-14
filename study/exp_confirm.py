"""Confirmatory runs per PREREG_confirm.md. usage: exp_confirm.py {p1|p24} CIRCUIT   (CIRCUIT in MR,ML,FR,FL)"""
import sys, json, time, numpy as np, core, core4, core_fw
part,circ=sys.argv[1],sys.argv[2]
c={"MR":lambda:core.build("R"),"ML":lambda:core.build("L"),"FR":lambda:core_fw.build("right"),"FL":lambda:core_fw.build("left")}[circ]()
t0=time.time(); out={}
if part=="p1":
    B=c.Nb.astype(float); Z=B/np.maximum(np.linalg.norm(B,axis=0),1e-9); G=Z.T@Z
    def stat(perm):
        Mc=c.M[perm]; v=[]
        for j in range(Mc.shape[1]):
            idx=np.where(Mc[:,j])[0]
            if len(idx)>1: g=G[np.ix_(idx,idx)]; v.append((g.sum()-np.trace(g))/(len(idx)*(len(idx)-1)))
        return float(np.mean(v))
    def search(target,rng,steps=4000):
        p=rng.permutation(c.NM); s=stat(p)
        for _ in range(steps):
            i,j=rng.choice(c.NM,2,replace=False); p2=p.copy(); p2[[i,j]]=p2[[j,i]]; s2=stat(p2)
            if abs(s2-target)<abs(s-target): p,s=p2,s2
            if abs(s-target)<0.004: break
        return p,s
    rng=np.random.default_rng(777); real=stat(np.arange(c.NM)); lo=stat(search(0.0,rng)[0]); hi=stat(search(1.0,rng)[0])
    targets=[lo+0.02,0.15,0.25,0.35,real,hi-0.02]; parts=[]
    for tg in targets:
        for _ in range(5): p,s=search(tg,rng); parts.append((tg,s,p))
    out=dict(real_overlap=real,lo=lo,hi=hi,parts=[])
    for tg,s,p in parts:
        Mc=c.M[p]; v=np.array([core.run(c,"real",24,sd,alloc="random",Mc=Mc) for sd in range(1000,1030)])
        out["parts"].append(dict(target=tg,overlap=s,learned=v[:,0].tolist(),forg=v[:,1].tolist())); print(round(time.time()-t0),"s",circ,"overlap %.3f forg %.4f"%(s,np.nanmean(v[:,1])),flush=True)
    out["ref"]={k:np.array([core.run(c,k,24,sd,alloc="random") for sd in range(1000,1030)]).tolist() for k in ["real","shuffled","none"]}
else:
    s=core4.signs(c); methods=["real","shuffled","none","delta","ewc10","ewc100","ewc1000","mh"]; seeds=range(1000,1060)
    for task in ["random","similar"]:
        for T in [12,48]:
            res={m:[] for m in methods}
            for sd in seeds:
                probe,tasks=core4.make_tasks(c,"pn",T,sd) if task=="random" else core4.make_tasks2(c,T,sd)
                for k in ["real","shuffled","none"]: res[k].append(core4.summarize(*core4.run_fly(c,k,probe,tasks,sd,s)))
                res["delta"].append(core4.summarize(*core4.run_delta(c,probe,tasks,sd)))
                for lam in [10,100,1000]: res[f"ewc{lam}"].append(core4.summarize(*core4.run_delta(c,probe,tasks,sd,ewc=float(lam))))
                res["mh"].append(core4.summarize(*core4.run_delta_mh(c,probe,tasks,sd)))
            out[f"{task}_T{T}"]=res; print(round(time.time()-t0),"s",circ,task,T,"done",flush=True)
json.dump(out,open(f"confirm_{part}_{circ}.json","w")); print("done")

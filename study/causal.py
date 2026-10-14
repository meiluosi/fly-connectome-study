"""Causal dose-response: permute MBON identities (group sizes & multi-membership preserved) to hit target within-compartment KC-input overlap."""
import numpy as np, core, json, time
c=core.build("R"); B=c.Nb.astype(float); Z=B/np.maximum(np.linalg.norm(B,axis=0),1e-9); G=Z.T@Z
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
rng=np.random.default_rng(1); real=stat(np.arange(c.NM)); print("real overlap",round(real,3),flush=True)
lo=stat(search(0.0,rng)[0]); hi=stat(search(1.0,rng)[0]); print("reachable range",round(lo,3),round(hi,3),flush=True)
targets=[lo+0.02,0.15,0.25,0.35,real,hi-0.02]; S=30;T=24
parts=[]
for tg in targets:
    for r_ in range(5): p,s=search(tg,rng); parts.append((tg,s,p))
print("partitions built",len(parts),flush=True)
out=[]; t0=time.time()
for tg,s,p in parts:
    Mc=c.M[p]; v=np.array([core.run(c,"real",T,sd,alloc="random",Mc=Mc) for sd in range(S)])
    out.append(dict(target=tg,overlap=s,learned=float(v[:,0].mean()),forg=float(v[:,1].mean()),forg_by_seed=v[:,1].tolist()))
    print(round(time.time()-t0),"s  overlap=%.3f forg=%.4f learned=%.3f"%(s,out[-1]["forg"],out[-1]["learned"]),flush=True)
ref={k:np.array([core.run(c,k,T,sd,alloc="random") for sd in range(S)]) for k in ["real","shuffled","none"]}
json.dump(dict(parts=out,real_overlap=real,ref={k:v.tolist() for k,v in ref.items()}),open("causal_results.json","w"))
print("done")

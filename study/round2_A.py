"""Round-2 A: in-degree-stratified partitions, accuracy-based forgetting (NaN-free). usage: round2_A.py MR|FR"""
import sys, json, time, numpy as np, core, core4, core_fw2
circ=sys.argv[1]; c=core.build("R") if circ=="MR" else core_fw2.build("right"); s=core4.signs(c)
B=c.Nb.astype(float); Z=B/np.maximum(np.linalg.norm(B,axis=0),1e-9); G=Z.T@Z; deg=c.Nb.sum(0).astype(float)
pos=np.where(deg>0)[0]; qs=np.quantile(deg[pos],[.25,.5,.75]); strat=np.full(c.NM,-1); strat[pos]=np.digitize(deg[pos],qs)
def stat(p):
    Mc=c.M[p]; v=[]
    for j in range(Mc.shape[1]):
        idx=np.where(Mc[:,j])[0]
        if len(idx)>1: g=G[np.ix_(idx,idx)]; v.append((g.sum()-np.trace(g))/(len(idx)*(len(idx)-1)))
    return float(np.mean(v))
def degvar(p):
    Mc=c.M[p]; v=[np.var(np.log(deg[np.where(Mc[:,j])[0]]+1)) for j in range(Mc.shape[1]) if Mc[:,j].sum()>1]; return float(np.mean(v))
def swap_perm(p,rng):
    while True:
        i,j=rng.choice(c.NM,2,replace=False)
        if strat[i]>=0 and strat[i]==strat[j]: q=p.copy(); q[[i,j]]=q[[j,i]]; return q
def search(target,rng,steps=5000):
    p=np.arange(c.NM)
    for _ in range(40): p=swap_perm(p,rng)           # random start inside strata
    sc=stat(p)
    for _ in range(steps):
        q=swap_perm(p,rng); s2=stat(q)
        if abs(s2-target)<abs(sc-target): p,sc=q,s2
        if abs(sc-target)<0.004: break
    return p,sc
rng=np.random.default_rng(888); lo=stat(search(0.0,rng)[0]); hi=stat(search(1.0,rng)[0]); print(circ,"stratified reachable overlap range",round(lo,3),round(hi,3),"real",round(stat(np.arange(c.NM)),3),flush=True)
targets=np.linspace(lo+0.01,hi-0.01,6); parts=[(t,)+search(t,rng) for t in targets for _ in range(5)]
seeds=range(4000,4030); T=24; task_cache={sd:core4.make_tasks(c,"pn",T,sd) for sd in seeds}; out=dict(lo=lo,hi=hi,real=stat(np.arange(c.NM)),parts=[]); t0=time.time()
for tg,p,sc in parts:
    Mc=c.M[p]; r=[core4.summarize(*core4.run_fly(c,"real",*task_cache[sd],sd,s,Mc=Mc)) for sd in seeds]
    out["parts"].append(dict(target=float(tg),overlap=sc,degvar=degvar(p),learn=[x["learn_acc"] for x in r],forg=[x["forg_acc"] for x in r])); print(round(time.time()-t0),"s ov %.3f dv %.3f forg %.4f"%(sc,degvar(p),np.mean([x["forg_acc"] for x in r])),flush=True)
out["ref_real_degvar"]=degvar(np.arange(c.NM)); json.dump(out,open(f"round2_A_{circ}.json","w")); print("done")

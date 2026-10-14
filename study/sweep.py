import numpy as np, itertools, time, json, sys
import learn_v3 as L
NK,NM,NC=L.NK,L.NM,L.NC
def odor_fn(coding,r,kact=0.05):
    if coding=="random": return lambda:(r.permutation(NK)<int(kact*NK)).astype(float)
    tot=np.maximum(L.P.sum(0),1)
    def f():
        x=np.zeros(L.NG); x[r.choice(L.NG,6,replace=False)]=r.uniform(.5,1,6); s=x@L.P
        if coding=="pn_norm": s=s/np.sqrt(tot)
        o=np.zeros(NK); o[np.argsort(-s)[:int(kact*NK)]]=1; return o
    return f
def run(cond,T,seed,coding="pn",alloc="random",rho=0.0,n_odor=5,eta=0.3,reps=3,cpt=2):
    rt=np.random.default_rng(seed); rc=np.random.default_rng(10_000+seed)
    odor=odor_fn(coding,rt); Mc=L.M[rc.permutation(NM)] if cond=="shuffled" else L.M
    perm=rt.permutation(NC); pool=perm[:4]
    probe=np.array([odor() for _ in range(40)]); q=np.full(L.Nsyn.shape,0.5); Nn,Nb=L.Nsyn,L.Nbin
    learned=np.zeros(T); tasks=[]
    def score(O,gm,y):
        nv=(probe@(Nn*q))[:,gm].mean(); return y*((O@(Nn*q))[:,gm].mean()-nv)/nv
    for t in range(T):
        O=np.array([odor() for _ in range(n_odor)]); y=rt.choice([-1,1])
        C={"random":lambda:rt.choice(NC,cpt,replace=False),"concentrated":lambda:rt.choice(pool,cpt,replace=False),
           "roundrobin":lambda:np.array([perm[(cpt*t)%NC],perm[(cpt*t+1)%NC]])}[alloc]()
        gm=np.ones(NM,bool) if cond=="none" else Mc[:,C].any(1)
        if not gm.any(): gm=np.ones(NM,bool)
        tasks.append((O,gm,y)); q=0.5+(q-0.5)*(1-rho)
        for _ in range(reps):
            for x in O:
                A=x[:,None]
                if y<0: q[:,gm]-=eta*A*q[:,gm]*Nb[:,gm]
                else:   q[:,gm]+=eta*A*(1-q[:,gm])*Nb[:,gm]
        learned[t]=score(*tasks[t])
    final=np.array([score(*tk) for tk in tasks]); return learned.mean(),(learned-final).mean()
rng=np.random.default_rng(0)
def boot(d,n=4000):
    m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); p=min(1,2*min((m<=0).mean(),(m>=0).mean()))
    return d.mean(),np.percentile(m,2.5),np.percentile(m,97.5),max(p,1/n)
S=60; rows=[]
def cell(tag,T,alloc,coding,rho,conds=("real","shuffled")):
    v={c:np.array([run(c,T,s,coding,alloc,rho) for s in range(S)]) for c in conds}
    d=boot(v["real"][:,1]-v["shuffled"][:,1]); r=dict(tag=tag,T=T,alloc=alloc,coding=coding,rho=rho,real_forg=v["real"][:,1].mean(),shuf_forg=v["shuffled"][:,1].mean(),
        real_learn=v["real"][:,0].mean(),shuf_learn=v["shuffled"][:,0].mean(),diff=d[0],lo=d[1],hi=d[2],p=d[3])
    if "none" in v: r["none_forg"]=v["none"][:,1].mean()
    rows.append(r); print(json.dumps({k:(round(x,4) if isinstance(x,float) else x) for k,x in r.items()}),flush=True)
t0=time.time()
for T,alloc in itertools.product([6,12,24,48],["random","concentrated","roundrobin"]): cell("A",T,alloc,"pn",0.0)
print("A done",round(time.time()-t0),"s",flush=True)
for coding,rho,T in [("random",0.0,12),("random",0.0,48),("pn_norm",0.0,12),("pn_norm",0.0,48),("pn",0.1,12),("pn",0.1,48)]: cell("B",T,"random",coding,rho)
cell("none-ref",48,"random","pn",0.0,conds=("real","shuffled","none"))
json.dump(rows,open("sweep_results.json","w"),indent=1); print("all done",round(time.time()-t0),"s")

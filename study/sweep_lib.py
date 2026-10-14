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

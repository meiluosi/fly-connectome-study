"""Reusable core: build(side) -> circuit; run(circuit, ...) -> learned, forgetting, stats. Partition (Mc) can be injected."""
import numpy as np, pandas as pd
from compartments import canon
_A=None
def _load():
    global _A
    if _A is None:
        _A=dict(ann=pd.read_csv("mb_annotations_malecns.csv"),e=pd.read_parquet("mb_edges_malecns.parquet"),
                full=pd.read_feather("../data_annot/male_body_annotations.feather"))
    return _A
class Circuit: pass
def build(side="R"):
    d=_load(); ann,e,full=d["ann"],d["e"],d["full"]; c=Circuit(); c.side=side
    kc=ann[(ann.role=="KC")&(ann.side==side)].bodyId.values; mb=ann[(ann.role=="MBON")&(ann.side==side)].reset_index(drop=True)
    ki={b:i for i,b in enumerate(kc)}; mi={b:i for i,b in enumerate(mb.bodyId)}
    k=e[e.body_pre.isin(ki)&e.body_post.isin(mi)]; N=np.zeros((len(kc),len(mb)))
    for a,b,w in zip(k.body_pre,k.body_post,k.weight): N[ki[a],mi[b]]=w
    N/=N[N>0].mean()
    comps=sorted({x for l in mb.compartment for x in canon(l)["primary"]}); ci={x:i for i,x in enumerate(comps)}
    M=np.zeros((len(mb),len(comps)),bool)
    for j,l in enumerate(mb.compartment):
        for x in canon(l)["primary"]: M[j,ci[x]]=True
    full=full.copy(); full["type"]=full.type.astype(str); pn=full[full["class"]=="ALPN"][["bodyId","type"]]; pn["gl"]=pn.type.str.replace(r"_.*$","",regex=True)
    pe=e[e.body_pre.isin(pn.bodyId)&e.body_post.isin(ki)].merge(pn,left_on="body_pre",right_on="bodyId")
    gls=sorted(pe.gl.unique()); gi={g:i for i,g in enumerate(gls)}; P=np.zeros((len(gls),len(kc)))
    for g,b,w in zip(pe.gl,pe.body_post,pe.weight): P[gi[g],ki[b]]+=w
    c.N,c.Nb,c.M,c.P,c.NK,c.NM,c.NC,c.NG=N,N>0,M,P,len(kc),len(mb),len(comps),len(gls)
    c.mb=mb; c.kc_ids=kc; c.kc_type=ann.set_index("bodyId").loc[kc].type.astype(str).values; return c
def odor_fn(c,coding,r,kact=0.05):
    if coding=="random": return lambda:(r.permutation(c.NK)<int(kact*c.NK)).astype(float)
    tot=np.maximum(c.P.sum(0),1)
    def f():
        x=np.zeros(c.NG); x[r.choice(c.NG,6,replace=False)]=r.uniform(.5,1,6); s=x@c.P
        if coding=="pn_norm": s=s/np.sqrt(tot)
        o=np.zeros(c.NK); o[np.argsort(-s)[:int(kact*c.NK)]]=1; return o
    return f
def run(c,cond,T,seed,coding="pn",alloc="random",rho=0.0,Mc=None,n_odor=5,eta=0.3,reps=3,cpt=2):
    rt=np.random.default_rng(seed); rc=np.random.default_rng(10_000+seed); odor=odor_fn(c,coding,rt)
    if Mc is None: Mc=c.M[rc.permutation(c.NM)] if cond=="shuffled" else c.M
    perm=rt.permutation(c.NC); pool=perm[:4]; probe=np.array([odor() for _ in range(40)]); q=np.full(c.N.shape,0.5); tasks=[]; learned=np.zeros(T)
    def score(O,gm,y):
        nv=(probe@(c.N*q))[:,gm].mean(); return y*((O@(c.N*q))[:,gm].mean()-nv)/nv
    for t in range(T):
        O=np.array([odor() for _ in range(n_odor)]); y=rt.choice([-1,1])
        C={"random":lambda:rt.choice(c.NC,cpt,replace=False),"concentrated":lambda:rt.choice(pool,cpt,replace=False),
           "roundrobin":lambda:np.array([perm[(cpt*t)%c.NC],perm[(cpt*t+1)%c.NC]])}[alloc]()
        gm=np.ones(c.NM,bool) if cond=="none" else Mc[:,C].any(1)
        if not gm.any(): gm=np.ones(c.NM,bool)
        tasks.append((O,gm,y)); q=0.5+(q-0.5)*(1-rho)
        for _ in range(reps):
            for x in O:
                A=x[:,None]
                if y<0: q[:,gm]-=eta*A*q[:,gm]*c.Nb[:,gm]
                else:   q[:,gm]+=eta*A*(1-q[:,gm])*c.Nb[:,gm]
        learned[t]=score(*tasks[t])
    final=np.array([score(*tk) for tk in tasks]); return learned.mean(),(learned-final).mean()
def overlap_stat(c,Mc):
    """mean pairwise cosine of KC-input vectors among MBONs that share a compartment label (under partition Mc)"""
    B=c.Nb.astype(float); Z=B/np.maximum(np.linalg.norm(B,axis=0),1e-9); G=Z.T@Z; v=[]
    for j in range(Mc.shape[1]):
        idx=np.where(Mc[:,j])[0]
        if len(idx)>1: g=G[np.ix_(idx,idx)]; v.append((g.sum()-np.trace(g))/(len(idx)*(len(idx)-1)))
    return float(np.mean(v))

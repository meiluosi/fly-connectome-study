"""Stage 0b: non-circular teachers and corrected metrics. Imports the frozen v4core unchanged.
Fixes vs stage 0: (1) KC silencing removes the KCs from the code (silenced KCs cannot fire; code is the top 5% of the rest, b0/sc recomputed);
(2) acc50 is read at trial 50 (eval every 10 trials); (3) 'silenced' is not defined for the linear learner (nan)."""
import numpy as np, v4core as V
NK,NG=V.NK,V.NG
def perturbed_P0(rng,frac=0.3):
    """real wiring with a fraction of edges moved to other PN rows of the same KC (keeps each KC's synapse counts)"""
    Q=V.P0.copy()
    for k in range(NK):
        nz=np.flatnonzero(Q[:,k]); m=int(round(frac*len(nz)))
        if m==0: continue
        src=rng.choice(nz,m,replace=False); zero=np.flatnonzero(Q[:,k]==0); dst=rng.choice(zero,m,replace=False)
        v=Q[src,k].copy(); Q[src,k]=0; Q[dst,k]=v
    return Q
def make_world(task,seed):
    rng=np.random.default_rng(seed)
    if task in("teacher_shuf","teacher_pert"):
        U=V.synth_odours(rng,900)
        Pt=V.make_P("shuffled",np.random.default_rng(seed+7)) if task=="teacher_shuf" else perturbed_P0(np.random.default_rng(seed+8))
        y=V.teacher_labels(U,Pt,rng); return U[:600],y[:600],U[600:],y[600:]
    return V.make_world(task,seed)
def codes_masked(U,P,rng,silence):
    psi=U@P+1e-6*rng.random((len(U),NK)); psi[:,silence]=-np.inf; k=int(V.KFRAC*NK); return np.argpartition(-psi,k-1,axis=1)[:,:k]
def run(task,seed,kind,eta,n_trials=400,eval_every=10):
    trU,trY,teU,teY=make_world(task,seed); rng=np.random.default_rng(seed+1000); acc=lambda v:float((np.sign(v+1e-12)==teY).mean())
    nz=lambda: teU*(rng.random(teU.shape)>0.15)
    if kind=="linear":
        L=V.LinL(eta); curve=[]
        for t in range(n_trials+1):
            if t%eval_every==0: curve.append(acc(L.val_u(teU)))
            if t==n_trials: break
            i=t%len(trU); u=trU[i]; L.update_u(u,trY[i]-float(L.val_u(u[None])[0]))
        noisy=acc(L.val_u(nz())); sil=float("nan")
    else:
        P=V.make_P(kind,rng); ctr=V.codes_for(trU,P,rng); cte=V.codes_for(teU,P,rng); b0t,sct=V.b0sc(cte); M=V.MBL(eta); curve=[]
        for t in range(n_trials+1):
            if t%eval_every==0: curve.append(acc(M.val(cte,b0t,sct)))
            if t==n_trials: break
            i=t%len(trU); c=ctr[i]; b0,sc=V.b0sc(c[None]); M.update(c,trY[i]-float(M.val(c[None],b0,sc)[0]))
        cn=V.codes_for(nz(),P,rng); b0n,scn=V.b0sc(cn); noisy=acc(M.val(cn,b0n,scn))
        cs=codes_masked(teU,P,rng,rng.choice(NK,int(0.2*NK),replace=False)); b0s,scs=V.b0sc(cs); sil=acc(M.val(cs,b0s,scs))
    c=np.array(curve); return dict(curve=c,final=float(c[-1]),auc=float(c.mean()),acc50=float(c[50//eval_every]),noisy=noisy,silenced=sil)

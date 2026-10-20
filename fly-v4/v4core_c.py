"""Stage 0c: conservative unsupervised PN->KC adaptation ('connectome as initialisation'). Imports frozen v4core and v4core_b."""
import numpy as np, v4core as V, v4core_b as B
def retention(P0_,P1):
    a=P0_/np.maximum(np.linalg.norm(P0_,axis=0),1e-9); b=P1/np.maximum(np.linalg.norm(P1,axis=0),1e-9); return float((a*b).sum(0).mean())
def run_ad(task,seed,kind,eta,eta_p,n_trials=400,eval_every=10):
    """kind in real/shuffled/random; eta_p=0 -> no adaptation (same pipeline otherwise)"""
    trU,trY,teU,teY=B.make_world(task,seed); rng=np.random.default_rng(seed+1000)
    P=V.make_P(kind,rng); P1=V.adapt(P,trU,rng,300,eta_p) if eta_p>0 else P; ret=retention(P,P1); P=P1
    ctr=V.codes_for(trU,P,rng); cte=V.codes_for(teU,P,rng); b0t,sct=V.b0sc(cte); M=V.MBL(eta); curve=[]
    acc=lambda v:float((np.sign(v+1e-12)==teY).mean())
    for t in range(n_trials+1):
        if t%eval_every==0: curve.append(acc(M.val(cte,b0t,sct)))
        if t==n_trials: break
        i=t%len(trU); c=ctr[i]; b0,sc=V.b0sc(c[None]); M.update(c,trY[i]-float(M.val(c[None],b0,sc)[0]))
    c=np.array(curve); return dict(auc=float(c.mean()),final=float(c[-1]),retention=ret)

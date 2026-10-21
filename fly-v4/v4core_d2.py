"""Stage 3b: individual differences with a third animal. Five aligned hemispheres (MaleCNS R/L, FlyWire female R/L, hemibrain female R; 65 glomeruli of the MaleCNS reference).
All learners use K = 1801 KCs (random fixed subset per hemisphere; KC->MBON matrix N uses a fixed random subset of K rows), so every wiring has the same size.
Patches the module globals of the frozen v4core (N, NK, NB, A_VEC, C_VEC): use only in processes dedicated to stage 3."""
import os, numpy as np, v4core as V
HERE=os.path.dirname(os.path.abspath(__file__)); K=1801
_I=np.load(os.path.join(HERE,"individuals_h.npz"),allow_pickle=True)
_r=np.random.default_rng(31415); _rows=np.sort(_r.choice(V.N.shape[0],K,replace=False))
V.N=V.N[_rows]; V.NB=V.NB[_rows]; V.NK=K; V.A_VEC=V.N@V.SIGNS; V.C_VEC=V.N@np.abs(V.SIGNS)
IND={}
for i,n in enumerate(("M_R","M_L","F_R","F_L","H_R")):
    A=_I[n].astype(np.float64); cols=np.sort(np.random.default_rng(100+i).choice(A.shape[1],K,replace=False)); IND[n]=A[:,cols]
NG=V.NG
def make_P(kind,rng):
    if kind in IND: return IND[kind]
    if kind.startswith("shuf_"):                     # per-KC shuffle of glomerulus identity of that hemisphere (degree, weights kept)
        A=IND[kind[5:]]; return np.stack([rng.permutation(A[:,k]) for k in range(K)],1)
    if kind.startswith("marg_"):                     # same in-degree and weights per KC, glomeruli drawn proportional to that hemisphere's glomerulus totals
        A=IND[kind[5:]]; p=A.sum(1)+1e-9; p/=p.sum(); Q=np.zeros_like(A)
        for k in range(K):
            nz=np.flatnonzero(A[:,k]); d=len(nz)
            if d==0: continue
            g=rng.choice(NG,d,replace=False,p=p); Q[g,k]=rng.permutation(A[nz,k])
        return Q
    if kind=="random":
        Q=np.zeros((NG,K))
        for k in range(K): Q[rng.choice(NG,6,replace=False),k]=1
        return Q
    raise ValueError(kind)
def make_world(task,seed):
    rng=np.random.default_rng(seed)
    if task.startswith("teacher_"):
        U=V.synth_odours(rng,900); y=V.teacher_labels(U,IND[task[8:]],rng); return U[:600],y[:600],U[600:],y[600:]
    return V.make_world(task,seed)
def run(task,seed,kind,eta,n_trials=400,eval_every=10):
    trU,trY,teU,teY=make_world(task,seed); rng=np.random.default_rng(seed+1000); acc=lambda v:float((np.sign(v+1e-12)==teY).mean())
    P=make_P(kind,rng); ctr=V.codes_for(trU,P,rng); cte=V.codes_for(teU,P,rng); b0t,sct=V.b0sc(cte); M=V.MBL(eta); curve=[]
    for t in range(n_trials+1):
        if t%eval_every==0: curve.append(acc(M.val(cte,b0t,sct)))
        if t==n_trials: break
        i=t%len(trU); c=ctr[i]; b0,sc=V.b0sc(c[None]); M.update(c,trY[i]-float(M.val(c[None],b0,sc)[0]))
    c=np.array(curve); return dict(auc=float(c.mean()),acc50=float(c[50//eval_every]),final=float(c[-1]))

"""Stage 7: representation-level tests on natural odour statistics (DoOR 2.0 consensus response vectors, 301 odorants x 65 glomeruli).
No learning rate: the KC code (top 5%, real/shuffled/random/binary/weight-shuffled wiring) is read out by (T1) a few-shot nearest-centroid classifier of the chemical class and (T2) neighbour retrieval,
i.e. how well the KC code preserves DoOR similarity. Imports frozen v4core."""
import numpy as np, v4core as V
D,CLS=V.door(); CLS=np.array([str(c) for c in CLS]); NK=V.NK
GOOD=[c for c in sorted(set(CLS)) if c not in("NA","other") and (CLS==c).sum()>=8]
def codes_bin(U,P,rng):
    c=V.codes_for(U,P,rng); X=np.zeros((len(U),NK),np.float32); np.put_along_axis(X,c,1.0,axis=1); return X
def cos(A,B):
    A=A/np.maximum(np.linalg.norm(A,axis=1,keepdims=True),1e-9); B=B/np.maximum(np.linalg.norm(B,axis=1,keepdims=True),1e-9); return A@B.T
def world(seed,kind,shots=(2,5),k=5,n_ret=150):
    rng=np.random.default_rng(seed); out={}
    if kind=="raw": X=D.astype(np.float32)                              # no expansion: the 65-d DoOR vector itself (reference)
    else: P=V.make_P(kind,rng); X=codes_bin(D,P,rng)                  # codes of all 301 odorants
    for sh in shots:                                                  # T1 few-shot class decoding (balanced accuracy)
        tr=[];te=[]
        for c in GOOD:
            idx=np.flatnonzero(CLS==c); idx=rng.permutation(idx); tr+= [(c,i) for i in idx[:sh]]; te+= [(c,i) for i in idx[sh:]]
        cent=np.stack([X[[i for cc,i in tr if cc==c]].mean(0) for c in GOOD]); S=cos(X[[i for _,i in te]],cent); pred=np.array(GOOD)[S.argmax(1)]; y=np.array([c for c,_ in te])
        out[f"acc_{sh}shot"]=float(np.mean([(pred[y==c]==c).mean() for c in GOOD]))
    sub=rng.choice(len(D),n_ret,replace=False); Sd=cos(D[sub],D[sub]); Sc=cos(X[sub],X[sub]); np.fill_diagonal(Sd,-9); np.fill_diagonal(Sc,-9)
    nd=np.argsort(-Sd,1)[:,:k]; nc=np.argsort(-Sc,1)[:,:k]                # T2 neighbour retrieval overlap with DoOR neighbours
    out["retrieval"]=float(np.mean([len(set(nd[i])&set(nc[i]))/k for i in range(n_ret)]))
    return out

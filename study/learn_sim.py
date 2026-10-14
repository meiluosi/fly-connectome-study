"""Toy compartmentalised mushroom-body continual-learning model on real MaleCNS KC->MBON wiring (right hemisphere).
Odors = random k-sparse KC patterns (no PN data used). DAN gating = which MBON compartments may depress.
Conditions: real | shuffled (MBON compartment labels permuted) | none (every MBON gated by every task)."""
import numpy as np, pandas as pd
from compartments import canon
ann=pd.read_csv("mb_annotations_malecns.csv"); e=pd.read_parquet("mb_edges_malecns.parquet")
kc=ann[(ann.role=="KC")&(ann.side=="R")].bodyId.values; mb=ann[(ann.role=="MBON")&(ann.side=="R")].reset_index(drop=True)
ki={b:i for i,b in enumerate(kc)}; mi={b:i for i,b in enumerate(mb.bodyId)}
k=e[e.body_pre.isin(ki)&e.body_post.isin(mi)]
W0=np.zeros((len(kc),len(mb)));
for a,b,w in zip(k.body_pre,k.body_post,k.weight): W0[ki[a],mi[b]]=w
W0/=W0[W0>0].mean()
comps=sorted({c for l in mb.compartment for c in canon(l)["primary"]}); ci={c:i for i,c in enumerate(comps)}
M=np.zeros((len(mb),len(comps)),bool)
for j,l in enumerate(mb.compartment):
    for c in canon(l)["primary"]: M[j,ci[c]]=True
NK,NM,NC=len(kc),len(mb),len(comps); print(f"R hemisphere: {NK} KCs, {NM} MBONs, {NC} compartments, {int((W0>0).sum())} KC->MBON edges")
def run(cond,T,seed,n_odor=5,kact=0.05,eta=0.3,reps=3,decay=0.15,cpt=2):
    r=np.random.default_rng(seed); Mc=M.copy()
    if cond=="shuffled": Mc=M[r.permutation(NM)]
    odor=lambda:(r.permutation(NK)<int(kact*NK)).astype(float)
    probe=np.array([odor() for _ in range(20)]); W=W0.copy()
    tasks=[]; R=np.zeros((T,T))
    def contrast(O,gm):
        tr=(O@W)[:,gm].mean(); nv=(probe@W)[:,gm].mean(); return 1-tr/nv
    for t in range(T):
        C=r.choice(NC,cpt,replace=False); gm=np.ones(NM,bool) if cond=="none" else Mc[:,C].any(1)
        if not gm.any(): gm=np.ones(NM,bool)
        O=np.array([odor() for _ in range(n_odor)]); tasks.append((O,gm))
        W=W0+(W-W0)*(1-decay)           # passive recovery toward initial weights
        for _ in range(reps):
            for x in O: W[:,gm]*=(1-eta*x[:,None])   # depress active KC -> gated MBONs
        for j in range(t+1): R[t,j]=contrast(*tasks[j])
    return R
if __name__=="__main__":
    T=12; out=[]
    for cond in ["real","shuffled","none"]:
        Rs=np.array([run(cond,T,s) for s in range(30)]); learned=np.array([np.diag(x) for x in Rs]); final=Rs[:,-1,:]
        forg=(learned-final).mean(); fin=final.mean()
        print(f"{cond:9s} learned(at training)={learned.mean():.3f}  final retention={fin:.3f}  mean forgetting={forg:.3f} +/- {(learned-final).mean(1).std()/np.sqrt(30):.3f}")
        out.append((cond,Rs))
    np.save("learn_results.npy",np.array([o[1] for o in out]))

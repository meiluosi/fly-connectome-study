"""v3: odor codes from REAL PN->KC wiring (MaleCNS, right hemisphere) + global APL-like k-winners-take-all.
Odor = k_gl random glomeruli driven (PN rate ~ U(0.5,1)); KC input = sum_pn P[pn,kc]*rate; top kact fraction of ALL KCs fire.
Tasks/odors drawn from a task-RNG that is independent of the condition, so conditions are paired."""
import numpy as np, pandas as pd, re
from learn_sim import W0, M, NK, NM, NC, kc as KC_IDS
a=pd.read_feather("../data_annot/male_body_annotations.feather"); a["type"]=a.type.astype(str)
e=pd.read_parquet("mb_edges_malecns.parquet"); ann=pd.read_csv("mb_annotations_malecns.csv")
ki={b:i for i,b in enumerate(KC_IDS)}
pn=a[a["class"]=="ALPN"][["bodyId","type"]]; pn["gl"]=pn.type.str.replace(r"_.*$","",regex=True)
pe=e[e.body_pre.isin(pn.bodyId)&e.body_post.isin(ki)].merge(pn,left_on="body_pre",right_on="bodyId")
gls=sorted(pe.gl.unique()); gi={g:i for i,g in enumerate(gls)}
P=np.zeros((len(gls),NK))
for g,b,w in zip(pe.gl,pe.body_post,pe.weight): P[gi[g],ki[b]]+=w      # glomerulus -> KC synapse count (all PNs of a glomerulus pooled)
NG=len(gls); sub=ann.set_index("bodyId").loc[KC_IDS].type.astype(str)
grp=np.array(["a'b'" if t.startswith("KCa'b'") else "ab" if t.startswith("KCab") else "g" if t.startswith("KCg") else "o" for t in sub])
Nsyn=W0.copy(); Nbin=Nsyn>0
def make_odor(P_,r,kact=0.05,k_gl=6):
    def odor():
        x=np.zeros(NG); x[r.choice(NG,k_gl,replace=False)]=r.uniform(.5,1,k_gl)
        s=x@P_; k=int(kact*NK); out=np.zeros(NK); out[np.argsort(-s)[:k]]=1; return out
    return odor
def run(cond,T,seed,coding="pn",n_odor=5,eta=0.3,reps=3,rho=0.0,cpt=2,kact=0.05):
    rt=np.random.default_rng(seed); rc=np.random.default_rng(10_000+seed)   # task rng vs condition rng
    P_=P
    if coding=="pnshuf": P_=np.stack([rc.permutation(P[:,k]) for k in range(NK)],1)
    odor=make_odor(P_,rt,kact) if coding!="random" else (lambda:(rt.permutation(NK)<int(kact*NK)).astype(float))
    Mc=M.copy(); Nn=Nsyn
    if cond=="shuffled": Mc=M[rc.permutation(NM)]
    probe=np.array([odor() for _ in range(40)]); q=np.full(Nsyn.shape,0.5); tasks=[]; R=np.zeros((T,T))
    resp=lambda O,gm:(O@(Nn*q))[:,gm]
    def score(O,gm,y): nv=resp(probe,gm).mean(); return y*(resp(O,gm).mean()-nv)/nv
    for t in range(T):
        O=np.array([odor() for _ in range(n_odor)]); C=rt.choice(NC,cpt,replace=False); y=rt.choice([-1,1])
        gm=np.ones(NM,bool) if cond=="none" else Mc[:,C].any(1)
        if not gm.any(): gm=np.ones(NM,bool)
        tasks.append((O,gm,y)); q=0.5+(q-0.5)*(1-rho)
        for _ in range(reps):
            for x in O:
                A=x[:,None]
                if y<0: q[:,gm]-=eta*A*q[:,gm]*Nbin[:,gm]
                else:   q[:,gm]+=eta*A*(1-q[:,gm])*Nbin[:,gm]
        for j in range(t+1): R[t,j]=score(*tasks[j])
    return R
def summ(R): return np.diag(R).mean(), (np.diag(R)-R[-1]).mean()
if __name__=="__main__":
    print(f"{NG} glomeruli, PN->KC synapses {int(P.sum())}, KC in-degree(glom) mean {(P>0).sum(0).mean():.1f}")
    r=np.random.default_rng(0); od=make_odor(P,r); X=np.array([od() for _ in range(300)])
    print("fraction of odors each KC subtype fires in:",{g:round(X[:,grp==g].mean(),3) for g in ["g","ab","a'b'"]})
    print("KC usage: fraction of KCs never active in 300 odors =",round((X.sum(0)==0).mean(),3))

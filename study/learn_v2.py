"""v2: bidirectional, bounded three-factor rule on real MaleCNS KC->MBON wiring (right hemisphere).
 weight  w_km = N_km * q_km,  N = real synapse count (frozen), q in [0,1] learnable efficacy, q0 = 0.5
 depress   (dopamine sign d=+1): q -= eta_d * x_k * q
 potentiate(dopamine sign d=-1): q += eta_p * x_k * (1-q)
 gate: only MBONs in compartments receiving that task's DAN signal learn.  decay rho=0 by default (swept separately).
Task j = (odor set O_j, compartments C_j, label y_j in {-1,+1}); teaching sign d = -y_j.
Score_j = y_j * (R_C(O_j) - R_C(novel)) / R_C(novel), R_C = mean MBON response over gated MBONs."""
import numpy as np, pandas as pd
from learn_sim import W0, M, NK, NM, NC
N=W0.copy(); Nbin=N>0
def run(cond,T,seed,n_odor=5,kact=0.05,eta=0.3,reps=3,rho=0.0,cpt=2,fixed=None):
    r=np.random.default_rng(seed); Mc=M.copy(); Nn=N
    if cond=="shuffled": Mc=M[r.permutation(NM)]
    if cond=="rewired":                       # per-MBON column shuffle of presynaptic KC identity (in-degree + weights kept)
        Nn=np.stack([r.permutation(N[:,m]) for m in range(NM)],1)
    odor=lambda:(r.permutation(NK)<int(kact*NK)).astype(float)
    probe=np.array([odor() for _ in range(40)]); q=np.full(N.shape,0.5); tasks=[]; R=np.zeros((T,T))
    resp=lambda O,gm:(O@(Nn*q))[:,gm]
    def score(O,gm,y): nv=resp(probe,gm).mean(); return y*(resp(O,gm).mean()-nv)/nv
    for t in range(T):
        if fixed: O,C,y=fixed[t]
        else: O=np.array([odor() for _ in range(n_odor)]); C=r.choice(NC,cpt,replace=False); y=r.choice([-1,1])
        gm=np.ones(NM,bool) if cond=="none" else Mc[:,C].any(1)
        if not gm.any(): gm=np.ones(NM,bool)
        tasks.append((O,gm,y)); q=0.5+(q-0.5)*(1-rho)
        for _ in range(reps):
            for x in O:
                a=x[:,None]
                if y<0: q[:,gm]-=eta*a*q[:,gm]*Nbin[:,gm]
                else:   q[:,gm]+=eta*a*(1-q[:,gm])*Nbin[:,gm]
        for j in range(t+1): R[t,j]=score(*tasks[j])
    return R
if __name__=="__main__":
    # sanity 1: one task retains exactly
    R=run("real",1,0); print("S1 single task learned score:",round(R[0,0],3))
    # sanity 2: same odors, same compartments, opposite labels, no gating -> must overwrite
    r=np.random.default_rng(1); O=np.array([(r.permutation(NK)<102).astype(float) for _ in range(5)])
    R=run("none",2,0,fixed=[(O,[0],-1),(O,[0],+1)]); print(f"S2 overwrite: task0 score after t0={R[0,0]:.3f}, after t1={R[1,0]:.3f}, task1={R[1,1]:.3f} (task0 must fall)")
    T=12
    for cond in ["real","shuffled","rewired","none"]:
        F=[];L=[]
        for s in range(30):
            R=run(cond,T,s); F.append((np.diag(R)-R[-1]).mean()); L.append(np.diag(R).mean())
        F=np.array(F); print(f"{cond:9s} (rho=0) learned={np.mean(L):.3f} forgetting={F.mean():.3f} +/- {F.std()/np.sqrt(30):.3f}")

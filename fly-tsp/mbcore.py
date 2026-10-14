"""Mushroom-body circuit pieces (same semantics as fly-foraging/forage.py; copied so the foraging code stays frozen). Real MaleCNS PN->KC and KC->MBON wiring."""
import numpy as np, os
D=np.load(os.path.join(os.path.dirname(__file__),"mb_circuit.npz"),allow_pickle=True); P0,N,SIGNS=D["P"].astype(np.float64),D["N"].astype(np.float64),D["signs"].astype(np.float64); NG,NK=P0.shape; NM=N.shape[1]; NB=(N>0)
A_VEC=N@SIGNS            # a_k = sum_m N_km s_m
C_VEC=N@np.abs(SIGNS)    # c_k = sum_m N_km |s_m|
def make_P(kind,rng):
    if kind=="real": return P0
    if kind=="shuffled": return np.stack([rng.permutation(P0[:,k]) for k in range(NK)],1)
    if kind=="random":
        Q=np.zeros_like(P0)
        for k in range(NK): Q[rng.choice(NG,6,replace=False),k]=1
        return Q
    raise ValueError(kind)
def kc_code_from_glom(glom_idx,P,rng,frac=0.05):
    u=np.zeros(NG); u[list(glom_idx)]=1; psi=u@P+1e-6*rng.random(NK); k=int(frac*NK); return np.argpartition(-psi,k-1)[:k]
class MB:
    def __init__(s,eta=0.4): s.q=np.full(N.shape,0.5); s.eta=eta
    def w(s): return (N*s.q)@SIGNS
    def update(s,code,delta):
        pot=(delta*SIGNS>0); g=s.eta*abs(delta); rows=N[code]>0; q=s.q[code]
        s.q[code]=q+g*rows*((1-q)*pot[None,:]-q*(~pot)[None,:])

"""Stage 6b: the stage-4 compartment learner (COMP: PAM/PPL1 clusters, dopamine prediction-error depression) inside the foraging arena of fly-foraging/forage.py (unchanged).
CompMB subclasses forage.MB so run_fly treats it as a mushroom-body learner (codes are KC 0/1 vectors)."""
import numpy as np, v4core as V, v4core_e as E
F=V.F; N,NB,SIGNS=V.N,V.NB,V.SIGNS
class CompMB(F.MB):
    def __init__(s,P,eta,arm,rng):
        super().__init__(P,eta=eta); s.arm=arm; s.cl=E.clusters(arm,rng); s.sg=-s.cl; s.q=np.full(N.shape,0.5)
        s.A=N@s.sg; s.C=N@np.abs(s.sg)
    def valence(s,code):
        w=(N*s.q)@s.sg; b=code@w; b0=0.5*(code@s.A); sc=0.5*(code@s.C); return float(np.clip((b-b0)/max(sc,1e-9),-1,1))
    def update(s,code,delta):
        g=s.eta*np.where(s.cl>0,max(delta,0.0),np.where(s.cl<0,max(-delta,0.0),0.0)); s.q-=g[None,:]*(code[:,None]*NB)*s.q
def make(arm,eta,seed):
    if arm=="global": return F.MB(F.P0,eta=eta)
    return CompMB(F.P0,eta,arm,np.random.default_rng(7000+seed))

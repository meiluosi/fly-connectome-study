"""Stage 6d: forage_comp.CompMB with a bounded update: g = min(eta * relu(delta), 1), so q stays in [0,1] (review of stage 6 found q leaving [0,1] at large eta)."""
import numpy as np, forage_comp as FC
F,N,NB=FC.F,FC.N,FC.NB
class CompMBB(FC.CompMB):
    def update(s,code,delta):
        g=np.minimum(s.eta*np.where(s.cl>0,max(delta,0.0),np.where(s.cl<0,max(-delta,0.0),0.0)),1.0); s.q-=g[None,:]*(code[:,None]*NB)*s.q
def make(arm,eta,seed):
    if arm=="global": return F.MB(F.P0,eta=eta)
    return CompMBB(F.P0,eta,arm,np.random.default_rng(7000+seed))

"""Fly swarm: n flies, each with its OWN mushroom body (real wiring) and own learning, sharing one world (shared source depletion = competition).
Modes: independent | attract (hand-written social attraction) | observe (nearby flies get a smaller prediction-error update when a fly eats) | broadcast (everyone gets it; ant-like shared memory, NOT biological)."""
import numpy as np, forage as F
def run_swarm(world,mode="independent",n=20,seed=0,P=None,eta=0.4,g_learn=2.0,k_turn=1.4,g_inn=0.3,sigma=0.12,g_soc=0.5,R_obs=20.0,alpha_obs=0.5,kind="real"):
    r=np.random.default_rng(seed); w=world; P=F.P0 if P is None else P; A=F.ARENA; w.refr[:]=0
    mbs=[F.MB(P,eta=eta) for _ in range(n)]; codes=[[F.kc_code(m,P,rng=r) for m in w.masks] for _ in range(n)]
    val=np.array([[mbs[i].valence(c) for c in codes[i]] for i in range(n)])
    pos=np.array([A/2,A/2])+r.normal(0,5,(n,2)); th=r.uniform(0,2*np.pi,n); rew=np.zeros(w.T); per=np.zeros(n)
    for t in range(w.T):
        h=np.stack([np.cos(th),np.sin(th)],1); nrm=np.stack([-h[:,1],h[:,0]],1); L=pos+1.5*nrm; Rr=pos-1.5*nrm
        cl=np.exp(-np.linalg.norm(w.pos[None]-L[:,None],axis=2)/w.lam); cr=np.exp(-np.linalg.norm(w.pos[None]-Rr[:,None],axis=2)/w.lam)
        wt=g_inn+g_learn*val; dl=(cl*wt).sum(1); dr=(cr*wt).sum(1)
        if mode=="attract":
            for arr,P_ in ((0,L),(1,Rr)):
                d=np.linalg.norm(P_[:,None]-pos[None],axis=2); soc=(1/(1+(d/8.0)**2)); np.fill_diagonal(soc,0); s=g_soc*soc.sum(1)*0.1
                if arr==0: dl=dl+s
                else: dr=dr+s
        th=th+k_turn*(dl-dr)/(np.abs(dl)+np.abs(dr)+0.02)+sigma*r.normal(size=n); pos=pos+np.stack([np.cos(th),np.sin(th)],1)
        for ax in (0,1):
            lo=pos[:,ax]<0; pos[lo,ax]=-pos[lo,ax]; th[lo]=(np.pi-th[lo]) if ax==0 else -th[lo]
            hi=pos[:,ax]>A; pos[hi,ax]=2*A-pos[hi,ax]; th[hi]=(np.pi-th[hi]) if ax==0 else -th[hi]
        w.refr=np.maximum(w.refr-1,0); dd=np.linalg.norm(w.pos[None]-pos[:,None],axis=2); cand=np.argwhere((dd<w.r_eat)&(w.refr[None]==0))
        for i,s in cand:
            if w.refr[s]>0: continue
            rv=w.reward_value(s,t); rew[t]+=rv; per[i]+=rv; w.refr[s]=30; mbs[i].update(codes[i][s],rv-val[i,s]); val[i]=[mbs[i].valence(c) for c in codes[i]]
            if mode in ("observe","broadcast"):
                for j in range(n):
                    if j==i: continue
                    if mode=="broadcast" or np.linalg.norm(pos[j]-pos[i])<R_obs:
                        mbs[j].update(codes[j][s],alpha_obs*(rv-val[j,s])); val[j]=[mbs[j].valence(c) for c in codes[j]]
    return rew,per

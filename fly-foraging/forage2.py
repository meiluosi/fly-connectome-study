"""v2: a mushroom-body learner whose plasticity RULE is parameterised (so an outer loop can evolve it).
theta (5 numbers) -> eta_pos, eta_neg (learning rates for positive / negative prediction errors, asymmetric), decay (per-tick relaxation of every synapse toward its start value = forgetting),
kc_frac (fraction of KCs active per odour = sparseness), g_learn (weight of the learned valence in steering). Motor constants (k_turn=1.4, g_inn=0.3) are NOT evolved."""
import numpy as np, forage as F
def sig(x): return 1/(1+np.exp(-x))
DEFAULT=dict(eta_pos=0.4,eta_neg=0.4,decay=0.0,kc_frac=0.05,g_learn=2.0)
def decode(th):
    return dict(eta_pos=10**(-2+2.5*sig(th[0])),eta_neg=10**(-2+2.5*sig(th[1])),decay=10**(-5+3.5*sig(th[2])),kc_frac=0.01+0.24*sig(th[3]),g_learn=0.5+4.5*sig(th[4]))
def logit(p): p=min(max(p,1e-6),1-1e-6); return np.log(p/(1-p))
def encode(prm):
    return np.array([logit((np.log10(prm["eta_pos"])+2)/2.5),logit((np.log10(prm["eta_neg"])+2)/2.5),logit((np.log10(max(prm["decay"],1e-5))+5)/3.5) if prm["decay"]>0 else -6.0,logit((prm["kc_frac"]-0.01)/0.24),logit((prm["g_learn"]-0.5)/4.5)])
class MB2(F.MB):
    def __init__(s,P,prm): super().__init__(P,eta=prm["eta_pos"]); s.ep,s.en,s.dec=prm["eta_pos"],prm["eta_neg"],prm["decay"]
    def update(s,code,delta):
        g=(s.ep if delta>0 else s.en)*abs(delta); pot=(delta*F.SIGNS>0)&~s.blocked; dep=(delta*F.SIGNS<=0)&~s.blocked; A=code[:,None]*F.NB
        s.q+=g*A*((1-s.q)*pot[None,:]-s.q*dep[None,:])
    def relax(s,steps):
        if s.dec>0: s.q=0.5+(s.q-0.5)*(1-s.dec)**steps
def run_fly2(world,prm,P,seed=0,k_turn=1.4,g_inn=0.3,sigma=0.12,speed=1.0,refresh=25):
    r=np.random.default_rng(seed); w=world; pos=np.array([F.ARENA/2,F.ARENA/2])+r.normal(0,5,2); th=r.uniform(0,2*np.pi); w.refr[:]=0
    mb=MB2(P,prm); codes=[F.kc_code(m,P,frac=prm["kc_frac"],rng=r) for m in w.masks]; act=F.SIGNS
    b0=np.array([0.5*(c@F.N)@act for c in codes]); sc=np.array([0.5*(c@F.N)@np.abs(act) for c in codes])
    def vals(): wv=(F.N*mb.q)@act; return np.clip((np.array([c@wv for c in codes])-b0)/np.maximum(sc,1e-9),-1,1)
    val=vals(); rew=np.zeros(w.T)
    for t in range(w.T):
        if t%refresh==0 and t>0: mb.relax(refresh); val=vals()
        h=np.array([np.cos(th),np.sin(th)]); L=pos+1.5*np.array([-h[1],h[0]]); R=pos-1.5*np.array([-h[1],h[0]])
        dl=(w.conc(L)*(g_inn+prm["g_learn"]*val)).sum(); dr=(w.conc(R)*(g_inn+prm["g_learn"]*val)).sum()
        th+=k_turn*(dl-dr)/(abs(dl)+abs(dr)+0.02)+sigma*r.normal(); pos=pos+speed*np.array([np.cos(th),np.sin(th)])
        for ax in (0,1):
            if pos[ax]<0: pos[ax]=-pos[ax]; th=np.pi-th if ax==0 else -th
            if pos[ax]>F.ARENA: pos[ax]=2*F.ARENA-pos[ax]; th=np.pi-th if ax==0 else -th
        w.refr=np.maximum(w.refr-1,0); d=np.linalg.norm(w.pos-pos,axis=1)
        for i in np.where((d<w.r_eat)&(w.refr==0))[0]:
            rv=w.reward_value(i,t); rew[t]+=rv; w.refr[i]=30; mb.update(codes[i],rv-val[i]); val=vals()
    return rew

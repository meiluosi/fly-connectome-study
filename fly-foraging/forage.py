"""Odour-foraging arena: a virtual fly with a mushroom-body valence learner (real MaleCNS PN->KC and KC->MBON wiring), control variants, an ant colony (pheromone), and a naive linear Q-learner.
WHAT IS REAL: PN->KC wiring (65 glomeruli -> 2045 KC), top-5% KC code, KC->MBON wiring and neurotransmitter signs, MBON cell types/compartments.
WHAT IS HAND-WRITTEN: the odour field, the steering rule that turns valence into movement, the reward schedule, and the learning rule (bounded delta rule)."""
import numpy as np
D=np.load("data/mb_circuit.npz"); P0,N,SIGNS=D["P"],D["N"],D["signs"]; NG,NK=P0.shape; NM=N.shape[1]; NB=(N>0)
ARENA=100.0
# ------------------------------------------------------------------ circuits
def make_P(kind,rng):
    if kind=="real": return P0
    if kind=="shuffled":                                   # per-KC column shuffle of presynaptic glomerulus identity (in-degree and weights kept)
        return np.stack([rng.permutation(P0[:,k]) for k in range(NK)],1)
    if kind=="real_binary": return (P0>0).astype(np.float32)          # real topology, all synapse counts set to 1 (removes input-strength heterogeneity)
    if kind=="shuffled_binary": return (make_P("shuffled",rng)>0).astype(np.float32)
    if kind=="random":                                     # each KC samples 6 random glomeruli, unit weight
        Q=np.zeros_like(P0)
        for k in range(NK): Q[rng.choice(NG,6,replace=False),k]=1
        return Q
    raise ValueError(kind)
def kc_code(u,P,frac=0.05,rng=None):
    """Top-frac KCs by summed input. Ties are broken with tiny random jitter (explicit, instead of argpartition's implementation-dependent choice)."""
    psi=u@P; k=int(frac*NK)
    if rng is not None: psi=psi+1e-6*rng.random(NK)
    o=np.zeros(NK,np.float32); o[np.argpartition(-psi,k-1)[:k]]=1; return o
class MB:
    """Valence learner on the real KC->MBON wiring. v(odour) = (B - B0)/scale in [-1,1]; B = sum_m sign_m * sum_k N_km q_km code_k; q in [0,1], q0=0.5."""
    def __init__(s,P,eta=0.15,silenced=None,plasticity_blocked=None):
        s.P=P; s.eta=eta; s.q=np.full(N.shape,0.5,np.float32); s.silenced=np.zeros(NM,bool) if silenced is None else silenced.copy(); s.blocked=np.zeros(NM,bool) if plasticity_blocked is None else plasticity_blocked.copy()
    def valence(s,code):
        act=~s.silenced; w=(N*s.q)@(SIGNS*act); b=code@w; b0=0.5*(code@N)@(SIGNS*act); sc=0.5*(code@N)@(np.abs(SIGNS)*act)
        return float(np.clip((b-b0)/max(sc,1e-9),-1,1))
    def update(s,code,delta):
        pot=(delta*SIGNS>0)&~s.blocked; dep=(delta*SIGNS<=0)&~s.blocked; A=code[:,None]*NB; g=s.eta*abs(delta)
        s.q+=g*A*((1-s.q)*pot[None,:]-s.q*dep[None,:])
class LinearValence:                                      # control: same body, valence learned by Rescorla-Wagner on the 65-d glomerulus vector (no expansion)
    def __init__(s,eta=0.15): s.w=np.zeros(NG); s.eta=eta
    def valence(s,x): return float(np.clip(s.w@x/ max(x.sum(),1),-1,1))
    def update(s,x,delta): s.w+=s.eta*delta*x/ max(x.sum(),1)*3
class NoLearning:
    def valence(s,x): return 0.0
    def update(s,x,delta): pass
# ------------------------------------------------------------------ world
class World:
    """6 sources in two odour families: F1={A,A',A''}, F2={B,B',B''}; variants share 4 of 6 glomeruli. Reward sign of a family flips every `rev` ticks (reversal)."""
    def __init__(s,seed=0,T=9000,rev=3000,conflict=False,lam=14.0):
        r=np.random.default_rng(seed); s.T,s.rev,s.lam=T,rev,lam; s.conflict=conflict
        def odor(): return r.choice(NG,6,replace=False)
        def variant(b): keep=r.choice(b,4,replace=False); new=set(keep.tolist())
        def variant(b):
            keep=r.choice(b,4,replace=False); new=set(int(x) for x in keep)
            while len(new)<6: new.add(int(r.integers(NG)))
            return np.array(sorted(new))
        A,B=odor(),odor(); fam=[[A,variant(A),variant(A)],[B,variant(B),variant(B)]]
        s.odors=[o for f in fam for o in f]; s.family=np.array([0,0,0,1,1,1])
        if conflict: s.family=np.array([0,1,0,1,0,1])         # similar odours (base vs variant) get opposite sign
        s.masks=np.zeros((6,NG),np.float32)
        for i,o in enumerate(s.odors): s.masks[i,o]=1
        pos=[]
        while len(pos)<6:
            p=r.uniform(10,ARENA-10,2)
            if all(np.linalg.norm(p-q)>22 for q in pos): pos.append(p)
        s.pos=np.array(pos); s.refr=np.zeros(6); s.r_eat=3.0
    def reward_value(s,i,t): ph=(t//s.rev)%2; return 1.0 if (s.family[i]==0)==(ph==0) else -1.0
    def conc(s,p): return np.exp(-np.linalg.norm(s.pos-p,axis=1)/s.lam)
# ------------------------------------------------------------------ agents
def run_fly(world,learner,P,seed=0,g_inn=0.3,g_learn=1.0,k_turn=0.45,sigma=0.12,speed=1.0):
    """Returns per-tick reward array and valence trace. Steering: turn = k*(dL-dR)/(|dL|+|dR|+eps) + noise, with drive_a = sum_i conc_i(antenna a)*(g_inn + valence_i)."""
    r=np.random.default_rng(seed); w=world; pos=np.array([ARENA/2,ARENA/2])+r.normal(0,5,2); th=r.uniform(0,2*np.pi); w.refr[:]=0
    codes=[kc_code(m,P,rng=r) for m in w.masks] if isinstance(learner,MB) else [m for m in w.masks]  # P unused for non-MB learners
    val=np.array([learner.valence(c) for c in codes]); rew=np.zeros(w.T); vtrace=np.zeros((w.T//50+1,6))
    for t in range(w.T):
        if t%50==0: vtrace[t//50]=val
        h=np.array([np.cos(th),np.sin(th)]); left=pos+1.5*np.array([-h[1],h[0]]); right=pos-1.5*np.array([-h[1],h[0]])
        dl=(w.conc(left)*(g_inn+g_learn*val)).sum(); dr=(w.conc(right)*(g_inn+g_learn*val)).sum()
        th+=k_turn*(dl-dr)/(abs(dl)+abs(dr)+0.02)+sigma*r.normal(); pos=pos+speed*np.array([np.cos(th),np.sin(th)])
        for ax in (0,1):
            if pos[ax]<0: pos[ax]=-pos[ax]; th=np.pi-th if ax==0 else -th
            if pos[ax]>ARENA: pos[ax]=2*ARENA-pos[ax]; th=np.pi-th if ax==0 else -th
        w.refr=np.maximum(w.refr-1,0); d=np.linalg.norm(w.pos-pos,axis=1); hit=np.where((d<w.r_eat)&(w.refr==0))[0]
        for i in hit:
            rv=w.reward_value(i,t); rew[t]+=rv; w.refr[i]=30; learner.update(codes[i],rv-val[i]); val=np.array([learner.valence(c) for c in codes])
    return rew,vtrace
def run_ants(world,n_ants=20,rho=0.01,Q=1.0,alpha=2.0,seed=0,cell=2.0):
    r=np.random.default_rng(seed); w=world; G=int(ARENA/cell); tau=np.zeros((G,G)); nest=np.array([ARENA/2,ARENA/2]); w.refr[:]=0
    pos=np.tile(nest,(n_ants,1))+r.normal(0,1,(n_ants,2)); th=r.uniform(0,2*np.pi,n_ants); carry=np.zeros(n_ants,bool); rew=np.zeros(w.T)
    cellof=lambda p:(min(G-1,max(0,int(p[0]/cell))),min(G-1,max(0,int(p[1]/cell))))
    for t in range(w.T):
        tau*=(1-rho); w.refr=np.maximum(w.refr-1,0)
        for a in range(n_ants):
            if carry[a]:                                       # return to nest, depositing pheromone
                v=nest-pos[a]; th[a]=np.arctan2(v[1],v[0])+0.15*r.normal(); pos[a]+=np.array([np.cos(th[a]),np.sin(th[a])]); tau[cellof(pos[a])]+=Q
                if np.linalg.norm(nest-pos[a])<4: carry[a]=False; rew[t]+=1.0
            else:
                cand=th[a]+np.array([-0.5,0,0.5]); pts=[pos[a]+4*np.array([np.cos(c),np.sin(c)]) for c in cand]; ph=np.array([tau[cellof(p)] for p in pts])+0.05; pr=ph**alpha; pr/=pr.sum()
                th[a]=cand[r.choice(3,p=pr)]+0.25*r.normal(); pos[a]+=np.array([np.cos(th[a]),np.sin(th[a])])
                for ax in (0,1):
                    if pos[a][ax]<0: pos[a][ax]=-pos[a][ax]; th[a]=np.pi-th[a] if ax==0 else -th[a]
                    if pos[a][ax]>ARENA: pos[a][ax]=2*ARENA-pos[a][ax]; th[a]=np.pi-th[a] if ax==0 else -th[a]
                d=np.linalg.norm(w.pos-pos[a],axis=1); hit=np.where((d<w.r_eat)&(w.refr==0))[0]
                if len(hit):
                    i=hit[0]; rv=w.reward_value(i,t); w.refr[i]=30
                    if rv>0: carry[a]=True
                    else: rew[t]+=rv; pos[a]=nest.copy()+r.normal(0,1,2)        # punished: penalty and sent home
    return rew
def run_qlearner(world,seed=0,alpha=0.01,eps=0.1,gamma=0.99,lam=0.9,turn=0.35,speed=1.0):
    """Naive end-to-end linear Q-learning with eligibility traces. Features: concentration-weighted glomerulus vectors at both antennae. Actions: turn left / straight / turn right."""
    r=np.random.default_rng(seed); w=world; W=np.zeros((3,2*NG+1)); pos=np.array([ARENA/2,ARENA/2])+r.normal(0,5,2); th=r.uniform(0,2*np.pi); w.refr[:]=0; rew=np.zeros(w.T); E=np.zeros_like(W)
    def feat(pos,th):
        h=np.array([np.cos(th),np.sin(th)]); L=pos+1.5*np.array([-h[1],h[0]]); R=pos-1.5*np.array([-h[1],h[0]]); return np.concatenate([w.conc(L)@w.masks,w.conc(R)@w.masks,[1.0]])
    f=feat(pos,th); a=int(r.integers(3))
    for t in range(w.T):
        th+=[-turn,0,turn][a]+0.05*r.normal(); pos=pos+speed*np.array([np.cos(th),np.sin(th)])
        for ax in (0,1):
            if pos[ax]<0: pos[ax]=-pos[ax]; th=np.pi-th if ax==0 else -th
            if pos[ax]>ARENA: pos[ax]=2*ARENA-pos[ax]; th=np.pi-th if ax==0 else -th
        w.refr=np.maximum(w.refr-1,0); d=np.linalg.norm(w.pos-pos,axis=1); hit=np.where((d<w.r_eat)&(w.refr==0))[0]; rv=0.0
        for i in hit: rv+=w.reward_value(i,t); w.refr[i]=30
        rew[t]=rv; f2=feat(pos,th); a2=int(r.integers(3)) if r.random()<eps else int(np.argmax(W@f2))
        delta=rv+gamma*(W[a2]@f2)-(W[a]@f); E*=gamma*lam; E[a]+=f; W+=alpha*delta*E; f,a=f2,a2
    return rew

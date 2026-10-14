"""v4: behaviour-level readout with MBON transmitter signs, plus algorithmic baselines (delta rule, EWC) on identical paired tasks.
Behaviour B(o) = sum_m s_m * r_m(o) over ALL MBONs, s = +1 (ACh, excitatory) / -1 (GABA, Glu, inhibitory). Task: push B above (y=+1, 'approach') or below (y=-1, 'avoid') its novel-odor baseline.
Teaching sign is valence-appropriate per MBON: depress if y*s<0 else potentiate. Metrics: accuracy (fraction of task odors on the correct side of the novel mean) and z-margin."""
import numpy as np, pandas as pd, core
def signs(c):
    if hasattr(c,"signs"): return c.signs
    n=pd.read_feather("../data_annot/male_neurotransmitters.feather").rename(columns={"body":"bodyId"}).set_index("bodyId").consensus_nt
    nt=n.reindex(c.mb.bodyId).values; return np.where(nt=="acetylcholine",1.0,-1.0)
def make_tasks(c,coding,T,seed,alloc="random",n_odor=5,cpt=2):
    rt=np.random.default_rng(seed); odor=core.odor_fn(c,coding,rt); perm=rt.permutation(c.NC); pool=perm[:4]
    probe=np.array([odor() for _ in range(40)]); tasks=[]
    for t in range(T):
        O=np.array([odor() for _ in range(n_odor)]); y=rt.choice([-1,1])
        C={"random":lambda:rt.choice(c.NC,cpt,replace=False),"concentrated":lambda:rt.choice(pool,cpt,replace=False),
           "roundrobin":lambda:np.array([perm[(cpt*t)%c.NC],perm[(cpt*t+1)%c.NC]])}[alloc]()
        tasks.append((O,C,y))
    return probe,tasks
def metrics(f_probe,f_task,y):
    mu,sd=f_probe.mean(),max(f_probe.std(),1e-9); return float((y*(f_task-mu)>0).mean()), float(y*(f_task.mean()-mu)/sd)
def run_fly(c,cond,probe,tasks,seed,s,Mc=None,eta=0.3,reps=3,mode="behavior"):
    rc=np.random.default_rng(10_000+seed)
    if Mc is None: Mc=c.M[rc.permutation(c.NM)] if cond=="shuffled" else c.M
    q=np.full(c.N.shape,0.5); Nn=c.N; learned=[]; spec=[]
    def B(X): return (X@(Nn*q))@s
    for O,C,y in tasks:
        gm=np.ones(c.NM,bool) if cond=="none" else Mc[:,C].any(1)
        if not gm.any(): gm=np.ones(c.NM,bool)
        dep=gm&(y*s<0); pot=gm&(y*s>0)
        for _ in range(reps):
            for x in O:
                A=x[:,None]; q[:,dep]-=eta*A*q[:,dep]*c.Nb[:,dep]; q[:,pot]+=eta*A*(1-q[:,pot])*c.Nb[:,pot]
        learned.append(metrics(B(probe),B(O),y))
    final=[metrics(B(probe),B(O),y) for O,C,y in tasks]
    return np.array(learned),np.array(final)
def run_delta(c,probe,tasks,seed,ewc=0.0,lr=0.5,reps=3,heads=False):
    rng=np.random.default_rng(seed); w=np.zeros(c.NK); b=0.0; wstar=w.copy(); F=np.zeros(c.NK); learned=[]
    f=lambda X:X@w+b
    for O,C,y in tasks:
        for _ in range(reps):
            for x in O:
                err=(w@x+b)-y; g=err*x; step=lr/(x@x+1.0)
                w-=step*g
                if ewc>0: w-=np.minimum(1.0,step*ewc*F)*(w-wstar)
                b-=step*err
        Fi=np.mean([((w@x+b)-y)**2*x**2 for x in O],axis=0); F+=Fi; wstar=w.copy()
        learned.append(metrics(f(probe),f(O),y))
    final=[metrics(f(probe),f(O),y) for O,C,y in tasks]; return np.array(learned),np.array(final)
def summarize(learned,final):   # columns: (acc, z)
    return dict(learn_acc=learned[:,0].mean(),forg_acc=(learned[:,0]-final[:,0]).mean(),final_acc=final[:,0].mean(),learn_z=learned[:,1].mean(),forg_z=(learned[:,1]-final[:,1]).mean())

def make_tasks2(c,T,seed,alloc="random",sim=0.6,n_odor=5,cpt=2,k_gl=6,kact=0.05):
    """Similar-odor tasks: each odor is, with prob sim, a variant (2 of 6 glomeruli replaced) of an odor from an EARLIER task."""
    rt=np.random.default_rng(seed); perm=rt.permutation(c.NC); pool=perm[:4]
    def code(gl):
        x=np.zeros(c.NG); x[list(gl.keys())]=list(gl.values()); s=x@c.P; o=np.zeros(c.NK); o[np.argsort(-s)[:int(kact*c.NK)]]=1; return o
    def fresh(): return {int(g):float(rt.uniform(.5,1)) for g in rt.choice(c.NG,k_gl,replace=False)}
    def variant(base):
        keys=list(base); drop=set(rt.choice(len(keys),2,replace=False).tolist()); new={keys[i]:base[keys[i]] for i in range(len(keys)) if i not in drop}
        while len(new)<k_gl:
            g=int(rt.integers(c.NG))
            if g not in new: new[g]=float(rt.uniform(.5,1))
        return new
    earlier=[]; probe=np.array([code(fresh()) for _ in range(40)]); tasks=[]
    for t in range(T):
        gls=[variant(earlier[rt.integers(len(earlier))]) if (earlier and rt.random()<sim) else fresh() for _ in range(n_odor)]
        O=np.array([code(g) for g in gls]); y=rt.choice([-1,1])
        C={"random":lambda:rt.choice(c.NC,cpt,replace=False),"concentrated":lambda:rt.choice(pool,cpt,replace=False),
           "roundrobin":lambda:np.array([perm[(cpt*t)%c.NC],perm[(cpt*t+1)%c.NC]])}[alloc]()
        tasks.append((O,C,y)); earlier+=gls
    return probe,tasks
def run_delta_mh(c,probe,tasks,seed,lr=0.5,reps=3):
    W=np.zeros((c.NC,c.NK)); f=lambda X:(X@W.T).sum(1); learned=[]
    for O,C,y in tasks:
        for _ in range(reps):
            for x in O:
                err=f(x[None])[0]-y; step=lr/((x@x+1.0)*len(C)); W[C]-=step*err*x[None]
        learned.append(metrics(f(probe),f(O),y))
    final=[metrics(f(probe),f(O),y) for O,C,y in tasks]; return np.array(learned),np.array(final)

import numpy as np, time, sys
from multiprocessing import Pool
D='/Users/meros/Desktop/fly-mb-compartments/'
d=np.load(D+'fly-foraging/data/mb_circuit.npz'); P=d['P'].astype(float); N=d['N'].astype(float); SG=d['signs'].astype(float)
U=np.load(D+'fly-v4/odours.npz')['U'].astype(float)
CL=np.load(D+'fly-v4/verification/replication/cluster_labels.npy').astype(float)
PSI=U@P; NK=P.shape[1]; NA=int(round(0.05*NK))  # 102
POS=(N>0)
GRID=[0.005,0.01,0.02,0.05,0.15,0.4,1.0]
LEARNERS=['GLOBAL','COMP','COMP_PERM']

def active_sets(rng,idx):
    out=[]
    for i in idx:
        r=rng.random(NK)
        order=np.lexsort((r,-PSI[i]))
        out.append(order[:NA])
    return np.array(out)

class L:
    def __init__(s,kind,eta,rng):
        s.eta=eta; s.q=np.full(N.shape,0.5)
        if kind=='GLOBAL': s.sg=SG.copy(); s.cl=None
        else:
            cl=CL.copy()
            if kind=='COMP_PERM':
                nz=np.where(cl!=0)[0]; cl[nz]=cl[rng.permutation(nz)]
            s.cl=cl; s.sg=-cl
        s.glob=(kind=='GLOBAL')
        s.Nabs=N*np.abs(s.sg)[None,:]
        s.Nsg0=(N*0.5*s.sg[None,:]).sum(1)   # per-KC baseline
    def _v(s,c):
        B=(N[c]*s.q[c]*s.sg).sum(); B0=s.Nsg0[c].sum(); sc=0.5*s.Nabs[c].sum()
        return float(np.clip((B-B0)/sc,-1,1)) if sc>0 else 0.0
    def trial(s,c,y):
        v=s._v(c); dl=y-v; q=s.q[c]; m=POS[c]
        if s.glob:
            up=(dl*s.sg>0)[None,:]
            nq=np.where(up,q+s.eta*abs(dl)*(1-q),q-s.eta*abs(dl)*q)
            s.q[c]=np.where(m,nq,q)
        else:
            g=np.where(s.cl>0,max(dl,0),np.where(s.cl<0,max(-dl,0),0.))*s.eta
            s.q[c]=np.where(m,q-g[None,:]*q,q)
    def vs(s,C):
        W=(N*s.q*s.sg).sum(1)
        B=W[C].sum(1); B0=s.Nsg0[C].sum(1); sc=0.5*s.Nabs.sum(1)[C].sum(1)
        return np.clip((B-B0)/np.where(sc>0,sc,1),-1,1)
def acc(v,y): return np.mean(np.where(v>=0,1,-1)==y)

def cl_world(seed,kind,eta):
    # world data depends on seed only (shared across learners)
    rng=np.random.default_rng(seed)
    idx=rng.choice(len(U),40,replace=False); y=rng.choice([-1,1],40)
    C=active_sets(rng,idx)
    lr=L(kind,eta,np.random.default_rng(seed+7_000_003))
    after=[]
    for t in range(4):
        sl=np.arange(10*t,10*t+10)
        for k in range(100):
            j=sl[k%10]; lr.trial(C[j],y[j])
        after.append(acc(lr.vs(C[sl]),y[sl]))
    return np.mean(after),acc(lr.vs(C),y)

def se_world(seed,kind,eta):
    rng=np.random.default_rng(seed)
    perm=rng.permutation(len(U)); te=perm[:100]; tr=perm[100:]
    grp=rng.integers(0,8,len(U)); gl=rng.choice([-1,1],8); lab=gl[grp]
    Cte=active_sets(rng,te); Ctr=active_sets(rng,tr)
    seq=rng.integers(0,len(tr),400)
    lr=L(kind,eta,np.random.default_rng(seed+7_000_003)); a=[]
    for t in range(400):
        j=seq[t]; lr.trial(Ctr[j],lab[tr[j]])
        if (t+1)%10==0: a.append(acc(lr.vs(Cte),lab[te]))
    return np.mean(a)

def job(a):
    exp,seed,kind,eta=a
    return (cl_world if exp=='CL' else se_world)(seed,kind,eta)

def boot(x,rng,n=10000):
    x=np.asarray(x); m=x[rng.integers(0,len(x),(n,len(x)))].mean(1)
    return x.mean(),np.percentile(m,2.5),np.percentile(m,97.5)

def run(exp,pool,ntune,ntest,out):
    tseeds=[100000+i for i in range(ntune)]; eseeds=[200000+i for i in range(ntest)]
    jobs=[(exp,s,k,e) for k in LEARNERS for e in GRID for s in tseeds]
    r=pool.map(job,jobs,chunksize=8); r=np.array(r,dtype=float)
    r=r.reshape(3,len(GRID),ntune,-1) if exp=='CL' else r.reshape(3,len(GRID),ntune,1)
    tm=r.mean(2)  # learner,eta,metric
    fi=-1 if exp=='CL' else 0
    best={k:GRID[int(np.argmax(tm[i,:,fi]))] for i,k in enumerate(LEARNERS)}
    out.append(f'\n### {exp} tuning (mean over {ntune} tuning worlds)\n')
    out.append('| learner | eta | '+('after | final' if exp=='CL' else 'auc')+' |\n|---|---|---|'+('---|' if exp=='CL' else '')+'\n')
    for i,k in enumerate(LEARNERS):
        for j,e in enumerate(GRID):
            out.append(f'| {k} | {e} | '+' | '.join(f'{x:.4f}' for x in tm[i,j])+' |\n')
    out.append('\nChosen eta: '+str(best)+'\n')
    cfg=dict(best)
    if exp=='CL':
        target=tm[1,GRID.index(best['COMP']),0]
        gm=GRID[int(np.argmin(np.abs(tm[0,:,0]-target)))]
        out.append(f'GLOBAL_MATCHED eta={gm} (tuned COMP after={target:.4f})\n')
        cfg['GLOBAL_MATCHED']=gm
    names=list(cfg)
    res={}
    jobs=[(exp,s,('GLOBAL' if n=='GLOBAL_MATCHED' else n),cfg[n]) for n in names for s in eseeds]
    r=np.array(pool.map(job,jobs,chunksize=4),dtype=float)
    r=r.reshape(len(names),ntest,-1)
    rng=np.random.default_rng(1)
    out.append(f'\n### {exp} test ({ntest} worlds)\n\n| learner | eta | '+('after | final' if exp=='CL' else 'auc')+' |\n|---|---|---|'+('---|' if exp=='CL' else '')+'\n')
    for i,n in enumerate(names):
        out.append(f'| {n} | {cfg[n]} | '+' | '.join(f'{x:.4f}' for x in r[i].mean(0))+' |\n')
    m=-1 if exp=='CL' else 0
    X={n:r[i,:,m] for i,n in enumerate(names)}
    out.append(f'\nPaired differences ({"final" if exp=="CL" else "auc"}), mean [95% bootstrap CI]:\n\n')
    pairs=[('COMP','GLOBAL'),('COMP','GLOBAL_MATCHED'),('COMP','COMP_PERM')] if exp=='CL' else [('COMP','GLOBAL'),('COMP','COMP_PERM')]
    for a,b in pairs:
        mu,lo,hi=boot(X[a]-X[b],rng)
        out.append(f'- {a} - {b}: {mu:+.4f} [{lo:+.4f}, {hi:+.4f}]\n')

if __name__=='__main__':
    t0=time.time(); out=['# raw output\n']
    with Pool(4) as pool:
        if len(sys.argv)>1 and sys.argv[1]=='quick':
            run('CL',pool,2,4,out); run('SE',pool,2,4,out)
        else:
            run('CL',pool,20,100,out); run('SE',pool,20,60,out)
    out.append(f'\nRuntime {time.time()-t0:.0f}s\n')
    open('/Users/meros/Desktop/fly-mb-compartments/fly-v4/verification/replication/rep_4_output.md','w').write(''.join(out))
    print(''.join(out))

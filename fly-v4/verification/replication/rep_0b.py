import numpy as np, time, sys
d=np.load('/Users/meros/Desktop/fly-mb-compartments/fly-foraging/data/mb_circuit.npz',allow_pickle=True)
P=d['P'].astype(float); N=d['N'].astype(float); sg=d['signs'].astype(float)
G,K=P.shape; J=N.shape[1]; NA=int(round(0.05*K)); ETA=0.05
NS=N*sg[None,:]; B0k=0.5*NS.sum(1); SCk=0.5*(N*np.abs(sg)[None,:]).sum(1); Npos=N>0

def odours(rng,n):
    X=np.zeros((n,G))
    for i in range(n): X[i,rng.choice(G,6,replace=False)]=1
    return X
def codes(X,W,rng):
    psi=X@W+rng.random((len(X),K))*0.5   # weights are integer counts; noise<1 breaks exact ties randomly
    # (if weights non-integer, ties among identical psi still broken since noise only matters for equal psi approx)
    return np.argpartition(-psi,NA-1,axis=1)[:,:NA]
def w_shuf(rng):
    W=P.copy()
    for k in range(K): W[:,k]=rng.permutation(W[:,k])
    return W
def w_rand(rng):
    W=np.zeros((G,K))
    for k in range(K): W[rng.choice(G,6,replace=False),k]=1
    return W
def w_pert(rng):
    W=P.copy()
    for k in range(K):
        nz=np.flatnonzero(P[:,k]); z=np.flatnonzero(P[:,k]==0)
        m=min(int(round(0.3*len(nz))),len(z))
        if m==0: continue
        src=rng.choice(nz,m,replace=False); dst=rng.choice(z,m,replace=False)
        W[dst,k]=P[src,k]; W[src,k]=0
    return W

def run_student(W,Xtr,ytr,Xte,yte,rng):
    ctr=codes(Xtr,W,rng); cte=codes(Xte,W,rng)
    q=np.full((K,J),0.5)
    def val(c):
        Bk=(NS*q)[c].sum(); B=Bk; b0=B0k[c].sum(); sc=SCk[c].sum()
        return np.clip((B-b0)/sc,-1,1)
    def acc():
        Bk=(NS*q).sum(1)
        B=Bk[cte].sum(1); v=np.clip((B-B0k[cte].sum(1))/SCk[cte].sum(1),-1,1)
        pred=np.where(v>=0,1,-1); return (pred==yte).mean()
    accs=[acc()]
    for t in range(400):
        i=t%600; c=ctr[i]; y=ytr[i]
        v=val(c); delta=y-v
        qs=q[c]; pos=(delta*sg>0)[None,:]; m=Npos[c]
        up=qs+ETA*abs(delta)*(1-qs); dn=qs-ETA*abs(delta)*qs
        q[c]=np.where(m,np.where(pos,up,dn),qs)
        if (t+1)%10==0: accs.append(acc())
    assert len(accs)==41
    return float(np.mean(accs))

def world(task,seed):
    rng=np.random.default_rng(seed)
    X=odours(rng,900)
    Wt=w_pert(rng) if task=='teacher_pert' else w_shuf(rng)
    qt=rng.random((K,J))
    c=codes(X,Wt,rng); out=((NS*qt).sum(1))[c].sum(1)
    y=np.where(out>=np.median(out),1,-1)
    Xtr,Xte,ytr,yte=X[:600],X[600:],y[:600],y[600:]
    r={}
    r['real']=run_student(P,Xtr,ytr,Xte,yte,rng)
    r['shuffled']=run_student(w_shuf(rng),Xtr,ytr,Xte,yte,rng)
    r['random']=run_student(w_rand(rng),Xtr,ytr,Xte,yte,rng)
    return r

def boot(x,rng,B=10000):
    x=np.asarray(x); idx=rng.integers(0,len(x),(B,len(x)))
    m=x[idx].mean(1); return np.percentile(m,[2.5,97.5])

if __name__=='__main__':
    task=sys.argv[1]; NW=int(sys.argv[2]) if len(sys.argv)>2 else 60
    base={'teacher_pert':100000,'teacher_shuf':200000}[task]
    t0=time.time(); R=[world(task,base+w) for w in range(NW)]
    rb=np.random.default_rng(1)
    lines=[f'## {task} (N_worlds={NW})','| student | mean auc | SD over worlds |','|---|---|---|']
    for s in ['real','shuffled','random']:
        a=[r[s] for r in R]; lines.append(f'| {s} | {np.mean(a):.4f} | {np.std(a,ddof=1):.4f} |')
    lines+=['','| paired diff | mean | 95% bootstrap CI | worlds diff>0 |','|---|---|---|---|']
    for a,b in [('real','shuffled'),('real','random'),('shuffled','random'),('shuffled','real')]:
        df=[r[a]-r[b] for r in R]; lo,hi=boot(df,rb)
        lines.append(f'| {a}-{b} | {np.mean(df):+.4f} | [{lo:+.4f}, {hi:+.4f}] | {sum(x>0 for x in df)}/{NW} |')
    lines.append(f'\nruntime {time.time()-t0:.0f}s')
    open(f'/Users/meros/Desktop/fly-mb-compartments/fly-v4/verification/replication/out_{task}.md','w').write('\n'.join(lines))
    print('\n'.join(lines))

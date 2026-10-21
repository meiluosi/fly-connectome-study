"""Independent re-implementation (rep_3). Usage: python3 rep_3.py work <teacher> <w0> <w1> | combine"""
import sys, time, numpy as np
ROOT='/Users/meros/Desktop/fly-mb-compartments/'
OUT=ROOT+'fly-v4/verification/replication/'
K=1800; NG=65; NODOR=900; NTR=600; NTRIAL=400; ETA=0.05; NACT=int(K*0.05)
HEMS=['M_R','M_L','F_R','F_L']
_c=np.load(ROOT+'fly-foraging/data/mb_circuit.npz',allow_pickle=True)
_Nfull=_c['N'].astype(np.float64); SIGN=_c['signs'].astype(np.float64)
_ind=np.load(ROOT+'fly-v4/individuals.npz')
N=_Nfull[np.random.default_rng(101).permutation(_Nfull.shape[0])[:K]]      # 1800x49, shared
NPOS=N>0
W=(N*np.abs(SIGN)).sum(1)                       # per-KC sum_j N|sign|
NS=N*SIGN                                       # N*sign
P={}
for i,h in enumerate(HEMS):
    m=_ind[h].astype(np.float64)
    P[h]=m[:,np.random.default_rng(200+i).choice(m.shape[1],K,replace=False)]  # 65x1800

def top_code(psi,rng):
    """psi: (n,K) -> (n,NACT) indices of top-5%, random tie break"""
    key=psi+rng.random(psi.shape)*0.5           # psi integer-valued -> noise only breaks ties
    return np.argpartition(-key,NACT-1,axis=1)[:,:NACT]

def random_wiring(rng):
    Pm=np.zeros((NG,K))
    for k in range(K):
        Pm[rng.choice(NG,6,replace=False),k]=1
    return Pm

def marg_wiring(h,rng):
    base=P[h]; rs=base.sum(1)
    logp=np.where(rs>0,np.log(np.maximum(rs,1e-300)),-np.inf)
    g=logp[:,None]+rng.gumbel(size=base.shape)   # Gumbel-top-k == sequential sampling w/o replacement prop. to rs
    order=np.argsort(-g,axis=0)                   # selection order per KC
    Pm=np.zeros((NG,K))
    for k in range(K):
        w=base[:,k]; w=w[w>0]; d=len(w)
        if d: Pm[order[:d,k],k]=rng.permutation(w)
    return Pm

def student_auc(Pm,Xtr_y,Xtr,Xte,yte,rng):
    # per-KC score a[k]=sum_j N sign (q-0.5) so that B-B0 = sum_{k in c} a[k]
    q=np.full((K,49),0.5); a=np.zeros(K)
    ctr=top_code(Xtr@Pm,rng); cte=top_code(Xte@Pm,rng)
    scale_te=0.5*W[cte].sum(1)
    def acc():
        v=np.clip(a[cte].sum(1)/scale_te,-1,1)
        pred=np.where(v>=0,1,-1) ; return (pred==yte).mean()
    accs=[acc()]
    for t in range(NTRIAL):
        idx=t%NTR; c=ctr[idx]; y=Xtr_y[idx]
        v=np.clip(a[c].sum()/(0.5*W[c].sum()),-1,1)
        d=y-v
        if d!=0:
            qa=q[c]; m=NPOS[c]; up=(d*SIGN>0)[None,:]
            ad=abs(d)
            new=np.where(up,qa+ETA*ad*(1-qa),qa-ETA*ad*qa)
            q[c]=np.where(m,new,qa)
            a[c]=(NS[c]*(q[c]-0.5)).sum(1)
        if (t+1)%10==0: accs.append(acc())
    return np.mean(accs)

def world(teacher,seed):
    rng=np.random.default_rng(seed)
    odours=np.zeros((NODOR,NG))
    for i in range(NODOR): odours[i,rng.choice(NG,6,replace=False)]=1
    qt=rng.random((K,49))
    code=top_code(odours@P[teacher],rng)
    out=np.einsum('nkj,kj->n',N[code]*SIGN[None,None,:],qt[code]) if False else np.array([(NS[c]*qt[c]).sum() for c in code])
    y=np.where(out>=np.median(out),1,-1)
    ytr,yte=y[:NTR],y[NTR:]; Xtr,Xte=odours[:NTR],odours[NTR:]
    res={}
    mats={h:P[h] for h in HEMS}
    mats['random']=random_wiring(rng)
    mats['marg_M_R']=marg_wiring('M_R',rng); mats['marg_F_R']=marg_wiring('F_R',rng)
    for name,Pm in mats.items():
        res[name]=student_auc(Pm,ytr,Xtr,Xte,yte,rng)
    return res

STUD=HEMS+['random','marg_M_R','marg_F_R']
TEACH=['M_R','F_R']
def work(ti,w0,w1):
    T=TEACH[ti]; rows=[]
    for w in range(w0,w1):
        r=world(T,[7,ti,w]) if False else world(T,int(np.random.SeedSequence([7,ti,w]).generate_state(1)[0]))
        rows.append([r[s] for s in STUD])
    np.save(OUT+f'rep3_{T}_{w0}_{w1}.npy',np.array(rows))

def boot(d,rng):
    idx=rng.integers(0,len(d),(10000,len(d))); m=d[idx].mean(1)
    return d.mean(),*np.percentile(m,[2.5,97.5])

def combine():
    rng=np.random.default_rng(5)
    lines=[]
    for T,pairs in [('M_R',[('M_L','random'),('F_R','random'),('F_R','marg_F_R'),('F_L','random')]),
                    ('F_R',[('F_L','random'),('M_R','random'),('M_R','marg_M_R'),('M_L','random')])]:
        A=np.vstack([np.load(OUT+f'rep3_{T}_0_30.npy'),np.load(OUT+f'rep3_{T}_30_60.npy')])
        lines.append(f'\nTeacher {T} (n={len(A)} worlds)\n\n| student | mean auc |\n|---|---|')
        for i,s in enumerate(STUD): lines.append(f'| {s} | {A[:,i].mean():.4f} |')
        lines.append('\n| contrast | mean diff | 95% CI |\n|---|---|---|')
        for a,b in pairs:
            m,lo,hi=boot(A[:,STUD.index(a)]-A[:,STUD.index(b)],rng)
            lines.append(f'| {a} - {b} | {m:+.4f} | [{lo:+.4f}, {hi:+.4f}] |')
    print('\n'.join(lines))
if __name__=='__main__':
    if sys.argv[1]=='work':
        t0=time.time(); work(int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])); print('done',time.time()-t0)
    else: combine()

"""Stage 0/1 core: odour-valence learning tasks (fast, no arena) to test the mushroom-body inductive bias directly.
A world = a task instance (odour pool + labels). A learner sees (odour, label) trials, predicts the sign of its valence, and updates with a bounded delta rule.
Metrics per world: held-out accuracy curve (sample efficiency), accuracy after few trials, final accuracy, robustness (input noise, KC silencing)."""
import os, sys, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,"..","fly-foraging")); os.chdir(os.path.join(HERE,"..","fly-foraging"))
import forage as F
os.chdir(HERE)
P0,N,SIGNS,NG,NK,NB=F.P0.astype(np.float64),F.N.astype(np.float64),F.SIGNS.astype(np.float64),F.NG,F.NK,F.NB
KFRAC=0.05
def make_P(kind,rng):
    if kind=="real_wshuf":                         # real topology, synaptic counts permuted among the real edges
        Q=P0.copy(); nz=Q>0; v=Q[nz].copy(); rng.shuffle(v); Q[nz]=v; return Q
    return F.make_P(kind,rng).astype(np.float64)
def codes_for(U,P,rng):
    """top-5% KCs per odour (ties broken by tiny jitter). U: (n,65) -> index array (n,k)"""
    psi=U@P+1e-6*rng.random((len(U),NK)); k=int(KFRAC*NK); return np.argpartition(-psi,k-1,axis=1)[:,:k]
class MBL:
    """Bounded delta rule on KC->MBON (same as forage.MB), vectorised evaluation."""
    def __init__(s,eta): s.q=np.full(N.shape,0.5); s.eta=eta
    def w(s): return (N*s.q)@SIGNS
    def val(s,codes,b0,sc,silence=None):
        w=s.w()
        if silence is not None: 
            m=np.ones(NK); m[silence]=0; c=(w*m)[codes].sum(1); b=c; 
        else: b=w[codes].sum(1)
        return np.clip((b-b0)/np.maximum(sc,1e-9),-1,1)
    def update(s,code,delta):
        pot=(delta*SIGNS>0); g=s.eta*abs(delta); rows=NB[code]; q=s.q[code]; s.q[code]=q+g*rows*((pot[None,:]*1.0)-q)
A_VEC=N@SIGNS; C_VEC=N@np.abs(SIGNS)
def b0sc(codes): return 0.5*A_VEC[codes].sum(1), 0.5*C_VEC[codes].sum(1)
class LinL:
    def __init__(s,eta): s.w=np.zeros(NG); s.eta=eta
    def val_u(s,U): return np.clip(U@s.w/np.maximum(U.sum(1),1),-1,1)
    def update_u(s,u,delta): s.w+=s.eta*delta*u/max(u.sum(),1)*3
# ---------------------------------------------------------------- odour pools and labels
def synth_odours(rng,n,k=6):
    U=np.zeros((n,NG)); 
    for i in range(n): U[i,rng.choice(NG,k,replace=False)]=1
    return U
def teacher_labels(U,Pt,rng):
    """label = sign of a mushroom-body teacher (wiring Pt, random KC->MBON synapses), centred so that classes are balanced"""
    codes=codes_for(U,Pt,rng); q=rng.random(N.shape); w=(N*q)@SIGNS; v=w[codes].sum(1); return np.where(v>=np.median(v),1.0,-1.0)
CONJ_FILL=2
def conj_task(rng,n):
    """balanced XOR of two glomeruli: each of the two is present with probability 0.5, the other 4 glomeruli are random fillers"""
    g=rng.choice(NG,2,replace=False); U=np.zeros((n,NG)); a=rng.random(n)<0.5; b=rng.random(n)<0.5
    for i in range(n):
        fill=[x for x in rng.choice(NG,8,replace=False) if x not in g][:4]; U[i,fill]=1
        if a[i]: U[i,g[0]]=1
        if b[i]: U[i,g[1]]=1
    return U,np.where(a^b,1.0,-1.0)
def family_task(rng,n_train_odours=6,n_test=300):
    """legacy synthetic families: two families of 6-glomerulus base odours, variants share 4 of 6; label = family"""
    bases=[rng.choice(NG,6,replace=False) for _ in range(2)]
    def var(b):
        keep=rng.choice(b,4,replace=False); s=set(int(x) for x in keep)
        while len(s)<6: s.add(int(rng.integers(NG)))
        u=np.zeros(NG); u[list(s)]=1; return u
    def make(n): 
        fam=rng.integers(0,2,n); return np.stack([var(bases[f]) for f in fam]),np.where(fam==0,1.0,-1.0)
    return make(600),make(n_test)
_DOOR=None
def door():
    global _DOOR
    if _DOOR is None:
        d=np.load(os.path.join(HERE,"odours.npz"),allow_pickle=True); _DOOR=(d["U"],d["classes"])
    return _DOOR
def make_world(task,seed):
    """returns (train_U, train_y, test_U, test_y)"""
    rng=np.random.default_rng(seed)
    if task=="family": (a,b),(c,d)=family_task(rng); return a,b,c,d
    if task=="linear_teacher":
        U=synth_odours(rng,900); w=rng.normal(size=NG); v=U@w; y=np.where(v>=np.median(v),1.0,-1.0); return U[:600],y[:600],U[600:],y[600:]
    if task in("teacher_real","teacher_random"):
        U=synth_odours(rng,900); y=teacher_labels(U,P0 if task=="teacher_real" else make_P("random",np.random.default_rng(seed+9)),rng)
        return U[:600],y[:600],U[600:],y[600:]
    if task in("door_class","door_teacher_real"):
        D,cls=door(); idx=rng.permutation(len(D)); tr,te=idx[:int(0.7*len(D))],idx[int(0.7*len(D)):]
        if task=="door_class":
            uc=sorted(set(cls)); val={c:(1.0 if i%2==0 else -1.0) for i,c in enumerate(rng.permutation(uc))}; y=np.array([val[c] for c in cls])
        else: y=teacher_labels(D,P0,rng)
        # sample training stream with replacement from the training odours (the pool is small)
        s=rng.choice(tr,600); return D[s],y[s],D[te],y[te]
    raise ValueError(task)
# ---------------------------------------------------------------- learner run
def adapt(P,U,rng,n_pre=300,eta_p=0.05):
    """unsupervised Hebbian adaptation of PN->KC: active KCs move their input profile toward the current odour, total synaptic weight per KC conserved"""
    P=P.copy(); tot=P.sum(0)+1e-9
    for t in range(n_pre):
        u=U[t%len(U)]; psi=u@P+1e-6*rng.random(NK); act=np.argpartition(-psi,int(KFRAC*NK)-1)[:int(KFRAC*NK)]
        P[:,act]=(1-eta_p)*P[:,act]+eta_p*(u[:,None]/max(u.sum(),1))*tot[act][None,:]
    return P
def run(task,seed,kind,eta,n_trials=400,eval_every=20,noise=None,silence_frac=0.0,n_pre=300,eta_p=0.05):
    """returns dict(curve=(n_eval,), final=float, auc=float, acc50=float, noisy=float, silenced=float)"""
    trU,trY,teU,teY=make_world(task,seed); rng=np.random.default_rng(seed+1000)
    if kind=="linear":
        L=LinL(eta); curve=[]
        for t in range(n_trials+1):
            if t%eval_every==0: curve.append(float((np.sign(L.val_u(teU)+1e-12)==teY).mean()))
            if t==n_trials: break
            i=t%len(trU); u=trU[i]; v=float(L.val_u(u[None])[0]); L.update_u(u,trY[i]-v)
        nz=teU*(rng.random(teU.shape)>0.15); noisy=float((np.sign(L.val_u(nz)+1e-12)==teY).mean()); sil=curve[-1]
    else:
        adapted=kind.endswith("+ad"); kind=kind[:-3] if adapted else kind
        P=make_P(kind,rng)
        if adapted: P=adapt(P,trU,rng,n_pre,eta_p)
        codes_tr=codes_for(trU,P,rng); codes_te=codes_for(teU,P,rng); b0t,sct=b0sc(codes_te)
        M=MBL(eta); curve=[]
        for t in range(n_trials+1):
            if t%eval_every==0: curve.append(float((np.sign(M.val(codes_te,b0t,sct)+1e-12)==teY).mean()))
            if t==n_trials: break
            i=t%len(trU); c=codes_tr[i]; b0,sc=b0sc(c[None]); v=float(M.val(c[None],b0,sc)[0]); M.update(c,trY[i]-v)
        nz=teU*(rng.random(teU.shape)>0.15); cn=codes_for(nz,P,rng); b0n,scn=b0sc(cn); noisy=float((np.sign(M.val(cn,b0n,scn)+1e-12)==teY).mean())
        sil=float((np.sign(M.val(codes_te,b0t,sct,silence=rng.choice(NK,int(0.2*NK),replace=False))+1e-12)==teY).mean())
    c=np.array(curve); return dict(curve=c,final=float(c[-1]),auc=float(c.mean()),acc50=float(c[int(50/eval_every)]) if len(c)>3 else float(c[-1]),noisy=noisy,silenced=sil)

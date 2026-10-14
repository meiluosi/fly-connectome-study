"""Exemplar-free prototype baselines and FlyModel variants (numpy). All share the cl_bench API: learn_class(X,c), predict(X,seen)."""
import numpy as np
import cl_bench as B
class _Proto:
    def __init__(s,d,K): s.S=np.zeros((K,d),np.float64); s.n=np.zeros(K)
    def learn_class(s,X,c): s.S[c]+=X.sum(0); s.n[c]+=len(X)
class NCM(_Proto):                                   # P1 euclid / P2 cosine
    def __init__(s,d,K,cosine=False): super().__init__(d,K); s.cos=cosine
    def predict(s,X,seen):
        M=s.S[seen]/s.n[seen,None]
        if s.cos: Xn=X/np.maximum(np.linalg.norm(X,axis=1,keepdims=True),1e-12); Mn=M/np.maximum(np.linalg.norm(M,axis=1,keepdims=True),1e-12); sc=Xn@Mn.T
        else: sc=X@M.T-0.5*(M**2).sum(1)
        return np.array(seen)[sc.argmax(1)]
class ClassSumDot(_Proto):                           # P3: raw-feature Hebbian class sums (no expansion, no WTA)
    def predict(s,X,seen): return np.array(seen)[(X@s.S[seen].T).argmax(1)]
class SLDA(_Proto):                                  # P4: shared-covariance LDA from streaming accumulators
    def __init__(s,d,K,shrink): super().__init__(d,K); s.Sxx=np.zeros((d,d)); s.shrink=shrink; s.d=d
    def learn_class(s,X,c): super().learn_class(X,c); s.Sxx+=X.T.astype(np.float64)@X
    def predict(s,X,seen):
        n=s.n[seen]; M=s.S[seen]/n[:,None]; N=n.sum(); within=(s.Sxx-sum(n[i]*np.outer(M[i],M[i]) for i in range(len(seen))))/N
        # scatter is accumulated over ALL classes learned so far, so restrict to the seen set (identical here: seen == learned)
        Lam=np.linalg.inv(within+s.shrink*np.trace(within)/s.d*np.eye(s.d)); W=M@Lam; b=-0.5*(W*M).sum(1)
        return np.array(seen)[(X@W.T+b).argmax(1)]
class FlyVariant(B.FlyModel):
    """norm in {'max' (F0 original, with WTA), 'l2_nowta' (F2), 'minmax_nowta' (F2b, paper's dense code)}"""
    def __init__(s,*a,mode="wta",**k): super().__init__(*a,**k); s.mode=mode
    def phi(s,X,chunk=2000):
        if s.mode=="wta": return super().phi(X,chunk)
        out=[]
        for i in range(0,len(X),chunk):
            psi=X[i:i+chunk]@s.Theta.T
            if s.mode=="l2_nowta": out.append(psi/np.maximum(np.linalg.norm(psi,axis=1,keepdims=True),1e-12))
            else: mn=psi.min(1,keepdims=True); mx=psi.max(1,keepdims=True); out.append((psi-mn)/np.maximum(mx-mn,1e-12))
        return np.concatenate(out)
class ExpansionNCM(FlyVariant):
    """Nearest-class-mean classifier in the (dense or WTA-sparse) random-expansion space: separates the representation from the Hebbian class-sum rule."""
    def __init__(s,d,m,k_inputs,l,beta,K,seed,mode,cosine):
        super().__init__(d,m,k_inputs,l,beta,K,seed,mode=mode); s.cosine=cosine; s.S=np.zeros((K,m),np.float64); s.n=np.zeros(K)
    def learn_class(s,X,c): ph=s.phi(X); s.S[c]+=ph.sum(0); s.n[c]+=len(X)
    def predict(s,X,seen):
        M=s.S[seen]/s.n[seen,None]; ph=s.phi(X)
        if s.cosine: sc=(ph/np.maximum(np.linalg.norm(ph,axis=1,keepdims=True),1e-12))@(M/np.maximum(np.linalg.norm(M,axis=1,keepdims=True),1e-12)).T
        else: sc=ph@M.T-0.5*(M**2).sum(1)
        return np.array(seen)[sc.argmax(1)]
def make(name,d,K,cfg,seed,hp=None):
    hp=hp or {}
    if name=="NCM_euclid": return NCM(d,K,False)
    if name=="NCM_cos": return NCM(d,K,True)
    if name=="ClassSumDot": return ClassSumDot(d,K)
    if name=="SLDA": return SLDA(d,K,hp["shrink"])
    l=hp.get("l",cfg["l"]); beta=hp.get("beta",cfg["beta"])
    if name=="Fly": return FlyVariant(d,cfg["m"],cfg["k_inputs"],l,beta,K,seed,mode="wta")
    if name=="Fly_dense_l2": return FlyVariant(d,cfg["m"],cfg["k_inputs"],cfg["m"],beta,K,seed,mode="l2_nowta")
    if name.startswith("ExpNCM_"):
        _,rep,met=name.split("_"); return ExpansionNCM(d,cfg["m"],cfg["k_inputs"],(cfg["l"] if rep=="wta" else cfg["m"]),cfg["beta"],K,seed,"wta" if rep=="wta" else "l2_nowta",met=="cos")
    if name=="Fly_dense_l2_noclip": return FlyVariant(d,cfg["m"],cfg["k_inputs"],cfg["m"],beta,K,seed,mode="l2_nowta",clip=np.inf)
    if name=="Fly_wta_noclip": return FlyVariant(d,cfg["m"],cfg["k_inputs"],l,beta,K,seed,mode="wta",clip=np.inf)
    if name=="Fly_dense_minmax": return FlyVariant(d,cfg["m"],cfg["k_inputs"],cfg["m"],beta,K,seed,mode="minmax_nowta")
    raise ValueError(name)

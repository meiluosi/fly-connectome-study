"""Learned edge heuristic for ACO-style tour construction. Edge features are HAND-WRITTEN and encoded as 'odours' (6 active glomeruli, one per feature group);
the learner maps the odour to a valence in [-1,1]. Learners: MB (real/shuffled/random PN->KC wiring), Linear (no expansion), None."""
import numpy as np, mbcore as M, tsp as T
OFF=dict(rj=0,db=11,mu=23,ri=25,ci=36,cj=44)      # glomerulus offsets per feature group (52 glomeruli used of 65)
def edge_signatures(X,D):
    n=len(D); Dm=D+np.diag(np.full(n,np.inf)); order=np.argsort(Dm,axis=1); R=np.empty((n,n),int); 
    for i in range(n): R[i,order[i]]=np.arange(n)
    rj=np.minimum(R,10)                                  # rank of j among i's neighbours
    nn1=np.sort(Dm,axis=1)[:,0].mean(); db=np.minimum((D/nn1*4).astype(int),11)
    mu=((R<5)&(R.T<5)).astype(int); ri=np.minimum(R.T,10)
    c=X.mean(0); dc=np.linalg.norm(X-c,axis=1); cb=np.minimum((dc/dc.max()*8).astype(int),7); ci=np.repeat(cb[:,None],n,1); cj=np.repeat(cb[None,:],n,0)
    key=((((rj*12+db)*2+mu)*11+ri)*8+ci)*8+cj; return key
def key_to_glom(key):
    cj=key%8; key//=8; ci=key%8; key//=8; ri=key%11; key//=11; mu=key%2; key//=2; db=key%12; key//=12; rj=key
    return [OFF['rj']+rj,OFF['db']+db,OFF['mu']+mu,OFF['ri']+ri,OFF['ci']+ci,OFF['cj']+cj]
class SigTable:
    """Global signature table: id per distinct edge signature, with its glomerulus set and (for MB) KC code. One table per learner type/wiring."""
    def __init__(s,kind,seed):
        s.kind=kind; s.rng=np.random.default_rng(seed); s.ids={}; s.glom=[]; s.code=[]; s.b0=[]; s.sc=[]
        s.P=None if kind in("linear","none") else M.make_P(kind,np.random.default_rng(seed+1))
        s.mb=M.MB() if s.P is not None else None; s.lw=np.zeros(M.NG) if kind=="linear" else None; s.lin_eta=1.0
    def ids_for(s,key):
        flat=key.ravel(); uk,inv=np.unique(flat,return_inverse=True); out=np.empty(len(uk),int)
        for t,k in enumerate(uk):
            k=int(k)
            if k not in s.ids:
                g=key_to_glom(k); s.ids[k]=len(s.glom); s.glom.append(g)
                if s.P is not None: c=M.kc_code_from_glom(g,s.P,s.rng); s.code.append(c); s.b0.append(0.5*M.A_VEC[c].sum()); s.sc.append(0.5*M.C_VEC[c].sum())
            out[t]=s.ids[k]
        return out[inv].reshape(key.shape)
    def valence(s,sig_ids):
        if s.kind=="none": return np.zeros(sig_ids.shape)
        u=np.unique(sig_ids); v=np.zeros(len(s.glom))
        if s.kind=="linear": 
            for i in u: g=s.glom[i]; v[i]=np.clip(s.lw[g].sum()/len(g),-1,1)
        else:
            w=s.mb.w()
            for i in u: v[i]=np.clip((w[s.code[i]].sum()-s.b0[i])/max(s.sc[i],1e-9),-1,1)
        return v[sig_ids]
    def update(s,i,delta):
        if s.kind=="none": return
        if s.kind=="linear": g=s.glom[i]; s.lw[g]+=s.lin_eta*delta/len(g)*3
        else: s.mb.update(s.code[i],delta)
def construct(D,W,r,n_ants):
    """Vectorised-over-ants tour construction with weight matrix W (n x n)."""
    n=len(D); tours=np.zeros((n_ants,n),int); cur=r.integers(n,size=n_ants); vis=np.zeros((n_ants,n),bool); tours[:,0]=cur; vis[np.arange(n_ants),cur]=True
    for k in range(1,n):
        p=np.where(vis,0.0,W[cur]); p=p/p.sum(1,keepdims=True); u=r.random(n_ants)[:,None]; nxt=(p.cumsum(1)<u).sum(1); nxt=np.minimum(nxt,n-1)
        bad=vis[np.arange(n_ants),nxt]
        if bad.any(): nxt[bad]=np.argmax(~vis[bad],axis=1)
        tours[:,k]=nxt; vis[np.arange(n_ants),nxt]=True; cur=nxt
    return tours
def lens(D,tours): return D[tours,np.roll(tours,-1,axis=1)].sum(1)
def train(table,instances,iters=10,n_ants=20,kappa=2.0,beta=3.0,seed=0,eta_mult=1.0):
    r=np.random.default_rng(seed)
    for X,D in instances:
        n=len(D); key=edge_signatures(X,D); sig=table.ids_for(key); eta=1.0/(D+np.eye(n)); eta[np.eye(n,dtype=bool)]=0
        for it in range(iters):
            V=table.valence(sig); W=(eta**beta)*np.exp(kappa*V); tours=construct(D,W,r,n_ants); L=lens(D,tours); rt=np.tanh((L.mean()-L)/(0.5*L.std()+1e-9))
            acc={}
            for k in range(n_ants):
                a=tours[k]; b=np.roll(a,-1); ids=sig[a,b]; vs=V[a,b]
                for i,v in zip(ids,vs): s_=acc.setdefault(int(i),[0.0,0]); s_[0]+=rt[k]-v; s_[1]+=1
            for i,(sd,c) in acc.items(): table.update(i,sd/c)

def aco_vec(D,V=None,kappa=0.0,n_ants=20,iters=25,alpha=1.0,beta=3.0,rho=0.1,seed=0):
    """MMAS-style ACO, vectorised over ants. Weights = tau^alpha * eta^beta * exp(kappa*V); V = learned edge valence matrix (None -> plain ACO).
    Returns (best_len, best-so-far history, constructions)."""
    r=np.random.default_rng(seed); n=len(D); eta=1.0/(D+np.eye(n)); eta[np.eye(n,dtype=bool)]=0; L0=T.tour_len(D,T.nn_tour(D)); tmax=1.0/(rho*L0); tmin=tmax/(2*n); tau=np.full((n,n),tmax)
    H=np.exp(kappa*V) if V is not None else 1.0; base=(eta**beta)*H; best=np.inf; hist=[]
    for it in range(iters):
        W=(tau**alpha)*base; tours=construct(D,W,r,n_ants); L=lens(D,tours); k=int(np.argmin(L)); best=min(best,float(L[k]))
        tau*=(1-rho); a=tours[k]; b=np.roll(a,-1); dep=1.0/L[k]; tau[a,b]+=dep; tau[b,a]+=dep; tau=np.clip(tau,tmin,tmax); hist.append(best)
    return best,hist,n_ants*iters

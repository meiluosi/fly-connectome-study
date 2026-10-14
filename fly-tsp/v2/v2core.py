"""v2: online (within-instance) mushroom-body learning, heterogeneous flocks, islands/communication, optional 2-opt. Imports the frozen v1 modules (tsp, fly_heuristic, mbcore) unchanged.
One ACO loop covers every arm: weights for ant k = tau[island(k)]^alpha * eta^beta * exp(kappa * V_fly(k)); flies learn from tour advantages (same reward as v1 train())."""
import sys, os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
import numpy as np, tsp as T, fly_heuristic as H, mbcore as M
def construct_multi(D,W,grp,r,n_ants):
    """Like fly_heuristic.construct, but W is (G,n,n) and ant k uses W[grp[k]]. With G=1 it consumes the RNG exactly like the v1 construct."""
    n=len(D); tours=np.zeros((n_ants,n),int); cur=r.integers(n,size=n_ants); vis=np.zeros((n_ants,n),bool); tours[:,0]=cur; ar=np.arange(n_ants); vis[ar,cur]=True
    for k in range(1,n):
        p=np.where(vis,0.0,W[grp,cur]); p=p/p.sum(1,keepdims=True); u=r.random(n_ants)[:,None]; nxt=np.minimum((p.cumsum(1)<u).sum(1),n-1)
        bad=vis[ar,nxt]
        if bad.any(): nxt[bad]=np.argmax(~vis[bad],axis=1)
        tours[:,k]=nxt; vis[ar,nxt]=True; cur=nxt
    return tours
class Circuit:
    """One fly. kind: real|shuffled|random (PN->KC wiring + KC->MBON learning) or linear. Signature codes are computed per instance (no cross-instance cache).
    q0/lw0: optional pretrained state to start from. learn=False freezes it. drop: fraction of KCs removed (individual variation)."""
    def __init__(s,kind,lr,seed,drop=0.0,q0=None,lw0=None,learn=True):
        s.kind=kind; s.lr=lr; s.learn=learn; s.rng=np.random.default_rng(seed); s.q0=q0; s.lw0=lw0
        if kind=="linear": s.P=None
        else:
            P=M.make_P(kind,np.random.default_rng(seed+1)); 
            if drop>0: P=P*(s.rng.random(M.NK)>=drop)[None,:]
            s.P=P
    def start(s,key):
        """new instance: compute the odour->KC code of every distinct edge signature, reset (or restore pretrained) learning state. Returns signature-id matrix."""
        uk,inv=np.unique(key.ravel(),return_inverse=True); G=np.stack(H.key_to_glom(uk.copy()),1); s.G=G; s.U=len(uk)
        if s.kind=="linear": s.lw=np.zeros(M.NG) if s.lw0 is None else s.lw0.copy()
        else:
            u=np.zeros((s.U,M.NG)); u[np.arange(s.U)[:,None],G]=1; psi=u@s.P+1e-6*s.rng.random((s.U,M.NK)); k=int(0.05*M.NK)
            s.codes=np.argpartition(-psi,k-1,axis=1)[:,:k]; s.b0=0.5*M.A_VEC[s.codes].sum(1); s.sc=np.maximum(0.5*M.C_VEC[s.codes].sum(1),1e-9)
            s.mb=M.MB(s.lr); 
            if s.q0 is not None: s.mb.q=s.q0.copy()
        s.inv=inv.reshape(key.shape); return s.inv
    def valence_u(s):
        if s.kind=="linear": return np.clip(s.lw[s.G].sum(1)/s.G.shape[1],-1,1)
        w=s.mb.w(); return np.clip((w[s.codes].sum(1)-s.b0)/s.sc,-1,1)
    def update_u(s,u,delta):
        if not s.learn: return
        if s.kind=="linear": s.lw[s.G[u]]+=s.lr*delta/s.G.shape[1]*3
        else:
            code=s.codes[u]; pot=(delta*M.SIGNS>0).astype(float); q=s.mb.q; qq=q[code]; q[code]=qq+(s.lr*abs(delta))*M.NB[code]*(pot[None,:]-qq)   # == M.MB.update (pot-q form)
def learn_from(circ,tours,rt,vmat_u,inv):
    """per-signature mean of (reward - predicted valence) over the edges of the given tours, then one update per signature (v1 train() semantics)."""
    a=tours; b=np.roll(tours,-1,axis=1); ids=inv[a,b].ravel(); adv=(rt[:,None]-vmat_u[inv[a,b]]).ravel()
    cnt=np.bincount(ids,minlength=circ.U); sm=np.bincount(ids,weights=adv,minlength=circ.U)
    for u in np.nonzero(cnt)[0]: circ.update_u(int(u),sm[u]/cnt[u])
def run(X,D,cfg,circuits=(),seed=0):
    """cfg: alpha,beta,rho,kappa,ants,iters, islands S (default 1), exch (iterations between elite exchange, None=never), broadcast (bool), ls (2-opt on every tour).
    circuits: list of Circuit (fly of ant k = k % len). Returns best tour length."""
    r=np.random.default_rng(seed); n=len(D); A=cfg["ants"]; al,be,rho,ka=cfg["alpha"],cfg["beta"],cfg["rho"],cfg.get("kappa",0.0); S=cfg.get("islands",1); ex=cfg.get("exch"); F=len(circuits)
    eta=1.0/(D+np.eye(n)); eta[np.eye(n,dtype=bool)]=0; L0=T.tour_len(D,T.nn_tour(D)); tmax=1.0/(rho*L0); tmin=tmax/(2*n); tau=np.full((S,n,n),tmax)
    key=H.edge_signatures(X,D) if F else None; invs=[c.start(key) for c in circuits]; isl=np.arange(A)%S; fly=np.arange(A)%F if F else np.zeros(A,int)
    best=np.inf; bt=None; eb=eta**be
    for it in range(cfg["iters"]):
        if F:
            vu=[c.valence_u() for c in circuits]; Vm=[vu[f][invs[f]] for f in range(F)]; base=[eb*np.exp(ka*V) for V in Vm]
        else: base=[eb]
        combos=sorted(set(zip(isl.tolist(),fly.tolist()))); cid={c:i for i,c in enumerate(combos)}
        W=np.stack([(tau[g]**al)*base[f] for g,f in combos]); grp=np.array([cid[(g,f)] for g,f in zip(isl.tolist(),fly.tolist())])
        tours=construct_multi(D,W,grp,r,A)
        if cfg.get("ls"): tours=np.stack([T.two_opt(D,t) for t in tours])
        L=H.lens(D,tours); k=int(np.argmin(L))
        if L[k]<best: best=float(L[k]); bt=tours[k].copy()
        for g in range(S):
            m=np.nonzero(isl==g)[0]; kg=m[int(np.argmin(L[m]))]; tau[g]*=(1-rho); a=tours[kg]; b=np.roll(a,-1); dep=1.0/L[kg]; tau[g][a,b]+=dep; tau[g][b,a]+=dep
            if S>1 and ex and (it+1)%ex==0: a=bt; b=np.roll(a,-1); d2=1.0/best; tau[g][a,b]+=d2; tau[g][b,a]+=d2
            tau[g]=np.clip(tau[g],tmin,tmax)
        if F and any(c.learn for c in circuits):
            for f,c in enumerate(circuits):
                if not c.learn: continue
                if cfg.get("broadcast",True) or F==1: m=np.arange(A)
                else: m=np.nonzero(fly==f)[0]
                Lm=L[m]; rt=np.tanh((Lm.mean()-Lm)/(0.5*Lm.std()+1e-9)); learn_from(c,tours[m],rt,vu[f],invs[f])
    return best
def make_flock(kind,F,lr,seed,drop=0.0,q0=None,lw0=None,learn=True):
    return [Circuit(kind,lr,seed*100+f,drop=drop,q0=q0,lw0=lw0,learn=learn) for f in range(F)]

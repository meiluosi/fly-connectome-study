"""Euclidean TSP baselines: instance generator, nearest neighbour, vectorised best-improvement 2-opt, MMAS-style ant colony. numpy only.
Budget convention: one 'construction' = one complete tour built by one ant/fly (local search is counted separately and reported)."""
import numpy as np
def make_instance(n,seed):
    r=np.random.default_rng(seed); X=r.random((n,2)); return X,np.linalg.norm(X[:,None]-X[None],axis=2)
def tour_len(D,t): return float(D[t,np.roll(t,-1)].sum())
def nn_tour(D,start=0):
    n=len(D); vis=np.zeros(n,bool); t=[start]; vis[start]=True
    for _ in range(n-1):
        d=np.where(vis,np.inf,D[t[-1]]); j=int(np.argmin(d)); t.append(j); vis[j]=True
    return np.array(t)
def two_opt(D,t,max_pass=10_000):
    t=np.array(t).copy(); n=len(t); mask=np.triu(np.ones((n,n),bool),k=2); mask[0,n-1]=False
    for _ in range(max_pass):
        a=t; b=np.roll(t,-1); e=D[a,b]; d=D[a[:,None],a[None,:]]+D[b[:,None],b[None,:]]-e[:,None]-e[None,:]; d=np.where(mask,d,0.0)
        k=int(np.argmin(d)); i,j=divmod(k,n)
        if d[i,j]>-1e-12: break
        t[i+1:j+1]=t[i+1:j+1][::-1].copy()
    return t
def or_opt_pass(D,t):                                  # move single cities to their best position (simple, used only for the reference solver)
    t=list(t); n=len(t); improved=True
    while improved:
        improved=False
        for i in range(n):
            c=t[i]; prev=t[i-1]; nxt=t[(i+1)%n]; rem=D[prev,c]+D[c,nxt]-D[prev,nxt]; rest=t[:i]+t[i+1:]; best=0.0; bj=None
            for j in range(len(rest)):
                a=rest[j]; b=rest[(j+1)%len(rest)]; add=D[a,c]+D[c,b]-D[a,b]
                if add-rem<best-1e-12: best=add-rem; bj=j
            if bj is not None: t=rest[:bj+1]+[c]+rest[bj+1:]; improved=True; break
    return np.array(t)
def reference_solver(D,restarts=30,seed=0):
    """Strong reference ('best known' proxy): many random-restart 2-opt + or-opt local optima."""
    r=np.random.default_rng(seed); n=len(D); best=None; bl=np.inf
    for k in range(restarts):
        t=nn_tour(D,int(r.integers(n))) if k%2==0 else r.permutation(n)
        for _ in range(3): t=or_opt_pass(D,two_opt(D,t))
        l=tour_len(D,t)
        if l<bl: bl=l; best=t
    return best,bl
def aco(D,n_ants=20,iters=50,alpha=1.0,beta=3.0,rho=0.1,seed=0,local_search=False,q0=0.0):
    """MMAS-style ACO. Returns (best_tour, best_len, history of best-so-far per iteration, n_constructions)."""
    r=np.random.default_rng(seed); n=len(D); eta=1.0/(D+np.eye(n)); eta[np.eye(n,dtype=bool)]=0; L0=tour_len(D,nn_tour(D)); tmax=1.0/(rho*L0); tmin=tmax/(2*n); tau=np.full((n,n),tmax)
    best=None; bl=np.inf; hist=[]; cons=0
    for it in range(iters):
        ib=None; ibl=np.inf
        for a in range(n_ants):
            w=(tau**alpha)*(eta**beta); cur=int(r.integers(n)); vis=np.zeros(n,bool); vis[cur]=True; t=[cur]
            for _ in range(n-1):
                p=np.where(vis,0.0,w[cur]); s=p.sum(); j=int(r.choice(n,p=p/s)) if s>0 else int(np.argmin(vis)); t.append(j); vis[j]=True; cur=j
            t=np.array(t); cons+=1
            if local_search: t=two_opt(D,t)
            l=tour_len(D,t)
            if l<ibl: ibl=l; ib=t
        if ibl<bl: bl=ibl; best=ib
        tau*=(1-rho); dep=1.0/ibl; e=np.roll(ib,-1); tau[ib,e]+=dep; tau[e,ib]+=dep; tau=np.clip(tau,tmin,tmax); hist.append(bl)
    return best,bl,hist,cons

def make_clustered(n,seed,k=5,sd=0.05):
    r=np.random.default_rng(seed); C=r.random((k,2)); lab=r.integers(k,size=n); X=np.clip(C[lab]+sd*r.normal(size=(n,2)),0,1); return X,np.linalg.norm(X[:,None]-X[None],axis=2)

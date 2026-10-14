"""v3: transition-context learning. The value of choosing j from i now also depends on the PREVIOUS city h (turning angle h->i->j), which neither the pheromone (per edge) nor eta (per edge) can express.
Signature of a transition = (rank of j, distance bin, mutual-neighbour flag, rank of i from j, centroid bin of j, turning-angle bin[8]) -> 6 glomeruli; learner = mushroom body (real/random wiring) or linear, as in v1/v2."""
import sys, os; HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,"..")); sys.path.insert(0,os.path.join(HERE,"..","v2"))
import numpy as np, tsp as T, fly_heuristic as H, mbcore as M, v2core as V
TURN_OFF=52                                            # glomeruli 52..59 (unused by v1's 52 odour glomeruli)
EDGES=[0.0,20.0,45.0,70.0,100.0,130.0,160.0]           # turning-angle bin edges in degrees (7 bins); bin 7 = "no previous city" (first step)
def turn_bins(X):
    """TB[h,i,j] = bin of the turning angle at i when going h->i->j; TB[n,i,j]=7 (start). Also cosine array for the hand-written control."""
    n=len(X); d=X[None,:,:]-X[:,None,:]; nr=np.linalg.norm(d,axis=2); nr[nr==0]=1; u=d/nr[:,:,None]          # u[a,b] = unit vector a->b
    cos=np.einsum('hik,ijk->hij',u,u); cos=np.clip(cos,-1,1); ang=np.degrees(np.arccos(cos)); idx=np.eye(n,dtype=bool)
    ang[idx[:,:,None].repeat(n,2)]=0; ang[np.broadcast_to(idx[None,:,:],(n,n,n))]=0                          # degenerate h==i or i==j: treat as straight
    tb=np.searchsorted(np.array(EDGES[1:]),ang,side='right').astype(np.int8)
    TB=np.empty((n+1,n,n),np.int8); TB[:n]=tb; TB[n]=7
    COS=np.ones((n+1,n,n)); COS[:n]=cos; return TB,COS
class Circuit3(V.Circuit):
    def start3(s,key_static,TB):
        """key_static: (n,n) v1 edge keys; TB: (n+1,n,n). Returns id array inv3 (n+1,n,n)."""
        n=key_static.shape[0]; tk=(key_static[None,:,:].astype(np.int64)*8+TB.astype(np.int64)); tk[n]=key_static.astype(np.int64)*8+7
        uk,inv=np.unique(tk.ravel(),return_inverse=True); st=uk//8; tb=uk%8; g=H.key_to_glom(st.copy()); G=np.stack([g[0],g[1],g[2],g[3],g[5],TURN_OFF+tb],1)
        s.G=G; s.U=len(uk)
        if s.kind=="linear": s.lw=np.zeros(M.NG)
        else:
            u=np.zeros((s.U,M.NG)); u[np.arange(s.U)[:,None],G]=1; psi=u@s.P+1e-6*s.rng.random((s.U,M.NK)); k=int(0.05*M.NK)
            s.codes=np.argpartition(-psi,k-1,axis=1)[:,:k]; s.b0=0.5*M.A_VEC[s.codes].sum(1); s.sc=np.maximum(0.5*M.C_VEC[s.codes].sum(1),1e-9); s.mb=M.MB(s.lr)
        return inv.reshape(tk.shape)
def construct_turn(Wb,E3,r,A):
    """Wb (n,n) = tau^a*eta^b ; E3 (n+1,n,n) = exp(kappa*V3). Weight of j from cur given prev = Wb[cur,j]*E3[prev,cur,j]. RNG use identical to v1 construct."""
    n=len(Wb); tours=np.zeros((A,n),int); cur=r.integers(n,size=A); prev=np.full(A,n); vis=np.zeros((A,n),bool); tours[:,0]=cur; ar=np.arange(A); vis[ar,cur]=True
    for k in range(1,n):
        p=np.where(vis,0.0,Wb[cur]*E3[prev,cur]); p=p/p.sum(1,keepdims=True); u=r.random(A)[:,None]; nxt=np.minimum((p.cumsum(1)<u).sum(1),n-1)
        bad=vis[ar,nxt]
        if bad.any(): nxt[bad]=np.argmax(~vis[bad],axis=1)
        tours[:,k]=nxt; vis[ar,nxt]=True; prev=cur; cur=nxt
    return tours
def run3(X,D,cfg,circ=None,hand_gamma=0.0,seed=0):
    """cfg: alpha,beta,rho,kappa,ants,iters. circ: Circuit3 (learned transition valence) or None. hand_gamma>0: fixed hand-written penalty exp(-gamma*(1-cos turning angle)) instead of a learner (no learning)."""
    r=np.random.default_rng(seed); n=len(D); A=cfg["ants"]; al,be,rho,ka=cfg["alpha"],cfg["beta"],cfg["rho"],cfg.get("kappa",0.0)
    eta=1.0/(D+np.eye(n)); eta[np.eye(n,dtype=bool)]=0; L0=T.tour_len(D,T.nn_tour(D)); tmax=1.0/(rho*L0); tmin=tmax/(2*n); tau=np.full((n,n),tmax); eb=eta**be
    TB,COS=turn_bins(X); inv3=None
    if circ is not None: inv3=circ.start3(H.edge_signatures(X,D),TB)
    best=np.inf
    for it in range(cfg["iters"]):
        if circ is not None: v=circ.valence_u(); E3=np.exp(ka*v[inv3])
        elif hand_gamma>0: E3=np.exp(-hand_gamma*(1-COS))
        else: E3=np.ones((n+1,n,n))
        tours=construct_turn((tau**al)*eb,E3,r,A); L=H.lens(D,tours); k=int(np.argmin(L)); best=min(best,float(L[k]))
        tau*=(1-rho); a=tours[k]; b=np.roll(a,-1); dep=1.0/L[k]; tau[a,b]+=dep; tau[b,a]+=dep; tau=np.clip(tau,tmin,tmax)
        if circ is not None and circ.learn:
            rt=np.tanh((L.mean()-L)/(0.5*L.std()+1e-9)); prev=np.concatenate([np.full((A,1),n),tours[:,:-2]],1); cur=tours[:,:-1]; nxt=tours[:,1:]
            ids=inv3[prev,cur,nxt].ravel(); adv=(rt[:,None]-v[inv3[prev,cur,nxt]]).ravel(); cnt=np.bincount(ids,minlength=circ.U); sm=np.bincount(ids,weights=adv,minlength=circ.U)
            for u in np.nonzero(cnt)[0]: circ.update_u(int(u),sm[u]/cnt[u])
    return best

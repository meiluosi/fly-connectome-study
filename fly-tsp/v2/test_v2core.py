import numpy as np, sys; sys.path.insert(0,'.')
import v2core as V, tsp as T, fly_heuristic as H, mbcore as M
X,D=T.make_instance(30,5); base=dict(alpha=1.0,beta=3.0,rho=0.1,ants=10,iters=8)
# 1. no circuits, S=1 == v1 aco_vec bit-for-bit
a=V.run(X,D,base,seed=3); b=H.aco_vec(D,n_ants=10,iters=8,alpha=1.0,beta=3.0,rho=0.1,seed=3)[0]; assert a==b,(a,b); print("1 ok: plain ACO identical to v1")
# 2. frozen untrained circuit with kappa: valence of a fresh MB is ~0 (cancels b0) -> same as plain ACO
c=V.make_flock("real",1,0.1,1,learn=False); a2=V.run(X,D,dict(base,kappa=3.0),c,seed=3); print("2 frozen untrained real:",a2,"vs plain",a)
# 3. valid tours and LS never worse in expectation; ls path runs
r=np.random.default_rng(0); W=np.ones((2,30,30)); t=V.construct_multi(D,W,np.arange(6)%2,r,6); assert all(sorted(x)==list(range(30)) for x in t); print("3 ok: tours are permutations")
l1=V.run(X,D,dict(base,ls=True),seed=3); print("   with 2-opt:",l1,"<= ~ plain",a)
# 4. learning sign: after online learning on a fixed instance, edges of the best tour should have higher valence than the average edge
circ=V.make_flock("real",1,0.3,1)
cfg=dict(base,kappa=2.0,iters=25,ants=20); 
res=[]
for kind,lr in (("real",0.3),("linear",1.0),("random",0.3)):
    c=V.make_flock(kind,1,lr,2); V.run(X,D,cfg,c,seed=1); v=c[0].valence_u(); inv=c[0].inv; Vm=v[inv]; opt=H.lens
    # best reference tour via 2-opt
    bt=T.two_opt(D,T.nn_tour(D)); e=Vm[bt,np.roll(bt,-1)].mean(); off=Vm[~np.eye(30,dtype=bool)].mean(); print("4",kind,"mean valence on good-tour edges %.3f vs all edges %.3f"%(e,off))
# 5. heterogeneous / islands / private run and F=1 broadcast==private
for name,cf,cs in (("het4 broadcast",dict(cfg,broadcast=True),V.make_flock("real",4,0.3,3,drop=0.3)),("het4 private",dict(cfg,broadcast=False),V.make_flock("real",4,0.3,3,drop=0.3)),("islands ex5",dict(base,islands=4,exch=5),[]),("islands none",dict(base,islands=4,exch=None),[])):
    print("5",name,V.run(X,D,cf,cs,seed=2))
a=V.run(X,D,dict(cfg,broadcast=True),V.make_flock("real",1,0.3,3),seed=2); b=V.run(X,D,dict(cfg,broadcast=False),V.make_flock("real",1,0.3,3),seed=2); assert a==b; print("5b ok: F=1 broadcast==private")
a=V.run(X,D,dict(base,islands=1,exch=5),seed=3); assert a==V.run(X,D,base,seed=3); print("5c ok: S=1 ignores exchange")
# 6. fast update equals mbcore.MB.update
c=V.make_flock("real",1,0.3,1)[0]; c.start(H.edge_signatures(X,D)); m=M.MB(0.3)
for u,dl in ((3,0.7),(5,-0.4),(3,-0.2),(9,0.9)): c.update_u(u,dl); m.update(c.codes[u],dl)
assert np.allclose(c.mb.q,m.q); print("6 ok: fast update == MB.update")

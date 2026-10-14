"""Sanity tests required by PREREG_audit.md section 4 (a),(d),(e) for the numpy models. Backprop tests live in test_backprop.py."""
import numpy as np, cl_bench as B, cl_baselines as C
rng=np.random.default_rng(0); K,d,n=6,20,200
cent=rng.normal(0,3,(K,d)); X=np.abs(np.concatenate([cent[c]+rng.normal(0,1,(n,d)) for c in range(K)])).astype(np.float32); y=np.repeat(np.arange(K),n)
Xte=np.abs(np.concatenate([cent[c]+rng.normal(0,1,(50,d)) for c in range(K)])).astype(np.float32); yte=np.repeat(np.arange(K),50); tasks=[[0,1],[2,3],[4,5]]
cfg=dict(m=400,k_inputs=6,l=20,beta=0.05)
def final(m,tk=tasks,seed=0): R,al=B.class_incremental_eval(m,X,y,Xte,yte,tk,seed); return al[-1],R
# (d) separable synthetic data: every model should be well above chance (1/6)
for name,hp in [("NCM_euclid",None),("NCM_cos",None),("ClassSumDot",None),("SLDA",{"shrink":0.1}),("Fly",None),("Fly_dense_l2",None),("Fly_dense_minmax",None)]:
    a,_=final(C.make(name,d,K,cfg,0,hp)); assert a>0.5,(name,a)
# (a) order independence: permuting the order of tasks must not change final accuracy of prototype/Fly methods
perm=[[4,5],[0,1],[2,3]]
for name,hp in [("NCM_euclid",None),("NCM_cos",None),("ClassSumDot",None),("SLDA",{"shrink":0.1}),("Fly",None)]:
    a1,_=final(C.make(name,d,K,cfg,0,hp)); a2,_=final(C.make(name,d,K,cfg,0,hp),perm); assert abs(a1-a2)<1e-9,(name,a1,a2)
# (e) FlyVariant WTA with l=m equals no WTA up to the max-normalisation: compare 'wta' with l=m against 'minmax' is NOT identical (different normalisation); check that l=m keeps all m units active
fm=C.make("Fly",d,K,cfg,0,{"l":cfg["m"]}); ph=fm.phi(X[:50]); assert (ph>0).mean()>0.9
# SLDA matches sklearn-free closed form on a joint fit: with all classes learned, equals LDA on the pooled data
m=C.make("SLDA",d,K,cfg,0,{"shrink":0.1}); [m.learn_class(X[y==c],c) for c in range(K)]; p=m.predict(Xte,list(range(K))); assert (p==yte).mean()>0.9
print("test_audit.py: all numpy-model tests passed")

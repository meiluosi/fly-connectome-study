import numpy as np, tsp as T, fly_heuristic as H
# 1. features: signatures are in range, glomerulus sets have 6 distinct entries within the 52 used glomeruli
X,D=T.make_instance(30,0); key=H.edge_signatures(X,D); assert key.shape==(30,30) and key.min()>=0
for k in np.unique(key)[:50]: g=H.key_to_glom(int(k)); assert len(set(g))==6 and max(g)<52
# 2. initial valence is zero for MB (q0=0.5) and linear; 'none' is zero
for kind in ("real","shuffled","random","linear","none"):
    tb=H.SigTable(kind,1); sig=tb.ids_for(key); assert np.allclose(tb.valence(sig),0,atol=1e-9),kind
# 3. construct returns valid permutations
r=np.random.default_rng(0); W=(1/(D+np.eye(30)))**3; tours=H.construct(D,W,r,10); assert all(sorted(t)==list(range(30)) for t in tours)
# 4. learning direction: after training, edges that are short/mutual-neighbour get higher valence than long edges (the tours that win use them)
tb=H.SigTable("real",2); insts=[T.make_instance(30,100+s) for s in range(15)]; H.train(tb,insts,iters=8,n_ants=20)
X,D=T.make_instance(30,999); sig=tb.ids_for(H.edge_signatures(X,D)); V=tb.valence(sig); nn=np.argsort(D+np.diag(np.full(30,9)),1)[:,0]; near=np.mean([V[i,nn[i]] for i in range(30)]); far=np.mean(V[np.triu_indices(30,5)])
print("mean valence of nearest-neighbour edges %.3f vs of typical long edges %.3f"%(near,far)); assert near>far
# 5. zero-shot: learned heuristic builds better tours than eta-only on held-out instances (small, sanity only)
def mean_best(tb,kappa,insts):
    res=[]
    for s,(X,D) in enumerate(insts):
        sig=tb.ids_for(H.edge_signatures(X,D)); V=tb.valence(sig); eta=1/(D+np.eye(len(D))); eta[np.eye(len(D),dtype=bool)]=0; W=(eta**3)*np.exp(kappa*V); res.append(H.lens(D,H.construct(D,W,np.random.default_rng(s),20)).min())
    return float(np.mean(res))
test=[T.make_instance(30,500+s) for s in range(15)]; a=mean_best(tb,2.0,test); b=mean_best(H.SigTable("none",0),2.0,test); print("zero-shot best-of-20 tour length: learned %.3f vs heuristic-only %.3f"%(a,b))
print("test_fly_heuristic.py passed (sanity checks only; no claim)")

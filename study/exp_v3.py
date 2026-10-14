import numpy as np, learn_v3 as L, sys, time
S=100; T=12; rng=np.random.default_rng(0)
def boot(d,n=4000):
    m=[d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]; return d.mean(),np.percentile(m,2.5),np.percentile(m,97.5)
res={}
t0=time.time()
for coding in ["random","pn"]:
    for cond in ["real","shuffled","none"]:
        res[(coding,cond)]=np.array([L.summ(L.run(cond,T,s,coding=coding)) for s in range(S)])
    print(coding,"done",round(time.time()-t0),"s",flush=True)
np.save("exp_v3_results.npy",{str(k):v for k,v in res.items()},allow_pickle=True)
for coding in ["random","pn"]:
    print(f"\n== coding={coding}, T={T}, {S} paired seeds (learned, forgetting)")
    for c in ["real","shuffled","none"]:
        v=res[(coding,c)]; print(f"  {c:9s} learned={v[:,0].mean():.3f} forgetting={v[:,1].mean():.3f}")
    for a,b in [("real","shuffled"),("none","real")]:
        for i,nm in [(0,"learned"),(1,"forgetting")]:
            m,lo,hi=boot(res[(coding,a)][:,i]-res[(coding,b)][:,i]); print(f"  paired {a}-{b} {nm:10s}: {m:+.4f} [{lo:+.4f},{hi:+.4f}]")

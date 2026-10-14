import numpy as np, bandits as B
K,T=8,2000
def mean_regret(make,kind,seeds=range(12),**kw): return float(np.mean([B.run(make,B.Env(K,T,kind,seed=s,**kw),seed=100+s)[0][-1] for s in seeds]))
rand=mean_regret(lambda k:B.Random(k),"stationary")
# 1. pairing: same env seed + same alg seed reproduces exactly; env realisation is shared across algorithms
e=B.Env(K,T,"switch",seed=3); a1,_=B.run(lambda k:B.UCB(k),e,5); a2,_=B.run(lambda k:B.UCB(k),B.Env(K,T,"switch",seed=3),5); assert np.array_equal(a1,a2)
# 2. stationary: every learner far better than random
for name,mk in [("eps",lambda k:B.EpsGreedy(k,0.05)),("ucb",lambda k:B.UCB(k)),("ts",lambda k:B.Thompson(k)),("aco",lambda k:B.ACOStyle(k))]:
    r=mean_regret(mk,"stationary"); assert r<0.35*rand,(name,r,rand)
# 3. known result (Garivier & Moulines 2011 and others): once each algorithm is TUNED on a small grid, forgetting variants beat their stationary versions under abrupt switches.
#    (Untuned c=1 forgetting variants over-explore because the effective sample size is small, so an unconditional assertion would be wrong.)
sd=range(8)
mr=lambda mk:float(np.mean([B.run(mk,B.Env(K,T,"switch",seed=s),seed=100+s)[0][-1] for s in sd]))
ucb=min(mr(lambda k,c=c:B.UCB(k,c=c)) for c in (0.1,0.5,1.0))
swu=min(mr(lambda k,c=c,w=w:B.UCB(k,c=c,window=w)) for c in (0.1,0.25) for w in (100,200))
du=min(mr(lambda k,c=c,g=g:B.UCB(k,c=c,gamma=g)) for c in (0.1,0.25) for g in (0.95,0.98))
ts=mr(lambda k:B.Thompson(k)); dts=min(mr(lambda k,g=g:B.Thompson(k,gamma=g)) for g in (0.95,0.99))
assert swu<ucb and du<ucb and dts<ts,(ucb,swu,du,ts,dts)
# 4. regret bookkeeping: oracle policy has zero regret; random has positive and ~linear
env=B.Env(K,T,"switch",seed=1)
class Oracle:
    def __init__(s,k): pass
    def select(s,t,rng): return int(np.argmax(env.p[t]))
    def update(s,a,r): pass
assert B.run(lambda k:Oracle(k),env,0)[0][-1]<1e-9
rr=B.run(lambda k:B.Random(k),env,0)[0]; assert rr[-1]>100 and abs(rr[T//2]*2-rr[-1])<0.2*rr[-1]
print("test_bandits.py passed | stationary random regret %.0f | switch (tuned): UCB %.0f, SW-UCB %.0f, D-UCB %.0f, TS %.0f, D-TS %.0f"%(rand,ucb,swu,du,ts,dts))

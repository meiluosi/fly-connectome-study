"""PREREG_audit.md section 4 tests (b),(c),(d) for the backprop baselines, on small synthetic data."""
import numpy as np, cl_backprop as P
rng=np.random.default_rng(1); K,d,n=6,12,150; cent=rng.normal(0,3,(K,d))
X=np.abs(np.concatenate([cent[c]+rng.normal(0,1,(n,d)) for c in range(K)])).astype(np.float32); y=np.repeat(np.arange(K),n)
Xte=np.abs(np.concatenate([cent[c]+rng.normal(0,1,(60,d)) for c in range(K)])).astype(np.float32); yte=np.repeat(np.arange(K),60); tasks=[[0,1],[2,3],[4,5]]
import os
DEV=os.environ.get('TEST_DEVICE','cpu')
run=lambda m,hp,ep=1,seed=0:P.run_backprop(m,X,y,Xte,yte,tasks,K,hp,seed,epochs=ep,mult=8,fisher_n=50,device=DEV)
# (b) EWC with lambda=0 is bit-identical to vanilla
Rv,av=run("v",dict(lr=1e-3)); Re,ae=run("e",dict(lr=1e-3,lam=0.0)); assert np.array_equal(np.nan_to_num(Rv),np.nan_to_num(Re)) and np.array_equal(av,ae)
# a positive-lambda EWC must differ from vanilla (not a no-op) 
Rl,al=run("e",dict(lr=1e-3,lam=1e4)); assert not np.array_equal(av,al), (av,al)
# vanilla in class-IL forgets: final accuracy close to 'last task only' (<= 1/3 + slack)
assert av[-1]<0.5, av
# (c) ER with buffer >= all data beats vanilla clearly and is close to offline
Rr,ar=run("er",dict(lr=1e-3,buffer=len(X)),ep=1); assert ar[-1]>av[-1]+0.2,(ar,av)
off=P.run_offline(X,y,Xte,yte,K,1e-3,5,0,mult=8); assert off[-1]>0.9 and ar[-1]>off[-1]-0.35,(ar[-1],off[-1])
# (d) all above chance at learning time on every task
for R in (Rv,Re,Rr): assert np.nanmin(np.diag(R))>0.5
# (f) interleaved stream: vanilla must learn the first task far better than with the class-ordered stream (which collapses within the task)
_,a_int=P.run_backprop("v",X,y,Xte,yte,tasks,K,dict(lr=1e-3),0,epochs=1,mult=8,fisher_n=50,device=DEV,interleave=True); assert a_int[0]>0.85 and a_int[0]>av[0]+0.15,(a_int,av)
print("test_backprop.py: all backprop-baseline tests passed (vanilla",np.round(av,2),"ewc1e4",np.round(al,2),"er",np.round(ar,2),")")

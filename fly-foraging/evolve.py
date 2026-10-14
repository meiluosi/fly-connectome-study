"""Outer loop: OpenAI-ES (antithetic, rank-shaped) over theta (5 numbers) to maximise mean net reward on TRAINING worlds of varying volatility. usage: evolve.py WIRING ES_SEED -> evo_WIRING_SEED.json"""
import sys, json, time, numpy as np, forage as F, forage2 as G
from multiprocessing import Pool
POP,SIGMA,LR,GENS,K=16,0.4,0.6,25,12; REVS=[1000,2000,3000]
def make_world(seed,rev,conflict): return F.World(seed,T=6000,rev=rev,conflict=conflict)
def worlds_for(gen,rng): return [(2000+gen*K+i,int(rng.choice(REVS)),bool(rng.random()<0.5)) for i in range(K)]
def evalcand(args):
    th,P,wl,fseed=args; prm=G.decode(th); return float(np.mean([G.run_fly2(make_world(s,rv,cf),prm,P,seed=fseed+s).sum() for s,rv,cf in wl]))
def wiring(kind,es_seed):
    rng=np.random.default_rng(10_000+es_seed); return F.make_P(kind,rng)
if __name__=="__main__":
    kind,es_seed=sys.argv[1],int(sys.argv[2]); P=wiring(kind,es_seed); rng=np.random.default_rng(es_seed); th=G.encode(G.DEFAULT); hist=[]; t0=time.time()
    with Pool(8) as pool:
        for gen in range(GENS):
            wl=worlds_for(gen,rng); eps=rng.normal(size=(POP//2,5)); E=np.concatenate([eps,-eps]); cands=[th+SIGMA*e for e in E]
            fit=np.array(pool.map(evalcand,[(c,P,wl,7000+gen) for c in cands])); center=evalcand((th,P,wl,7000+gen))
            ranks=np.argsort(np.argsort(fit)); shaped=(ranks/(POP-1)-0.5); grad=(shaped[:,None]*E).sum(0)/(POP*0.5); th=th+LR*SIGMA*grad*2
            hist.append(dict(gen=gen,mean_fit=float(fit.mean()),best=float(fit.max()),center=center,theta=th.tolist(),prm=G.decode(th))); print(f"{kind} es{es_seed} gen {gen:2d} pop mean {fit.mean():+6.1f} best {fit.max():+6.1f} center {center:+6.1f} | {round(time.time()-t0)}s",flush=True)
    json.dump(dict(kind=kind,es_seed=es_seed,final_theta=th.tolist(),final_prm=G.decode(th),hist=hist),open(f"evo_{kind}_{es_seed}.json","w")); print("done")

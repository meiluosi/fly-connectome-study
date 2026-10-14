"""Re-run of the meta-learning evolution with the decay parameter's initial theta moved from the flat tail (-6) to the sigmoid centre (0). Everything else is evolve.py unchanged.
usage: evolve_b.py WIRING ES_SEED -> evo2_WIRING_SEED.json (in this folder)"""
import sys, os, json, time, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); PARENT=os.path.dirname(HERE); sys.path.insert(0,PARENT); os.chdir(PARENT)
import forage as F, forage2 as G, evolve as E
from multiprocessing import Pool
if __name__=="__main__":
    kind,es_seed=sys.argv[1],int(sys.argv[2]); P=E.wiring(kind,es_seed); rng=np.random.default_rng(es_seed); th=G.encode(G.DEFAULT); th[2]=0.0; hist=[]; t0=time.time()
    POP,SIGMA,LR,GENS,K=E.POP,E.SIGMA,E.LR,E.GENS,E.K
    with Pool(8) as pool:
        for gen in range(GENS):
            wl=E.worlds_for(gen,rng); eps=rng.normal(size=(POP//2,5)); Ee=np.concatenate([eps,-eps]); cands=[th+SIGMA*e for e in Ee]
            fit=np.array(pool.map(E.evalcand,[(c,P,wl,7000+gen) for c in cands])); center=E.evalcand((th,P,wl,7000+gen))
            ranks=np.argsort(np.argsort(fit)); shaped=(ranks/(POP-1)-0.5); grad=(shaped[:,None]*Ee).sum(0)/(POP*0.5); th=th+LR*SIGMA*grad*2
            hist.append(dict(gen=gen,mean_fit=float(fit.mean()),best=float(fit.max()),center=center,theta=th.tolist(),prm=G.decode(th))); print(f"{kind} es{es_seed} gen {gen:2d} pop mean {fit.mean():+6.1f} best {fit.max():+6.1f} center {center:+6.1f} decay {G.decode(th)['decay']:.2e} | {round(time.time()-t0)}s",flush=True)
    json.dump(dict(kind=kind,es_seed=es_seed,final_theta=th.tolist(),final_prm=G.decode(th),hist=hist),open(os.path.join(HERE,f"evo2_{kind}_{es_seed}.json"),"w")); print("done")

"""Held-out evaluation (worlds 5000-5099) of default vs evolved parameters, per (wiring, ES seed), three volatility conditions."""
import json, numpy as np, forage as F, forage2 as G, evolve as E
from multiprocessing import Pool
_cache={}
def getP(kind,es):
    if (kind,es) not in _cache: _cache[(kind,es)]=E.wiring(kind,es)
    return _cache[(kind,es)]
def world_for(cond,s):
    if cond=="indist": return F.World(s,T=6000,rev=[1000,2000,3000][s%3],conflict=(s%2==1))
    if cond=="fast": return F.World(s,T=6000,rev=500,conflict=(s%2==1))
    return F.World(s,T=6000,rev=6000,conflict=(s%2==1))
def job(a):
    kind,es,which,prm,cond,s=a; return (kind,es,which,cond,s,float(G.run_fly2(world_for(cond,s),prm,getP(kind,es),seed=9000+s).sum()))
if __name__=="__main__":
    tasks=[]; evo={}
    for kind in ("real","shuffled","random"):
        for es in (0,1,2):
            d=json.load(open(f"evo_{kind}_{es}.json")); evo[(kind,es)]=d["final_prm"]
            for which,prm in (("default",G.DEFAULT),("evolved",d["final_prm"])):
                for cond in ("indist","fast","stationary"): tasks+=[(kind,es,which,prm,cond,s) for s in range(5000,5100)]
    out={}
    with Pool(8) as p:
        for r in p.imap_unordered(job,tasks,chunksize=20): out.setdefault(f"{r[0]}|{r[1]}|{r[2]}|{r[3]}",{})[r[4]]=r[5]
    out={k:[v[s] for s in sorted(v)] for k,v in out.items()}; json.dump(dict(results=out,params={f"{k[0]}|{k[1]}":v for k,v in evo.items()}),open("eval_meta.json","w")); print("saved",len(out))

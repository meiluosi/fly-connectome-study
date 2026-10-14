import sys, os, json, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); PARENT=os.path.dirname(HERE); sys.path.insert(0,PARENT); os.chdir(PARENT)
import forage as F, forage2 as G, evolve as E
from multiprocessing import Pool
def world_for(cond,s):
    if cond=="indist": return F.World(s,T=6000,rev=[1000,2000,3000][s%3],conflict=(s%2==1))
    if cond=="fast": return F.World(s,T=6000,rev=500,conflict=(s%2==1))
    return F.World(s,T=6000,rev=6000,conflict=(s%2==1))
_c={}
def getP(kind,es):
    if (kind,es) not in _c: _c[(kind,es)]=E.wiring(kind,es)
    return _c[(kind,es)]
def job(a):
    kind,es,which,prm,cond,s=a; return (kind,es,which,cond,s,float(G.run_fly2(world_for(cond,s),prm,getP(kind,es),seed=9000+s).sum()))
if __name__=="__main__":
    tasks=[]; params={}
    for kind in ("real","shuffled","random"):
        for es in (0,1,2):
            e1=json.load(open(os.path.join(PARENT,f"evo_{kind}_{es}.json")))["final_prm"]; e2=json.load(open(os.path.join(HERE,f"evo2_{kind}_{es}.json")))["final_prm"]; params[f"{kind}|{es}"]=dict(evo1=e1,evo2=e2)
            for which,prm in (("default",G.DEFAULT),("evo1",e1),("evo2",e2)):
                for cond in ("indist","fast","stationary"): tasks+=[(kind,es,which,prm,cond,s) for s in range(6100,6200)]
    out={}
    with Pool(8) as p:
        for r in p.imap_unordered(job,tasks,chunksize=20): out.setdefault(f"{r[0]}|{r[1]}|{r[2]}|{r[3]}",{})[r[4]]=r[5]
    out={k:[v[s] for s in sorted(v)] for k,v in out.items()}; json.dump(dict(results=out,params=params),open(os.path.join(HERE,"eval_meta2.json"),"w")); print("saved",len(out))

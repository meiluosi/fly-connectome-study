import sys, os, json, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); PARENT=os.path.dirname(HERE); RES=os.path.join(HERE,'results'); sys.path.insert(0,PARENT); os.chdir(PARENT)   # forage.py loads data/mb_circuit.npz relative to its own folder
import forage as F, forage2 as G
from multiprocessing import Pool
D=G.DEFAULT
def world_for(cond,s):
    if cond=="indist": return F.World(s,T=6000,rev=[1000,2000,3000][s%3],conflict=(s%2==1))
    if cond=="fast": return F.World(s,T=6000,rev=500,conflict=(s%2==1))
    return F.World(s,T=6000,rev=6000,conflict=(s%2==1))
def configs():
    c={}
    for d in (0,1e-4,1e-3,3e-3,1e-2,3e-2): c[f"decay={d:g}"]=dict(D,decay=d)
    for sc in (0.25,0.5,2,4): c[f"lrx{sc:g}"]=dict(D,eta_pos=0.4*sc,eta_neg=0.4*sc)
    for p,n in ((0.4,0.8),(0.8,0.4),(0.4,1.6)): c[f"asym({p:g},{n:g})"]=dict(D,eta_pos=p,eta_neg=n)
    for es in (0,1,2):
        ev=json.load(open(os.path.join(PARENT,f"evo_real_{es}.json")))["final_prm"]
        c[f"evo{es}"]=ev
        for d in (1e-3,1e-2): c[f"evo{es}+decay={d:g}"]=dict(ev,decay=d)
    return c
def job(a):
    name,cond,s=a; f=os.path.join(RES,f"{name}__{cond}__{s}.json")
    if os.path.exists(f): return a
    r=float(G.run_fly2(world_for(cond,s),CFG[name],F.P0,seed=9000+s).sum()); os.makedirs(RES,exist_ok=True); json.dump(r,open(f+".tmp","w")); os.replace(f+".tmp",f); return a
CFG=configs()
if __name__=="__main__":
    jobs=[(n,c,s) for n in CFG for c in ("fast","indist","stationary") for s in range(6000,6100)]
    with Pool(10) as p:
        for k,_ in enumerate(p.imap_unordered(job,jobs,chunksize=10)):
            if k%500==0: print(k,"/",len(jobs),flush=True)
    print("done")

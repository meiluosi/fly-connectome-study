"""stage 6d runner: run_v4h3.py tune | eval ; results_h3/"""
import sys, os, json, time, itertools, numpy as np; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import forage_comp_b as FC
F=FC.F; HERE=os.path.dirname(os.path.abspath(__file__))
T,REV=6000,3000
ARMS=["global","comp_real","comp_shuf","comp_shufbal","no_learning"]; CONDS=(("consistent",False),("conflict",True))
GRID=[dict(eta=e,g_learn=g,k_turn=1.4) for e in (0.4,0.8,2.0,4.0) for g in (1.0,2.0,3.0,6.0,10.0)]; TUNE=range(20,40); TEST=range(800,1000)
def one(cond,arm,prm,s):
    conflict=dict(CONDS)[cond]; w=F.World(s,T=T,rev=REV,conflict=conflict); sd=5000+s
    if arm=="no_learning": return float(F.run_fly(w,F.NoLearning(),None,seed=sd,k_turn=1.4)[0].sum())
    L=FC.make(arm,prm["eta"],s); return float(F.run_fly(w,L,F.P0,seed=sd,g_learn=prm["g_learn"],k_turn=prm["k_turn"])[0].sum())
def tune_job(a):
    cond,arm,i=a; return a,float(np.mean([one(cond,arm,GRID[i],s) for s in TUNE]))
def eval_job(a):
    cond,arm,prm,s=a; f=os.path.join(HERE,"results_h3",f"{cond}__{arm}__{s}.json")
    if not os.path.exists(f): os.makedirs(os.path.dirname(f),exist_ok=True); json.dump({"net":one(cond,arm,prm,s)},open(f,"w"))
    return a
if __name__=="__main__":
    t0=time.time()
    if sys.argv[1]=="tune":
        jobs=[(c,a,i) for c,_ in CONDS for a in ARMS[:-1] for i in range(len(GRID))]
        with Pool(10) as p: res=dict(p.imap_unordered(tune_job,jobs,chunksize=1))
        best={}
        for c,_ in CONDS:
            for a in ARMS[:-1]: i=max(range(len(GRID)),key=lambda j:res[(c,a,j)]); best[f"{c}|{a}"]=dict(prm=GRID[i],score=res[(c,a,i)],all=[res[(c,a,j)] for j in range(len(GRID))])
        json.dump(best,open(os.path.join(HERE,"tuning_v4h3.json"),"w"),indent=1); print("tuned",round(time.time()-t0),"s")
        for k,v in best.items(): print(k,v["prm"],round(v["score"],1))
    else:
        B=json.load(open(os.path.join(HERE,"tuning_v4h3.json"))); jobs=[]
        for c,_ in CONDS:
            for a in ARMS:
                prm=None if a=="no_learning" else B[f"{c}|{a}"]["prm"]
                for s in TEST: jobs.append((c,a,prm,s))
        with Pool(10) as p:
            for i,_ in enumerate(p.imap_unordered(eval_job,jobs,chunksize=2)):
                if i%200==0: print(i,"/",len(jobs),round(time.time()-t0),"s",flush=True)
        print("done",round(time.time()-t0),"s")

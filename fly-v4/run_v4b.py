"""tune and eval for stage 0b. usage: run_v4b.py tune | eval ; results in results_b/"""
import sys, os, json, time, numpy as np; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import v4core_b as B
HERE=os.path.dirname(os.path.abspath(__file__))
TASKS=["teacher_pert","teacher_shuf","teacher_real","teacher_random","linear_teacher","door_class","door_teacher_real"]
KINDS=["real","shuffled","random","real_binary","real_wshuf","linear"]
GRID_MB=(0.02,0.05,0.15,0.4,1.0); GRID_LIN=(0.1,0.3,1.0,3.0); TUNE=range(1000,1020); TEST=range(5000,5100)
def tune_job(a):
    t,k,e=a; return a,float(np.mean([B.run(t,s,k,e)["auc"] for s in TUNE]))
def eval_job(a):
    t,k,e,s=a; f=os.path.join(HERE,"results_b",f"{t}__{k}__{s}.json")
    if os.path.exists(f): return a
    r=B.run(t,s,k,e); r["curve"]=[round(float(x),4) for x in r["curve"]]; os.makedirs(os.path.dirname(f),exist_ok=True); json.dump(r,open(f+".tmp","w")); os.replace(f+".tmp",f); return a
if __name__=="__main__":
    mode=sys.argv[1]; t0=time.time()
    if mode=="tune":
        jobs=[(t,k,e) for t in TASKS for k in KINDS for e in (GRID_LIN if k=="linear" else GRID_MB)]
        with Pool(10) as p: res=dict(p.imap_unordered(tune_job,jobs,chunksize=2))
        best={}
        for t in TASKS:
            for k in KINDS:
                g=GRID_LIN if k=="linear" else GRID_MB; e=max(g,key=lambda x:res[(t,k,x)]); best[f"{t}|{k}"]=dict(eta=e,auc=res[(t,k,e)],grid={str(x):res[(t,k,x)] for x in g})
        json.dump(best,open(os.path.join(HERE,"tuning_v4b.json"),"w"),indent=1); print("tuned",round(time.time()-t0),"s")
        for k,v in best.items(): print(k,v["eta"],round(v["auc"],3))
    else:
        T=json.load(open(os.path.join(HERE,"tuning_v4b.json"))); jobs=[(t,k,T[f"{t}|{k}"]["eta"],s) for t in TASKS for k in KINDS for s in TEST]
        with Pool(10) as p:
            for i,_ in enumerate(p.imap_unordered(eval_job,jobs,chunksize=4)):
                if i%500==0: print(i,"/",len(jobs),round(time.time()-t0),"s",flush=True)
        print("done",round(time.time()-t0),"s")

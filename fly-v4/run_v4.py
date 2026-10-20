"""tune and eval for stage 0. usage: run_v4.py tune | eval | analyse ; per-key resumable result files."""
import sys, os, json, time, itertools, numpy as np; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import v4core as V
HERE=os.path.dirname(os.path.abspath(__file__))
TASKS=["teacher_real","teacher_random","linear_teacher","family","door_class","door_teacher_real"]
MB=["real","shuffled","random","real_binary","real_wshuf"]; AD=["real+ad","shuffled+ad","random+ad"]; KINDS=MB+["linear"]+AD
GRID_MB=(0.05,0.15,0.4,1.0); GRID_LIN=(0.1,0.3,1.0,3.0); TUNE=range(1000,1020); TEST=range(5000,5100)
def tune_job(a):
    task,kind,eta=a; return a,float(np.mean([V.run(task,s,kind,eta)["auc"] for s in TUNE]))
def eval_job(a):
    task,kind,eta,seed=a; f=os.path.join(HERE,"results",f"{task}__{kind}__{seed}.json")
    if os.path.exists(f): return a
    r=V.run(task,seed,kind,eta); r["curve"]=[round(float(x),4) for x in r["curve"]]; os.makedirs(os.path.dirname(f),exist_ok=True); json.dump(r,open(f+".tmp","w")); os.replace(f+".tmp",f); return a
if __name__=="__main__":
    mode=sys.argv[1]; t0=time.time()
    if mode=="tune":
        jobs=[(t,k,e) for t in TASKS for k in MB+["linear"] for e in (GRID_LIN if k=="linear" else GRID_MB)]
        with Pool(10) as p: res=dict((a,v) for a,v in p.imap_unordered(tune_job,jobs,chunksize=2))
        best={}
        for t in TASKS:
            for k in MB+["linear"]:
                g=GRID_LIN if k=="linear" else GRID_MB; e=max(g,key=lambda x:res[(t,k,x)]); best[f"{t}|{k}"]=dict(eta=e,auc=res[(t,k,e)],grid={str(x):res[(t,k,x)] for x in g})
        json.dump(best,open(os.path.join(HERE,"tuning_v4.json"),"w"),indent=1); print("tuned",round(time.time()-t0),"s")
        for k,v in best.items(): print(k,v["eta"],round(v["auc"],3))
    elif mode=="eval":
        B=json.load(open(os.path.join(HERE,"tuning_v4.json")))
        eta=lambda t,k: B[f"{t}|{k[:-3] if k.endswith('+ad') else k}"]["eta"]
        jobs=[(t,k,eta(t,k),s) for t in TASKS for k in KINDS for s in TEST]
        with Pool(10) as p:
            for i,_ in enumerate(p.imap_unordered(eval_job,jobs,chunksize=4)):
                if i%500==0: print(i,"/",len(jobs),round(time.time()-t0),"s",flush=True)
        print("done",round(time.time()-t0),"s")

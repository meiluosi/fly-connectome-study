"""stage 5 runner: results_f/{task}__{kind}__{seed}.json"""
import sys, os, json, time; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import v4core_f as F
HERE=os.path.dirname(os.path.abspath(__file__)); TASKS=["door_class","door_teacher_real"]; KINDS=["real","shuffled","random"]; TEST=range(5000,5100)
def job(a):
    t,k,s=a; f=os.path.join(HERE,"results_f",f"{t}__{k}__{s}.json")
    if not os.path.exists(f): r=F.run(t,s,k); os.makedirs(os.path.dirname(f),exist_ok=True); json.dump(r,open(f+".tmp","w")); os.replace(f+".tmp",f)
    return a
if __name__=="__main__":
    t0=time.time()
    with Pool(10) as p: list(p.imap_unordered(job,[(t,k,s) for t in TASKS for k in KINDS for s in TEST],chunksize=2))
    print("done",round(time.time()-t0),"s")

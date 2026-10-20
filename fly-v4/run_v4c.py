"""stage 0c runner: results_c/{task}__{kind}__{eta_p}__{seed}.json"""
import sys, os, json, time; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import v4core_c as C
HERE=os.path.dirname(os.path.abspath(__file__)); T=json.load(open(os.path.join(HERE,"tuning_v4b.json")))
TASKS=["door_class","door_teacher_real","teacher_pert"]; KINDS=["real","shuffled","random"]; EP=(0.0,0.003,0.01,0.03); TEST=range(5000,5100)
def job(a):
    t,k,ep,s=a; f=os.path.join(HERE,"results_c",f"{t}__{k}__{ep}__{s}.json")
    if not os.path.exists(f): r=C.run_ad(t,s,k,T[f"{t}|{k}"]["eta"],ep); os.makedirs(os.path.dirname(f),exist_ok=True); json.dump(r,open(f+".tmp","w")); os.replace(f+".tmp",f)
    return a
if __name__=="__main__":
    t0=time.time()
    with Pool(10) as p: list(p.imap_unordered(job,[(t,k,e,s) for t in TASKS for k in KINDS for e in EP for s in TEST],chunksize=4))
    print("done",round(time.time()-t0),"s")

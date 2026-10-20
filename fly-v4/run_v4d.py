"""stage 3 runner: results_d/{task}__{kind}__{eta}__{seed}.json"""
import sys, os, json, time; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import v4core_d as D
HERE=os.path.dirname(os.path.abspath(__file__))
TASKS=["teacher_M_R","teacher_F_R","teacher_M_L","teacher_F_L","door_class"]; KINDS=["M_R","M_L","F_R","F_L","shuf_M_R","shuf_F_R","marg_M_R","marg_F_R","random"]; ETAS=(0.05,0.15); TEST=range(5000,5100)
def job(a):
    t,k,e,s=a; f=os.path.join(HERE,"results_d",f"{t}__{k}__{e}__{s}.json")
    if not os.path.exists(f): r=D.run(t,s,k,e); os.makedirs(os.path.dirname(f),exist_ok=True); json.dump(r,open(f+".tmp","w")); os.replace(f+".tmp",f)
    return a
if __name__=="__main__":
    t0=time.time()
    with Pool(10) as p: list(p.imap_unordered(job,[(t,k,e,s) for t in TASKS for k in KINDS for e in ETAS for s in TEST],chunksize=4))
    print("done",round(time.time()-t0),"s")

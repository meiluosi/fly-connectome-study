"""stage 3b runner: results_d2/{task}__{kind}__{eta}__{seed}.json"""
import sys, os, json, time; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import v4core_d2 as D
HERE=os.path.dirname(os.path.abspath(__file__))
TASKS=["teacher_H_R","teacher_M_R","teacher_F_R","door_class"]; KINDS=["M_R","M_L","F_R","F_L","H_R","shuf_H_R","marg_M_R","marg_F_R","marg_H_R","random"]; ETAS=(0.05,); TEST=range(5000,5100)
def job(a):
    t,k,e,s=a; f=os.path.join(HERE,"results_d2",f"{t}__{k}__{e}__{s}.json")
    if not os.path.exists(f): r=D.run(t,s,k,e); os.makedirs(os.path.dirname(f),exist_ok=True); json.dump(r,open(f+".tmp","w")); os.replace(f+".tmp",f)
    return a
if __name__=="__main__":
    t0=time.time()
    with Pool(10) as p: list(p.imap_unordered(job,[(t,k,e,s) for t in TASKS for k in KINDS for e in ETAS for s in TEST],chunksize=4))
    print("done",round(time.time()-t0),"s")

"""stage 7 runner: results_i/{kind}__{seed}.json"""
import sys, os, json, time; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import v4core_i as I
HERE=os.path.dirname(os.path.abspath(__file__)); KINDS=["real","shuffled","random","real_binary","real_wshuf","raw"]; TEST=range(5000,5100)
def job(a):
    k,s=a; f=os.path.join(HERE,"results_i",f"{k}__{s}.json")
    if not os.path.exists(f): r=I.world(s,k); os.makedirs(os.path.dirname(f),exist_ok=True); json.dump(r,open(f,"w"))
    return a
if __name__=="__main__":
    t0=time.time()
    with Pool(10) as p: list(p.imap_unordered(job,[(k,s) for k in KINDS for s in TEST],chunksize=2))
    print("done",round(time.time()-t0),"s")

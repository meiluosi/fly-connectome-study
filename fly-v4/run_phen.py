"""stage 2 runner: run_phen.py eval ; results_phen/{kind}__{seed}.json"""
import sys, os, json, time; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import phenomena as Ph
HERE=os.path.dirname(os.path.abspath(__file__)); KINDS=["real","shuffled","random","real_binary","real_wshuf"]; TEST=range(5000,5100)
def job(a):
    k,s=a; f=os.path.join(HERE,"results_phen",f"{k}__{s}.json")
    if not os.path.exists(f): r=Ph.world(k,s); os.makedirs(os.path.dirname(f),exist_ok=True); json.dump(r,open(f+".tmp","w")); os.replace(f+".tmp",f)
    return a
if __name__=="__main__":
    t0=time.time()
    with Pool(10) as p: list(p.imap_unordered(job,[(k,s) for k in KINDS for s in TEST],chunksize=2))
    print("done",round(time.time()-t0),"s")

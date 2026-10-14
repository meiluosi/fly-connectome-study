"""Formal v3 evaluation on fresh TEST instances (R1 9000-9299, R2 9300-9599, R3 9600-9899), resumable per-key results. Parameters from tuning_v3.json (and v2 final for ACO / ON-*)."""
import sys, os, json, time, numpy as np; sys.path.insert(0,'.')
from multiprocessing import Pool
import arms3 as A
TUN3=json.load(open("tuning_v3.json"))
def params(reg): return dict(turn={k:tuple(TUN3[reg]["TURN-"+k]["best"]) for k in ("real","random","linear")},gamma=float(TUN3[reg]["HAND-turn"]["best"]))
def job(a):
    arm,reg,rep,c=a; f=f"results/{reg}/{arm}__r{rep}__c{c}.json"
    if os.path.exists(f): return a
    ins=A.test_insts(reg)[c*A.CH:(c+1)*A.CH]; L=A.run_arm(arm,reg,params(reg),ins,[rep],seed0=c*A.CH)[:,0]; os.makedirs(f"results/{reg}",exist_ok=True); json.dump(L.tolist(),open(f+".tmp","w")); os.replace(f+".tmp",f); return a
if __name__=="__main__":
    t0=time.time()
    for reg in A.REGS: A.ref_for(reg,"test",A.test_insts(reg)); print(reg,"refs ready",round(time.time()-t0),"s",flush=True)
    jobs=[(arm,reg,rep,c) for reg in A.REGS for arm in A.ARMS for rep in range(A.NREP) for c in range(A.NTEST//A.CH)]
    jobs.sort(key=lambda j:-((j[1]=="R2")*2+j[0].startswith("TURN")))
    with Pool(10) as p:
        for k,a in enumerate(p.imap_unordered(job,jobs)):
            if k%100==0: print(k,"/",len(jobs),round(time.time()-t0),"s",flush=True)
    print("done",round(time.time()-t0),"s")

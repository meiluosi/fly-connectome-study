"""Formal v2 evaluation on TEST instances (seeds 7000-8049), per-key resumable result files in results/. Parameters come from tuning_v2_final.json (frozen & hashed in PREREG_v2)."""
import sys, os, json, time, numpy as np; sys.path.insert(0,'.')
from multiprocessing import Pool
import arms as A
TUN=json.load(open("tuning_v2_final.json")); CH=10
def params(reg): t=TUN[reg]; return dict(aco=tuple(t["aco"]["best"]),on={k:tuple(v["best"]) for k,v in t["on"].items()})
def job(a):
    arm,reg,rep,c=a; f=f"results/{reg}/{arm}__r{rep}__c{c}.json"
    if os.path.exists(f): return a
    ins=A.test_insts(reg)[c*CH:(c+1)*CH]; L=A.run_arm(arm,reg,params(reg),ins,[rep])[:,0]; os.makedirs(f"results/{reg}",exist_ok=True); json.dump(L.tolist(),open(f+".tmp","w")); os.replace(f+".tmp",f); return a
if __name__=="__main__":
    t0=time.time(); regs=sys.argv[1:] or list(A.REG)
    for reg in regs: ins=A.test_insts(reg); A.ref_for(reg,"test",ins); print(reg,"refs ready",round(time.time()-t0),"s",flush=True)
    cfgs=sorted({(A.v1_cfg(reg)+(7+rep,)) for reg in regs for rep in range(A.NREP)})
    with Pool(len(cfgs)) as p: p.starmap(A.pretrain,cfgs)       # pretrain (cached) the frozen/pretrained learners' states
    print("pretrained",round(time.time()-t0),"s",flush=True)
    jobs=[]
    for reg in regs:
        nc=A.REG[reg]["ntest"]//CH
        for arm in (A.ARMS_R4 if reg=="R4" else A.ARMS):
            for rep in range(A.NREP):
                for c in range(nc): jobs.append((arm,reg,rep,c))
    jobs.sort(key=lambda j:-(j[0].startswith("HET4")*4+(j[1]=="R2")*2))   # heavy first
    with Pool(10) as p:
        for k,a in enumerate(p.imap_unordered(job,jobs)):
            if k%100==0: print(k,"/",len(jobs),round(time.time()-t0),"s",flush=True)
    print("done",round(time.time()-t0),"s")

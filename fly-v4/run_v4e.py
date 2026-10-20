"""stage 4 runner: run_v4e.py tune | eval | phen ; results_e/"""
import sys, os, json, time, numpy as np; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import v4core_e as E, v4core as V
HERE=os.path.dirname(os.path.abspath(__file__))
TASKS=["door_class","door_teacher_real","linear_teacher","teacher_real"]; ARMS=["global","comp_real","comp_shuf","comp_shufbal","unsigned"]
GRID=(0.005,0.01,0.02,0.05,0.15,0.4,1.0); TUNE=range(1000,1020); TEST=range(5000,5100)
def tune_job(a):
    t,k,e=a
    if t=="cl": r=[E.run_cl(s,k,e) for s in TUNE]; return a,{m:float(np.mean([x[m] for x in r])) for m in("final","after","forgetting")}
    return a,{"auc":float(np.mean([E.run(t,s,k,e)["auc"] for s in TUNE]))}
def eval_job(a):
    t,k,e,s,tag=a; f=os.path.join(HERE,"results_e",f"{t}__{tag}__{s}.json")
    if not os.path.exists(f):
        r=E.run_cl(s,k,e) if t=="cl" else E.run(t,s,k,e); os.makedirs(os.path.dirname(f),exist_ok=True); json.dump(r,open(f+".tmp","w")); os.replace(f+".tmp",f)
    return a
ISIS=(-8.0,-6.0,-3.0,-1.5,-0.5,0.5,1.5,3.0,4.0,8.0)
def phen_job(a):
    arm,variant,s=a; f=os.path.join(HERE,"results_e","phen",f"{arm}__{variant}__{s}.json")
    if os.path.exists(f): return a
    out={}
    for R in (1.0,-1.0):
        for isi in ISIS:
            rng=np.random.default_rng(s); u=V.synth_odours(rng,1); c=V.codes_for(u,V.P0,rng)[0]
            kw=dict(ablate=variant if variant in("PAM","PPL") else None,timing=(variant!="notiming"))
            out[f"{R}|{isi}"]=E.pairing(arm,np.random.default_rng(s+7),c,R,isi,**kw)
    os.makedirs(os.path.dirname(f),exist_ok=True); json.dump(out,open(f,"w")); return a
if __name__=="__main__":
    mode=sys.argv[1]; t0=time.time()
    if mode=="tune":
        jobs=[(t,k,e) for t in TASKS+["cl"] for k in ARMS for e in GRID]
        with Pool(10) as p: res=dict(p.imap_unordered(tune_job,jobs,chunksize=2))
        best={}
        for t in TASKS+["cl"]:
            key="final" if t=="cl" else "auc"
            for k in ARMS:
                e=max(GRID,key=lambda x:res[(t,k,x)][key]); best[f"{t}|{k}"]=dict(eta=e,**res[(t,k,e)],grid={str(x):res[(t,k,x)] for x in GRID})
        tgt=best["cl|comp_real"]["after"]; em=min(GRID,key=lambda x:abs(res[("cl","global",x)]["after"]-tgt)); best["cl|global_matched"]=dict(eta=em,target_after=tgt,**res[("cl","global",em)])
        json.dump(best,open(os.path.join(HERE,"tuning_v4e.json"),"w"),indent=1); print("tuned",round(time.time()-t0),"s")
        for k,v in best.items(): print(k,v["eta"],{m:round(v[m],3) for m in v if m in("auc","final","after","forgetting")})
    elif mode=="eval":
        T=json.load(open(os.path.join(HERE,"tuning_v4e.json"))); jobs=[]
        for t in TASKS:
            for k in ARMS:
                for s in TEST: jobs.append((t,k,T[f"{t}|{k}"]["eta"],s,k))
        for k in ARMS:
            for s in TEST: jobs.append(("cl",k,T[f"cl|{k}"]["eta"],s,k))
        for s in TEST: jobs.append(("cl","global",T["cl|global_matched"]["eta"],s,"global_matched"))
        for k in ("global","comp_real"):                       # frontier over the whole grid (descriptive)
            for e in GRID:
                for s in TEST: jobs.append(("cl",k,e,s,f"front_{k}_{e}"))
        with Pool(10) as p:
            for i,_ in enumerate(p.imap_unordered(eval_job,jobs,chunksize=4)):
                if i%500==0: print(i,"/",len(jobs),round(time.time()-t0),"s",flush=True)
        print("done",round(time.time()-t0),"s")
    else:
        jobs=[(arm,v,s) for arm in("comp_real","comp_shuf","comp_shufbal") for v in("intact","PAM","PPL","notiming") for s in TEST]
        with Pool(10) as p: list(p.imap_unordered(phen_job,jobs,chunksize=4))
        print("done",round(time.time()-t0),"s")

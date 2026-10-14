"""Round-2 B: proper EWC (exact diagonal Gaussian Fisher), real multi-head, delta lr grid, fly eta grid. usage: round2_B.py MR|FR"""
import sys, json, time, numpy as np, core, core4, core_fw2
circ=sys.argv[1]; c=core.build("R") if circ=="MR" else core_fw2.build("right"); s=core4.signs(c); M=core4.metrics
def run_delta2(probe,tasks,lr=0.5,lam=0.0,reps=3):
    w=np.zeros(c.NK); b=0.0; wstar=w.copy(); F=np.zeros(c.NK); learned=[]; f=lambda X:X@w+b
    for O,C,y in tasks:
        for _ in range(reps):
            for x in O:
                err=w@x+b-y; step=lr/(x@x+1.0); w-=step*err*x
                if lam>0: w-=np.minimum(1.0,step*lam*F)*(w-wstar)
                b-=step*err
        F+=np.mean(O**2,axis=0); wstar=w.copy(); learned.append(M(f(probe),f(O),y))
    final=[M(f(probe),f(O),y) for O,C,y in tasks]; return np.array(learned),np.array(final)
def run_mh2(probe,tasks,lr=0.5,reps=3):
    W=np.zeros((c.NC,c.NK)); learned=[]; fC=lambda X,C:(X@W[C].T).mean(1)
    for O,C,y in tasks:
        for _ in range(reps):
            for x in O:
                err=fC(x[None],C)[0]-y; step=lr/((x@x+1.0)); W[C]-=step*err*x[None]/len(C)
        learned.append(M(fC(probe,C),fC(O,C),y))
    final=[M(fC(probe,C),fC(O,C),y) for O,C,y in tasks]; return np.array(learned),np.array(final)
out={}; t0=time.time(); seeds=range(5000,5040)
for task in ["random","similar"]:
    for T in [12,48]:
        res={}
        for sd in seeds:
            probe,tasks=core4.make_tasks(c,"pn",T,sd) if task=="random" else core4.make_tasks2(c,T,sd)
            def add(k,v): res.setdefault(k,[]).append(core4.summarize(*v))
            for eta in [0.1,0.3,0.5]:
                for cond in ["real","none"]: add(f"fly_{cond}_{eta}",core4.run_fly(c,cond,probe,tasks,sd,s,eta=eta))
            for lr in [0.005,0.01,0.02,0.05,0.1,0.25,0.5]: add(f"delta_{lr}",run_delta2(probe,tasks,lr))
            for lam in [1,10,100,1000]: add(f"ewc_{lam}",run_delta2(probe,tasks,0.5,lam))
            add("mh",run_mh2(probe,tasks))
        out[f"{task}_T{T}"]=res; print(round(time.time()-t0),"s",circ,task,T,flush=True)
json.dump(out,open(f"round2_B_{circ}.json","w")); print("done")

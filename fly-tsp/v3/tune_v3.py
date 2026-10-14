"""Tuning on the v2 TUNING instances (seeds 8000-8239, 40/regime, 2 reps). TURN-k: lr {0.03,0.1,0.3} x kappa {2,4,8,16} (ACO alpha/beta/rho from v2 final). HAND-turn: gamma {0.5,1,2,4,8,16}."""
import sys, json, time, numpy as np; sys.path.insert(0,'.')
from multiprocessing import Pool
import arms3 as A
def job(a):
    arm,reg,par=a; ins=A.tune_insts(reg)
    P=dict(turn={arm.split("-")[1]:par} if arm.startswith("TURN") else {},gamma=par if arm=="HAND-turn" else 0)
    return a,A.run_arm(arm,reg,P,ins,range(2))
if __name__=="__main__":
    t0=time.time(); out={}
    for reg in A.REGS:
        ins=A.tune_insts(reg); ref=np.array(A.ref_for(reg,"tune",ins)); gap=lambda L:float(np.mean(L/ref[:,None]-1)); out[reg]={}
        with Pool(10) as p:
            for arm in ("TURN-real","TURN-random","TURN-linear"):
                rr=sorted([(a[2],gap(L)) for a,L in p.map(job,[(arm,reg,(lr,k)) for lr in (0.03,0.1,0.3) for k in (2.0,4.0,8.0,16.0)])],key=lambda x:x[1]); out[reg][arm]=dict(best=rr[0][0],gap=rr[0][1],grid=rr); print(reg,arm,"best",rr[0][0],"%.2f%%"%(100*rr[0][1]),"worst %.2f%%"%(100*rr[-1][1]),round(time.time()-t0),"s",flush=True)
            rr=sorted([(a[2],gap(L)) for a,L in p.map(job,[("HAND-turn",reg,g) for g in (0.5,1.0,2.0,4.0,8.0,16.0)])],key=lambda x:x[1]); out[reg]["HAND-turn"]=dict(best=rr[0][0],gap=rr[0][1],grid=rr); print(reg,"HAND-turn best gamma",rr[0][0],"%.2f%%"%(100*rr[0][1]),"worst %.2f%%"%(100*rr[-1][1]),round(time.time()-t0),"s",flush=True)
            base=A.run_arm("ACO",reg,{},ins,range(2)); print(reg,"ACO (v2 params) tuning gap %.2f%%"%(100*gap(base)),flush=True); out[reg]["ACO"]=gap(base)
        json.dump(out,open("tuning_v3.json","w"),default=str)

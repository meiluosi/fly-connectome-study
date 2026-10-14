"""Tuning on TUNING instances only (seeds 8000-8339; disjoint from test 7000-8049 and training 2000-2099). ACO: 27 configs (12 in R4). Each base online arm ON-k: 9 (lr,kappa) configs with the regime's tuned ACO alpha/beta/rho.
Structural variants (NOTAU, HET4, HET4P, ONd, ISL4*) inherit the parameters of their base arm and are NOT tuned. FROZEN/PRE use the v1-tuned (lr,kappa)."""
import sys, json, time, itertools, numpy as np; sys.path.insert(0,'.')
from multiprocessing import Pool
import arms as A
REGS=sys.argv[1:] or ["R1","R2","R3","R4"]
def acoj(a):
    reg,al,be,rho=a; ins=A.tune_insts(reg); L=A.run_arm("ACO",reg,dict(aco=(al,be,rho)),ins,range(A.NREP_TUNE)); return a,L
def onj(a):
    reg,arm,lr,ka,acop=a; ins=A.tune_insts(reg); L=A.run_arm(arm,reg,dict(aco=acop,on={arm:(lr,ka)}),ins,range(A.NREP_TUNE)); return a,L
if __name__=="__main__":
    t0=time.time(); out={}
    for reg in REGS:
        ins=A.tune_insts(reg); ref=np.array(A.ref_for(reg,"tune",ins)); print(reg,"refs",round(time.time()-t0),"s",flush=True)
        gap=lambda L:float(np.mean(L/ref[:,None]-1))
        grid=[(reg,al,be,rho) for al in ((1.0,2.0) if reg=="R4" else (0.5,1.0,2.0)) for be in (3.0,5.0,8.0) for rho in ((0.1,0.3) if reg=="R4" else (0.1,0.3,0.5))]
        with Pool(10) as p:
            rr=sorted([(a,gap(L)) for a,L in p.map(acoj,grid)],key=lambda x:x[1]); best=rr[0][0][1:]; out[reg]=dict(aco=dict(best=best,gap=rr[0][1],grid=rr),on={}); print(reg,"ACO best",best,"%.2f%%"%(100*rr[0][1]),"worst %.2f%%"%(100*rr[-1][1]),round(time.time()-t0),"s",flush=True)
            kinds=("real","random","linear") if reg=="R4" else A.ON_KINDS
            for k in kinds:
                arm="ON-"+k; lrs=(0.01,0.03,0.1)
                rr=sorted([(a[2:4],gap(L)) for a,L in p.map(onj,[(reg,arm,lr,ka,best) for lr in lrs for ka in (2.0,4.0,8.0)])],key=lambda x:x[1]); out[reg]["on"][arm]=dict(best=rr[0][0],gap=rr[0][1],grid=rr); print(reg,arm,"best (lr,kappa)",rr[0][0],"%.2f%%"%(100*rr[0][1]),"worst %.2f%%"%(100*rr[-1][1]),round(time.time()-t0),"s",flush=True)
        json.dump(out,open(f"tuning_v2_{'_'.join(REGS) if len(REGS)<4 else 'all'}.json","w"),default=str)

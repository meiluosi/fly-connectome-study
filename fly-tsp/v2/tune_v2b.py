"""Stage 2 of tuning (declared before looking at any test data): stage 1 put the best ACO config and the best (lr,kappa) at grid edges, so the grids are EXTENDED and the online arms are re-tuned with the final ACO parameters.
ACO: union of stage-1 grid and extension (alpha {1,2} x beta {8,12,16} x rho {0.5,0.7,0.9}); online arms: lr {0.03,0.1,0.3} x kappa {4,8,16}. Output tuning_v2_final.json (same format as eval_v2 expects)."""
import sys, json, time, numpy as np; sys.path.insert(0,'.')
from multiprocessing import Pool
import arms as A
from tune_v2 import acoj, onj
S1=json.load(open("tuning_v2_all.json")); REGS=sys.argv[1:] or ["R1","R2","R3","R4"]
if __name__=="__main__":
    t0=time.time(); out={}
    for reg in REGS:
        ins=A.tune_insts(reg); ref=np.array(A.ref_for(reg,"tune",ins)); gap=lambda L:float(np.mean(L/ref[:,None]-1))
        with Pool(10) as p:
            ext=[(reg,al,be,rho) for al in (1.0,2.0) for be in (8.0,12.0,16.0) for rho in (0.5,0.7,0.9) if not (be==8.0 and rho==0.5)]
            old=[(tuple(a[1:]),g) for a,g in S1[reg]["aco"]["grid"]]
            if reg=="R4": old=[]; ext=[(reg,al,be,rho) for al in (1.0,2.0) for be in (3.0,5.0,8.0) for rho in (0.1,0.3,0.5)]   # R4 was redefined after stage 1 (n=100, 30 tours): full grid
            new=[(a[1:],gap(L)) for a,L in p.map(acoj,ext)]; allr=sorted(old+new,key=lambda x:x[1]); best=allr[0][0]
            out[reg]=dict(aco=dict(best=best,gap=allr[0][1],grid=allr),on={}); print(reg,"ACO best",best,"%.2f%%"%(100*allr[0][1]),"worst %.2f%%"%(100*allr[-1][1]),round(time.time()-t0),"s",flush=True)
            kinds=("real","random","linear") if reg=="R4" else A.ON_KINDS
            for k in kinds:
                arm="ON-"+k; rr=sorted([(a[2:4],gap(L)) for a,L in p.map(onj,[(reg,arm,lr,ka,best) for lr in (0.03,0.1,0.3) for ka in (4.0,8.0,16.0)])],key=lambda x:x[1])
                out[reg]["on"][arm]=dict(best=rr[0][0],gap=rr[0][1],grid=rr); print(reg,arm,"best (lr,kappa)",rr[0][0],"%.2f%%"%(100*rr[0][1]),"worst %.2f%%"%(100*rr[-1][1]),round(time.time()-t0),"s",flush=True)
        json.dump(out,open("tuning_v2_final.json","w"),default=str)

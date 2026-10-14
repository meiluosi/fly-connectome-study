"""Stage 2 for HAND-turn only: stage 1 put gamma at the lower grid edge (0.5) in R1/R2, so add gamma {0.1,0.25} and keep the best of the union."""
import sys, json, numpy as np; sys.path.insert(0,'.')
from multiprocessing import Pool
import arms3 as A
from tune_v3 import job
if __name__=="__main__":
    T3=json.load(open("tuning_v3.json"))
    for reg in A.REGS:
        ins=A.tune_insts(reg); ref=np.array(A.ref_for(reg,"tune",ins)); gap=lambda L:float(np.mean(L/ref[:,None]-1))
        with Pool(10) as p: new=[(a[2],gap(L)) for a,L in p.map(job,[("HAND-turn",reg,g) for g in (0.1,0.25)])]
        old=[(float(g),x) for g,x in T3[reg]["HAND-turn"]["grid"]]; allr=sorted(old+new,key=lambda x:x[1]); T3[reg]["HAND-turn"]=dict(best=allr[0][0],gap=allr[0][1],grid=allr); print(reg,"HAND best gamma",allr[0][0],"%.2f%%"%(100*allr[0][1]),flush=True)
    json.dump(T3,open("tuning_v3.json","w"),default=str)

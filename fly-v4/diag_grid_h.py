"""exploratory (not registered): does a wider grid close the comp_real gap in the foraging arena? tuning seeds 20-31, consistent worlds"""
import numpy as np, collections
from multiprocessing import Pool
import run_v4h as H
def f(a): c,arm,prm,s=a; return (arm,prm["eta"],prm["g_learn"]),H.one(c,arm,prm,s)
if __name__=="__main__":
    jobs=[("consistent",arm,dict(eta=e,g_learn=g,k_turn=1.4),s) for arm in("comp_real","global") for e in (0.8,2.0,4.0) for g in (1.0,3.0,6.0,10.0) for s in range(20,32)]
    with Pool(10) as p: res=p.map(f,jobs)
    d=collections.defaultdict(list)
    for k,v in res: d[k].append(v)
    for k,v in sorted(d.items()): print(k,round(np.mean(v),1))

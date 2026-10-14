"""POST-HOC (not preregistered): FlyWire with MBON25,MBON34 restored; real vs shuffled forgetting_acc, v4 readout, random task, seeds 3000-3059."""
import numpy as np, json, core4, core_fw2
rng=np.random.default_rng(5); out={}
def boot(d,n=4000):
    m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return float(d.mean()),*[float(x) for x in np.percentile(m,[2.5,97.5])]
for side,nm in [("right","FR2"),("left","FL2")]:
    c=core_fw2.build(side); s=core4.signs(c); print(nm,"MBON",c.NM,"dropped",c.dropped_mbon,"comp sizes y1,y2:",[int(c.M[:,i].sum()) for i in range(c.NC)][:0],flush=True)
    for T in [12,48]:
        R={"real":[],"shuffled":[]}
        for sd in range(3000,3060):
            probe,tasks=core4.make_tasks(c,"pn",T,sd)
            for k in R: R[k].append(core4.summarize(*core4.run_fly(c,k,probe,tasks,sd,s))["forg_acc"])
        d=np.array(R["real"])-np.array(R["shuffled"]); out[f"{nm}_T{T}"]=dict(real=float(np.mean(R["real"])),shuf=float(np.mean(R["shuffled"])),diff=boot(d))
        print(nm,T,out[f"{nm}_T{T}"],flush=True)
json.dump(out,open("posthoc_fw.json","w"),indent=1); print("done")

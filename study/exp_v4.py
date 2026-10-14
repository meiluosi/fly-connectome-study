import numpy as np, core, core4, json, time
c=core.build("R"); s=core4.signs(c); print("MBON signs: +",int((s>0).sum()),"-",int((s<0).sum()),flush=True)
rng=np.random.default_rng(0); S=60; out=[]
def boot(d,n=4000):
    m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return d.mean(),np.percentile(m,2.5),np.percentile(m,97.5)
t0=time.time()
for T in [12,48]:
    res={k:[] for k in ["real","shuffled","none","delta","ewc10","ewc100"]}
    for sd in range(S):
        probe,tasks=core4.make_tasks(c,"pn",T,sd)
        for k in ["real","shuffled","none"]: res[k].append(core4.summarize(*core4.run_fly(c,k,probe,tasks,sd,s)))
        res["delta"].append(core4.summarize(*core4.run_delta(c,probe,tasks,sd))); res["ewc10"].append(core4.summarize(*core4.run_delta(c,probe,tasks,sd,ewc=10.0))); res["ewc100"].append(core4.summarize(*core4.run_delta(c,probe,tasks,sd,ewc=100.0)))
    print(f"\n== v4 behaviour readout, T={T}, {S} paired seeds  [{round(time.time()-t0)}s]")
    for k,v in res.items(): print(f"  {k:9s} learn_acc={np.mean([r['learn_acc'] for r in v]):.3f} final_acc={np.mean([r['final_acc'] for r in v]):.3f} forg_acc={np.mean([r['forg_acc'] for r in v]):.3f} forg_z={np.mean([r['forg_z'] for r in v]):.3f}",flush=True)
    for m in ["forg_acc","forg_z"]:
        d=np.array([a[m]-b[m] for a,b in zip(res['real'],res['shuffled'])]); mm,lo,hi=boot(d); print(f"  real-shuffled {m}: {mm:+.4f} [{lo:+.4f},{hi:+.4f}]")
    out.append(dict(T=T,res=res))
json.dump(out,open("exp_v4_results.json","w")); print("done")

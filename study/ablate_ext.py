import sys, json, numpy as np, core, core4
sys.argv=[sys.argv[0],sys.argv[1]]; rule=sys.argv[1]
src=open("ablate.py").read(); head=src.split("out={}; t0=time.time()")[0]
exec(head.replace('rule=sys.argv[1]; ',"").replace('ETAS={"bounded"','ETAS_UNUSED={"bounded"'))
EXT={"bounded":[.005,.01,.02],"additive0":[.002,.005,.01],"multup":[.002,.005,.01]}[rule]; out={}
for task in ["random","similar"]:
    for eta in EXT:
        rows=[]
        for sd in seeds:
            probe,tasks=core4.make_tasks(c,"pn",T,sd) if task=="random" else core4.make_tasks2(c,T,sd)
            l,f=run_fly_rule(c,"none",probe,tasks,sd,s,eta); rows.append(core4.summarize(l,f))
        out[f"{task}|none|{eta}"]=rows; print(task,eta,"learn %.3f forg %.3f"%(np.mean([r['learn_acc'] for r in rows]),np.mean([r['forg_acc'] for r in rows])),flush=True)
json.dump(out,open(f"ablate_ext_{rule}.json","w")); print("done")

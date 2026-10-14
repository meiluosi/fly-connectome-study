import sys, json, numpy as np, core, core4, core_fw2
circ=sys.argv[1]; c=core.build("R") if circ=="MR" else core_fw2.build("right"); M=core4.metrics
exec(open("round2_B.py").read().split("out={}")[0].split("def run_delta2")[1].join(["def run_delta2",""]) if False else "")
src=open("round2_B.py").read(); ns={}; exec("import numpy as np, core4\nc=c\nM=core4.metrics\n"+"def run_delta2"+src.split("def run_delta2")[1].split("def run_mh2")[0],{"np":np,"core4":core4,"c":c,"M":M},ns)
run_delta2=ns["run_delta2"]; out={}
for task in ["random","similar"]:
    for T in [12,48]:
        res={}
        for sd in range(5010,5040):
            probe,tasks=core4.make_tasks(c,"pn",T,sd) if task=="random" else core4.make_tasks2(c,T,sd)
            for lr in [0.0005,0.001,0.002]: res.setdefault(f"delta_{lr}",[]).append(core4.summarize(*run_delta2(probe,tasks,lr)))
        out[f"{task}_T{T}"]=res; print(circ,task,T,{k:round(float(np.mean([x["learn_acc"] for x in v])),3) for k,v in res.items()},flush=True)
json.dump(out,open(f"round2_B_ext_{circ}.json","w")); print("done")

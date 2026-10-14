"""Rule ablation per PREREG_ablation.md. usage: ablate.py RULE   (bounded|additive0|multup|delta)  -> ablate_RULE.json"""
import sys, json, time, numpy as np, core, core4
rule=sys.argv[1]; c=core.build("R"); s=core4.signs(c); seeds=range(2000,2030); T=48
ETAS={"bounded":[.05,.1,.2,.3,.5,.8],"additive0":[.02,.05,.1,.2,.4,.8],"multup":[.02,.05,.1,.2,.3],"delta":[.02,.05,.1,.25,.5]}[rule]
def run_fly_rule(c,cond,probe,tasks,seed,s,eta,reps=3):
    rc=np.random.default_rng(10_000+seed); Mc=c.M; q=np.full(c.N.shape,0.5); Nn=c.N; Nb=c.Nb; learned=[]
    B=lambda X:(X@(Nn*q))@s
    for O,C,y in tasks:
        gm=np.ones(c.NM,bool) if cond=="none" else Mc[:,C].any(1)
        if not gm.any(): gm=np.ones(c.NM,bool)
        dep=gm&(y*s<0); pot=gm&(y*s>0)
        for _ in range(reps):
            for x in O:
                A=x[:,None]
                if rule=="bounded":
                    q[:,dep]-=eta*A*q[:,dep]*Nb[:,dep]; q[:,pot]+=eta*A*(1-q[:,pot])*Nb[:,pot]
                elif rule=="additive0":
                    q[:,dep]=np.maximum(0,q[:,dep]-eta*A*Nb[:,dep]); q[:,pot]+=eta*A*Nb[:,pot]
                else:
                    q[:,dep]-=eta*A*q[:,dep]*Nb[:,dep]; q[:,pot]=np.minimum(1000.,q[:,pot]+eta*A*q[:,pot]*Nb[:,pot])
        learned.append(core4.metrics(B(probe),B(O),y))
    final=[core4.metrics(B(probe),B(O),y) for O,C,y in tasks]; return np.array(learned),np.array(final)
out={}; t0=time.time()
for task in ["random","similar"]:
    for cond in (["real","none"] if rule!="delta" else ["delta"]):
        for eta in ETAS:
            rows=[]
            for sd in seeds:
                probe,tasks=core4.make_tasks(c,"pn",T,sd) if task=="random" else core4.make_tasks2(c,T,sd)
                if rule=="delta": l,f=core4.run_delta(c,probe,tasks,sd,lr=eta)
                else: l,f=run_fly_rule(c,cond,probe,tasks,sd,s,eta)
                rows.append(core4.summarize(l,f))
            out[f"{task}|{cond}|{eta}"]=rows; print(round(time.time()-t0),"s",task,cond,eta,"learn %.3f forg %.3f"%(np.mean([r['learn_acc'] for r in rows]),np.mean([r['forg_acc'] for r in rows])),flush=True)
json.dump(out,open(f"ablate_{rule}.json","w")); print("done")

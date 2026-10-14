"""usage: matched.py MR|FR random|similar 12|48  -> matched_{circ}_{task}_{T}.json"""
import sys, json, time, numpy as np, core, core4, core_fw2
circ,task,T=sys.argv[1],sys.argv[2],int(sys.argv[3]); c=core.build("R") if circ=="MR" else core_fw2.build("right"); s=core4.signs(c); seeds=range(6000,6040)
GRID={("bounded","real"):[.03,.05,.08,.12,.2,.3,.5,.8],("bounded","none"):[.003,.005,.008,.012,.02,.03,.05],("additive0","real"):[.02,.05,.1,.2,.4,.8],("additive0","none"):[.002,.004,.008,.015,.03]}
def run(rule,cond,probe,tasks,eta,reps=3):
    q=np.full(c.N.shape,0.5); Nn,Nb=c.N,c.Nb; learned=[]; B=lambda X:(X@(Nn*q))@s
    for O,C,y in tasks:
        gm=np.ones(c.NM,bool) if cond=="none" else c.M[:,C].any(1)
        if not gm.any(): gm=np.ones(c.NM,bool)
        dep=gm&(y*s<0); pot=gm&(y*s>0)
        for _ in range(reps):
            for x in O:
                A=x[:,None]
                if rule=="bounded": q[:,dep]-=eta*A*q[:,dep]*Nb[:,dep]; q[:,pot]+=eta*A*(1-q[:,pot])*Nb[:,pot]
                else: q[:,dep]=np.maximum(0,q[:,dep]-eta*A*Nb[:,dep]); q[:,pot]+=eta*A*Nb[:,pot]
        learned.append(core4.metrics(B(probe),B(O),y))
    final=[core4.metrics(B(probe),B(O),y) for O,C,y in tasks]; return core4.summarize(np.array(learned),np.array(final))
out={}; t0=time.time(); cache={sd:(core4.make_tasks(c,"pn",T,sd) if task=="random" else core4.make_tasks2(c,T,sd)) for sd in seeds}
for (rule,cond),etas in GRID.items():
    for eta in etas:
        out[f"{rule}|{cond}|{eta}"]=[run(rule,cond,*cache[sd],eta) for sd in seeds]; r=out[f"{rule}|{cond}|{eta}"]
        print(round(time.time()-t0),"s",circ,task,T,rule,cond,eta,"learn %.3f forg %.3f"%(np.mean([x["learn_acc"] for x in r]),np.mean([x["forg_acc"] for x in r])),flush=True)
json.dump(out,open(f"matched_{circ}_{task}_{T}.json","w")); print("done")

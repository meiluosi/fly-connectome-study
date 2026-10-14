"""usage: lif_experiment.py raw|top5 random|similar 12|48  (per PREREG_lif.md; seeds 7000-7029; MR circuit; LIF-derived KC codes)"""
import sys, json, time, numpy as np, core, core4
binar,task,T=sys.argv[1],sys.argv[2],int(sys.argv[3]); c=core.build("R"); s=core4.signs(c); seeds=range(7000,7030)
cnt=np.load("lif_kc_counts.npy").astype(float); meta=json.load(open("lif_kc_meta.json")); kinds=meta["kinds"]
tie=np.random.default_rng(2718).random(cnt.shape)*1e-3
def code(i): 
    if binar=="raw": return (cnt[i]>0).astype(float)
    o=np.zeros(c.NK); o[np.argsort(-(cnt[i]+tie[i]))[:int(0.05*c.NK)]]=1; return o
base_idx={i:n for n,(k,i,j) in enumerate(kinds) if k=="b"}; var_idx={(i,j):n for n,(k,i,j) in enumerate(kinds) if k=="v"}
BASE=np.array([code(base_idx[i]) for i in range(320)]); VAR={k:code(n) for k,n in var_idx.items()}
def make_tasks(seed,sim):
    rt=np.random.default_rng(seed); order=list(rt.permutation(320)); probe_ids=order[:40]; fresh=order[40:]; used=[]; tasks=[]; fi=0
    for t in range(T):
        O=[]
        for _ in range(5):
            if sim and used and rt.random()<0.6: b=used[rt.integers(len(used))]; O.append(VAR[(b,int(rt.integers(2)))])
            else: b=fresh[fi]; fi+=1; used.append(b); O.append(BASE[b])
        C=rt.choice(c.NC,2,replace=False); y=rt.choice([-1,1]); tasks.append((np.array(O),C,y))
    return BASE[probe_ids],tasks
M=core4.metrics
def run_fly(cond,probe,tasks,eta,reps=3):
    q=np.full(c.N.shape,0.5); learned=[]; B=lambda X:(X@(c.N*q))@s
    for O,C,y in tasks:
        gm=np.ones(c.NM,bool) if cond=="none" else c.M[:,C].any(1)
        if not gm.any(): gm=np.ones(c.NM,bool)
        dep=gm&(y*s<0); pot=gm&(y*s>0)
        for _ in range(reps):
            for x in O: A=x[:,None]; q[:,dep]-=eta*A*q[:,dep]*c.Nb[:,dep]; q[:,pot]+=eta*A*(1-q[:,pot])*c.Nb[:,pot]
        learned.append(M(B(probe),B(O),y))
    return core4.summarize(np.array(learned),np.array([M(B(probe),B(O),y) for O,C,y in tasks]))
def run_delta(probe,tasks,lr=0.5,lam=0.0,reps=3):
    w=np.zeros(c.NK); b=0.0; ws=w.copy(); F=np.zeros(c.NK); learned=[]; f=lambda X:X@w+b
    for O,C,y in tasks:
        for _ in range(reps):
            for x in O:
                err=w@x+b-y; st=lr/(x@x+1.0); w-=st*err*x
                if lam>0: w-=np.minimum(1.0,st*lam*F)*(w-ws)
                b-=st*err
        F+=np.mean(O**2,axis=0); ws=w.copy(); learned.append(M(f(probe),f(O),y))
    return core4.summarize(np.array(learned),np.array([M(f(probe),f(O),y) for O,C,y in tasks]))
GRID={"real":[.03,.05,.08,.12,.2,.3,.5,.8],"none":[.003,.005,.008,.012,.02,.03,.05]}; out={}; t0=time.time()
cache={sd:make_tasks(sd,task=="similar") for sd in seeds}
for cond,etas in GRID.items():
    for eta in etas:
        out[f"bounded|{cond}|{eta}"]=[run_fly(cond,*cache[sd],eta) for sd in seeds]; r=out[f"bounded|{cond}|{eta}"]
        print(round(time.time()-t0),"s",binar,task,T,cond,eta,"learn %.3f forg %.3f"%(np.mean([x["learn_acc"] for x in r]),np.mean([x["forg_acc"] for x in r])),flush=True)
out["delta"]=[run_delta(*cache[sd]) for sd in seeds]; out["ewc10"]=[run_delta(*cache[sd],lam=10.0) for sd in seeds]
json.dump(out,open(f"lif_{binar}_{task}_{T}.json","w")); print("done")

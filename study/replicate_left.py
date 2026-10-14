import numpy as np, core, json, time, itertools
rng=np.random.default_rng(0)
def boot(d,n=4000):
    m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return d.mean(),np.percentile(m,2.5),np.percentile(m,97.5)
rows=[]
for side in ["L","R"]:
    c=core.build(side)
    for T,alloc in itertools.product([12,24,48],["random","roundrobin"]):
        v={k:np.array([core.run(c,k,T,s,alloc=alloc) for s in range(60)]) for k in ["real","shuffled","none"]}
        d=boot(v["real"][:,1]-v["shuffled"][:,1]); r=dict(side=side,T=T,alloc=alloc,real=v["real"][:,1].mean(),shuf=v["shuffled"][:,1].mean(),none=v["none"][:,1].mean(),diff=d[0],lo=d[1],hi=d[2])
        rows.append(r); print(json.dumps({k:(round(x,4) if isinstance(x,float) else x) for k,x in r.items()}),flush=True)
json.dump(rows,open("replicate_left.json","w"),indent=1); print("done")

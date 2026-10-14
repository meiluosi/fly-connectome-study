import pandas as pd, numpy as np
from compartments import canon
ann=pd.read_csv("mb_annotations_malecns.csv"); e=pd.read_parquet("mb_edges_malecns.parquet")
role=ann.set_index("bodyId").role.to_dict()
ann["prim"]=ann.compartment.map(lambda l:set(canon(l)["primary"]) if isinstance(l,str) else set())
prim=ann.set_index("bodyId").prim.to_dict()
e["pre_role"]=e.body_pre.map(role); e["post_role"]=e.body_post.map(role)
print("edge counts by role pair:\n",e.groupby(["pre_role","post_role"]).weight.agg(["size","sum"]).to_string())
d2m=e[(e.pre_role=="DAN")&(e.post_role=="MBON")].copy()
# infer unlabeled DAN compartments from the compartment of the MBONs they target
unl=[b for b in ann[ann.role=="DAN"].bodyId if not prim[b]]
inf={}
for b in unl:
    w=d2m[d2m.body_pre==b]; sc={}
    for _,r in w.iterrows():
        for c in prim[r.body_post]: sc[c]=sc.get(c,0)+r.weight
    inf[b]=max(sc,key=sc.get) if sc else None
print("unlabeled DANs:",len(unl),"-> inferred (by MBON targets):",pd.Series(inf).value_counts(dropna=False).to_dict())
lab={b:p for b,p in prim.items() if p}
d2m=d2m[d2m.body_pre.map(lambda b:bool(lab.get(b))) & d2m.body_post.map(lambda b:bool(lab.get(b)))]
def same_frac(post_lab):
    s=np.array([bool(lab[a]&post_lab[b]) for a,b in zip(d2m.body_pre,d2m.body_post)])
    return (d2m.weight.values*s).sum()/d2m.weight.sum()
obs=same_frac(lab)
mbon=[b for b in ann[ann.role=="MBON"].bodyId]
rng=np.random.default_rng(0); null=[]
for _ in range(1000):
    perm=dict(zip(mbon,[lab[m] for m in rng.permutation(mbon)])); null.append(same_frac(perm))
null=np.array(null)
print(f"\nDAN->MBON weight on same-compartment targets: observed {obs:.3f}; shuffled-MBON-label null mean {null.mean():.3f} (95% {np.percentile(null,2.5):.3f}-{np.percentile(null,97.5):.3f}); p={(null>=obs).mean():.4f}")
print("DAN->MBON total synapse weight (labeled):",int(d2m.weight.sum()))
k2m=e[(e.pre_role=="KC")&(e.post_role=="MBON")]
print("KC->MBON edges:",len(k2m),"total weight:",int(k2m.weight.sum()))

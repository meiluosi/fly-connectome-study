import pandas as pd, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from compartments import canon
ann=pd.read_csv("mb_annotations_malecns.csv"); e=pd.read_parquet("mb_edges_malecns.parquet")
kc=ann[ann.role=="KC"].set_index("bodyId"); mb=ann[ann.role=="MBON"].set_index("bodyId")
def grp(t):
    t=str(t); return "a'b'" if t.startswith("KCa'b'") else "ab" if t.startswith("KCab") else "g" if t.startswith("KCg") else "other"
kc["grp"]=kc.type.map(grp)
k=e[e.body_pre.isin(kc.index)&e.body_post.isin(mb.index)].copy()
k["grp"]=k.body_pre.map(kc.grp)
rows=[]
for _,r in k.iterrows():
    cs=canon(mb.compartment[r.body_post])["primary"]
    for c in cs: rows.append((r.grp,c,r.weight/len(cs)))
m=pd.DataFrame(rows,columns=["grp","comp","w"]).pivot_table(index="comp",columns="grp",values="w",aggfunc="sum",fill_value=0)
order=["g"]+[]; 
ordc=[c for c in ["y1","y2","y3","y4","y5","B'1","B'2","a'1","a'2","a'3","B1","B2","a1","a2","a3","calyx"] if c in m.index]
m=m.loc[ordc]; print(m.round(0).astype(int).to_string())
frac=m.div(m.sum(1),axis=0); print("\nrow-normalized:\n",frac.round(2).to_string())
m.to_csv("kc_mbon_by_compartment.csv")
fig,ax=plt.subplots(1,2,figsize=(9,5.5))
for a,(M,t,fmt) in zip(ax,[(np.log10(m+1),"log10 synapse weight","{:.1f}"),(frac,"fraction of compartment's KC input","{:.2f}")]):
    im=a.imshow(M.values,aspect="auto",cmap="viridis"); a.set_xticks(range(M.shape[1]),M.columns); a.set_yticks(range(M.shape[0]),M.index)
    a.set_title(t,fontsize=10); a.set_xlabel("KC subtype group"); plt.colorbar(im,ax=a,fraction=.05)
ax[0].set_ylabel("MBON compartment"); plt.suptitle("MaleCNS v1.0: KC -> MBON input by compartment"); plt.tight_layout(); plt.savefig("kc_mbon_by_compartment.png",dpi=140)

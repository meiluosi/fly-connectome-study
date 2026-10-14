import numpy as np, pandas as pd, core, core_fw, json
from compartments import canon
from scipy.cluster.hierarchy import linkage, fcluster
from math import comb
def ari(a,b):
    a=np.unique(a,return_inverse=True)[1]; b=np.unique(b,return_inverse=True)[1]; t=np.zeros((a.max()+1,b.max()+1),int)
    for i,j in zip(a,b): t[i,j]+=1
    s=sum(comb(int(x),2) for x in t.ravel()); sa=sum(comb(int(x),2) for x in t.sum(1)); sb=sum(comb(int(x),2) for x in t.sum(0)); n=comb(len(a),2); e=sa*sb/n
    return (s-e)/(0.5*(sa+sb)-e)
def kcgrp(t): return "a'b'" if (t.startswith("KCa'b'") or t.startswith("KCapbp")) else "ab" if t.startswith("KCab") else "g" if t.startswith("KCg") else "o"
circs={"MR":core.build("R"),"ML":core.build("L"),"FR":core_fw.build("right"),"FL":core_fw.build("left")}
res={}
for k,c in circs.items():
    comp=c.mb.compartment.astype(str).tolist(); first=[canon(l)["primary"][0] if canon(l)["primary"] else "x" for l in comp]
    B=c.Nb.astype(float); Z=B/np.maximum(np.linalg.norm(B,axis=0),1e-9)
    keep=B.sum(0)>0; cl=fcluster(linkage(Z.T[keep],"average",metric="cosine"),t=16,criterion="maxclust"); first=[f for f,kp in zip(first,keep) if kp]
    r=np.random.default_rng(0); sh=[core.overlap_stat(c,c.M[r.permutation(c.NM)]) for _ in range(300)]; real=core.overlap_stat(c,c.M)
    grp=np.array([kcgrp(t) for t in c.kc_type]); 
    # KC-group composition of KC->MBON synapse weight per MBON
    comp_g=pd.DataFrame({g:(c.N[grp==g].sum(0)) for g in ["g","ab","a'b'"]}); comp_g=comp_g.div(comp_g.sum(1).replace(0,1),axis=0)
    res[k]=dict(n_mbon_no_kc_input=int((~keep).sum()),n_kc=c.NK,n_mbon=c.NM,n_comp=c.NC,edges=int(c.Nb.sum()),mean_in_kc_per_mbon=float(c.Nb.sum(0).mean()),real_overlap=real,shuf_overlap_mean=float(np.mean(sh)),shuf_overlap_sd=float(np.std(sh)),
        z_real_vs_shuf=float((real-np.mean(sh))/np.std(sh)),ARI_label_vs_KCinput_cluster=float(ari(first,cl)),mbon_per_comp=dict(zip(c.M.sum(0).tolist(),[0]*c.NC)) if False else None,
        kc_groups={g:int((grp==g).sum()) for g in ["g","ab","a'b'","o"]},frac_mbon_pure_lobe=float((comp_g.max(1)>0.9).mean()))
    res[k]["mbon_counts_by_compartment"]=None
print(json.dumps({k:{a:(round(b,3) if isinstance(b,float) else b) for a,b in v.items() if a not in("mbon_counts_by_compartment","mbon_per_comp")} for k,v in res.items()},indent=1))
# compartment-level MBON counts side by side (R hemisphere)
def cnt(c):
    from collections import Counter
    comps=sorted({x for l in c.mb.compartment for x in canon(l)["primary"]}); return pd.Series(c.M.sum(0),index=comps)
tab=pd.DataFrame({k:cnt(c) for k,c in circs.items()}).fillna(0).astype(int); print(tab.to_string())
# which FlyWire MBON types were dropped (no hemibrain compartment)
f=pd.read_csv("../data_annot/flywire_neuron_annotations.tsv",sep="\t",low_memory=False); h=pd.read_csv("../data_annot/hemibrain_meta.csv",low_memory=False); ht=set(h.type.astype(str))
mb=f[f.cell_type.astype(str).str.startswith("MBON")]; print("FlyWire MBON types lacking hemibrain type:",sorted(set(mb.cell_type[~mb.cell_type.isin(ht)])), " counts per side:",mb[~mb.cell_type.isin(ht)].side.value_counts().to_dict())
male=set(pd.read_csv("mb_annotations_malecns.csv").query("role=='MBON'").type.astype(str)); fw=set(mb.cell_type.astype(str)); print("types only in MaleCNS:",sorted(male-fw)," only in FlyWire:",sorted(fw-male))
tab.to_csv("fw_vs_male_mbon_counts.csv"); json.dump({k:{a:b for a,b in v.items() if a not in("mbon_counts_by_compartment","mbon_per_comp")} for k,v in res.items()},open("fw_vs_male.json","w"),indent=1)

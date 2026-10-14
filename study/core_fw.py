"""FlyWire (female, v783) circuit with the same interface as core.build. MBON compartments are TRANSFERRED from hemibrain instance names via cell type
(hemibrain meta, Supplemental_file5), not annotated in FlyWire itself. Signs from FlyWire top_nt."""
import numpy as np, pandas as pd, re, core
from compartments import canon
def build(side="right"):
    f=pd.read_csv("../data_annot/flywire_neuron_annotations.tsv",sep="\t",low_memory=False)
    h=pd.read_csv("../data_annot/hemibrain_meta.csv",low_memory=False); e=pd.read_parquet("../data_annot/flywire_connectivity_783.parquet",columns=["Presynaptic_ID","Postsynaptic_ID","Connectivity"])
    e.columns=["pre","post","w"]; c=core.Circuit(); c.side=side
    h["type"]=h.type.astype(str); hc=h[h.type.str.startswith("MBON")].drop_duplicates("type").set_index("type").instance.map(lambda s:re.search(r"\(([^)]*)\)",s).group(1))
    mb=f[(f.cell_type.astype(str).str.startswith("MBON"))&(f.side==side)][["root_id","cell_type","top_nt"]].copy(); mb["compartment"]=mb.cell_type.map(hc)
    c.dropped_mbon=int(mb.compartment.isna().sum()); mb=mb.dropna(subset=["compartment"]).reset_index(drop=True); mb=mb.rename(columns={"root_id":"bodyId"})
    kc=f[(f.cell_class.astype(str).str.contains("Kenyon|KC"))&(f.side==side)]; kcid=kc.root_id.values; ki={b:i for i,b in enumerate(kcid)}; mi={b:i for i,b in enumerate(mb.bodyId)}
    k=e[e.pre.isin(ki)&e.post.isin(mi)]; N=np.zeros((len(kcid),len(mb)))
    for a,b,w in zip(k.pre,k.post,k.w): N[ki[a],mi[b]]=w
    N/=N[N>0].mean()
    comps=sorted({x for l in mb.compartment for x in canon(l)["primary"]}); ci={x:i for i,x in enumerate(comps)}; M=np.zeros((len(mb),len(comps)),bool)
    for j,l in enumerate(mb.compartment):
        for x in canon(l)["primary"]: M[j,ci[x]]=True
    pn=f[f.cell_class.astype(str)=="ALPN"][["root_id","cell_type"]]; pn["gl"]=pn.cell_type.astype(str).str.replace(r"_.*$","",regex=True)
    pe=e[e.pre.isin(pn.root_id)&e.post.isin(ki)].merge(pn,left_on="pre",right_on="root_id"); gls=sorted(pe.gl.unique()); gi={g:i for i,g in enumerate(gls)}; P=np.zeros((len(gls),len(kcid)))
    for g,b,w in zip(pe.gl,pe.post,pe.w): P[gi[g],ki[b]]+=w
    c.N,c.Nb,c.M,c.P,c.NK,c.NM,c.NC,c.NG=N,N>0,M,P,len(kcid),len(mb),len(comps),len(gls); c.mb=mb; c.kc_ids=kcid; c.kc_type=kc.cell_type.astype(str).values
    c.signs=np.where(mb.top_nt.values=="acetylcholine",1.0,-1.0); return c

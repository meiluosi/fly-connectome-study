"""Stage 3b: aligned PN->KC matrix for the hemibrain (female, right MB, v1.2). Reads data_hemibrain/exported-traced-adjacencies-v1.2/*.csv (downloaded from storage.googleapis.com/hemibrain/v1.2/exported-traced-adjacencies-v1.2.tar.gz, Janelia FlyEM, CC BY 4.0).
Glomerulus = prefix of the PN type before '_' (same rule as the MaleCNS / FlyWire builds); KCs = types starting with 'KC'. Writes individuals_h.npz with the stage-3 hemispheres plus 'H_R'."""
import os, numpy as np, pandas as pd
HERE=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(HERE,"data_hemibrain","exported-traced-adjacencies-v1.2")
n=pd.read_csv(os.path.join(D,"traced-neurons.csv")); n["type"]=n.type.astype(str); c=pd.read_csv(os.path.join(D,"traced-total-connections.csv"))
ref=np.load(os.path.join(HERE,"..","fly-foraging","data","mb_circuit.npz"),allow_pickle=True); gls=[str(g) for g in ref["gls"]]
kc=n[n.type.str.startswith("KC")][["bodyId","type"]]; pn=n[n.type.str.contains("PN") & ~n.type.str.startswith("KC")][["bodyId","type"]].copy()
pn["gl"]=pn.type.str.replace(r"_.*$","",regex=True)
e=c[c.bodyId_pre.isin(pn.bodyId)&c.bodyId_post.isin(kc.bodyId)].merge(pn,left_on="bodyId_pre",right_on="bodyId")
kid={b:i for i,b in enumerate(kc.bodyId.values)}; A=np.zeros((len(gls),len(kid)),np.float32); hit=set(); miss=set()
for g,b,w in zip(e.gl,e.bodyId_post,e.weight):
    if g in gls: A[gls.index(g),kid[b]]+=w; hit.add(g)
    else: miss.add(g)
print("KCs",len(kid),"PN->KC edges",len(e),"| reference glomeruli covered",len(hit),"of",len(gls),"| hemibrain PN labels not in reference:",sorted(miss))
print("KCs with any PN input:",int((A.sum(0)>0).sum()),"| mean total weight per KC",round(float(A.sum()/len(kid)),1),"| mean glomeruli per KC",round(float((A>0).sum(0).mean()),2))
old=np.load(os.path.join(HERE,"individuals.npz"),allow_pickle=True); out={k:old[k] for k in old.files}; out["H_R"]=A
np.savez_compressed(os.path.join(HERE,"individuals_h.npz"),**out)

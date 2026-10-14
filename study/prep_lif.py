"""Prepare LIF odor specs: glomerulus -> ALPN body ids (those synapsing on right-hemisphere KCs), right KC ids, 320 base odors + 2 variants each."""
import numpy as np, pandas as pd, json, core
c=core.build("R"); full=pd.read_feather("../data_annot/male_body_annotations.feather"); e=pd.read_parquet("mb_edges_malecns.parquet")
full["type"]=full.type.astype(str); pn=full[full["class"]=="ALPN"][["bodyId","type"]]; pn["gl"]=pn.type.str.replace(r"_.*$","",regex=True)
kc=set(c.kc_ids.tolist()); pe=e[e.body_pre.isin(pn.bodyId)&e.body_post.isin(kc)].merge(pn,left_on="body_pre",right_on="bodyId")
gls=sorted(pe.gl.unique()); assert len(gls)==c.NG, (len(gls),c.NG)
gl2ids={g:sorted(set(pe[pe.gl==g].body_pre.astype(int).tolist())) for g in gls}
rng=np.random.default_rng(31415); NG=len(gls); base=[sorted(rng.choice(NG,6,replace=False).tolist()) for _ in range(320)]
def variant(b):
    keep=list(rng.choice(b,4,replace=False)); new=set(keep)
    while len(new)<6: new.add(int(rng.integers(NG)))
    return sorted(int(x) for x in new)
variants=[[variant(b) for _ in range(2)] for b in base]
json.dump(dict(gls=gls,gl2ids=gl2ids,kc_ids=[int(x) for x in c.kc_ids],base=base,variants=variants),open("lif_prep.json","w"))
print("glomeruli",NG,"ALPN neurons used",sum(len(v) for v in gl2ids.values()),"KC",len(c.kc_ids),"odors",320+640)

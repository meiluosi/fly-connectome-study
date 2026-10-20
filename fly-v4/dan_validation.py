"""Stage 6a: check the PAM/PPL1 cluster assignment of the 49 right-hemisphere MBONs against the MaleCNS DAN->MBON synapses.
For each MBON, the cluster of its dominant DAN input (summed synapse weight from PAM vs PPL1 DANs; DAN types PAM01-15, PPL101-108 from the body annotations).
Compares with the compartment-label assignment used in v4core_e.CL_REAL. Run from anywhere; writes dan_annotations.csv, dan_to_mbon_edges.csv, cl_data.npy next to this file."""
import os, sys, numpy as np, pandas as pd, pyarrow.dataset as ds
HERE=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(HERE,"..")
a=pd.read_feather(os.path.join(R,"data_annot","male_body_annotations.feather")); t=a.type.astype(str)
dan=a[t.str.startswith("PAM")|t.str.startswith("PPL1")][["bodyId","type","instance","somaSide"]].copy()
dan["cl"]=np.where(dan.type.str.startswith("PAM"),"PAM","PPL1"); dan["comp"]=dan.instance.str.extract(r"\(([^)]*)\)")[0]
sys.path.insert(0,os.path.join(R,"study")); os.chdir(os.path.join(R,"study")); import core
c=core.build("R"); ids=c.mb.bodyId.values
d=ds.dataset(os.path.join(R,"data_annot","male_weights.feather"),format="feather")
e=d.to_table(filter=ds.field("body_pre").isin(dan.bodyId.tolist())&ds.field("body_post").isin(ids.tolist())).to_pandas()
e=e.merge(dan[["bodyId","cl","comp"]],left_on="body_pre",right_on="bodyId")
dan.to_csv(os.path.join(HERE,"dan_annotations.csv"),index=False); e.to_csv(os.path.join(HERE,"dan_to_mbon_edges.csv"),index=False)
tab=e.pivot_table(index="body_post",columns="cl",values="weight",aggfunc="sum",fill_value=0)
g=lambda i,k: float(tab.loc[i,k]) if (i in tab.index and k in tab.columns) else 0.0
pam=np.array([g(i,"PAM") for i in ids]); ppl=np.array([g(i,"PPL1") for i in ids]); cl_data=np.where(pam+ppl==0,0,np.where(pam>=ppl,1,-1))
np.save(os.path.join(HERE,"cl_data.npy"),cl_data.astype(float))
sys.path.insert(0,HERE); os.chdir(HERE); import v4core_e as E
lit=E.CL_REAL; m=(cl_data!=0)&(lit!=0)
print("MBONs with DAN input:",int((pam+ppl>0).sum()),"/",len(ids)); print("agreement where both defined:",int((cl_data[m]==lit[m]).sum()),"/",int(m.sum()))
print("literature PAM/PPL1/none:",int((lit>0).sum()),int((lit<0).sum()),int((lit==0).sum()),"| data:",int((cl_data>0).sum()),int((cl_data<0).sum()),int((cl_data==0).sum()))
for j in np.flatnonzero(cl_data!=lit): print("differs:",c.mb.type[j],c.mb.compartment[j],"literature",int(lit[j]),"data (PAM,PPL1 weight)",int(pam[j]),int(ppl[j]))

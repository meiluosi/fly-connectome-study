"""Build 65-glomerulus odour vectors from the DoOR 2.0 consensus response matrix (data downloaded from github.com/ropensci/DoOR.data, CC BY-SA 4.0).
Output: odours.npz with U (n_odorants x 65, responses scaled to [0,1], 0 where no data), has (bool mask of measured entries), names, classes, glom_covered.
Raw files stay in data_door/ (not committed)."""
import csv, os, numpy as np, re
HERE=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(HERE,"data_door")
def rd(f):
    with open(os.path.join(D,f),newline="",encoding="utf-8") as fh: return list(csv.reader(fh,delimiter=";"))
R=rd("door_response_matrix.csv"); O=rd("odor.csv"); Mp=rd("door_mappings.csv")
cols=R[0]; rows=R[1:]; names_o=[r[2] for r in O[1:]]; classes=[r[1] for r in O[1:]]
assert len(rows)==len(O)-1, (len(rows),len(O)-1)
gls=[str(g) for g in np.load(os.path.join(HERE,"..","fly-foraging","data","mb_circuit.npz"),allow_pickle=True)["gls"]]; gi={g:i for i,g in enumerate(gls)}
# mapping rows have one more field than the header (leading row index): receptor=row[1], sensillum=row[2], OSN=row[3], glomerulus=row[4], code=row[-2] (receptor code), code.OSN=row[-1]
col2glom={}
for r in Mp[1:]:
    rec,osn,glom=r[1],r[3],r[4]
    for key in (rec,osn,r[-1]):
        if key and key not in ("?","NA"): col2glom.setdefault(key,glom)
mapped={}
for j,c in enumerate(cols):
    g=col2glom.get(c) or col2glom.get(c.replace(".","+"))
    if g and g in gi: mapped[j]=gi[g]
U=np.zeros((len(rows),65)); has=np.zeros((len(rows),65),bool)
for i,r in enumerate(rows):
    vals=r[1:]                                     # first field is the row label
    for j,gidx in mapped.items():
        try: v=float(vals[j])
        except (ValueError,IndexError): continue
        if np.isnan(v): continue
        U[i,gidx]=max(U[i,gidx],v); has[i,gidx]=True
U=np.clip(U,0,1)
keep=np.array([n!="sfr" and has[i].sum()>=3 for i,n in enumerate(names_o)])
np.savez(os.path.join(HERE,"odours.npz"),U=U[keep],has=has[keep],names=np.array(names_o)[keep],classes=np.array(classes)[keep],glom=np.array(gls))
print("columns in response matrix:",len(cols),"| mapped to our glomeruli:",len(mapped),"| glomeruli covered:",len(set(mapped.values())),"of 65")
print("odorants kept (>=3 measured glomeruli):",int(keep.sum()),"of",len(rows),"| median measured per odorant:",int(np.median(has[keep].sum(1))))
print("fraction of entries > 0.5 among measured:",round(float((U[has]>0.5).mean()),3))
from collections import Counter; print(Counter(np.array(classes)[keep]).most_common(10))

"""Build aligned PN->KC matrices (65 glomeruli of the MaleCNS reference x KCs) for four hemispheres: MaleCNS R/L and FlyWire (female v783) R/L.
Run from study/ (uses core.py / core_fw.py). Writes fly-v4/individuals.npz."""
import numpy as np, sys, os, core, core_fw
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"individuals.npz")
ref=np.load("../fly-foraging/data/mb_circuit.npz",allow_pickle=True); gls=[str(g) for g in ref["gls"]]; P0=ref["P"]
out={"gls":np.array(gls)}; info={}
for name,c in(("M_R",core.build("R")),("M_L",core.build("L")),("F_R",core_fw.build("right")),("F_L",core_fw.build("left"))):
    cg=[str(g) for g in c.gls] if hasattr(c,"gls") else None
    if cg is None: print(name,"circuit has no gls attribute; attrs:",[a for a in dir(c) if not a.startswith("_")][:40]); sys.exit(1)
    A=np.zeros((len(gls),c.P.shape[1]),np.float32); hit=0
    for i,g in enumerate(cg):
        if g in gls: A[gls.index(g)]=c.P[i]; hit+=1
    out[name]=A; info[name]=(c.P.shape,hit,int((A.sum(1)>0).sum()),float(np.abs(A-P0).max()) if A.shape==P0.shape else None)
    print(name,info[name])
np.savez_compressed(OUT,**out)

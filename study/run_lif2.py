"""usage (engine venv, cwd=repos/drosophila-brain-mlx): run_lif_codes2.py GAIN APLMULT TAG -> ../../study/lif2_TAG_kc_counts.npy"""
import json, sys, time, numpy as np, pyarrow.feather as feather
sys.path.insert(0,"src")
from lif import core, engine_fused
import mlx.core as mx
gain,aplm,tag=float(sys.argv[1]),float(sys.argv[2]),sys.argv[3]
P=json.load(open("../../study/lif_prep.json")); pack=core.load_pack("data/pack/male_cns_v1")
idx={int(b):i for i,b in enumerate(pack.neuron_ids)}; kc_idx=np.array([idx[b] for b in P["kc_ids"]]); gls=P["gls"]; gl_idx={g:np.array([idx[b] for b in ids],dtype=np.int32) for g,ids in P["gl2ids"].items()}
tab=feather.read_table("../../data_annot/male_body_annotations.feather",columns=["bodyId","type"]); b=tab.column("bodyId").to_numpy(); t=tab.column("type").to_pylist()
apl=[idx[int(x)] for x,y in zip(b,t) if y=="APL" and int(x) in idx]; kc_all=[idx[int(x)] for x,y in zip(b,t) if y is not None and str(y).startswith("KC") and int(x) in idx]
rp=np.array(pack.row_ptr); sc0=np.array(pack.signed_counts).copy(); dst=np.array(pack.destinations); kcset=np.zeros(pack.n_neurons,bool); kcset[kc_all]=True
ae=np.concatenate([np.arange(rp[a],rp[a+1])[kcset[dst[rp[a]:rp[a+1]]]] for a in apl]); sc=sc0.copy(); sc[ae]=np.round(sc0[ae]*aplm).astype(np.int32); pack.signed_counts=mx.array(sc.astype(np.int32)); core.W_SYN=core.W_SYN*gain
specs=[("b",i,0,s) for i,s in enumerate(P["base"])]+[("v",i,j,s) for i,vs in enumerate(P["variants"]) for j,s in enumerate(vs)]
out=np.zeros((len(specs),len(kc_idx)),np.int16); t0=time.time()
for n,(kind,i,j,s) in enumerate(specs):
    tg=np.unique(np.concatenate([gl_idx[gls[g]] for g in s])).astype(np.int32); r=engine_fused.run(pack,core.make_stimulus_for(pack,tg,100.0,3000,seed=1000+n)); out[n]=r.spike_counts[kc_idx]
    if n%80==0: print(n,"/",len(specs),round(time.time()-t0),"s KC active %.4f"%((out[n]>0).mean()),flush=True)
np.save(f"../../study/lif2_{tag}_kc_counts.npy",out); json.dump(dict(kinds=[(k,i,j) for k,i,j,_ in specs],gain=gain,apl=aplm),open(f"../../study/lif2_{tag}_meta.json","w")); print("done",round(time.time()-t0),"s")

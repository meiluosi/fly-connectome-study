"""Run the MaleCNS LIF engine for each odor spec; save right-KC spike counts. Run with the engine venv, cwd = repos/drosophila-brain-mlx."""
import json, sys, time, numpy as np
sys.path.insert(0,"src")
from lif import core, engine_fused
P=json.load(open("../../study/lif_prep.json")); pack=core.load_pack("data/pack/male_cns_v1")
idx={int(b):i for i,b in enumerate(pack.neuron_ids)}; kc_idx=np.array([idx[b] for b in P["kc_ids"]])
gl_idx={g:np.array([idx[b] for b in ids],dtype=np.int32) for g,ids in P["gl2ids"].items()}; gls=P["gls"]
specs=[("b",i,0,s) for i,s in enumerate(P["base"])]+[("v",i,j,s) for i,vs in enumerate(P["variants"]) for j,s in enumerate(vs)]
NT=int(sys.argv[1]) if len(sys.argv)>1 else 3000; RATE=100.0; out=np.zeros((len(specs),len(kc_idx)),np.int16); t0=time.time(); tot=[]
for n,(kind,i,j,s) in enumerate(specs):
    tg=np.unique(np.concatenate([gl_idx[gls[g]] for g in s])).astype(np.int32)
    stim=core.make_stimulus_for(pack,tg,RATE,NT,seed=1000+n); r=engine_fused.run(pack,stim)
    out[n]=r.spike_counts[kc_idx]; tot.append(int(r.spike_counts.sum()))
    if n%40==0: print(n,"/",len(specs),round(time.time()-t0),"s  KC active %.3f  total spikes %d"%((out[n]>0).mean(),tot[-1]),flush=True)
    if n%160==159: np.save("../../study/lif_kc_counts_partial.npy",out[:n+1])
np.save("../../study/lif_kc_counts.npy",out); json.dump(dict(kinds=[(k,i,j) for k,i,j,_ in specs],n_ticks=NT,rate_hz=RATE,total_spikes=tot),open("../../study/lif_kc_meta.json","w")); print("done",round(time.time()-t0),"s")

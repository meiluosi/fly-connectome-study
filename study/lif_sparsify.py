"""Sweep global synaptic gain x APL->KC multiplier. Run with engine venv, cwd=repos/drosophila-brain-mlx. Output ../../study/lif_sweep.json"""
import json, sys, time, itertools, numpy as np, pyarrow.feather as feather
sys.path.insert(0,"src")
from lif import core, engine_fused
P=json.load(open("../../study/lif_prep.json")); pack=core.load_pack("data/pack/male_cns_v1")
idx={int(b):i for i,b in enumerate(pack.neuron_ids)}; kc_idx=np.array([idx[b] for b in P["kc_ids"]]); gls=P["gls"]
gl_idx={g:np.array([idx[b] for b in ids],dtype=np.int32) for g,ids in P["gl2ids"].items()}
ann=feather.read_table("../../data_annot/male_body_annotations.feather",columns=["bodyId","type","class"]).to_pandas() if False else None
tab=feather.read_table("../../data_annot/male_body_annotations.feather",columns=["bodyId","type"]); b=tab.column("bodyId").to_numpy(); t=tab.column("type").to_pylist()
apl=[idx[int(x)] for x,y in zip(b,t) if y=="APL" and int(x) in idx]; print("APL neurons:",len(apl),flush=True)
# all KC (both hemispheres) as APL targets
kc_all=[idx[int(x)] for x,y in zip(b,t) if y is not None and str(y).startswith("KC") and int(x) in idx]
rp=np.array(pack.row_ptr); sc0=np.array(pack.signed_counts).copy(); dst=np.array(pack.destinations); kcset=np.zeros(pack.n_neurons,bool); kcset[kc_all]=True
apl_edges=np.concatenate([np.arange(rp[a],rp[a+1])[kcset[dst[rp[a]:rp[a+1]]]] for a in apl]); print("APL->KC edges:",len(apl_edges),"mean signed count",float(sc0[apl_edges].mean()),flush=True)
import mlx.core as mx
rng=np.random.default_rng(999); NG=len(gls); specs=[sorted(rng.choice(NG,6,replace=False).tolist()) for _ in range(24)]
W_SYN0=core.W_SYN; res=[]; t0=time.time()
GRID=json.loads(sys.argv[1]) if len(sys.argv)>1 else dict(g=[1.0,0.7,0.5,0.4,0.3],a=[1,3,10]); OUT=sys.argv[2] if len(sys.argv)>2 else 'lif_sweep.json'
for gain,aplm in itertools.product(GRID['g'],GRID['a']):
    core.W_SYN=W_SYN0*gain; sc=sc0.copy(); sc[apl_edges]=sc0[apl_edges]*aplm; pack.signed_counts=mx.array(sc.astype(np.int32))
    codes=[]
    for n,s in enumerate(specs):
        tg=np.unique(np.concatenate([gl_idx[gls[g]] for g in s])).astype(np.int32); r=engine_fused.run(pack,core.make_stimulus_for(pack,tg,100.0,3000,seed=5000+n)); codes.append(r.spike_counts[kc_idx]>0)
    C=np.array(codes); act=C.mean(1); jac=np.mean([(C[i]&C[j]).sum()/max((C[i]|C[j]).sum(),1) for i in range(24) for j in range(i+1,24)])
    res.append(dict(gain=gain,apl=aplm,active=float(act.mean()),active_min=float(act.min()),active_max=float(act.max()),jaccard=float(jac),never=float((C.sum(0)==0).mean()),always=float((C.sum(0)==24).mean())))
    print(round(time.time()-t0),"s",json.dumps({k:(round(v,3) if isinstance(v,float) else v) for k,v in res[-1].items()}),flush=True)
core.W_SYN=W_SYN0; json.dump(res,open("../../study/"+OUT,"w"),indent=1); print("done")

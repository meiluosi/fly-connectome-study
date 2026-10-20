"""Stage 5: targeted lesions of KC classes defined on the training window (design pattern borrowed from WorldSimulationLab: archetypes defined on a training prefix, deterministic 50% subset, counterfactual lesion, matched random control).
Rankings (fixed a priori, outcome-free): hub = KC->MBON out-strength (summed N row, wiring-independent); active = activation frequency over the training odours (fraction of odours whose top-5% code contains the KC; depends on the PN->KC wiring).
Lesion: silence the top-m KCs of a ranking, m in {5%, 20%, 40%} of all KCs; control: m KCs drawn at random.
Imports the frozen v4core / v4core_b unchanged."""
import numpy as np, v4core as V, v4core_b as B
NK=V.NK; FRAC=0.10
DOSES=(102,409,818)                             # 5%, 20%, 40% of the 2045 KCs
def order(trU,P,rng):
    """KC rankings: by KC->MBON out-strength (hub) and by activation frequency over the training odours (active); ties by index"""
    codes=V.codes_for(trU,P,rng); freq=np.bincount(codes.ravel(),minlength=NK)/len(trU)
    return np.argsort(-V.N.sum(1),kind="stable"),np.argsort(-freq,kind="stable"),freq
def run(task,seed,kind,eta=0.05,n_trials=400):
    trU,trY,teU,teY=B.make_world(task,seed); rng=np.random.default_rng(seed+1000); acc=lambda v:float((np.sign(v+1e-12)==teY).mean())
    P=V.make_P(kind,rng); hub,act,freq=order(trU,P,rng); ctr=V.codes_for(trU,P,rng); cte=V.codes_for(teU,P,rng); b0t,sct=V.b0sc(cte); M=V.MBL(eta)
    for t in range(n_trials):
        i=t%len(trU); c=ctr[i]; b0,sc=V.b0sc(c[None]); M.update(c,trY[i]-float(M.val(c[None],b0,sc)[0]))
    out={"intact":acc(M.val(cte,b0t,sct))}; perm=rng.permutation(NK)
    for m in DOSES:
        for name,s in(("hub",hub[:m]),("active",act[:m]),("random",perm[:m])):
            cs=B.codes_masked(teU,P,rng,s); b0s,scs=V.b0sc(cs); out[f"post_{name}_{m}"]=acc(M.val(cs,b0s,scs))   # trained synapses kept, KCs silenced at test
            M2=V.MBL(eta); c2=B.codes_masked(trU,P,rng,s)                                                          # KCs absent from training and test
            for t in range(n_trials):
                i=t%len(trU); c=c2[i]; b0,sc=V.b0sc(c[None]); M2.update(c,trY[i]-float(M2.val(c[None],b0,sc)[0]))
            out[f"pre_{name}_{m}"]=acc(M2.val(cs,b0s,scs))
    return out

"""Stage 5b: targeted lesions at the glomerulus (PN channel) level. Hub glomerulus = high KC fan-out; bridger glomerulus = fan-out spread across the three KC lobe groups
(g, ab, a'b'), participation coefficient PC = 1 - sum_g (k_g/k)^2, computed among glomeruli with above-median fan-out. Rankings computed from the wiring in use (so shuffled/random wirings get their own).
Lesion = the odour channel is silenced (set to 0) for all odours. Imports frozen v4core / v4core_b unchanged."""
import numpy as np, v4core as V, v4core_b as B
_d=np.load(V.os.path.join(V.HERE,"..","fly-foraging","data","mb_circuit.npz"),allow_pickle=True)
def _grp(t): return 0 if t.startswith("KCg") else 1 if t.startswith("KCab") else 2
GRP=np.array([_grp(str(t)) for t in _d["kc_type"]]); NG=V.NG
DOSES=(3,7,13)                                     # about 5%, 10%, 20% of the 65 glomeruli
def rankings(P):
    fan=(P>0).sum(1).astype(float); G=np.stack([((P>0)[:,GRP==g]).sum(1) for g in range(3)],1).astype(float)
    pc=1-((G/np.maximum(fan[:,None],1))**2).sum(1); elig=fan>=np.median(fan)
    hub=np.argsort(-fan,kind="stable"); score=np.where(elig,pc,-1.0); bridger=np.argsort(-score,kind="stable")
    return hub,bridger,fan,pc
def run(task,seed,kind,eta=0.05,n_trials=400):
    trU,trY,teU,teY=B.make_world(task,seed); rng=np.random.default_rng(seed+1000); acc=lambda v:float((np.sign(v+1e-12)==teY).mean())
    P=V.make_P(kind,rng); hub,bridger,fan,pc=rankings(P); perm=rng.permutation(NG)
    def train(U):
        c=V.codes_for(U,P,rng); M=V.MBL(eta)
        for t in range(n_trials):
            i=t%len(U); b0,sc=V.b0sc(c[i][None]); M.update(c[i],trY[i%len(trY)]-float(M.val(c[i][None],b0,sc)[0]))
        return M
    def test(M,U): c=V.codes_for(U,P,rng); b0,sc=V.b0sc(c); return acc(M.val(c,b0,sc))
    M=train(trU); out={"intact":test(M,teU),"overlap_hub_bridger_7":int(len(set(hub[:7])&set(bridger[:7])))}
    for m in DOSES:
        for name,s in(("hub",hub[:m]),("bridger",bridger[:m]),("random",perm[:m])):
            mask=np.ones(NG); mask[s]=0
            out[f"post_{name}_{m}"]=test(M,teU*mask)                         # trained synapses kept, channels silenced at test
            out[f"pre_{name}_{m}"]=test(train(trU*mask),teU*mask)            # channels absent throughout
    return out

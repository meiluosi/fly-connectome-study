import numpy as np, learn_v3 as L
P,NK,grp,NG=L.P,L.NK,L.grp,L.NG
tot=P.sum(0); deg=(P>0).sum(0)
print("KCs with zero PN input:",int((tot==0).sum()),"| by subtype:",{g:int(((tot==0)&(grp==g)).sum()) for g in ["g","ab","a'b'","o"]})
print("PN input (synapses) median by subtype:",{g:float(np.median(tot[grp==g])) for g in ["g","ab","a'b'"]})
print("glomerular in-degree mean by subtype:",{g:round(float(deg[grp==g].mean()),2) for g in ["g","ab","a'b'"]})
def codes(variant,n=400,seed=0,kact=0.05):
    r=np.random.default_rng(seed); X=[]
    for _ in range(n):
        x=np.zeros(NG); x[r.choice(NG,6,replace=False)]=r.uniform(.5,1,6); s=x@P
        if variant=="norm": s=s/np.maximum(tot,1)**0.5          # divide by sqrt(total PN input): input-normalised
        if variant=="sub":  # per-subtype top-k (homeostatic per lobe class)
            o=np.zeros(NK)
            for g in ["g","ab","a'b'"]:
                idx=np.where(grp==g)[0]; k=int(kact*len(idx)); o[idx[np.argsort(-s[idx])[:k]]]=1
            X.append(o); continue
        o=np.zeros(NK); o[np.argsort(-s)[:int(kact*NK)]]=1; X.append(o)
    return np.array(X)
for v in ["global","norm","sub"]:
    X=codes(v); f=X.mean(0)
    print(f"{v:7s} dead={float((X.sum(0)==0).mean()):.3f}  subtype density={ {g:round(float(X[:,grp==g].mean()),3) for g in ['g','ab',chr(97)+chr(39)+'b'+chr(39)]} }  max single-KC firing prob={f.max():.2f}  mean odor-overlap(Jaccard)={np.mean([ (X[i]*X[j]).sum()/((X[i]+X[j])>0).sum() for i in range(0,200,2) for j in range(1,200,2)]):.3f}")

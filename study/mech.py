import numpy as np, sweep_lib as SL, learn_v3 as L
from scipy import stats
NK,NM,NC=L.NK,L.NM,L.NC; Nb=L.Nbin; N=L.Nsyn
def run(cond,T,seed,alloc="random",coding="pn",n_odor=5,eta=0.3,reps=3,cpt=2):
    rt=np.random.default_rng(seed); rc=np.random.default_rng(10_000+seed)
    odor=SL.odor_fn(coding,rt); Mc=L.M[rc.permutation(NM)] if cond=="shuffled" else L.M
    perm=rt.permutation(NC); pool=perm[:4]
    probe=np.array([odor() for _ in range(40)]); q=np.full(N.shape,0.5); tasks=[]; learned=np.zeros(T)
    def score(O,gm,y):
        nv=(probe@(N*q))[:,gm].mean(); return y*((O@(N*q))[:,gm].mean()-nv)/nv
    for t in range(T):
        O=np.array([odor() for _ in range(n_odor)]); y=rt.choice([-1,1])
        C={"random":lambda:rt.choice(NC,cpt,replace=False),"concentrated":lambda:rt.choice(pool,cpt,replace=False),
           "roundrobin":lambda:np.array([perm[(cpt*t)%NC],perm[(cpt*t+1)%NC]])}[alloc]()
        gm=np.ones(NM,bool) if cond=="none" else Mc[:,C].any(1)
        if not gm.any(): gm=np.ones(NM,bool)
        tasks.append((O,gm,y,O.max(0)>0))
        for _ in range(reps):
            for x in O:
                A=x[:,None]
                if y<0: q[:,gm]-=eta*A*q[:,gm]*Nb[:,gm]
                else:   q[:,gm]+=eta*A*(1-q[:,gm])*Nb[:,gm]
        learned[t]=score(*tasks[t][:3])
    final=np.array([score(*tk[:3]) for tk in tasks]); forg=(learned-final).mean()
    # per-task gating geometry
    cos=[];edges=[];
    for O,gm,y,_ in tasks:
        B=Nb[:,gm].astype(float); edges.append(B.sum())
        if gm.sum()>1:
            Z=B/np.maximum(np.linalg.norm(B,axis=0),1e-9); G=Z.T@Z; cos.append((G.sum()-np.trace(G))/(gm.sum()*(gm.sum()-1)))
    # interference predictor: shared (KC,MBON) synapses touched by both tasks of OPPOSITE label
    opp=[];same=[]
    for i in range(T):
        for j in range(i+1,T):
            Oi,gi,yi,ai=tasks[i]; Oj,gj,yj,aj=tasks[j]
            sh=(Nb[ai][:,gi&gj][:, :].astype(bool) & aj[ai][:,None]).sum() if (gi&gj).any() else 0
            (opp if yi!=yj else same).append(sh)
    return dict(forg=forg,learned=learned.mean(),cos=np.mean(cos),edges=np.mean(edges),opp=np.mean(opp),same=np.mean(same))
if __name__=="__main__":
    S=100;T=12
    for alloc in ["random","roundrobin"]:
        R={c:[run(c,T,s,alloc) for s in range(S)] for c in ["real","shuffled","none"]}
        print(f"\n=== alloc={alloc}, T={T}, {S} paired seeds")
        for c in R: print(f"  {c:9s}", {k:round(float(np.mean([r[k] for r in R[c]])),3) for k in ["forg","cos","edges","opp","same"]})
        for k in ["cos","edges","opp"]:
            d=np.array([a[k]-b[k] for a,b in zip(R["real"],R["shuffled"])]); m=[d[np.random.default_rng(i).integers(0,S,S)].mean() for i in range(2000)]
            print(f"  real-shuffled {k:6s}: {d.mean():+.4f} [{np.percentile(m,2.5):+.4f},{np.percentile(m,97.5):+.4f}]")
        allr=[(r["opp"],r["forg"],c) for c in R for r in R[c]]
        x=np.array([a for a,_,_ in allr]); y=np.array([b for _,b,_ in allr]); print(f"  pooled (3 conds) spearman(opp-shared synapses, forgetting) = {stats.spearmanr(x,y)[0]:.3f}")
        for c in ["real","shuffled"]:
            xs=np.array([r['opp'] for r in R[c]]); ys=np.array([r['forg'] for r in R[c]]); print(f"  within {c:8s}: spearman = {stats.spearmanr(xs,ys)[0]:.3f}")
        dx=np.array([a['opp']-b['opp'] for a,b in zip(R['real'],R['shuffled'])]); dy=np.array([a['forg']-b['forg'] for a,b in zip(R['real'],R['shuffled'])])
        print(f"  paired-diff spearman(d_opp, d_forg) across seeds = {stats.spearmanr(dx,dy)[0]:.3f}")

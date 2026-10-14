"""Framework-agnostic continual-learning metrics and matched-learning (stability-plasticity frontier) comparison.
R[i][j] = accuracy on task j after training on task i (i>=j meaningful). All functions take numpy arrays."""
import numpy as np

def learning_acc(R):            # mean accuracy on each task right after learning it (plasticity)
    return float(np.mean(np.diag(R)))
def final_acc(R):               # mean accuracy over all tasks after the last one
    return float(np.mean(R[-1]))
def forgetting(R, include_last=False):
    """Mean over tasks of (accuracy just after learning - final accuracy). Standard definition excludes the last task
    (its forgetting is 0 by construction); include_last=True reproduces the convention used in the fly-MB study."""
    T=R.shape[0]; js=range(T) if include_last else range(T-1)
    return float(np.mean([R[j][j]-R[-1][j] for j in js]))
def norm_forgetting(R, chance):
    """Forgetting divided by the room available to forget, (learning acc - chance). Undefined if learning acc <= chance."""
    la=np.mean([R[j][j] for j in range(R.shape[0]-1)])-chance
    return float(forgetting(R)/la) if la>1e-9 else float("nan")
def bwt(R):                     # backward transfer = -forgetting when measured from R[j][j]
    return -forgetting(R)
def intransigence(R, ref):      # ref[j] = accuracy of a reference learner (e.g. joint training) on task j
    return float(np.mean([ref[j]-R[j][j] for j in range(R.shape[0])]))

def interp_at(learn, forg, target):
    """Per-seed interpolation of forgetting at a learning-accuracy target along a hyperparameter sweep.
    learn, forg: arrays (n_settings, n_seeds). Returns array (n_seeds,) with NaN where the sweep does not cover the target."""
    out=np.full(learn.shape[1],np.nan)
    for s in range(learn.shape[1]):
        o=np.argsort(learn[:,s]); x,y=learn[o,s],forg[o,s]
        if x[0]<=target<=x[-1]: out[s]=np.interp(target,x,y)
    return out

def matched_diff(learnA, forgA, learnB, forgB, targets, margin=0.02, min_n=None, n_boot=4000, seed=0):
    """Compare forgetting of method A minus method B at matched learning accuracy.
    Each cell is 'incomparable' unless both sweeps cover the target for >= min_n seeds (default 75% of seeds).
    Status: 'equivalent' if the 95% bootstrap CI lies within +-margin; 'A_worse' if CI > +margin; 'A_better' if CI < -margin; else 'inconclusive'."""
    rng=np.random.default_rng(seed); n=learnA.shape[1]; min_n=min_n or int(np.ceil(0.75*n)); rows=[]
    for t in targets:
        a,b=interp_at(learnA,forgA,t),interp_at(learnB,forgB,t); ok=~np.isnan(a)&~np.isnan(b); k=int(ok.sum())
        if k<min_n: rows.append(dict(target=t,n=k,status="incomparable")); continue
        d=(a-b)[ok]; m=np.array([d[rng.integers(0,k,k)].mean() for _ in range(n_boot)]); lo,hi=np.percentile(m,[2.5,97.5])
        st="equivalent" if lo>-margin and hi<margin else "A_worse" if lo>margin else "A_better" if hi<-margin else "inconclusive"
        rows.append(dict(target=t,n=k,mean=float(d.mean()),lo=float(lo),hi=float(hi),status=st))
    return rows

def frontier_area_gap(learnA, forgA, learnB, forgB, lo, hi, n_grid=50):
    """Mean forgetting difference (A-B) over the learning range [lo,hi] covered by both sweeps (seed-averaged curves). NaN if no overlap."""
    mA=np.array([learnA.mean(1),forgA.mean(1)]); mB=np.array([learnB.mean(1),forgB.mean(1)])
    oA,oB=np.argsort(mA[0]),np.argsort(mB[0]); xa,ya,xb,yb=mA[0][oA],mA[1][oA],mB[0][oB],mB[1][oB]
    lo_,hi_=max(lo,xa[0],xb[0]),min(hi,xa[-1],xb[-1])
    if lo_>=hi_: return float("nan")
    g=np.linspace(lo_,hi_,n_grid); return float(np.mean(np.interp(g,xa,ya)-np.interp(g,xb,yb)))

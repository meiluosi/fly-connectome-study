"""Class-incremental benchmark scaffold + FlyModel (per REPLICATION_NOTES.md). numpy only."""
import numpy as np
def load(name):
    d=np.load(f"data/features/{name}.npz"); return d["Xtr"].astype(np.float32),d["ytr"],d["Xte"].astype(np.float32),d["yte"]
def task_classes(n_classes,per_task): return [list(range(i,i+per_task)) for i in range(0,n_classes,per_task)]
def class_incremental_eval(model, Xtr,ytr,Xte,yte, tasks, seed):
    """Train model sequentially (model.learn_class(X, c) per class, samples shuffled by seed). After each task, accuracy on each learned task's test classes,
    predicting only among classes seen so far. Returns R[i][j] (j<=i, NaN above diagonal) and acc over all seen classes per step."""
    rng=np.random.default_rng(seed); T=len(tasks); R=np.full((T,T),np.nan); seen=[]; allseen=[]
    for i,cls in enumerate(tasks):
        for c in cls:
            idx=np.where(ytr==c)[0]; rng.shuffle(idx); model.learn_class(Xtr[idx],c)
        seen+=cls; mask=np.isin(yte,seen); pred=model.predict(Xte[mask],seen); yy=yte[mask]
        allseen.append(float((pred==yy).mean()))
        for j in range(i+1):
            mj=np.isin(yy,tasks[j]); R[i][j]=float((pred[mj]==yy[mj]).mean())
    return R,np.array(allseen)

class FlyModel:
    """Fixed sparse random expansion (m KCs, each summing s random inputs) -> top-l WTA -> divide by max -> Hebbian class-sum weights clipped to [0,1]."""
    def __init__(s,d,m,k_inputs,l,beta,n_classes,seed,clip=1.0):
        rng=np.random.default_rng(seed); s.m,s.l,s.beta,s.clip=m,l,beta,clip; s.W=np.zeros((m,n_classes),np.float32)
        s.idx=np.stack([rng.choice(d,k_inputs,replace=False) for _ in range(m)])        # (m, k_inputs)
        s.Theta=np.zeros((m,d),np.float32); np.put_along_axis(s.Theta,s.idx,1.0,axis=1)
    def phi(s,X,chunk=2000):
        out=[]
        for i in range(0,len(X),chunk):
            psi=X[i:i+chunk]@s.Theta.T; top=np.argpartition(-psi,s.l-1,axis=1)[:,:s.l]; ph=np.zeros_like(psi); np.put_along_axis(ph,top,np.take_along_axis(psi,top,1),axis=1)
            mx=ph.max(1,keepdims=True); mx[mx==0]=1; out.append(ph/mx)
        return np.concatenate(out)
    def learn_class(s,X,c):
        ph=s.phi(X); s.W[:,c]=np.minimum(s.clip,s.W[:,c]+s.beta*ph.sum(0))     # exact: increments >=0, so clip-after-sum == clip-each-step
    def predict(s,X,seen):
        sc=s.phi(X)@s.W[:,seen]; return np.array(seen)[sc.argmax(1)]
def summarize(R,allseen):
    T=R.shape[0]; ml=np.mean([R[j][j]-R[T-1][j] for j in range(T)])
    return dict(acc_final=float(allseen[-1]),acc_half=float(allseen[T//2-1]),mem_loss=float(ml),learn_acc=float(np.mean(np.diag(R))))

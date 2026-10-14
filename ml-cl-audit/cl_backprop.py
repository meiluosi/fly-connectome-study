"""Backprop baselines for class-incremental learning: vanilla fine-tune, online EWC (diagonal Fisher accumulated, single anchor), ER (reservoir), and a joint/offline upper bound.
Architecture per the paper: d -> 40*d ReLU -> K. Logits of not-yet-seen classes are masked in both loss and prediction."""
import numpy as np, torch, torch.nn as nn
def _net(d,K,mult,seed):
    torch.manual_seed(seed); return nn.Sequential(nn.Linear(d,mult*d),nn.ReLU(),nn.Linear(mult*d,K))
def _masked(logits,seen_mask): return logits.masked_fill(~seen_mask,-1e9)
def _stream(Xtr,ytr,cls_list,rng,epochs,interleave=False):
    """Yield index arrays per epoch. Epoch 1 is class-ordered (as in the paper); later epochs shuffle the task's data jointly."""
    per=[np.where(ytr==c)[0] for c in cls_list]; allidx=np.concatenate(per)
    first=rng.permutation(allidx) if interleave else np.concatenate([rng.permutation(p) for p in per]); yield first
    for _ in range(epochs-1): yield rng.permutation(allidx)
def run_backprop(method,Xtr,ytr,Xte,yte,tasks,K,hp,seed,epochs=1,bs=10,mult=40,fisher_n=500,threads=3,device='cpu',interleave=False):
    torch.set_num_threads(threads); dev=torch.device(device); rng=np.random.default_rng(seed); d=Xtr.shape[1]; net=_net(d,K,mult,seed).to(dev)
    opt=torch.optim.Adam(net.parameters(),lr=hp["lr"]); Xt=torch.tensor(Xtr).to(dev); yt=torch.tensor(ytr).long().to(dev); Xe=torch.tensor(Xte).to(dev); ye=np.asarray(yte)
    seen=[]; seen_mask=torch.zeros(K,dtype=torch.bool,device=dev); R=np.full((len(tasks),len(tasks)),np.nan); allseen=[]
    lam=hp.get("lam",0.0); F=[torch.zeros_like(p) for p in net.parameters()]; anchor=[p.detach().clone() for p in net.parameters()]
    M=hp.get("buffer",0); bufX=torch.zeros((M,d),device=dev) if M else None; bufy=torch.zeros(M,dtype=torch.long,device=dev) if M else None; nseen_total=0
    for ti,cls in enumerate(tasks):
        seen+=cls; seen_mask[cls]=True
        for order in _stream(Xtr,ytr,cls,rng,epochs,interleave):
            for i in range(0,len(order),bs):
                idx=order[i:i+bs]; tidx=torch.as_tensor(idx,device=dev); xb,yb=Xt[tidx],yt[tidx]
                if M and nseen_total>0:
                    k=min(bs,min(nseen_total,M)); ri=torch.as_tensor(rng.integers(0,min(nseen_total,M),k),device=dev); xb=torch.cat([xb,bufX[ri]]); yb=torch.cat([yb,bufy[ri]])
                loss=nn.functional.cross_entropy(_masked(net(xb),seen_mask),yb); opt.zero_grad(); loss.backward()
                if lam>0:
                    for p,f,a in zip(net.parameters(),F,anchor): p.grad+=lam*f*(p.detach()-a)
                opt.step()
                if M:                                                   # reservoir update with the CURRENT (non-replayed) samples
                    for j in idx:
                        if nseen_total<M: bufX[nseen_total]=Xt[j]; bufy[nseen_total]=yt[j]
                        else:
                            r=int(rng.integers(0,nseen_total+1))
                            if r<M: bufX[r]=Xt[j]; bufy[r]=yt[j]
                        nseen_total+=1
        if lam>0:                                                       # accumulate diagonal empirical Fisher on this task, move the anchor
            sub=rng.choice(np.concatenate([np.where(ytr==c)[0] for c in cls]),min(fisher_n,sum((ytr==c).sum() for c in cls)),replace=False); Ft=[torch.zeros_like(p) for p in net.parameters()]
            for j in sub:
                net.zero_grad(); nn.functional.cross_entropy(_masked(net(Xt[j:j+1]),seen_mask),yt[j:j+1]).backward()
                for f,p in zip(Ft,net.parameters()): f+=p.grad.detach()**2
            F=[f+ft/len(sub) for f,ft in zip(F,Ft)]; anchor=[p.detach().clone() for p in net.parameters()]
        net.eval()
        with torch.no_grad(): mask=np.isin(ye,seen); pred=_masked(net(Xe[torch.as_tensor(mask,device=dev)]),seen_mask).argmax(1).cpu().numpy(); yy=ye[mask]
        net.train(); allseen.append(float((pred==yy).mean()))
        for j in range(ti+1): mj=np.isin(yy,tasks[j]); R[ti][j]=float((pred[mj]==yy[mj]).mean())
    return R,np.array(allseen)
def run_offline(Xtr,ytr,Xte,yte,K,lr,epochs,seed,bs=128,mult=40,threads=3):
    """Joint training on all classes; returns test accuracy after each epoch (caller selects the epoch on validation)."""
    torch.set_num_threads(threads); net=_net(Xtr.shape[1],K,mult,seed); opt=torch.optim.Adam(net.parameters(),lr=lr); Xt=torch.tensor(Xtr); yt=torch.tensor(ytr).long(); Xe=torch.tensor(Xte); rng=np.random.default_rng(seed); accs=[]
    for ep in range(epochs):
        p=rng.permutation(len(Xt))
        for i in range(0,len(p),bs): idx=p[i:i+bs]; loss=nn.functional.cross_entropy(net(Xt[idx]),yt[idx]); opt.zero_grad(); loss.backward(); opt.step()
        with torch.no_grad(): accs.append(float((net(Xe).argmax(1).numpy()==np.asarray(yte)).mean()))
    return accs

"""Stage 2: do the model arms reproduce known qualitative fly learning phenomena? Imports frozen v4core unchanged.
P1 generalisation gradient with odour overlap; P2 loss of feedback inhibition (denser KC code, 5% -> 20%) reduces the valence separation between trained similar odours (A+ vs A'-) of similar but not dissimilar odours;
P3 reversal learning; P4 extinction. All with a fixed learning rate ETA, no tuning."""
import numpy as np, v4core as V
NG,NK=V.NG,V.NK; ETA=0.05; OV=(6,5,4,3,2,0); NTRAIN=10; NREV=30
def odour(glom): u=np.zeros(NG); u[list(glom)]=1; return u
def variant(A,o,rng):
    """odour sharing o glomeruli with A (A is a 6-set); remaining glomeruli drawn from outside A"""
    keep=rng.choice(A,o,replace=False); out=[g for g in range(NG) if g not in set(int(x) for x in A)]; fill=rng.choice(out,6-o,replace=False); return odour(list(keep)+list(fill))
def val(M,u,P,rng):
    c=V.codes_for(u[None],P,rng); b0,sc=V.b0sc(c); return float(M.val(c,b0,sc)[0]),c[0]
def train(M,u,y,P,rng):
    v,c=val(M,u,P,rng); b0,sc=V.b0sc(c[None]); M.update(c,y-v); return v
def kindP(kind,rng): return V.make_P(kind,rng)
def world(kind,seed):
    rng=np.random.default_rng(seed); P=kindP(kind,rng); A=rng.choice(NG,6,replace=False); out={}
    # P1 gradient
    M=V.MBL(ETA)
    for _ in range(NTRAIN): train(M,odour(A),1.0,P,rng)
    out["G"]=[float(np.mean([val(M,variant(A,o,rng) if o<6 else odour(A),P,rng)[0] for _ in range(10)])) for o in OV]
    # P2 discrimination with sparse (5%) vs dense (20%) code
    for kf,name in((0.05,"s"),(0.20,"d")):
        old=V.KFRAC; V.KFRAC=kf
        try:
            for o,tag in((5,"sim"),(0,"dis")):
                acc=[]
                for _ in range(5):
                    M=V.MBL(ETA); a=odour(A); b=variant(A,o,rng)
                    for t in range(NTRAIN): train(M,a,1.0,P,rng); train(M,b,-1.0,P,rng)
                    acc.append(0.5*(val(M,a,P,rng)[0]-val(M,b,P,rng)[0]))
                out[f"sep_{tag}_{name}"]=float(np.mean(acc))
        finally: V.KFRAC=old
    # P3 reversal, P4 extinction
    for tag,y2 in(("rev",-1.0),("ext",0.0)):
        M=V.MBL(ETA); a=odour(A)
        for _ in range(NTRAIN): train(M,a,1.0,P,rng)
        v0=val(M,a,P,rng)[0]; vs=[train(M,a,y2,P,rng) for _ in range(NREV)]
        if tag=="rev": out["flip"]=float(next((i for i,v in enumerate(vs) if v<0),NREV)); out["v_peak"]=v0
        else: out["ratio"]=float(vs[-1]/v0) if v0>1e-6 else float("nan")
    return out

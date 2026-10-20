"""Stage 4: compartment-specific, dopamine-timed learning. Imports frozen v4core unchanged (original 2045 KCs, real PN->KC wiring P0).
MBON clusters from the MaleCNS compartment labels: PAM compartments (reward DAN) = {g3,g4,g5,b1,b2,b'1,b'2,a1}, PPL1 compartments (punishment DAN) = {g1,g2,a'1,a'2,a'3,a2,a3};
an MBON takes the cluster of its first primary compartment; the calyx MBON has none and does not learn.
Rule COMP: dopamine signals are prediction errors, D_PAM = relu(R - V) (reward), D_PPL = relu(V - R) (punishment); an MBON's KC synapses depress in proportion to the dopamine of its own cluster."""
import os, sys, numpy as np, v4core as V
sys.path.insert(0,os.path.join(V.HERE,"..","study")); from compartments import canon
PAM={"y3","y4","y5","B1","B2","B'1","B'2","a1"}; PPL={"y1","y2","a'1","a'2","a'3","a2","a3"}
_d=np.load(os.path.join(V.HERE,"..","fly-foraging","data","mb_circuit.npz"),allow_pickle=True)
def _cl(c):
    if c=="calyx": return 0
    p=canon(c)["primary"]
    return 1 if p and p[0] in PAM else -1 if p and p[0] in PPL else 0
CL_REAL=np.array([_cl(c) for c in _d["mbon_comp"]],float)       # +1 PAM, -1 PPL1, 0 none
N,SIGNS,NB,NK,NG=V.N,V.SIGNS,V.NB,V.NK,V.NG
def clusters(arm,rng):
    if arm in("comp_real","unsigned"): return CL_REAL.copy()
    if arm=="comp_shuf": return rng.permutation(CL_REAL)
    if arm=="comp_shufbal":                     # permute labels but keep the summed KC->MBON synapse mass of each cluster within 10% of the real one
        nz=np.flatnonzero(CL_REAL!=0); tgt=[N[:,CL_REAL>0].sum(),N[:,CL_REAL<0].sum()]
        for _ in range(5000):
            c=np.zeros_like(CL_REAL); c[nz]=rng.permutation(CL_REAL[nz])
            if abs(N[:,c>0].sum()/tgt[0]-1)<0.1 and abs(N[:,c<0].sum()/tgt[1]-1)<0.1: return c
        raise RuntimeError("no balanced permutation")
    raise ValueError(arm)
class COMP:
    ROLE=True
    def __init__(s,eta,arm,rng,lam=0.0):
        s.q=np.full(N.shape,0.5); s.eta=eta; s.arm=arm; s.cl=clusters(arm,rng); s.lam=lam
    def sgn(s): return -s.cl if s.ROLE else SIGNS          # readout sign per MBON
    def val(s,codes,b0,sc):
        sg=s.sgn(); w=(N*s.q)@sg; b0r=0.5*(N@sg)[codes].sum(1); scr=0.5*(N@np.abs(sg))[codes].sum(1)
        return np.clip((w[codes].sum(1)-b0r)/np.maximum(scr,1e-9),-1,1)
    def dan(s,e):
        if s.arm=="unsigned": return np.where(s.cl!=0,abs(e),0.0)
        return np.where(s.cl>0,max(e,0.0),np.where(s.cl<0,max(-e,0.0),0.0))
    def update(s,code,e,gate=None):
        """e = R - V; gate: optional per-cluster multiplier (e.g. ablation) ; trace=1 for plain coincidence"""
        g=s.eta*s.dan(e)
        if gate is not None: g=g*gate
        rows=NB[code]; q=s.q[code]; s.q[code]=q-g[None,:]*rows*q
        if s.lam>0: s.q+=s.lam*(0.5-s.q)
def run(task,seed,arm,eta,n_trials=400,eval_every=10,lam=0.0):
    """supervised odour-valence stream (R = label). arm in comp_real/comp_shuf/unsigned/global (global = the stage 0 bounded delta rule)"""
    import v4core_b as B
    trU,trY,teU,teY=B.make_world(task,seed); rng=np.random.default_rng(seed+1000); acc=lambda v:float((np.sign(v+1e-12)==teY).mean())
    ctr=V.codes_for(trU,V.P0,rng); cte=V.codes_for(teU,V.P0,rng); b0t,sct=V.b0sc(cte)
    M=V.MBL(eta) if arm=="global" else COMP(eta,arm,rng,lam); curve=[]
    for t in range(n_trials+1):
        if t%eval_every==0: curve.append(acc(M.val(cte,b0t,sct)))
        if t==n_trials: break
        i=t%len(trU); c=ctr[i]; b0,sc=V.b0sc(c[None]); e=trY[i]-float(M.val(c[None],b0,sc)[0]); M.update(c,e)
    c=np.array(curve); return dict(auc=float(c.mean()),acc50=float(c[50//eval_every]),final=float(c[-1]))

TAU_E,TAU_D,T_ODOUR,RHO=1.5,1.5,2.0,1.0
def pairing(arm,rng,codes,R,isi,eta=0.3,n_pair=3,ablate=None,timing=True):
    """single odour, n_pair pairings with a dopamine pulse (R=+1 reward -> PAM, R=-1 punishment -> PPL) at time isi relative to odour onset (odour lasts T_ODOUR).
    forward (isi>=0): depression of the coincident synapses, eligibility decays after odour offset; backward (isi<0): potentiation, proportional to the remaining dopamine trace at odour onset.
    returns the valence after training (centred as in COMP.val)"""
    M=COMP(eta,arm,rng); b0,sc=0.0,1.0
    gate=np.ones_like(M.cl)
    if ablate=="PAM": gate=np.where(M.cl>0,0.0,1.0)
    if ablate=="PPL": gate=np.where(M.cl<0,0.0,1.0)
    D=np.where(M.cl>0,max(R,0.0),np.where(M.cl<0,max(-R,0.0),0.0))*gate
    elig=np.exp(-max(isi-T_ODOUR,0.0)/TAU_E) if isi>=0 else 0.0
    trace=np.exp(-abs(isi)/TAU_D) if isi<0 else 0.0
    if not timing: trace=0.0
    for _ in range(n_pair):
        rows=NB[codes]; q=M.q[codes]
        q=q-eta*D[None,:]*elig*rows*q
        q=q+eta*RHO*D[None,:]*trace*rows*(1-q)
        M.q[codes]=q
    return float(M.val(codes[None,:],np.zeros(1),np.ones(1))[0])
# ---------------------------------------------------------------- continual learning: 4 sequential tasks of 10 odours with random +-1 labels
NT_TASKS,N_PER,TRIALS_PER=4,10,100
def run_cl(seed,arm,eta):
    """retention of earlier tasks after learning later ones. odours from the DoOR pool, labels random +-1 (memorisation, not generalisation).
    returns final = mean accuracy over all 40 odours at the end, after = mean accuracy of each task right after it was learned, forgetting = (after - final)/(after - 0.5)"""
    D,_=V.door(); rng=np.random.default_rng(seed); idx=rng.choice(len(D),NT_TASKS*N_PER,replace=False); U=D[idx]; y=rng.choice([-1.0,1.0],len(idx))
    rng2=np.random.default_rng(seed+1000); codes=V.codes_for(U,V.P0,rng2); b0,sc=V.b0sc(codes)
    M=V.MBL(eta) if arm=="global" else COMP(eta,arm,rng2)
    acc=lambda sl:float((np.sign(M.val(codes[sl],b0[sl],sc[sl])+1e-12)==y[sl]).mean())
    after=[]
    for k in range(NT_TASKS):
        sl=slice(k*N_PER,(k+1)*N_PER)
        for t in range(TRIALS_PER):
            i=k*N_PER+t%N_PER; c=codes[i]; v=float(M.val(c[None],b0[i:i+1],sc[i:i+1])[0]); M.update(c,y[i]-v)
        after.append(acc(sl))
    fin=acc(slice(0,len(idx))); fin_by=[acc(slice(k*N_PER,(k+1)*N_PER)) for k in range(NT_TASKS)]
    a=float(np.mean(after)); return dict(final=fin,after=a,forgetting=float((a-fin)/max(a-0.5,1e-3)),first_final=fin_by[0],last_final=fin_by[-1])

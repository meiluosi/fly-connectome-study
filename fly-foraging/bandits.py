"""Non-stationary bandit ('foraging') environments and baseline algorithms. numpy only.
Env: K arms (odour patches), Bernoulli reward probabilities p[t,k] that change over time. Rewards use pre-drawn uniforms u[t,k] (common random numbers),
so every algorithm faces the identical realised environment -> paired comparisons. Metric: cumulative pseudo-regret vs the per-step best arm."""
import numpy as np
class Env:
    def __init__(s,K=8,T=2000,kind="switch",seed=0,period=250,drift=0.02,gap=0.4,base=0.2):
        r=np.random.default_rng(seed); s.K,s.T=K,T; p=np.full((T,K),base)
        if kind=="stationary":
            best=r.integers(K); p[:,best]=base+gap
        elif kind=="switch":                      # best arm jumps to a new arm every `period` steps (abrupt change)
            t=0; last=-1
            while t<T:
                b=r.choice([k for k in range(K) if k!=last]); p[t:t+period,b]=base+gap; last=b; t+=period
        elif kind=="drift":                       # independent random walks on the logit scale, clipped
            z=r.normal(-1.0,0.5,K); 
            for t in range(T): z=z+r.normal(0,drift*4,K); z=np.clip(z,-3,3); p[t]=1/(1+np.exp(-z))
        elif kind=="reversal":                    # two good arms swap roles halfway repeatedly
            a,b=r.choice(K,2,replace=False)
            for t in range(T): p[t,a if (t//period)%2==0 else b]=base+gap
        else: raise ValueError(kind)
        s.p=np.clip(p,0.01,0.99); s.u=r.random((T,K)); s.best=s.p.max(1)
    def reward(s,t,arm): return float(s.u[t,arm]<s.p[t,arm])
class EpsGreedy:
    def __init__(s,K,eps=0.1,alpha=None): s.K,s.eps,s.alpha=K,eps,alpha; s.q=np.zeros(K); s.n=np.zeros(K)
    def select(s,t,rng): return int(rng.integers(s.K)) if rng.random()<s.eps else int(np.argmax(s.q+1e-9*rng.random(s.K)))
    def update(s,a,r): s.n[a]+=1; s.q[a]+=((1/s.n[a]) if s.alpha is None else s.alpha)*(r-s.q[a])
class UCB:                                          # UCB1 (stationary); with gamma<1 -> discounted UCB; with window -> sliding-window UCB
    def __init__(s,K,c=1.0,gamma=1.0,window=None): s.K,s.c,s.g,s.w=K,c,gamma,window; s.S=np.zeros(K); s.N=np.zeros(K); s.hist=[]
    def select(s,t,rng):
        if s.w: 
            S=np.zeros(s.K); N=np.zeros(s.K)
            for a,r in s.hist[-s.w:]: S[a]+=r; N[a]+=1
        else: S,N=s.S,s.N
        if (N==0).any(): return int(rng.choice(np.where(N==0)[0]))
        tot=N.sum(); return int(np.argmax(S/N+s.c*np.sqrt(np.log(max(tot,2))/N)))
    def update(s,a,r):
        if s.w: s.hist.append((a,r))
        else: s.S*=s.g; s.N*=s.g; s.S[a]+=r; s.N[a]+=1
class Thompson:                                     # Beta-Bernoulli Thompson; gamma<1 discounts the posterior counts toward the prior
    def __init__(s,K,gamma=1.0): s.K,s.g=K,gamma; s.a=np.ones(K); s.b=np.ones(K)
    def select(s,t,rng): return int(np.argmax(rng.beta(s.a,s.b)))
    def update(s,a,r): s.a=1+s.g*(s.a-1); s.b=1+s.g*(s.b-1); s.a[a]+=r; s.b[a]+=1-r
class ACOStyle:                                     # ant-colony-style pheromone reinforcement on arms: evaporate all, deposit on the chosen arm in proportion to reward
    def __init__(s,K,rho=0.05,Q=1.0,alpha=2.0,tau_min=0.02,eps=0.02): s.K,s.rho,s.Q,s.al,s.tmin,s.eps=K,rho,Q,alpha,tau_min,eps; s.tau=np.ones(K)
    def select(s,t,rng):
        if rng.random()<s.eps: return int(rng.integers(s.K))
        w=s.tau**s.al; return int(rng.choice(s.K,p=w/w.sum()))
    def update(s,a,r): s.tau=np.maximum((1-s.rho)*s.tau,s.tmin); s.tau[a]+=s.Q*r*s.rho*s.K*0.5
class Random:
    def __init__(s,K): s.K=K
    def select(s,t,rng): return int(rng.integers(s.K))
    def update(s,a,r): pass
def run(make,env,seed=0):
    rng=np.random.default_rng(seed); alg=make(env.K); reg=np.zeros(env.T); arms=np.zeros(env.T,int)
    for t in range(env.T):
        a=alg.select(t,rng); r=env.reward(t,a); alg.update(a,r); reg[t]=env.best[t]-env.p[t,a]; arms[t]=a
    return np.cumsum(reg),arms

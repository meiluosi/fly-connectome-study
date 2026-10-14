import numpy as np, clmetrics as M
# 1. basic metrics on a hand-made matrix
R=np.array([[0.9,0.0,0.0],[0.6,0.8,0.0],[0.5,0.5,0.7]]); assert abs(M.learning_acc(R)-0.8)<1e-9; assert abs(M.final_acc(R)-0.5667)<1e-3
assert abs(M.forgetting(R)-((0.9-0.5)+(0.8-0.5))/2)<1e-9; assert abs(M.forgetting(R,include_last=True)-((0.4+0.3+0.0)/3))<1e-9
assert abs(M.norm_forgetting(R,0.5)-(0.35/(0.85-0.5)))<1e-9 and np.isnan(M.norm_forgetting(R,0.9)) and abs(M.bwt(R)+0.35)<1e-9
# 2. matched-learning logic: forgetting is a pure function of learning for both methods -> A vs B must be 'equivalent' even though A learns more
rng=np.random.default_rng(0); S=40; etasA=np.linspace(0.1,0.9,8); etasB=np.linspace(0.02,0.4,8)
def sweep(etas,g): L=np.clip(0.5+0.5*(1-np.exp(-g*etas[:,None]))+rng.normal(0,.005,(len(etas),S)),0,1); return L,0.4*(L-0.5)**1.5+rng.normal(0,.003,(len(etas),S))
LA,FA=sweep(etasA,3.0); LB,FB=sweep(etasB,3.0)
# method A reaches higher learning than B: naive default-setting comparison finds A 'forgets more'; matched comparison must not
naive=FA[-1].mean()-FB[-1].mean(); assert naive>0.01, naive
rows=M.matched_diff(LA,FA,LB,FB,targets=[0.62,0.66,0.7],margin=0.02); assert all(r["status"] in ("equivalent","incomparable") for r in rows) and any(r["status"]=="equivalent" for r in rows), rows
# 3. a genuinely more stable method must be detected: B forgets half as much at the same learning
FB2=FB*0.4; rows=M.matched_diff(LA,FA,LB,FB2,targets=[0.7,0.75],margin=0.005); assert any(r["status"]=="A_worse" for r in rows), rows
# 4. coverage rule: a target outside B's range is incomparable, never extrapolated
rows=M.matched_diff(LA,FA,LB,FB,targets=[0.99]); assert rows[0]["status"]=="incomparable"
# 5. frontier gap ~0 for identical curves, positive when A is worse
assert abs(M.frontier_area_gap(LA,FA,LB,FB,0.55,0.75))<0.01 and M.frontier_area_gap(LA,FA,LB,FB2,0.55,0.75)>0.01
print("all clmetrics tests passed")

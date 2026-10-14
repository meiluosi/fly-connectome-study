import numpy as np, sys; sys.path.insert(0,'.')
import v3core as V3, v2core as V, tsp as T, fly_heuristic as H
X,D=T.make_instance(30,5); cfg=dict(alpha=1.0,beta=3.0,rho=0.1,ants=10,iters=8)
# 1. no circuit, no hand penalty: run3 == v1 aco_vec bit-for-bit (same RNG use)
a=V3.run3(X,D,cfg,seed=3); b=H.aco_vec(D,n_ants=10,iters=8,alpha=1.0,beta=3.0,rho=0.1,seed=3)[0]; assert a==b,(a,b); print("1 ok: plain == v1 aco_vec")
# 2. turning-angle bins: straight line -> bin 0, U-turn -> bin 6, start -> 7
Xs=np.array([[0,0],[1,0],[2,0],[0.5,0.0]]); TB,COS=V3.turn_bins(Xs); assert TB[0,1,2]==0 and TB[0,1,3]==6 and TB[4,1,2]==7,(TB[0,1,2],TB[0,1,3]); print("2 ok: turn bins")
Xr=np.array([[0,0],[1,0],[1,1.0]]); TBr,_=V3.turn_bins(Xr); assert TBr[0,1,2]==3 or TBr[0,1,2]==4; print("   right angle bin",TBr[0,1,2])
# 3. valid tours with hand penalty and with learners; learners run
c=V3.construct_turn(np.ones((30,30)),np.ones((31,30,30)),np.random.default_rng(0),6); assert all(sorted(x)==list(range(30)) for x in c); print("3 ok: permutations")
print("hand",V3.run3(X,D,dict(cfg,kappa=0),hand_gamma=2.0,seed=3))
for kind,lr in (("real",0.1),("random",0.1),("linear",0.1)):
    ci=V3.Circuit3(kind,lr,5); print(kind,V3.run3(X,D,dict(cfg,kappa=4.0),ci,seed=3))
# 4. learning signal exists: after learning on a 50-city instance, a sharp turn gets lower valence than straight on average
X2,D2=T.make_instance(50,9); cf=dict(alpha=1.0,beta=5.0,rho=0.5,ants=20,iters=25,kappa=4.0)
for kind,lr in (("real",0.1),("linear",0.1)):
    ci=V3.Circuit3(kind,lr,5); V3.run3(X2,D2,cf,ci,seed=1); v=ci.valence_u(); tb=ci.G[:,5]-V3.TURN_OFF
    print("4",kind,"mean valence by turn bin (signatures present):",[round(float(v[tb==b].mean()),3) if (tb==b).any() else None for b in range(8)])

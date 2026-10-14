import numpy as np, tsp as T, fly_heuristic as H
# the vectorised ACO must be statistically equivalent to the loop ACO in tsp.py (same algorithm) and valid
g1=[];g2=[]
for s in range(10):
    X,D=T.make_instance(30,300+s); ref=T.reference_solver(D,restarts=6)[1]; _,b1,_,_=T.aco(D,n_ants=20,iters=25,seed=s); b2,h,c=H.aco_vec(D,n_ants=20,iters=25,seed=s); g1.append(b1/ref-1); g2.append(b2/ref-1); assert c==500 and all(h[i+1]<=h[i]+1e-12 for i in range(len(h)-1))
print("mean gap to reference: loop ACO %.2f%%  vectorised ACO %.2f%%"%(100*np.mean(g1),100*np.mean(g2))); assert abs(np.mean(g1)-np.mean(g2))<0.03
# a heuristic-only run (no pheromone effect: alpha=0) must be worse than with pheromone
w=[];wo=[]
for s in range(10):
    X,D=T.make_instance(30,300+s); w.append(H.aco_vec(D,seed=s)[0]); wo.append(H.aco_vec(D,alpha=0.0,seed=s)[0])
print("with pheromone %.3f vs alpha=0 (no learning from pheromone) %.3f"%(np.mean(w),np.mean(wo))); assert np.mean(w)<np.mean(wo)
print("test_aco_vec.py passed")

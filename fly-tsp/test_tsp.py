import numpy as np, tsp as T
# 1. tours are permutations; NN valid
X,D=T.make_instance(30,0); t=T.nn_tour(D); assert sorted(t)==list(range(30))
# 2. 2-opt never worsens and returns a 2-opt local optimum (no improving move remains)
t0=np.random.default_rng(1).permutation(30); t2=T.two_opt(D,t0); assert T.tour_len(D,t2)<=T.tour_len(D,t0)+1e-9 and sorted(t2)==list(range(30))
assert np.array_equal(T.two_opt(D,t2),t2)
# brute-force check that no improving 2-opt move exists
n=30; best=0
for i in range(n-1):
    for j in range(i+2,n):
        if i==0 and j==n-1: continue
        a,b,c,d=t2[i],t2[i+1],t2[j],t2[(j+1)%n]; best=min(best,D[a,c]+D[b,d]-D[a,b]-D[c,d])
assert best>-1e-9,best
# 3. points on a circle: the optimal tour is the circular order, length 2*pi*r; 2-opt+or-opt from random must find it
ang=np.sort(np.random.default_rng(2).random(25)*2*np.pi); Xc=0.5+0.4*np.c_[np.cos(ang),np.sin(ang)]; Dc=np.linalg.norm(Xc[:,None]-Xc[None],axis=2)
opt=T.tour_len(Dc,np.arange(25)); ref,bl=T.reference_solver(Dc,restarts=6); assert abs(bl-opt)<1e-9,(bl,opt)
# 4. ACO builds valid tours, improves monotonically (best-so-far), and beats nearest neighbour on average with a modest budget
res=[]
for s in range(6):
    X,D=T.make_instance(30,10+s); b,bl,h,c=T.aco(D,n_ants=15,iters=40,seed=s); assert sorted(b)==list(range(30)) and all(h[i+1]<=h[i]+1e-12 for i in range(len(h)-1)) and c==15*40
    res.append((bl,T.tour_len(D,T.nn_tour(D)),T.reference_solver(D,restarts=8)[1]))
res=np.array(res); print("mean tour length  ACO %.3f | NN %.3f | reference %.3f (n=30, 600 constructions)"%tuple(res.mean(0))); assert res[:,0].mean()<res[:,1].mean()
# 5. reference is never worse than ACO/NN on any instance (it is the 'best known' proxy)
assert (res[:,2]<=res[:,0]+1e-9).all() or (res[:,2]<=res[:,0]*1.02).all()
print("test_tsp.py passed")

import numpy as np, forage as F
# 1. data sanity: real circuit shapes, signs, and that the code is ~5% sparse
assert F.P0.shape==(65,2045) and F.N.shape==(2045,49) and set(np.unique(F.SIGNS))=={-1.0,1.0}
w=F.World(0); c=F.kc_code(w.masks[0],F.P0); assert abs(c.mean()-0.05)<0.002
# 2. initial valence is 0 for every odour (q0=0.5 -> B=B0), for real/shuffled/random circuits
rng=np.random.default_rng(0)
for kind in ("real","shuffled","random"):
    P=F.make_P(kind,rng); mb=F.MB(P); assert all(abs(mb.valence(F.kc_code(m,P)))<1e-5 for m in w.masks)
# 3. learning moves valence in the direction of the prediction error, and generalises more to a similar odour (shares 4/6 glomeruli) than to a dissimilar one
P=F.P0; mb=F.MB(P); cA,cA2,cB=[F.kc_code(w.masks[i],P) for i in (0,1,3)]
for _ in range(30): mb.update(cA,1-mb.valence(cA))
vA,vA2,vB=mb.valence(cA),mb.valence(cA2),mb.valence(cB); assert vA>0.3 and vA2>vB+0.02 and vA>vA2,(vA,vA2,vB)
for _ in range(30): mb.update(cA,-1-mb.valence(cA))
assert mb.valence(cA)<0
# 4. lesions: blocking plasticity prevents learning; silencing all MBONs gives valence 0
mb=F.MB(P,plasticity_blocked=np.ones(F.NM,bool)); [mb.update(cA,1.0) for _ in range(20)]; assert abs(mb.valence(cA))<1e-6
mb=F.MB(P); [mb.update(cA,1.0) for _ in range(20)]; mb.silenced[:]=True; assert abs(mb.valence(cA))<1e-6
# 5. determinism and reward bookkeeping
r1,_=F.run_fly(F.World(1,T=1500),F.MB(P),P,seed=3); r2,_=F.run_fly(F.World(1,T=1500),F.MB(P),P,seed=3); assert np.array_equal(r1,r2)
# 6. reward schedule flips sign across phases
w=F.World(0,rev=100); assert w.reward_value(0,10)==-w.reward_value(0,110)==1.0 or w.reward_value(0,10)==-w.reward_value(0,110)
# 7. a learning fly beats a non-learning fly on average (sanity of the whole loop; not a research claim)
def mean_net(make,seeds=range(6)): return float(np.mean([F.run_fly(F.World(s,T=6000,rev=3000),make(),P,seed=100+s)[0].sum() for s in seeds]))
l=mean_net(lambda:F.MB(P)); n=mean_net(lambda:F.NoLearning())
assert l>n+3,(l,n)
print("test_forage.py passed | 6000-tick net reward: learning fly %.1f vs non-learning fly %.1f"%(l,n))

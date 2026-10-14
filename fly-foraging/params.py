"""Demo parameters, chosen on TUNING worlds (seeds 1000-1004; see tune.py / tuning_results.json). Test worlds use seeds 0-19."""
FLY_MB=dict(eta=0.4,g_learn=2.0,k_turn=1.4)
FLY_LINEAR=dict(eta=1.0,g_learn=2.0,k_turn=1.4)
FLY_NOLEARN=dict(k_turn=0.45)
ANTS=dict(rho=0.01,alpha=3.0)
QL=dict(alpha=0.003,eps=0.05)
T,REV=6000,3000

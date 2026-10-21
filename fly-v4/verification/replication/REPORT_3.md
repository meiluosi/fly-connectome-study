# REPORT_3 (independent re-implementation)

Code: rep_3.py (run 4 workers of 30 worlds, then `combine`). Runtime: ~85 s wall for 120 worlds x 7 students on 4 processes (~2.6 s/world single). Seeds: SeedSequence([7,teacher_idx,world]).

## Results

Teacher M_R (n=60 worlds)

| student | mean auc |
|---|---|
| M_R | 0.6501 |
| M_L | 0.6266 |
| F_R | 0.6221 |
| F_L | 0.6280 |
| random | 0.6121 |
| marg_M_R | 0.6320 |
| marg_F_R | 0.6308 |

| contrast | mean diff | 95% CI |
|---|---|---|
| M_L - random | +0.0145 | [+0.0095, +0.0198] |
| F_R - random | +0.0101 | [+0.0054, +0.0149] |
| F_R - marg_F_R | -0.0087 | [-0.0124, -0.0050] |
| F_L - random | +0.0159 | [+0.0111, +0.0205] |

Teacher F_R (n=60 worlds)

| student | mean auc |
|---|---|
| M_R | 0.6249 |
| M_L | 0.6293 |
| F_R | 0.6540 |
| F_L | 0.6337 |
| random | 0.6061 |
| marg_M_R | 0.6317 |
| marg_F_R | 0.6320 |

| contrast | mean diff | 95% CI |
|---|---|---|
| F_L - random | +0.0276 | [+0.0237, +0.0316] |
| M_R - random | +0.0188 | [+0.0143, +0.0235] |
| M_R - marg_M_R | -0.0068 | [-0.0107, -0.0026] |
| M_L - random | +0.0232 | [+0.0185, +0.0280] |

(Teacher-hemisphere student, e.g. M_R under T=M_R, is also in the tables: 0.6501 / 0.6540.)

## Ambiguities and resolutions
- Hemisphere subsets: 1800 KC columns drawn without replacement, seed 200+index; N rows: permutation seed 101, first 1800. Subset includes KCs with zero in-degree (not filtered); they never enter the top 5% unless ties.
- Code size 90 = int(1800*0.05). Tie break: integer psi plus uniform noise in [0,0.5).
- PN->KC counts used directly as weights (not normalised). Random student: 6 distinct glomeruli, weight 1.
- marg: sampling without replacement proportional to row sums via Gumbel-top-k (equivalent to sequential sampling); zero-sum glomeruli never drawn; weights randomly permuted over chosen glomeruli; KCs with in-degree 0 stay empty. Both marg_M_R and marg_F_R generated in every world and for both teachers.
- Valence uses the signed sum with B-B0 = sum N sign (q-0.5); scale = 0.5*sum N|sign| (signs are +-1). v computed before the update; no update if delta=0; "else" branch (delta*sign<=0) decays q. Only synapses with N>0 updated.
- Train stream: trial t uses training odour t mod 600, in order. Accuracy at t=0,10,...,400 (41 points); prediction sign(v), v=0 -> +1.
- Teacher: q uniform per world, same N; label +1 if output >= median over all 900.
- Odours: 6 distinct random glomeruli. Bootstrap: 10000 resamples of worlds, percentile 95% CI, seed 5.
- mb_circuit.npz needed allow_pickle=True (object arrays present); only N and signs were used.

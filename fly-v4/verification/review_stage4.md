# Stage 4 review (context-free)

Hashes: all 7 files in PREREG_v4_stage4.sha256 verify OK (the "improperly formatted line" warning is only the comment header).
Scratch scripts are in the session scratchpad (a1..a5.py). All runs were small and read-only on the project.

## Ranked findings

1. CONFIRMED. The headline "real beats shufbal (+0.119)" is mostly a learning-level effect, and real is not exceptional among permutations.
   - I drew 200 further mass-balanced (+-10%) permutations. Each was run with comp_real's own eta=0.05 on 30 fresh seeds (2000-2029).
   - Real: after 0.910, final 0.849. Permutations: after 0.797 on average, final 0.709 on average (sd 0.097, max 0.881).
   - 7.5% of permutations match or beat real on final accuracy (one-sided p about 0.075). An earlier run with 60 permutations on 10 seeds gave 6.7%.
   - Among the 39 permutations whose "after" is within 0.02 of real, mean final is 0.837 (max 0.881) against real 0.849, so there is no real advantage at matched learning.
   - The after-to-final drop is 0.088 for permutations and 0.061 for real. The gap is small compared with the 0.11 difference in "after".
   - So comparison 7 mostly measures that random partitions learn worse. It does not show that the real assignment forgets less.
   - The paired CI over worlds averages over permutations. It cannot support "the real assignment is special".
   - The fraction of MBON labels shared with the real assignment does not predict performance (corr 0.00). KC-input purity per cluster does not either (corr -0.08).

2. CONFIRMED. shufbal "balance" is loose and the residual imbalance drives the null.
   - The +-10% window on summed N leaves a signed mass difference that correlates r=+0.50 with final accuracy across permutations (r=0.45 with cluster-A mass).
   - The heavy-tailed N matters. One MBON holds 28% of PAM mass (MBON 0, N 2845) and another 26% of PPL1 mass (MBON 6, N 3369).
   - Control only the totals and you still randomise which giant MBON sits where. Real (A 10018, B 12805) sits at the null mean on mass. Mass is therefore not why real is better, but the null is noisy and not a clean "assignment only" control.
   - shufbal is also tuned separately (eta 0.01 vs 0.05), which adds noise. The tuning grid is coarse (factor 2.5-3).

3. CONFIRMED. The "global vs COMP" difference is the rule family (one-sided, gated plasticity), not readout signs or compartment role. The global rule is a gauge-invariant strawman for the structure question.
   - Global bidirectional bounded delta is exactly invariant to flipping an MBON's readout sign, because q maps to 1-q. I built global_role, which uses the role signs -cl and excludes the calyx MBON, with the same bidirectional update. Its test frontier is identical to global to 3 decimals (after/final 0.875/0.785, 0.902/0.797, 0.940/0.802).
   - So the signs, the calyx MBON and the role assignment cannot cause the difference. What differs is:
     - COMP is depression-only. q lies in (0,0.5], there is no potentiation, so old traces are not overwritten.
     - The gating is by error sign per cluster.
     - The calyx MBON and 4 zero-input MBONs do not learn.
   - "Global" has no decay or structure, but neither does COMP. Neither has a decay term (lam=0). That part is fair.
   - Missing control: a non-compartment depression-only or asymmetric-rate global rule. This would separate "compartmentalisation" from "one-sided plasticity". Only comp_shuf and shufbal exist as nulls, and they conflate partition quality with learning ability.
   - A transmitter-consistent partition (cl=-SIGNS, 34/48 MBONs agree with the role assignment) fails at about chance. Final accuracy is 0.52-0.54 on tuning seeds at every eta. So success depends on the particular partition, not on "depress-only + any sensible signs".

4. CONFIRMED. The matched-learning contrast holds only partly, and it is marginal.
   - Frontier on the test seeds (paired comp_real minus global at matched "after", with 99.3% CIs):

     | comp_real eta | global eta | after diff | final diff | final CI |
     |---|---|---|---|---|
     | 0.02 | 0.005 | -0.002 | +0.028 | [0.013, 0.043] |
     | 0.05 | 0.01 | +0.003 | +0.048 | [0.029, 0.067] |
     | 0.15 | 0.02 | -0.017 | +0.041 | [0.021, 0.062] |
     | 0.01 | 0.005 | -0.023 | +0.004 | [-0.009, 0.018] |

   - The headline +0.048 is the most favourable match. It is the grid point where comp_real peaks.
   - Both ★5 (+0.044 [0.024, 0.065]) and ★6 (+0.048 [0.029, 0.067]) have lower bounds below s=0.03. Under the PREREG tiers they are not meaningful-strict, only the analysis's ad hoc "meaningful (边缘)" tier. PREREG's licence ("both meaningful → compartmentalisation reduces forgetting") is therefore weak.
   - The matching variable is a grid choice. "after" is the mean accuracy of each task right after learning.
   - comp_real is flatter across tasks: first_final 0.833 vs 0.716 and last_final 0.859 vs 0.928 for global. This is recency-versus-primacy, not uniformly less forgetting. At matched "after" comp_real is lower on the latest task.
   - The matched eta differs by 5x between arms, which is fine.
   - Normalised forgetting (0.144 vs 0.254) is a ratio-of-small-numbers metric. Per-world division by max(a-0.5,1e-3) blows up for comp_shuf (mean 2.151, median 0.265, 27 of 100 worlds with after<=0.6). The reported forgetting for shuf and shufbal is unreliable. For real and global it is stable (no world has after<=0.6).

5. PLAUSIBLE. Selection and tuning.
   - The tuning is on 20 seeds and picks the argmax of final. The differences between neighbouring etas are within noise (comp_real 0.829 at 0.05 vs 0.816 at 0.15). The test seeds are independent, so there is no leakage, only mild noise.
   - global peaks at 0.02 (final 0.802). comp_real is flat from 0.05 to 1.0 (0.82-0.85) while global declines at high eta. Part of the "advantage" is robustness to eta rather than peak performance.

6. CONFIRMED. Code checks pass; I found no bug in the COMP core.
   - Role-based centring is consistent: b0r and scr use the same sg, and the value is invariant at q=0.5.
   - The update is correct. Depress for cl>0 when e>0, which raises V because those MBONs have sign -1. The mirror holds for cl<0.
   - DAN gating, the update and the lam=0 default are consistent.
   - Clusters: 20/28/1 match the PREREG. shufbal permutes only the non-calyx labels. The rejection sampling is correct and the target is the real masses. Sampling a new permutation per world (via rng2) is fine.
   - The b0 and sc arguments to COMP.val are dead (it recomputes), which is harmless.
   - run_cl: accuracy uses sign(v+1e-12)==y. Ties at v=0 resolve to +1. This is why unsigned sits at 0.49-0.5. "after" is measured only on the task just learned, and "final" on all 40. Matching and indexing are correct.
   - The calyx MBON is in global's readout, learns, and carries mass 1267. Gauge invariance removes any role for its sign, but global learns through it and COMP does not. This is a minor unfairness. Global_role without calyx showed no difference.

7. PLAUSIBLE. Family and tiers.
   - 7 comparisons at 99.3% is correct (1-0.05/7). The bootstrap is paired, 10000 resamples, 100 worlds.
   - Of the 7, ★2 and ★4 (sample efficiency vs global) are non-positive for comp_real (equivalent and small-real negative). Only the CL and shufbal comparisons are positive. Teacher_real and door_teacher_real (non-family) show global clearly better.
   - Phenomenon block A (P1-P3) is close to tautological. Timing, signs and ablations are built in, and the shuf arms pass too. It supports the rule's self-consistency only. The PREREG says as much.

## Would a NOTES-style claim "compartmentalisation reduces forgetting" be supported?
No, not as stated. Supported, with caveats:
- A depression-only, error-sign-gated rule with the real PAM/PPL1 partition retains about 0.03-0.05 more accuracy than the bidirectional global delta rule at similar learning level, in a 4-task random-label memorisation test. The effect is marginal (lower CI bound below s) and is largest at one favourable grid point.
- The real partition is not shown to be special. About 7% of random mass-balanced partitions do as well, and the shufbal deficit disappears at matched learning level.
- "Compartmentalisation" is confounded with one-sided plasticity (no potentiation to overwrite memories). Say "gated depression-only plasticity with partition P", not "compartmentalisation".
- Recommended extra controls:
  - a permutation-percentile test of real against many partitions;
  - matched-"after" comparison for the null;
  - a global rule with depression-only or asymmetric plasticity and no partition;
  - tighter mass control, including top-MBON placement.

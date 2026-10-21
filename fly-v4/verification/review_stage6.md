# Review of stage 6 (6a, 6b, 6c). Context-free, independent recompute.

Hashes: PREREG_v4_stage6b.sha256 and PREREG_v4_stage6c.sha256 all verify (one malformed comment line is harmless).
File times: the 6c tuning finished 06:11:31, the freeze was 06:11:55, and the first results_h2 file is 06:11:59. The freeze order is correct.

## Ranked findings

1. CONFIRMED (high). The "bounded depression" in CompMB is not bounded, and the 6c consistent-world win depends on this.
   - `update` computes `q -= g*code*NB*q` with g = eta*relu(delta) and delta in [-2,2]. Once g > 1, q flips sign and is amplified.
   - I logged q for world 20, comp_real, eta 4.0: q ranges over [-6.9, +9.5]. At eta 0.8 (the 6b setting) q already reaches -0.07.
   - global `forage.MB` also leaves [0,1] at its tuned eta 0.8 (q max 1.44, min -0.43), but only mildly.
   - Control: the same rule with g clipped to <= 1 (a truly bounded depression), run on tuning worlds 20-39, consistent, g_learn 1.0:

     | eta | clipped | unclipped |
     |---|---|---|
     | 2 | 8.2 | 9.8 |
     | 4 | 8.2 | 54.0 |
     | 8 | 8.2 | 56.4 |

   - At g_learn 2.0, clipped gives -1.0 for every eta, against 53.6 unclipped at eta 4.
   - So "comp_real +53.8, equal to or better than global" comes from a sign-flipping, amplifying regime (one-shot valence saturation after clipping), not from the stage-4 bounded rule.
   - A genuinely bounded comp learner at eta >= 2 is one-shot and fails in this arena.
   - NOTES and RESULTS describe the 6c arm as the "stage-4 learner at a wider grid". That is misleading: the tuning grid moved the rule into a different dynamical regime. The same concern applies to any stage-4 result at eta >= 1/2.
   - The conflict result is less affected: clipped 29.5 against unclipped 30.2 at eta 2, g 6.

2. CONFIRMED (medium). The NOTES conclusion "6b gap was a grid artefact; no stable advantage or disadvantage" is stronger than the data, and it is not the outcome the 6c prereg's own decision rule defined.
   - The prereg rule: "still clearly worse -> 6b stands; equivalent -> 6b was tuning".
   - Actual 6c results, at 98.8% CI:
     - consistent: +8.6 [+2.4, +14.6]
     - conflict: -9.3 [-14.9, -3.7]
   - Both intervals exclude 0, with opposite signs. Neither is equivalent (neither CI sits inside ±6). That is a world-type-dependent difference of moderate size, not "no advantage or disadvantage".
   - The 6c prereg predictions both failed:
     - comp_real vs global "equivalent or slightly worse": consistent is better.
     - comp_real vs shufbal "equivalent": conflict is -7.9 [-14.6, -0.6], and consistent is +1.4 [-5.0, +8.0], which is not equivalent either.
   - NOTES does not say the predictions failed.
   - The 6b-to-6c conflict gap shrank from -22.8 to -9.3, but it did not vanish.
   - The 6b and 6c numbers are not directly comparable: different test worlds, different grids, and global moved from g_learn 1 to g_learn 6 in conflict.
   - Suggested wording: "6b's large gap was mostly grid width; at the wider grid comp_real is better in consistent and worse in conflict, each by <= ~9 (edge tier), and the consistent win depends on q leaving [0,1] (finding 1)."

3. CONFIRMED (medium-low). The grid-edge issue is real but does not overturn the conclusions. NOTES understates it.
   - Edges found:
     - comp_real consistent: eta 4.0 is the upper edge, and g_learn 1.0 is also the lower edge.
     - 6b global consistent: eta 0.8 was at the upper edge, not just the three comp arms.
     - conflict: g_learn 6.0 is the upper edge for global, comp_real and shufbal. For global, eta 0.4 is also the lower edge.
   - Extended runs on tuning worlds 20-39 (20 worlds, noise about ±5), comp_real consistent:
     - eta 8, g 0.5-1.0: 56.4-56.6, against 54.0 at the 6c optimum. Beyond eta 16 it falls (to 31-47).
     - So extending the edge gives only about +2.5 on tuning worlds.
   - Conflict:
     - comp_real: best (2, 15) = 33.0, against 30.2 at the 6c optimum.
     - global: (0.4, 6) = 43.6 is a spike. (0.4, 10) = 29.9, (0.4, 15) = 28.4, and (0.15, g) is about 26.
   - The conflict gap (global above comp_real by about 10) persists on tuning worlds.
   - The global conflict tuned score of 43.65 became 32.4 on test (winner's curse, -11). comp_real fell 30.2 to 23.2.
   - Best-of-16 selection on 20 worlds, with a landscape noise of about ±5, makes the conflict ordering shaky, and the plateau is flat.
   - The grid upper bound eta 4.0 was chosen after the unregistered diagnostic showed comp_real's peak there (diag_grid_h.log: comp_real best 63.9 at (4, 1); global best 64.2 at (2, 6)). The design is therefore tuned toward including comp_real's optimum. The consequence is small, since the extension gains little.

4. CONFIRMED (low). Everything else in the CompMB mechanics checked out.
   - Sign logic is consistent: sg = -cl. Reward depresses the PAM cluster, which has readout -1, so valence goes up. Punishment depresses PPL1, which has readout +1, so valence goes down.
   - Centring: b0 = 0.5*code@A matches q0 = 0.5. The scale excludes the calyx MBON (sg = 0).
   - Calyx handling is harmless.
   - cl_data.npy and CL_REAL index alignment: the type column matches 49/49 in order. The compartment strings differ in spelling, but the types align.
   - Paired design: agent seeds (5000+s) and world seeds are identical across arms. In forage.run_fly the code-jitter RNG is the same for global and comp, because CompMB is an MB subclass.
   - Cluster RNG is 7000+s. comp_shuf permutes the 0 entry too, so the calyx slot can get a learning label, which is fine. comp_shufbal permutes the non-zero labels only.
   - The comp arms use depression only and global uses both potentiation and depression, with a different effective scale (g = eta*|delta| for global against relu per cluster for comp). The "same eta" label in tables is therefore not the same quantity; the per-arm tuning is what makes the comparison fair.
   - The "Bounded delta rule" docstring and PREREG language is false for both arms (finding 1).

5. CONFIRMED (6a, low-to-medium).
   - Recompute: 49/49 MBONs have DAN input. 48/48 agree. The only difference is the calyx MBON22 (data: PAM 24, PPL1 0). Cluster sizes are 20/28/1 for the literature and 21/28/0 for the data. All of this matches NOTES.
   - Not circular in the way suspected. The DAN cluster comes from `type` (PAM*/PPL1*), not from the compartment in the instance name; `comp` is extracted but never used in the classification. The MBON side comes from MBON compartment labels.
   - But it is a weak check:
     - The compartment-to-PAM/PPL1 map is close to the definition of the DAN types.
     - The agreement is expected a priori and tests only the literature mapping.
     - Dominance margin: 41/49 MBONs are >= 90% one cluster and 46/49 are >= 80%. The weakest are MBON33 (59 against 158), MBON30 (58 against 156) and some MBON10 (12 against 4, 20 against 4). 39/49 MBONs receive both clusters.
     - Coverage: 8 of the 49 MBONs have a total DAN weight under 30.
   - PPL1 coverage is thin by construction: 16 PPL1 DAN bodies, 2 per type PPL101-108. They still account for 5647 of the 20388 total DAN-to-MBON weight, and they dominate the 28 PPL1 MBONs.
   - MBON22 (calyx) is the 1/49 exception and has little effect on 6b/6c. No re-run with cl_data instead of CL_REAL was done.
   - The note's own caveat holds: valence (PAM = reward) is not validated.
   - Wording fix: "supports the cluster assignment" is fine; "100%" should come with the weak-prior caveat.

6. PLAUSIBLE (low). The statistics and tiers are correct (spot-checked: m >= 6 with lo < 6 gives "meaningful (边缘)"; equivalence needs the full 98.8% CI inside ±6, which is conservative).
   - Family size 4 at 98.8% matches the prereg (1 - 0.05/4 = 98.75%). It is per stage; across 6b+6c there are effectively 8 family tests, and the 6c conclusions are re-decisions on the same hypothesis after a failed first run.
   - The shared RNG state for the bootstrap makes intervals order-dependent but valid.
   - The descriptive 95% tiers are labelled "meaningful-strict" without multiplicity control; the NOTES uses only the starred ones, which is fine.

7. PLAUSIBLE (low). Tuning-world overlap. The 12 diag worlds are a subset of tuning worlds 20-39, not of the test worlds 400-599 / 600-799. No test-set leakage found.

## Bottom line
The numerical results reproduce, the preregistration and hashes are consistent, and I found no leakage. The main problems are interpretive.
(a) The comp learner's 6c consistent win relies on q leaving [0,1].
(b) The conclusion "no stable advantage or disadvantage" is not supported by the intervals.
(c) The 6c prereg's predictions and decision rule were not met, and the NOTES does not say so.
Scratch scripts (not in the project): /private/tmp/claude-501/-Users-meros-Desktop-fly-mb-compartments/ed04186f-d12d-4fef-91e6-c9b4ab208526/scratchpad/{a6,q,g,c}.py

# Independent code review (read-only; sanity scripts in scratchpad)

## CRITICAL

1. **C3: `run_delta_mh` is mathematically identical to `run_delta`, so it is not a control.** core4.py:71-78. The readout is the sum over all heads, and the update of the active heads is `step/len(C)` each. The summed weight therefore changes exactly as in the single-head delta rule. The only difference is the bias `b`, which cancels against the probe mean. I checked on MR: accuracies are identical, and the per-task metric differs by at most 0.06 (the bias term). This is why delta and mh match to three decimals (0.769/0.766, forgetting 0.222/0.222). RESULTS_confirm.md (P4c) and BLOG.md line 38 read this as "gating alone does not lower forgetting". That is a tautology of the implementation, not evidence. Fix: make a real multi-head learner, with per-head readout or heads chosen per task and an output nonlinearity or normalization. Alternatively, apply the connectome's M gating to the delta rule on the MBON-level readout. Otherwise delete the claim.

2. **C1: the "overlap" manipulation is confounded with MBON in-degree homogeneity, and the NaN exclusion removes the high-overlap end.**
   - Searched partitions (MR, 24 partitions, targets 0.06 to 0.64) show r = -0.93 between overlap and the within-compartment variance of log KC in-degree. The variance falls from 4.5 to 1.2 as overlap rises. Overlap is the cosine of binary KC vectors, so it is driven by degree.
   - The dose-response may therefore reflect "which MBONs, and how many dead or low-degree ones, are co-gated". It is not a clean causal effect of KC overlap. MR has 4 MBONs with zero KC input and many with very low input (degrees 0, 0, 0, 0, 2, 4, 13 against a median of 309).
   - exp_confirm.py:27 and core.py:42 define `score = y*(mean_gm(O.Nq) - nv)/nv`. If every gated MBON is dead, nv = 0 and the score is 0/0 = NaN. The same 5 seeds (indices 1, 12, 14, 23, 28) give NaN in every affected partition, for both MR and FR. These are the seeds whose random compartment pair is a dead pair.
   - These NaNs occur only at the top two overlap levels. analysis_confirm.py:11 drops whole partitions, which leaves 1/5 at 0.65 (MR) and 2/5 at 0.59 (FR). The high-leverage end of the regression rests on one or two partitions.
   - A fairer sensitivity analysis drops the 5 bad seeds from all partitions. I recomputed it from the stored JSON. MR slope is 0.029 [0.018, 0.044]. **FR slope is 0.012 [-0.008, 0.033], so the interval includes 0.** The "nanmean" figure used in DEVIATIONS (0.019) is itself inconsistent, because it averages different seed sets across partitions. The P1 FR "pass" depends on the preregistered exclusion rule.
   - Fix: define the score without dividing by nv (use the difference, or an accuracy score). Regress partition-level forgetting on overlap and in-degree homogeneity jointly. Constrain partitions to match degree distribution per compartment, then re-run.

## MAJOR

3. **C2/C3: forgetting is compared across learners with very different learned levels.** Real fly learned about 0.77, none and delta about 0.98. Forgetting is capped by (learned - 0.5), so weak learners are favoured by construction (blog and RESULTS acknowledge this partly). P3 (none - real > 0.05) is nearly guaranteed by the floor effect. Report forgetting normalized by (learned - 0.5), or match the learned level by tuning eta. Gating also makes tasks that land on dead compartments unlearnable (accuracy near chance), which mechanically contributes to "less forgetting".

4. **C3: EWC is weak and the λ choice is test-selected.** core4.py:44-45.
   - Fisher is computed after training the task (residuals err are small), as a mean of err²x². I measured F max about 0.009, step about 0.005, so `step*λ*F` is at most about 0.04 per sample at λ=1000. The clip at 1 never binds. The "EWC works only at large λ" finding is really "the penalty is tiny", and it still selects the best of 3 on final accuracy on the evaluation tasks.
   - Fisher uses the empirical error, not the model's own predictive distribution. The penalty is applied as a separate shrink (not as a gradient of the penalized loss). It is anchored to the last task's weights only, with F accumulated (a mix of online-EWC and EWC).
   - delta uses NLMS (lr 0.5, unbounded weights), which is not matched to fly eta=0.3. Fix: compute the Fisher before the last epochs, or use a proper penalty gradient, and select λ on separate seeds.

5. **P2 statistics.** analysis_confirm.py:25-31. MR and ML come from one animal, FR and FL from another. The 8 tests are not independent, the same seeds feed every circuit, and one shuffle is drawn per seed (the shuffle varies with seed, which is fine). Holm over 8 assumes independence-ish structure. The report already hedges, but "3/8 significant" is an optimistic count. Use a mixed model or an individual-level test.

## MINOR

6. **Label parsing** (compartments.py:6-14). `a2p3p -> a2a3`, "sc/sp/mp/ap" subregions are dropped, `a/B` is dropped, and "B1>a" or "y4>y1y2" keep only the primary token. 19 of 49 MBONs are multi-hot. A shuffle is a row permutation of M, so compartment sizes and gate sizes are preserved (good). Co-membership structure is kept, so the null is somewhat conservative. It does not bias real vs shuffled directionally. The calyx MBON counts as a "compartment" (NC=16 includes it). A task that picks it gates a single MBON.

7. **FlyWire transfer** (core_fw.py:9): `drop_duplicates("type")` keeps the first hemibrain instance per type. Hemibrain labels with `_bilateral` and similar are not checked. This is acknowledged.

8. **Pairing is sound.** In core.run and make_tasks, cond never alters `rt` consumption (rc is separate, and `none` still draws C). Probe odors are generated before tasks, and probe/task odors are only used for readout. There is no train/test leakage, but there is also no held-out generalization test: "final" re-tests the training odors. Bootstrap and Holm (sorted ascending, running max) are correct.

9. **Blog overstatements.**
   - BLOG.md:26 says T=48 none forgets 0.45 and gated 0.28. The confirmatory logs give none 0.385 to 0.392 and real 0.141 to 0.148 (forg_acc). Those figures come from an earlier v2 experiment. Cite the right source or update.
   - The mh sentence at line 38 is invalid (finding 1).
   - "Causal knob" at lines 30-34 should say "co-varies with in-degree homogeneity".
   - "Both individuals confirm" is not robust for FR (finding 2).

## Verdict
- **C1: not established as stated.** MR remains positive (0.029 to 0.040), but it is confounded with degree homogeneity, and FR is not significant once seed handling is made consistent.
- **C2: stands but is trivially inflated.** Gating lowers forgetting, partly through lower learning (floor effect).
- **C3: weakened.** The multi-head baseline is a no-op, EWC is a weak implementation tuned on the test tasks, and the "gating alone does not help" conclusion is unsupported. "The circuit is a worse final-accuracy learner than delta" does stand.

# Independent code review: fly-tsp (read-only; small checks only)

Checks run: frozen file hashes match PREREG_tsp.sha256 for tsp.py, fly_heuristic.py, mbcore.py and tuning_tsp2.json. aco_vec with V=0 reproduces plain aco_vec exactly (same best length, same seed). construct() empirical first-step frequencies match W/sum (max error 0.002 at 200k samples). Glomerulus offsets (fly_heuristic.py:4) tile 0..51 without overlap, and the key encoding at :12 and :14 is a consistent mixed radix.

## CRITICAL
None found that invalidate the code or the data split.

## MAJOR
1. **The "equivalent, no beating ACO beyond 0.5pp" claim is not what the verdicts show.**
   - T1 is "uncertain" in R1 (CI [-0.59,+0.14]) and R2 ([-0.72,+0.05]). Both CIs include improvements larger than 0.5pp.
   - In R2 every learner is 0.2 to 0.35pp better than ACO. Pooling the four learners gives a bootstrap CI of about [-0.66,+0.04] against ACO. The two MB-real vs ACO CIs are not independent evidence of "no effect". The point estimates are consistently in the direction the pre-reg expected for R2.
   - Per-instance SD of paired differences is about 1.4 to 1.8pp, so n=100 only just reaches a +-0.5 equivalence band (analysis_tsp.py:5, PREREG limitations).
   - Fix: say "no learned map shown better than ACO; learners vs ACO inconclusive in R1/R2; MB-real vs controls equivalent". Or increase the number of test instances (about 300+) and run several ACO seeds.
2. **Selection and winner's-curse asymmetry, plus tuning noise.** tune_tsp2.py:13-14, 19-23, 29, 33-35.
   - ACO takes the best of 27 configs, and the best sits at the grid corner (beta=5, rho=0.3; for R3 also alpha=2). It is therefore not tuned to convergence.
   - Learners take the best of 12 configs, each from ONE training run (table seed 7, train seed 3) with ACO parameters fixed. Config-to-config SD on tuning is 0.3 to 0.65pp (my computation from tuning_tsp2.json), the same size as the effects tested. The "best" config is largely a noise draw.
   - Evidence of regression: the tuned real learner gap is 2.68 on R2 tuning vs 3.39 on test; ACO is 4.84 on tuning vs 3.71 on test. Tuning-set difficulty and selection both move gaps by about 1pp.
   - The tuned seed (7) is reused as an eval seed (eval_tsp.py:28), so 1/3 of the evaluated runs reuse the selected wiring and training draw. That favours the learners slightly.
   - Fix: re-select with 3 training seeds and a larger tuning set, or report results for a fixed, un-tuned (lr,kappa) as a sensitivity analysis. Extend the ACO grid beyond beta=5 and rho=0.3.
3. **Real-wiring test is weak by construction.** fly_heuristic.py:4-15, mbcore.py:14.
   - The assignment of edge features to glomerulus indices is arbitrary. Real P0 degrees are extremely uneven: glomerulus 0 feeds 2 KCs, glomerulus 7 feeds 9622 (weighted counts), and some glomeruli are almost silent.
   - Whether an edge feature lands on a silent or a hub glomerulus is therefore random. The test cannot probe connectome specificity, only "weighted sparse expansion vs shuffled/random".
   - Each signature also gets its own table entry (ids_for) with a 5% top-k KC code. The learner is essentially tabular over about 10^5 signatures with weak generalisation. The null MB-real = MB-random is expected a priori.
   - Fix: temper the wording to "with arbitrary feature-to-glomerulus assignment"; optionally repeat with several random assignments (permuting OFF indices).

## MINOR
4. **Training uses beta from R1 for all regimes** (eval_tsp.py:17). It is harmless here because beta=5 in all three regimes (tuning_tsp2.json), but it is a latent mismatch. Training also uses no pheromone (alpha=0), whereas test uses alpha=1 or 2. Both are shared by all learners, so they are fair, but they do not give learners their best chance.
5. **Pairing is nominal.** seed=i is shared between ACO and learner (eval_tsp.py:18,21), but the start-city streams diverge as soon as V changes the probabilities. The pairing mainly pairs instances, which is fine. ACO is a single run per instance while learners are 3-seed means (fewer variance sources); the learner SD is 1.6 vs ACO 2.3pp. The bootstrap treats the learner mean as exact, so training-seed variance (range 0.3 to 0.4pp in R1/R2) is not in the CI (analysis_tsp.py:10). Fix: run ACO with 3 search seeds too and bootstrap over (instance, seed).
6. **Reference.** 30 restarts of 2-opt+Or-opt gives negative ACO gaps only rarely (min -0.7%, 2 to 3 instances per regime), so the reference is reasonable for n=50 and probably weaker at n=100. Paired differences are in percent of the same reference per instance, so a weak reference mainly shifts absolute gaps rather than compressing paired differences. ref_for seeds with i (eval_tsp.py:9) are consistent. ref_for caches pickles by name without a check on instance identity (stale-cache risk). Note ref_tune.pkl is a leftover from the n=50 v1 tuning.
7. **Process.** analysis_tsp.py (mtime 19:21:44) and eval_tsp.py are not in the hash list, and the analysis file was edited 40 s after the pre-reg. The verdict function itself matches PREREG (analysis_tsp.py:5). Nothing is dropped: all 100 instances are used. The bootstrap uses a global RNG (fine). Another small point is that the "95% CI inside +-0.5" rule is stricter than TOST, which is conservative.
8. **Seed-space overlap.** make_instance(100,s) contains make_instance(50,s) as its first 50 cities (same RNG stream), and make_clustered shares the first centre draws. This is not train/test leakage (tuning 1000s, training 2000s, test 5000s are disjoint and used only as stated: tune_tsp2.py:6, eval_tsp.py:5), but R1 and R2 are correlated and should not be treated as independent replicates.
9. **Results/docs.** RESULTS_tsp.md is regenerated by analysis_tsp.py:20 and contains no interpretation. PROPOSAL.md still says "not yet registered". The "5% top-k" and the exp(kappa*v) clip to [-1,1] limit the maximum modulation.

## Correctness verdicts
- edge_signatures/key_to_glom: invertible, offsets non-overlapping. Per-instance normalisation (nn1, dc.max) uses no test information. Unseen signatures have v=0 (q=0.5 gives b0 cancellation), so there is no leakage at test time.
- SigTable: none=0 exactly. Linear/MB signs are consistent (shorter tours give positive reward, positive delta potentiates the positive MBONs). train() uses the aggregated mean per signature; no sign error found.
- construct(): the cumsum inversion is correct and visited cities cannot be sampled (zero-width intervals). The fallback only fires on rounding, taking the first unvisited city, which is negligible. aco_vec: MMAS bounds use a fixed tmax=1/(rho L0) and the iteration-best update, which is standard enough and identical for all arms.

## Verdict
The pipeline is clean (no leakage, no sign or sampling bugs, fair paired data split). The comparison MB-real vs MB-random/shuffled/linear (T2-T4) is reasonably supported as "equivalent within about +-0.5pp, with arbitrary glomerulus assignment". The headline "no feature map beats tuned ACO beyond +-0.5pp" is NOT established: T1 is inconclusive in R1/R2, ACO is under-tuned at the grid edge, learner tuning is noisy, and learners show a consistent 0.2-0.35pp advantage in R2. "Real wiring gives no advantage" is trustworthy only as "no detectable advantage in this arbitrary-assignment setting".

# Independent code review: v3 (turning-angle context)

## Checks passed
- (a) `shasum -c PREREG_v3.sha256` returns OK for all 14 files, including v1 and v2 dependencies. Only NOTES_v3.md and RESULTS_v3.md are newer (07:36), and neither is in the hash list.
  - Tune seeds are 8000-8239 (arms3.py:7 via v2 `tune0`). Test seeds are 9000-9899 (arms3.py:3). They are disjoint, and none of the v2 test ranges (7000-7899) overlap either.
  - Caveat: the hash was taken at 02:26, after tuning ran (tune_v3b.py 02:23, tuning_v3.json 02:25). It freezes the tuning outcome. It does not show that the design was fixed before tuning.
  - Tuning used no test data.
- (b) Correctness holds.
  - The turn_bins angle is the deviation angle (0 = straight), with u[h,i]·u[i,j] (v3core.py:9-10). Edges and `side='right'` give 7 bins (:12). TB[n]=7 is the start bin (:13). The degenerate cases h==i and i==j are zeroed (:11).
  - COS is not zeroed for h==i. That case never occurs in a tour, so it is harmless.
  - start3 (:18-19): tk=key*8+TB, with st=uk//8 and tb=uk%8. G keeps rj, db, mu, ri, cj, plus turn at glomerulus 52+tb. I ran it: the 6 glomeruli are distinct and max=59 (<65). The static key has no ci information in G, so signatures differing only in ci get separate unique ids with identical glomeruli (:19, :23).
  - Learning (:49-51) is aligned: prev=[n,t0..t_{n-3}], cur=t0..t_{n-2}, nxt=t1..t_{n-1}. The sign is correct. `v` is the start-of-iteration value (:45), and per-signature means are used. The closing edge is excluded, which is consistent with construction.
  - construct_turn has the same RNG order as v1. I verified run3 (no circuit) == v2 `V.run` bit-for-bit on 3 R1 and 3 R3 tuning instances. test_v3core.py passes.
  - The hand penalty exp(-γ(1-cos)) is correct in form (:44).

## CRITICAL
1. **The null for TURN-real/random is largely non-expression, not evidence about wiring.** I trained Circuit3 on 3 R1 tuning instances with the tuned parameters (lr 0.1, κ 4) and took the learned valence residual within each static signature, by turn bin.
   - Real: residuals are +-0.01 to 0.02 with no monotone trend, against |v| of 0.4-0.6 from static features.
   - Random: +-0.04, sign-inconsistent.
   - Linear: +-0.1 to 0.26, sign-inconsistent across instances, so it is noise.
   - The turn glomerulus is 1 of 6 inputs, so the 5% KC codes barely differ across bins. The budget is only 25 learning steps (R1; 50 in R2, via v2 `iters`), against about 4000 signatures per instance. The reward is route-level.
   - So TURN-real ≈ ON-real is guaranteed by construction. "Real wiring adds nothing" cannot be inferred from it.
   - test_v3core.py:17-18 already printed flat valence by turn bin (real -0.43 to -0.47) but no assertion or discussion followed.
   - Fix: report this probe. Add a positive-control task where a planted turn effect exists, and show the learners detect it, before concluding anything about wiring.

## MAJOR
2. **The hand-turn control cannot support "turn context has no usable information".** It is a one-parameter, one-signed penalty on turning, with β=8 (tuning_v2_final: ACO α1, β8, ρ0.9). Tuning gap rises monotonically with γ (tuning_v3.json), so γ→0 (= ACO) is optimal by construction. Straight-line preference is the only hypothesis tested. NOTES_v3.md:6 overclaims.
3. **Tuning noise is about 0.4pp, comparable to every effect reported.** In R1, HAND γ=0.1 is nearly a no-op yet scores 1.38% vs ACO 1.77% on tuning (tuning_v3.json). Tuned learner "gains" of 0.3-0.4pp (R1 TURN-random 1.36%) are therefore seed noise, and the winner's curse is mostly this. Fix: more tuning reps, or tune against a paired baseline.
4. **Grid edges were hit.** κ=2 is the lower edge for TURN-linear in R1 and R2. lr 0.03 is the lower edge for TURN-real in R2 and TURN-random in R1. κ=16 is the upper edge for TURN-random in R3. The grid has no κ<2, so learners cannot approach "no effect" smoothly. This is mild unfairness against learners.

## MINOR
5. Equivalence shown at ±0.5pp is not informative here. All differences are under 0.35pp, and the margin exceeds the largest effect of interest. R3 TURN-real−ACO is [-0.37, +0.00] at 99.2%, which is "equivalent" but not "no gain" (the CI touches 0). The verdict rule is not written in PREREG_v3.md ("same as v2"). Make it explicit (analysis_v3.py:13).
6. Headline family: 3 contrasts at 99.2% is correct (analysis_v3.py:14, :26). The other 8 contrasts × 3 regimes are 95% with no multiplicity control, but they are labelled descriptive. The "R2 HAND-turn +0.32 [+0.17,+0.47]" is labelled "equivalent" although the CI excludes 0.
7. Seeds are paired and sound. The ACO search seed is 3*(global instance index)+rep for all arms (arms3.py:22; eval_v3.py:10 with seed0=c*CH). The circuit seed is 11+rep, the same for every instance. Pairing is exact only until the arms' trajectories diverge.
8. TURN learners inherit ACO α/β/ρ (arms3.py:12). This is acknowledged. ON-* parameters are reused from v2 on new instances, which is fair (they were tuned on the same 8000-series sets).
9. NOTES_v3.md:7 "no advantage of real wiring" and :6 "no usable information in turn context" are overclaims (see 1-2). NOTES:8 says R3 learners gain about 0.3pp "regardless of wiring". For TURN-real the gain is only -0.18 [-0.37, +0.00]. The ~0.3pp gain holds for ON-* and TURN-random (-0.28, -0.35, -0.33).

## Verdict
- Supported: under this protocol (500-1000 constructions, β=8, ρ=0.9, ACO-inherited parameters, 25-50 learning steps), no learner arm differs from tuned ACO by more than ±0.5pp, and the code is correct.
- Supported with a caveat: a mild R3 gain exists for static/random-wired learners (≈0.3pp).
- Not supported: "turning-angle context gives no gain" in general. Only a monotone straight-line penalty was tested.
- Not supported: "real wiring adds nothing". The learned valence does not express the turn feature at all (probe above), so the real vs random contrast is uninformative about turn context.

# Independent code review: ml-cl-audit (read-only; sanity checks run in scratch)

## CRITICAL
1. **B1 (vanilla) and B2 (EWC) are degenerate chance-level baselines, so H3 is effectively "FlyModel vs ER-200 only".** `cl_backprop.py:7-11,20` presents each task's data class-by-class (`np.concatenate(per)`; the docstring says "as in the paper", but no REPLICATION_NOTES/PREREG line establishes this). With 2-4 classes per task the net sees a long run of a single class, so it forgets the earlier class inside the same task. Evidence in `results/mnist20`:
   - B1/B2 learning accuracy A_jj is about 0.52, i.e. 2-class chance.
   - Final accuracy is 0.0523/0.0529. The last class (19) is exactly 5.0% of the test set, so the nets predict only the final class.
   - Validation for all lr >= 1e-3 and all lam >= 100 is exactly 0.05 with learn 0.504.
   - EWC's best setting (lam=1, lr=1e-4) is indistinguishable from vanilla. EWC protects across tasks only (Fisher computed at task end, line 36) and cannot fix intra-task forgetting.
   
   Fix: add a task-shuffled stream variant (interleave the classes of a task) for B1-B3 as a sensitivity run, and report the H3 verdict under both. Do not describe B1/B2 as "fairly tuned EWC".
2. **Backprop tuning grid is truncated at the edge.** `audit_run.py:37`: lr in {1e-4,1e-3,1e-2}. Every MNIST backprop winner is lr=1e-4, the smallest value, and EWC's winner is lam=1, the smallest value that is not collapsed. Larger lr and lam collapsed to chance. Lower lr (1e-5), lam in (0,1), and lr x lam interactions with Adam were never tested. The budget is also unequal: FlyModel 12 configs, SLDA 4, ER 3, vanilla 3. Fix: extend the grid downward before claiming H3 holds "under fair tuning".
3. **Results are incomplete, and the stated verdicts do not follow from them.**
   - **H3:** no CIFAR backprop results exist (`results/cifar100*` have no B* keys), so H3 has 1 of 3 benchmarks. `analysis_audit.py:62` labels this "不全成立" ("not all hold"), which reads as a negative result when it is missing data. A partial B-set also silently shrinks `best_BP` (`analysis_audit.py:52`), which favours FlyModel.
   - **MNIST F1:** the validation grid is only 8/12 and there is no `best|Fly_F1`, so MNIST has no F1 test results.
   - **`RESULTS_audit_auto.md`:** it is stale (it shows 3 seeds for F0; the current store gives 5 seeds, F0 0.7065, delta -0.0538). Re-running `analysis_audit.py` on the store reproduces H1 and H2 for all benchmarks and H3 for MNIST only.

## MAJOR
4. **The H1 label "原型等价成立" ("prototype equivalence holds") overstates the data.** `analysis_audit.py:44` assigns "no substantial advantage" whenever delta < 0.02, including large negatives: SLDA beats F0 by 0.054/0.060/0.131. The correct statement is "FlyModel is dominated by SLDA and no better than NCM on strong features". "Equivalence" was never tested.
5. **Selection on test in `best_P` (`analysis_audit.py:41-43`) biases H1 toward "no advantage" (against FlyModel).** It takes the max over four test means. Here SLDA wins every benchmark by at least 0.05 over the next prototype, so the bias is immaterial to the verdict. H3's best-of-three over test means (line 52) has the same direction; there ER-200 is far ahead. Fix: choose the comparator by validation.
6. **Asymmetric tuning in H1.** F0 (paper defaults, untuned) is compared to validation-tuned SLDA. F1 (tuned) would shrink the gap only slightly (CIFAR-224: 0.540 vs 0.639; CIFAR-A: F1 equals F0; MNIST: absent). The pre-registered rule is followed, but report F1 − best_P as well.
7. **H2's F2 and F2b are saturated or degenerate controls.**
   - F2b is exactly chance (0.0100; 0.0490 on MNIST, the class-0 share), because min-max features with beta*sum clipped to [0,1] make all weights 1 and argmax ties pick class 0.
   - F2 (`cl_baselines.py:53`) gets no beta tuning (grid `[{}]`) while F1 gets 12 configs, and the dense score is the class-sum dot rule, which `ClassSumDot` already shows is weak.
   - So "WTA has value" mainly shows the Hebbian rule fails on dense features, not that sparsity helps. The exploratory ExpNCM controls are the informative ones. Qualify the H2 wording.
8. **Seed pairing in H2 (`analysis_audit.py:48`)** uses `zip` of the two sorted lists, not a match on seed. Currently both have seeds 0-4, but a missing seed would silently misalign them. Fix: join on the seed index.
9. **`collect()` ep5 parsing bug (`analysis_audit.py:21`).** For `test|B1_vanilla|ep5|{hp}|s0` the tag is `parts[2]` but the code uses `parts[3]`, so the name becomes `B1_vanilla|{hp}`. Multi-pass results would be mislabelled, never reach H3, and appear as extra rows. No ep5 results exist yet, so nothing is wrong today.

## MINOR
10. **Hidden width differs from the PREREG.** `mult*d` gives 3360 (MNIST) and 20480 (CIFAR) vs the stated 3200/20000 (`cl_backprop.py:4`); STATUS/PREREG say 3200. Unlisted deviation.
11. **FlyModel clip semantics are correct** (`cl_bench.py:32`). I verified that all three feature sets have min = 0.0 (post-ReLU), so psi >= 0, increments >= 0, and clip-after-sum equals clip-each-step.
12. **`class_incremental_eval` and `summ` are consistent, but the metrics degenerate for chance-level methods.**
    - `memloss` includes the last task (R[T-1][T-1] - R[T-1][T-1] = 0), which dilutes it by 1/T. This is documented in `clmetrics.py`.
    - F2b shows memloss 0.0000 and F2 0.004, and they look "perfectly stable" at chance. Report memloss only next to learn_acc and final accuracy.
    - Accuracy is sample-weighted and MNIST-20 is class-imbalanced (5.4k-6.7k per class), so chance is not exactly 1/K.
13. **Leakage: none found.**
    - `audit_run.py:7-9` takes a 10% per-class val set. Tuning runs on Xs -> Xv (lines 23-25), and the final run uses Xtr -> Xte. No hyperparameter reads test data except the analysis max in 5.
    - Features come from KMNIST-trained LeNet and an ImageNet ResNet; neither saw the test sets. ImageNet pretraining gives semantic overlap with CIFAR-100, a caveat rather than a leak.
    - Validation uses seed 0 only (noisy for random methods; seed-0 projection is also in the test seeds, which is harmless).
    - The offline lr is hardcoded 1e-3 (`audit_run.py:47`), not tuned.
14. **SLDA is correct.**
    - The scatter is (Sxx - sum n_i m_i m_i^T)/N, which is right (`cl_baselines.py:20`).
    - The shrink is a ridge of shrink*tr/d (not a convex combination), and the discriminant W=MΛ, b=-0.5 mΛm is right.
    - Seen == learned at every prediction, so restricting to seen is consistent.
    - Winners at the grid edge (shrink 1e-3) only make SLDA slightly conservative.
    - NCM and ClassSumDot are also correct.
    - ER reservoir sampling and replay are correct (`cl_backprop.py:23-35`).
    - The unused `method` argument is harmless: behaviour is selected by hp.
15. **Store race.** The per-key file with `os.replace` fixes the lost update (`audit_run.py:13-14`). `*.json.tmpPID` files are not matched by the `*.json` glob. Remaining races are benign:
    - `cached()` checks a snapshot taken at start-up, so two processes can both compute a key and the last write wins. This could mix cpu/mps values for one key, and `best|` is chosen from the stale snapshot.
    - `test_store.py` tests a copy of the write pattern, not `put()` itself.
16. **Overstatement in STATUS.** "SLDA beats FlyModel +0.054/0.060/0.131" is confirmed. "Preliminary" numbers are described as unreviewed, which is correct. The "H3 holds on MNIST" verdict (+0.084 vs ER-200) rests on the degenerate B1/B2 and an ER-200 at an lr-grid edge.

## Verdict
- **H1 (as a direction), trustworthy:** FlyModel F0 does not beat SLDA on any benchmark. The margins (0.05-0.13) far exceed the test-max bias and tuning asymmetry. The wording should be "dominated", not "equivalent".
- **H2 is computed as pre-registered but weakly interpretable** (see 7). The statistics are fine.
- **H3 is NOT trustworthy.** It has 1 of 3 benchmarks, the vanilla/EWC baselines are at chance because of intra-task class-ordered streaming, and the grids are truncated. Do not cite it until items 1-3 are addressed.

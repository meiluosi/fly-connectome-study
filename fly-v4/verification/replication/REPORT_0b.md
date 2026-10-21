# Independent replication, stage 0b (teacher_pert, teacher_shuf)

Code: rep_0b.py (own implementation; run as `python3 rep_0b.py <task> 60`). Seeds: numpy default_rng, world w seeded base+w (100000 pert, 200000 shuf). Bootstrap: 10000 resamples of worlds, seed 1. 60 worlds per task; auc = mean of 41 test accuracies.

## teacher_pert (N_worlds=60)
| student | mean auc | SD over worlds |
|---|---|---|
| real | 0.7371 | 0.0261 |
| shuffled | 0.6720 | 0.0219 |
| random | 0.6732 | 0.0238 |

| paired diff | mean | 95% bootstrap CI | worlds diff>0 |
|---|---|---|---|
| real-shuffled | +0.0650 | [+0.0601, +0.0701] | 60/60 |
| real-random | +0.0639 | [+0.0581, +0.0696] | 60/60 |
| shuffled-random | -0.0011 | [-0.0050, +0.0028] | 27/60 |
| shuffled-real | -0.0650 | [-0.0699, -0.0601] | 0/60 |

runtime 46s

## teacher_shuf (N_worlds=60)
| student | mean auc | SD over worlds |
|---|---|---|
| real | 0.6058 | 0.0265 |
| shuffled | 0.6263 | 0.0258 |
| random | 0.6282 | 0.0302 |

| paired diff | mean | 95% bootstrap CI | worlds diff>0 |
|---|---|---|---|
| real-shuffled | -0.0204 | [-0.0256, -0.0151] | 12/60 |
| real-random | -0.0224 | [-0.0273, -0.0170] | 8/60 |
| shuffled-random | -0.0020 | [-0.0055, +0.0017] | 26/60 |
| shuffled-real | +0.0204 | [+0.0151, +0.0257] | 48/60 |

runtime 44s

## Ambiguities resolved
- Tie-breaking: random uniform noise in [0,0.5) added to psi (psi values are sums of integer-valued counts, so noise only reorders exact ties). Applied to teacher, student, train and test codes.
- 30% perturbation: m = round(0.3 * nonzero count) per KC, capped by number of zero rows; moved entries keep values; destinations are distinct random zero rows. KCs with m=0 unchanged.
- Teacher uses the same top-5% (102) rule on all 2045 KCs; teacher q ~ U[0,1] drawn per world; median over the 900 outputs; >= median gives +1.
- Each student's codes use that student's wiring; N and signs are always the real ones. Real student uses P unchanged (so under teacher_pert it sees the unperturbed P).
- Odours: 6 distinct glomeruli, independent draws (duplicates among odours possible, not removed).
- Training cycles odour index t mod 600 for 400 trials (so only first 400 odours used). Measurement at t=0 before learning and after trials 10,...,400 -> 41 points. Update of q only for the active KCs and (k,j) with N>0; delta computed from v before update. v sign: >=0 predicts +1.
- Shuffled/random students and the teacher are fresh draws per world; all three students share the same odours, labels and teacher within a world but have independent wiring/tie-break draws.
- The sign(v) accuracy for a valence of exactly 0 counts as +1 as specified.
- The held-out test accuracy for the random-wiring student uses the real N rows (spec silent; assumed).

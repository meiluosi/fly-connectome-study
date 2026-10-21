# REPORT_4 - independent re-implementation (rep_4.py)

Code: rep_4.py (run `OMP_NUM_THREADS=1 python3 rep_4.py`; 4 worker processes). Runtime 106 s for everything. Raw tables below are the script output (rep_4_output.md).

## Ambiguities and how I resolved them
- Active set is drawn once per odour per world (random tie-break via random key), and shared across learners within a world (same world seed -> same odours, labels, active sets), so differences are paired. Tuning seeds 100000+i, test seeds 200000+i. COMP_PERM's permutation uses a separate rng seeded from the world seed.
- GLOBAL baseline B0 uses q=0.5 with sign; scale = 0.5*sum N|sign| over active KCs (|sign|=1). COMP scale uses |s_j|, so cl=0 MBONs are excluded.
- delta=0 gives no change. v is computed before the update with the current q. Accuracy: sign(v), v=0 -> +1.
- 'after' = mean over the 4 tasks of accuracy on that task's 10 odours immediately after finishing it. 'final' = accuracy on all 40 after task 4.
- COMP_PERM tuned its own eta from the grid (as "per learner"). GLOBAL_MATCHED = GLOBAL at the grid eta whose tuning-mean 'after' is closest to COMP's tuned mean 'after'.
- SE: spec says both "600 training trials" and "400 trials"; I used 400. Per world: 100 test odours held out at random, training odours drawn with replacement from the other 201; 8 random groups over all 301 odours, random +-1 group labels; test accuracy measured after every 10 trials (40 points, no point at trial 0); auc = mean of these. SE tuning criterion: max mean auc.
- Bootstrap: 10000 resamples of worlds, percentile 95% CI.


### CL tuning (mean over 20 tuning worlds)
| learner | eta | after | final |
|---|---|---|---|
| GLOBAL | 0.005 | 0.8575 | 0.7787 |
| GLOBAL | 0.01 | 0.8887 | 0.7913 |
| GLOBAL | 0.02 | 0.9313 | 0.7888 |
| GLOBAL | 0.05 | 0.9713 | 0.7625 |
| GLOBAL | 0.15 | 0.9887 | 0.7438 |
| GLOBAL | 0.4 | 0.9687 | 0.7212 |
| GLOBAL | 1.0 | 0.8175 | 0.6275 |
| COMP | 0.005 | 0.8238 | 0.7750 |
| COMP | 0.01 | 0.8387 | 0.7900 |
| COMP | 0.02 | 0.8612 | 0.8125 |
| COMP | 0.05 | 0.8950 | 0.8262 |
| COMP | 0.15 | 0.9200 | 0.8263 |
| COMP | 0.4 | 0.9100 | 0.8037 |
| COMP | 1.0 | 0.9075 | 0.8000 |
| COMP_PERM | 0.005 | 0.7313 | 0.6725 |
| COMP_PERM | 0.01 | 0.7537 | 0.6912 |
| COMP_PERM | 0.02 | 0.7775 | 0.7263 |
| COMP_PERM | 0.05 | 0.7913 | 0.7300 |
| COMP_PERM | 0.15 | 0.7925 | 0.6988 |
| COMP_PERM | 0.4 | 0.7700 | 0.6850 |
| COMP_PERM | 1.0 | 0.7662 | 0.6838 |

Chosen eta: {'GLOBAL': 0.01, 'COMP': 0.15, 'COMP_PERM': 0.05}
GLOBAL_MATCHED eta=0.02 (tuned COMP after=0.9200)

### CL test (100 worlds)

| learner | eta | after | final |
|---|---|---|---|
| GLOBAL | 0.01 | 0.8967 | 0.7892 |
| COMP | 0.15 | 0.9157 | 0.8288 |
| COMP_PERM | 0.05 | 0.7283 | 0.6362 |
| GLOBAL_MATCHED | 0.02 | 0.9320 | 0.7862 |

Paired differences (final), mean [95% bootstrap CI]:

- COMP - GLOBAL: +0.0395 [+0.0260, +0.0530]
- COMP - GLOBAL_MATCHED: +0.0425 [+0.0282, +0.0565]
- COMP - COMP_PERM: +0.1925 [+0.1670, +0.2185]

### SE tuning (mean over 20 tuning worlds)
| learner | eta | auc |
|---|---|---|
| GLOBAL | 0.005 | 0.6320 |
| GLOBAL | 0.01 | 0.6318 |
| GLOBAL | 0.02 | 0.6320 |
| GLOBAL | 0.05 | 0.6294 |
| GLOBAL | 0.15 | 0.6251 |
| GLOBAL | 0.4 | 0.6078 |
| GLOBAL | 1.0 | 0.5812 |
| COMP | 0.005 | 0.6335 |
| COMP | 0.01 | 0.6343 |
| COMP | 0.02 | 0.6356 |
| COMP | 0.05 | 0.6370 |
| COMP | 0.15 | 0.6270 |
| COMP | 0.4 | 0.5964 |
| COMP | 1.0 | 0.5679 |
| COMP_PERM | 0.005 | 0.6252 |
| COMP_PERM | 0.01 | 0.6248 |
| COMP_PERM | 0.02 | 0.6214 |
| COMP_PERM | 0.05 | 0.6128 |
| COMP_PERM | 0.15 | 0.5931 |
| COMP_PERM | 0.4 | 0.5582 |
| COMP_PERM | 1.0 | 0.5312 |

Chosen eta: {'GLOBAL': 0.005, 'COMP': 0.05, 'COMP_PERM': 0.005}

### SE test (60 worlds)

| learner | eta | auc |
|---|---|---|
| GLOBAL | 0.005 | 0.6365 |
| COMP | 0.05 | 0.6310 |
| COMP_PERM | 0.005 | 0.6053 |

Paired differences (auc), mean [95% bootstrap CI]:

- COMP - GLOBAL: -0.0055 [-0.0105, -0.0007]
- COMP - COMP_PERM: +0.0257 [+0.0064, +0.0483]

Runtime 106s

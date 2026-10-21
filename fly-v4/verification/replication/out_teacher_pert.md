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
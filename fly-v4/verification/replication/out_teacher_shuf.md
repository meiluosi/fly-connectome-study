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
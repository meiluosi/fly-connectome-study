# raw output

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

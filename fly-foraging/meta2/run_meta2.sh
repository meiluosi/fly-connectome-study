#!/bin/bash
cd "$(dirname "$0")"
PY=/Users/meros/Desktop/fly-mb-compartments/ml-cl-audit/.venv/bin/python
export OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
for s in 0 1 2; do for k in real shuffled random; do $PY evolve_b.py $k $s > evo2_${k}_${s}.log 2>&1; done; done
$PY eval_meta2.py > eval_meta2.log 2>&1
echo META2_DONE

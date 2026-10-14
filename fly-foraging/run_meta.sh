#!/bin/bash
cd "$(dirname "$0")"
PY=/Users/meros/Desktop/fly-mb-compartments/ml-cl-audit/.venv/bin/python
for s in 0 1 2; do for k in real shuffled random; do $PY evolve.py $k $s; done; done
echo META_ALL_DONE

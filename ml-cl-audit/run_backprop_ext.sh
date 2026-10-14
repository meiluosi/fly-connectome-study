#!/bin/bash
# MNIST-20 backprop baselines: extended grids (class-ordered stream, registered) then interleaved stream (pre-declared extension). Sequential on purpose.
cd "$(dirname "$0")"
AUDIT_STREAM=ordered .venv/bin/python audit_run.py mnist20 backprop 3
AUDIT_STREAM=inter   .venv/bin/python audit_run.py mnist20 backprop 3
echo BACKPROP_EXT_DONE

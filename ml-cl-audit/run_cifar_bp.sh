#!/bin/bash
# CIFAR-100 backprop baselines for H3 (registered grids, class-ordered stream first, then the pre-declared interleaved stream), sequential on MPS. Cached per key; safe to re-run.
cd "$(dirname "$0")"
export AUDIT_DEVICE=mps
for b in cifar100 cifar100_224; do AUDIT_STREAM=ordered .venv/bin/python audit_run.py $b backprop 3; done
for b in cifar100 cifar100_224; do AUDIT_STREAM=inter .venv/bin/python audit_run.py $b backprop 3; done
echo CIFAR_BP_DONE

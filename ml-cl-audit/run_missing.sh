#!/bin/bash
# sequential re-run of lost / pending stages (cache fills only what is missing)
cd "$(dirname "$0")"
for b in mnist20 cifar100 cifar100_224; do .venv/bin/python audit_run.py $b proto; done
for b in mnist20 cifar100 cifar100_224; do .venv/bin/python audit_run.py $b supp; done
for b in mnist20 cifar100 cifar100_224; do .venv/bin/python audit_run.py $b offline 4; done
echo ALL_FAST_STAGES_DONE

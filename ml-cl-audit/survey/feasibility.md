# Feasibility: bio-inspired CL methods on an M4 laptop (16 GB, MPS/CPU)

Method: README/arXiv pages only; nothing cloned. Confidence in brackets. Compute figures are my estimates unless a README says otherwise.

## Candidates

**1. FlyModel (Shen, Dasgupta, Navlakha, Neural Comput. 2023)**
- Official repo: none found. The MIT page returned 403 and searches surfaced no author code. [medium]
- Only a third-party port exists: https://github.com/Ramos-Ramos/FlyModel. It is unofficial, MIT, pip-installable, and targets the 2021 arXiv version (2107.07617). It has 5 stars and 11 commits, and its README shows no reproduction of the paper's numbers. [high]
- Paper datasets (my recollection, unverified): MNIST and FashionMNIST, class-incremental. [medium]
- The algorithm is a sparse random projection, k-WTA, and a Hebbian-style update with a frozen rest, with no backprop. It is easy to re-implement in about 100 lines of NumPy/PyTorch. Compute is minutes on CPU. No Apple obstacles.
- Verdict: re-implement from the paper and use the port only as a cross-check.

**2. SDM Continual Learner (Bricken et al., ICLR 2023)**
- Official repo: https://github.com/TrentBrick/SDMContinualLearner [high]
- License: not seen in the fetched summary. Check the repo before reuse. [unknown]
- Requirements: Python 3.9, setuptools 59.5.0, `requirements.txt`, and Numenta's Active Dendrites codebase (for baselines). Optional wandb. Versions are pinned to older PyTorch, so the README warns alternatives carry no guarantee.
- Datasets: MNIST and CIFAR-10 auto-download (MNIST about 12 MB packed, CIFAR-10 about 170 MB). Pre-computed ConvMixer CIFAR-10 embeddings are provided. CIFAR-100 (about 160 MB) and ImageNet32 embeddings are on Google Drive (sizes unstated).
- Reproduction: the README claims all paper experiments except FashionMNIST, with hyperparameters in `exp_commands/`.
- Compute: not stated. With frozen embeddings I expect minutes to about an hour on CPU or MPS. CUDA use in the code is unverified.
- Obstacles: old pinned stack, the Active Dendrites dependency, and Google Drive downloads. Python 3.9 should work on arm64 via conda or uv.

**3. FlyPrompt (arXiv 2602.01976, ICLR 2026)**
- Official repo: https://github.com/AnAppleCore/FlyGCL [high, linked from the arXiv abstract page]. MIT license.
- Requirements: Python 3.10+, PyTorch with CUDA, `requirements.txt`.
- Datasets: CIFAR-100 (auto, about 160 MB), ImageNet-R (manual, about 2 GB), CUB-200-2011 (manual, about 1.1 GB).
- Backbone: pretrained ViT-B/16 checkpoints from Hugging Face or Baidu (about 350 MB).
- Setting: Si-Blurry GCL. README claims were not verified as exact numbers. [low]
- Compute: ViT-B/16 forward and backward on 100-class data. Mammoth-style prompt methods usually need a GPU. Inference-only feature extraction on MPS is feasible, but full training is likely too slow (many hours). The CUDA assumption must be patched (device strings, AMP).
- Verdict: not practical in full. Feasible only as frozen-feature routing, which is a re-implementation.

**4. Other fly/sparse-expansion methods**
- Fly-CL (ICLR 2026, arXiv 2510.16877): https://github.com/gfyddha/Fly-CL [high]. MIT. Python 3.9, PyTorch 1.13.1+cu117, torchvision 0.14.1, timm 0.9.16, numpy<2.0.
- Fly-CL datasets: CIFAR-100, CUB-200, VTAB. It uses a frozen pretrained backbone with a fly-style expansion and decorrelation head, so it is training-light.
- Fly-CL on Mac: the only CUDA-specific item is the cu117 pin. Feature extraction on MPS or CPU is fine, and the head is cheap. This is the most laptop-friendly published fly CL with official code. [medium]
- A Hopfield/SDM-style paper (arXiv 2307.15040) exists, but I did not check its code.
- fly-critic (bryjudy/fly-critic) appeared in search. I did not assess it. I do not know whether it is related to your project.

**5. Baselines and libraries**
- Mammoth (https://github.com/aimagelab/mammoth): needs PyTorch >= 2.1, includes EWC, LwF, ER, and DER++, and is well-maintained with 70+ methods and 20+ datasets. MPS is not documented, so test it. It is heavier in code and abstraction. [high]
- Avalanche (https://github.com/ContinualAI/avalanche): MIT, `pip install avalanche-lib`, active (about 3.9k commits), with Naive, EWC, LwF, and Replay. It is still labelled Beta. MPS is not documented, but it is plain PyTorch with a `device` argument. Pinned torch versions may lag. [medium]
- Lightest and best-maintained pick: write EWC, LwF, replay, and fine-tune in about 200 lines of PyTorch for full control. Avalanche is the best library fallback for an audit because the strategies are small and readable. Use Mammoth only if you need DER++ or the transformer-era benchmarks. continuum was not assessed.

## Recommended minimal laptop suite
Each benchmark takes under about 1 hour for a small MLP, 5 seeds, and all baselines on MPS or CPU.

| Benchmark | Source | Size |
|---|---|---|
| Split-MNIST (5 tasks, class-IL and task-IL) | torchvision `MNIST` (`train-images-idx3-ubyte.gz` etc.) | about 12 MB |
| Permuted-MNIST (about 10 tasks) | same files | none extra |
| Split-FashionMNIST | torchvision `FashionMNIST` | about 30 MB |
| Split-CIFAR-10 / CIFAR-100 on frozen features | torchvision `cifar-10-python.tar.gz` (about 163 MB); CIFAR-100 about 161 MB; a frozen ResNet-18/ViT-S extractor, run once (weights about 45 to 85 MB, from torchvision or timm) | about 0.2 to 0.4 GB |

Optional: SDM's provided ConvMixer CIFAR-10 embeddings, to avoid running an extractor and to match the paper.

Methods to include:
- Bio-inspired: FlyModel (own re-implementation), SDM (official code or re-implementation), Fly-CL head.
- Baselines: fine-tune (lower bound), joint (upper bound), EWC, LwF, replay (buffer of 200 and 1000), and optionally DER++ or SI.

## Downloads requiring your approval
All sources are the official hosts through torchvision/timm. The Google Drive embeddings, ImageNet-R/CUB, and the ViT-B/16 checkpoint are not in the minimal set.
- MNIST: 4 files, about 12 MB.
- FashionMNIST: 4 files, about 30 MB.
- CIFAR-10: `cifar-10-python.tar.gz`, about 163 MB.
- CIFAR-100: `cifar-100-python.tar.gz`, about 161 MB.
- Pretrained backbone weights: about 45 to 85 MB (for example torchvision resnet18, or timm vit_small).
- Python packages (torch, torchvision, optionally avalanche-lib): roughly 0.5 GB or more.

## Bottom line
- Official laptop-friendly code: Fly-CL (frozen features) and SDMContinualLearner (older pinned stack).
- FlyPrompt: official repo exists but is CUDA-oriented and heavy.
- FlyModel: no official code. Re-implement it, since it is simple.
- Baselines: hand-write them or use Avalanche.

Sources:
- https://github.com/TrentBrick/SDMContinualLearner
- https://github.com/AnAppleCore/FlyGCL
- https://arxiv.org/abs/2602.01976
- https://github.com/gfyddha/Fly-CL
- https://github.com/Ramos-Ramos/FlyModel
- https://github.com/aimagelab/mammoth
- https://github.com/ContinualAI/avalanche

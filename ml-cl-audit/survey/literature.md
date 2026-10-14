# Literature audit: bio-inspired CL under matched plasticity

Search limits: WebSearch and WebFetch only. Several full PDFs (FlyModel, SDM) came back as binary, and bioRxiv/MIT returned 403. So details below that I did not see in a primary text are marked UNVERIFIED. Confidence is given per claim.

## 1. Bio-inspired CL papers

| Paper | Claim (verified from abstract/snippet) | Benchmarks / baselines / metrics |
|---|---|---|
| Shen, Dasgupta, Navlakha, Neural Comput. 35(11), 2023. https://direct.mit.edu/neco/article/35/11/1797/117579 (also https://cseweb.ucsd.edu/~dasgupta/papers/SDN23.pdf) | Sparse high-dimensional expansion plus updating only synapses between active neurons and the target output; frozen elsewhere. Claimed to reduce forgetting vs perceptron and to beat existing CL methods in class-incremental settings. | Details UNVERIFIED (PDF unreadable). From memory: MNIST/Fashion-MNIST/CIFAR-100 features, class-incremental, baselines EWC/GEM/BI-R-type, accuracy. I did not confirm that learning accuracy (A_jj) is reported separately or that baselines were tuned per-method. |
| Robinson et al., bioRxiv 2023. https://www.biorxiv.org/content/10.1101/2023.01.18.524467v1.full | Generative replay as a model of the mushroom-body long-term-memory circuit. Claimed +20% on CIFAR-100 class-incremental, within 2% of the non-incremental upper bound. | Only the abstract was seen. Baselines and tuning UNVERIFIED. |
| Bricken et al., ICLR 2023. https://arxiv.org/abs/2303.11934 | SDM-derived MLP (top-k activation, etc.) is a continual learner with no replay or task info; all components necessary; combined with EWC it is SOTA on CIFAR-10. | Benchmark and metric details UNVERIFIED (I only saw the abstract). Note that top-k sparsity directly limits per-task plasticity, which is exactly the confound in question. |
| FlyPrompt, ICLR 2026. https://arxiv.org/abs/2602.01976 | Random expansion routing plus temporal-ensemble experts. Up to +11.2/12.4/7.6 pp A_auc and +13.5/16.5/12.3 pp A_last on CIFAR-100/ImageNet-R/CUB-200. | Si-Blurry GCL, pretrained ViT. Baselines are L2P, DualPrompt, CODA-P, MVP, MISA, S-Prompt++, HiDe, NoRGa, SD-LoRA. Metrics are A_auc and A_last, with anytime-accuracy curves. No separate A_jj or forgetting table was seen in the HTML summary. Baseline tuning not stated in what I saw. Code: https://github.com/AnAppleCore/FlyGCL |

Other related papers seen (not examined in depth): Continual Learning via Sparse Memory Finetuning, https://arxiv.org/abs/2510.15103; sparse-recurrent/activity-regularization CL, https://arxiv.org/abs/2212.04316; Hebbian/sparse CL survey, https://arxiv.org/abs/2407.17305; Distillation-Guided Structural Transfer beyond SDM, https://arxiv.org/abs/2512.15267. Confidence that the list is incomplete: high.

Pattern (medium confidence, from abstracts only): the fly papers headline final accuracy or A_last, and I found no evidence of matched-plasticity comparison in any of them.

## 2. Evaluation-pitfall literature (verified at abstract/snippet level)

- Chaudhry et al., RWalk, ECCV 2018. Introduces forgetting and intransigence as separate metrics and reports the trade-off. https://openaccess.thecvf.com/content_ECCV_2018/html/Arslan_Chaudhry__Riemannian_Walk_ECCV_2018_paper.html (high)
- Farquhar & Gal 2018, https://arxiv.org/abs/1805.09733. Desiderata for evaluation (shared head, no task labels, more than 2 tasks). The abstract does not address the forgetting-vs-learning confound (high).
- Mai et al. 2022, Neurocomputing, https://arxiv.org/abs/2101.10423. Empirical online-CL survey with fair-comparison protocol and tricks such as NCM and review (high).
- Cha & Cho, "Hyperparameters in Continual Learning: A Reality Check", TMLR 2025, https://arxiv.org/abs/2403.09066. Tuning on the test scenario overestimates; over 8,000 runs show most SOTA methods fail to replicate (high).
- Michel et al. 2023, "New metrics for analyzing continual learners", https://arxiv.org/abs/2309.00462. "Setup-induced forgetting"; standard metrics confound difficulty with stability (high).
- De Lange et al., stability gap, https://arxiv.org/abs/2205.13452 (continual evaluation; high).
- Pareto Continual Learning, https://arxiv.org/abs/2503.23390. Treats stability-plasticity as multi-objective with a Pareto front, but as a method, not as an audit of published claims (high).
- Rethinking stability-plasticity from an architectural perspective, https://arxiv.org/abs/2506.03951. Compares at matched parameter counts and discusses frontier shifts (medium; skimmed via search snippet).
- Forget Forgetting, https://arxiv.org/abs/2502.07274, and the Forgetting-vs-relative-forgetting commentary surfaced in search (snippet-level, low-medium).
- The snippet "forgetting metric unfairly favors models with poorer initial performance" appeared in search results without a source I could pin down. Do NOT cite it until traced (low).

I did not find a paper that explicitly requires comparing methods at matched A_jj as a standard protocol. RWalk and the Pareto/trade-off work come closest.

## 3. Novelty verdict

Verdict: (b)/(c). The general principle is known (RWalk 2018; Michel 2023; Cha & Cho 2025; Pareto CL 2025). I found NO paper that systematically re-evaluates fly/mushroom-body/SDM/k-WTA CL claims under matched-plasticity or Pareto-front protocols. For the bio-inspired-specific audit the idea is open (c); for the general principle it is partly done (b), so the contribution must be framed as an empirical audit plus a concrete protocol, not a new insight.

Confidence: about 70% that nothing directly equivalent exists. Limits: US-only WebSearch, no Google Scholar or OpenReview search, PDFs unreadable, and 2026 preprints are poorly indexed. Before committing, search Semantic Scholar and Google Scholar for "matched plasticity", "iso-plasticity", "forgetting confounded by learning accuracy", and citations of FlyModel and Bricken.

## 4. Suggested re-evaluation targets (ranked by informativeness, laptop-feasible)

1. FlyModel (Shen 2023) vs EWC/SI/replay on Split-MNIST and Split-CIFAR-100 on frozen features. Cheap, and the method has a sparsity/learning-rate knob that sweeps plasticity. Highest value because it is the canonical fly claim.
2. Bricken SDM-MLP (top-k, sparse init) vs a dense MLP with a matched learning-rate/epoch sweep on Split-CIFAR-10 and FMNIST. Tests whether sparsity helps forgetting only by lowering A_jj.
3. FlyPrompt random-expansion head vs a simple RanPAC/ridge-projection or NCM baseline on frozen-backbone CIFAR-100 (Si-Blurry or class-incremental). The backbone is a pretrained ViT, so use cached features. Tests whether the gain is routing or just a stronger or less plastic head.
4. Your compartmentalised-gating ablation, generalized: the same method with the gating strength swept and compared at equal A_jj.
5. Robinson generative-replay LTM vs a plain replay baseline at matched buffer and compute (lower priority; replay budget is a confound).

Protocol for each: tune every method with the same hyperparameter budget, ideally using the Cha & Cho two-phase idea (tune on a different dataset). Sweep a plasticity knob (learning rate, epochs, sparsity k, gating strength) for every method. Report:
- A_jj (accuracy right after learning task j) and average learning accuracy
- final accuracy A_T and average accuracy
- forgetting F = mean(A_jj - A_Tj) and relative forgetting F/A_jj (to remove the plasticity bias)
- intransigence (RWalk) against a joint-training reference
- stability-plasticity frontier: curve of A_T versus mean A_jj for each method, with the area under the frontier (or hypervolume) and the gap between frontiers at matched A_jj
- at least 5 seeds with confidence intervals; compare methods only at matched A_jj via interpolation along the frontier.

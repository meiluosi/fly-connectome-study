# Review: Bennett, Philippides, Nowotny 2021 (Nat Commun) and the novelty of an MB-bandit project

Read: PMC full text, first ~100k of 139k chars (Methods, Results, Predictions); the last ~39k chars (mostly Methods tail, Data availability) were read only through a targeted extraction. Not read: the bioRxiv version, and the Supplementary Information beyond what the main text states. All quotes below came through a summarising fetch tool, so verify them against the PDF before citing.
URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC8105414/

## 1. Model (Methods; Results)
- **Units.** Rate units y = f(sum w_j x_j), f = max(0,.). PNs are not modelled ("bypass the computations performed in nuclei upstream").
  - KCs: "unique population of 10 KCs to each cue", each at 1 Hz, so N_K = 10 x N_cues and cues do not overlap.
  - Supplementary variant: 2000 KCs, each assigned to a cue with p = 0.05, with total activity normalised to 10 Hz. A blocking variant uses overlapping KC sets.
  - Two MBONs: M+ (approach) and M- (avoid). Two DANs: D+ and D-.
  - Reinforcement: r+ = max(0,r) and r- = min(0,r).
- **Readout.** KC to MBON weights are plastic, initialised w = 0.1*U[0,1]. The reinforcement prediction (RP) is m_hat = m+ - m-.
- **DANs (VS model, valence-specific).** d±_q = f(r±_q + w_M m∓_q + w_K·k_q), with w_M = 1 and w_K = gamma*1.
- **DANs (MV model, mixed-valence).** d±_q = f(r±_q - r∓_q - w_M m±_q - m∓_q + w_K·k_q).
- **Objective and rule.** The cost is C = 1/2 sum (r_hat - m_hat)^2, so the DAN difference d+ - d- implements a reinforcement prediction error (RPE).
  - Plasticity (Eq. 21, VS): w±(t+1) = w± + eta*k_q*(w_K·k_q - d∓_q). The VS_lambda variant replaces w_K·k with a constant lambda.
  - MV rule (Eq. 22): eta*k*(d± - d∓).
  - Only the chosen cue's weights are updated. This is a delta rule.
- **Parameters.** eta = 0.025 (Figs 2-3), 0.1 (Fig 4), 0.05 (Fig 5), halved for MV. sigma_R = 0.1.
  - lambda is "11.5" in Results and 12 in Methods, an unresolved inconsistency. gamma is 0 to 1.1.
  - The softmax beta is a "constant" but no value is given in what I read.
- **Task (multi-armed bandit, forced choice).** Each trial:
  1. Compute m_hat for each cue.
  2. Softmax: p_i = exp(beta m_hat_i)/sum_j exp(beta m_hat_j). Choice is by inverse-CDF sampling.
  3. Receive reinforcement (mean mu plus noise) and update the chosen cue only.
- **Arms.** 2 in the main figures; up to 200 reported; 2 odours (CS+, CS-) in conditioning.
- **Conditioning protocol (Fig 5).** 10 CS+/US trials, 10 CS- trials, 2 test trials; shibire-like block (x0.1) and dTrpA1-like activation (+5).

## 2. Non-stationarity and baselines
| Question | Answer |
|---|---|
| Non-stationary reward | **Yes, but narrow.** Figs 2-3: mu steps of +1 at trials 21, 41, 141, 161 and -1 at 61, 81, 101, 121. Fig 4 and Supp Fig 6: filtered Gaussian noise, tau = 10 trials. The text does not call these reversal learning. |
| Reversal learning (named) | No |
| Extinction | Not simulated as a protocol. Discussed in Predictions. Supp Fig 8 fits re-evaluation data (re-exposure of CS+ or CS-), and the repo includes Felsenberg extinction data. |
| Rescorla-Wagner | Partial. RW is invoked to explain blocking, and the rule is described as a delta rule and "a simplified case" of TD. It is not a separate benchmark. |
| TD / Q-learning | TD discussed, not implemented. Q-learning not mentioned. |
| UCB, Thompson, epsilon-greedy, sliding-window | **No** |
| Any baseline | Only a "perfect plasticity" model (RP = last reward). VS_lambda and MV are "only marginally outperformed" by it. |

Their model has no explicit exploration mechanism beyond softmax. A valence-specific variant can converge to equal predictions across cues and then choose randomly (reported in the abstract-level summary; I did not locate the exact passage).

## 3. Code
- Archived at Zenodo DOI 10.5281/zenodo.4531420. Latest version: https://github.com/BrainsOnBoard/paper_RPEs_in_drosophila_mb
- **MATLAB** only, license **GPL-3.0**, 15 commits (last date not visible).
- Setup: unzip `zmy_utils.zip`, set `fpath`, and run `mb_vs_mv_analysis(flag)`.
  - A single VS run takes under a second. The Fig 5 sweep (96 interventions) takes hours.
  - It needs the Parallel Computing Toolbox for some flags. The README reports testing on R2012a and R2018b.
  - It contains `mb_reward_schedules.m` and `mb_vs.m` (the core file). Easy to port to Python from the equations above (a few lines); Octave compatibility is untested.
  - A GPL-3.0 port would need to stay GPL-compatible if it copies code. Re-implementing from the paper avoids this.

## 4. Related work (2021-2026)
1. Danieli & Lepperod, "A bio-inspired minimal model for non-stationary K-armed bandits" (arXiv 2025; Biol Cybern 2026). Rate-neuron model (OFC/ACC-inspired, **not MB**). Benchmarks against TS and UCB on piecewise, drifting and sinusoidal non-stationary bandits. https://arxiv.org/abs/2509.22209
2. Springer & Nawrot, minimalistic MB circuit model of conditioning and extinction (eNeuro 2021; titled "A Mechanistic Model for Reward Prediction and Extinction Learning in the Fruit Fly"). Covers extinction, no bandit baselines. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8211469/
3. Jiang & Litwin-Kumar, "Models of heterogeneous dopamine signaling in an insect learning and memory center" (PLoS CB 2021). RPE emerges across the DAN population. I could not confirm reversal or extinction content from the full text. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8354444/
4. Gkanias et al., "An incentive circuit for memory dynamics in the mushroom body" (eLife 2022, 75611). Covers memory dynamics including reversal and extinction. I could not load it and did not read it, so this is from the search listing only. https://elifesciences.org/articles/75611
5. McCurdy et al. (Nat Commun 2021), dopaminergic encoding of punishment omission during reversal learning in flies. Experimental, not a model. (Cited via search result; I did not fetch it.)

Also: Prediction-error spiking larva MB model (iScience 2024), https://pmc.ncbi.nlm.nih.gov/articles/PMC10824792/. Gap-junction MB-inspired network for sparse-reward RL (PLoS CB 2024), https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11152299/.

**None found compares an MB model to UCB, Thompson sampling or ant-colony optimisation.** Web search only; it is not an exhaustive literature search.

## 5. Verdict
**Novelty: largely open (about 75% confidence).** The pieces exist separately: MB RPE model, MB extinction and reversal models, and bio-inspired non-stationary bandit models benchmarked against TS and UCB. I found no matched-budget MB versus bandit and pheromone comparison. I did not search Google Scholar's citing-papers list, so absence is not proven.

**Risks.**
1. **Reviewer framing: "just a delta rule."** The VS/MV rule is a delta rule on one-hot-like KC codes (10 KCs per cue, no overlap), so it is mathematically close to a constant-step-size Q-learner or exponential recency average, and softmax exploration is not exploration-aware. Expect it to match discounted epsilon-greedy and lose to discounted-UCB, sliding-window UCB or Thompson on regret. The ablations must show whether sparse expansion adds anything beyond a tabular learner.
2. **Sparse expansion can matter only with structure.** With independent arms, KC expansion is irrelevant. It helps only with correlated or contextual arms, noisy cue identity, or generalisation. Without that, the result is a null by construction.
3. **Underspecified and unfair comparisons.** Beta, lambda (11.5 vs 12) and gamma are unspecified or inconsistent, so tuning budgets must be equalised. The "pheromone" baseline is a loose analogue of bandit value tracking (evaporation plays the role of discounting), so it adds little, and "matched budget" needs a precise definition (parameters, tuning trials, compute).

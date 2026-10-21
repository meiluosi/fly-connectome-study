# Review of stage 5 and 5b (context-free)

Scope: PREREG_v4_stage5/5b, v4core_f/g, run_v4f/g, analysis_v4f/g, RESULTS, NOTES. I did not modify any project files.
SHA256 files: all listed files verify OK with `sha256sum -c` (the two "improperly formatted" warnings are the `#` header lines).
I re-ran small diagnostics (scratchpad `chk.py`, `chk2.py`, and inline snippets, seeds 5000-5059) to check each finding below.

## Verdict
There are no outright code bugs in the lesion mechanics, the bookkeeping or the CI/tier code. The problems are in design and interpretation. The rankings are confounded with how much of the code (stage 5) or how much of the odour signal (5b) each lesion removes. The main teacher-task contrasts are circular in a different way than NOTES says. Several NOTES sentences are stronger than the data.

## Ranked findings

### 1. [CONFIRMED, high] Stage 5 "excess loss" for `active` is a code-coverage artefact, so the headline family is nearly tautological
- Seed 5003, door_teacher_real, real wiring:
  - `active` 818 removes 93% of the intact code slots; a random 818 removes 40%.
  - 33% of the lesioned code then lands on KCs never active in training (random: 3%; intact: 1%).
  - 1263 of 2045 KCs are ever active in training, and the top-409 `active` KCs carry 75% of all activation mass.
- So `active` and random lesions are not equal in effective dose. "Matched size" means matched KC count, not matched code coverage or trained-synapse coverage.
- PREREG admits the frequency confound, but the registered interpretation rule still says 1, 2, 6 and 7 "meaningful" means a bottleneck. That rule cannot be falsified by the design.
- The same artefact shows up with wiring that has nothing to do with the teacher. shuffled/post/active 818 = +0.098 (door_teacher_real), random wiring +0.039, and door_class real +0.043.
- `hub` 818 also removes more code slots than random (57% vs 40% in the same world). Its overlap with `active` 818 is 399, against about 327 expected by chance. Its excess is therefore not clean either.
- NOTES give a mechanism ("synapses updated more"). The measured coverage numbers say that mechanism is not the first-order explanation, and it was never tested.
- Fix: control with random KC sets matched on code-slot coverage (or on frequency).

### 2. [CONFIRMED, high] 5b `hub` effect on the clean task is explained by odour-channel activity, not by fan-out or topology
- Hub channels are more active in the odours: present in 47% of odours (all channels: 28%), mean response 0.077 vs 0.041. The correlation between fan-out and mean odour activity is 0.53.
- I ran door_class, real wiring, post lesion, 13 channels, 60 worlds, with a wiring-independent control that silences the 13 most active odour channels on the training set (the `oact` ranking):

| Lesion | Mean loss | Excess vs random |
|---|---|---|
| hub | 0.036 | +0.020 |
| `oact` | 0.056 | +0.040 |
| random | 0.016 | |

  - hub − `oact` = −0.020, i.e. `oact` is larger.
- So the "small-real" hub effect (+0.019) is odour-signal removal. NOTES line "真实连线里有扇出集中的嗅小球,对这个任务有一点重要性" and "hub 有小而可测的作用" over-read it.
- Related: the registered primary tier for the pre-lesion version (family 3) is `equivalent` at 99.3% ([−0.001, +0.026]). Only the 95% descriptive intervals say "small-real".
- The PREREG's own rule says a structural claim needs the pre-lesion result to be meaningful. It is not, so "hub has a small effect" is stronger than the registration supports.

### 3. [CONFIRMED, high] The 5b "circular teacher" explanation is half right, and the real-vs-shuffled contrasts (family 6 and 7) are misleading
- Rankings are computed from the wiring in use. Shuffled and random wirings have nearly flat glomerulus fan-out (SD 12 vs 112 for real; range 144-202). Their `hub` channels are therefore essentially random.
- The shuffled `hub` set overlaps the real `hub` set by 1 of 13 (random wiring: 4 of 13).
- A zero excess for shuffled/random `hub` is thus almost guaranteed. "Real − shuffled" in family 6 (+0.059) compares different channel sets, not wirings.
- Direct test (door_teacher_real, pre-lesion, 13 channels, 50 worlds): silencing the real-P0 hub channels in the shuffled learner gives an excess of +0.057. The real learner gives +0.065, and the random-wiring learner +0.038.
- So the loss is label information that the P0 teacher puts on its own hub channels, not a property of the learner's wiring. NOTES wording ("教师依赖的通道") is directionally right. The registered family-6 contrast is still uninterpretable, and the cause is the ranking mismatch.
- Shuffling per KC column also destroys the fan-out heterogeneity that defines `hub`. A fan-out-preserving null is the fair control.

### 4. [CONFIRMED, medium-high] Stage 5 headline family is mostly on the circular task, and NOTES 5 does not say so
- Six of the eight registered contrasts (1-5 and 8) use door_teacher_real with a P0 teacher. Test labels come from the intact P0 code.
- A learner with real wiring, silenced at test, loses agreement with the labels partly because its code no longer matches the teacher's.
- Real vs shuffled and real vs random-wiring contrasts (4, 5) are therefore confounded by teacher-wiring identity. Real intact accuracy is 0.809 against 0.770 and 0.767.
- 5b flags this circularity and 5 does not. NOTES 5 should flag it too.
- On the clean task, `hub` has no effect at any dose (818: −0.007), so the "hub needs 40% to show an effect" sentence is circular-task only.

### 5. [CONFIRMED, medium] "Bridger" (participation coefficient) is barely a bridger
- Among eligible glomeruli (fan ≥ median = 164, 34 of 65), PC ranges only 0.50-0.65. The theoretical value for a population-proportional mix is 0.626 (group shares 0.37, 0.45, 0.17).
- The top-PC glomeruli are those whose KC lobe mix matches the population. That is a near-constant plus noise, not a cross-module connector.
- PC is weakly negatively related to fan-out (r = −0.17 among eligible).
- Low fan-out is handled by the median filter. Without it, fan 2 gives PC = 0 and fan 3 gives 0.44. This is not a bug, but the filter is what makes the ranking meaningful, and it was set after thinking about the ranking.
- Unlike the source project (non-hub with train_out ≥ 4), the 5b bridgers can be hubs. Overlap in 7 is 1.0 (real), and 5 of 13 in a seed-0 check.
- The group-assignment alignment (GRP vs P0 columns) is OK: both come from the same `mb_circuit.npz` (`kc_type` 2045 entries, same order as P columns). Lone KC types ("KC", KCg-s1..4) go to γ or α′β′ by the prefix rule. Harmless.
- NOTES "bridger 在所有设置里都没有效应(等价或略为负)" is slightly overstated. In door_teacher_real real wiring, bridger 3 gives +0.023 post and +0.022 pre, small-real with CIs excluding 0, and bridger 13 post gives −0.023. These are small and mixed in sign, but not all equivalent.

### 6. [CONFIRMED, medium] "No structural bottleneck" (stage 5) rests on weak evidence
- It is based on pre-lesion `active` 409 (a single registered contrast) plus descriptive pre rows. The pre rows are all small-real negative or equivalent.
- Pre-removal of the most frequent KCs just re-routes the code to the next-ranked KCs and retrains on them. That shows redundancy under retraining, not the absence of concentration.
- Power is limited by accuracy: door_class intact accuracy is 0.69, so the maximum possible loss is about 0.19. Two tasks, one learning rate, a fixed top-5% code, and dose ≤ 40%.
- The sentence "没有测出集中在少数 KC 的结构性鲁棒性瓶颈" (no structural robustness bottleneck concentrated in a few KCs was detected) is OK as worded. The bare phrase "no structural bottleneck" is not.

### 7. [PLAUSIBLE, low-medium] Other unsupported explanations
- "random sparse wiring has flatter frequencies" (stage 5): not tested.
- Real vs random-wiring +0.035 (family 5) is confounded by teacher circularity (finding 4).
- The 5b NOTES sentence "前 2% 用户占 32% 的事件" restates the other project's result wrongly. In the other project, −32.26% is the traffic drop after quarantining half of the top-2% hubs. It counts events where a hub is actor or target, and that does not mean "top 2% users account for 32% of events". The direction of the argument (the KC layer is less concentrated) holds.
- Verified correct: KC strength Gini 0.241 with top 2% = 4.0%; glomerulus fan-out Gini 0.379 with top 10% = 21.7%; KC glomerulus in-degree mean 5.28, SD 2.39.

## Checks that passed
- **Rankings.** `order()` uses wiring-dependent frequency from the training stream and ties by stable index. Hub ranking by N row-sum is wiring-independent, as stated.
- **Lesion masking.** `codes_masked` sets psi to −inf before top-k, so the code is the top 5% of the remaining KCs. b0/sc are recomputed from the masked codes. In the pre variant, training and test both use masked codes. All of this is correct.
- **Channel silencing (5b).** Multiplying `U` by the mask silences the odour columns correctly. Training uses `trU*mask`, test uses `teU*mask`, and the intact condition uses neither.
- **Pre/post bookkeeping.** Loss = intact − lesioned, excess = ranked − random, and the random set `perm` is shared across doses (nested, from the full set). Random sets are drawn from all KCs or channels, including those that overlap hub/active by chance. The size match is fair in count (not in effect: findings 1-2).
- **CI and tiers.** Family sizes are 8 (99.4%) and 7 (99.3%), consistent with 1 − 0.05/k. The tier function matches the declared rule, s = 0.03. Equivalence by CI containment is stricter than TOST and fine. NOTES tables match RESULTS, including the "边缘" labels and #8 [−0.020, −0.000].
- **Deviations from PREREG.** Doses, tasks, seeds 5000-5099 and learning rate 0.05 match the registration. The pilot seeds used for the predictions (1000-1007 and 1000-1005) are disclosed, with the pilot outcome stated. No unregistered analysis in the families.

## Claim about the other project (WorldSimulationLab)
- CONFIRMED correct in substance. `cascade_amplification_multiplier` = (direct + indirect removed) / direct, in `research-core/counterfactual_engine.py` lines ~169-183. The values are 1.023 = (19236+441)/19236 and 1.343 = (1870+641)/1870.
  - "Indirect" removals come from a hand-written rule on timestamped retweets: an event is removed if the actor was suppressed in the last 6 hours and the event is an RT. The data are not re-simulated, so it is an accounting heuristic, not a dynamic cascade.
- The hub is the top 2% by training in-degree. The bridger is a non-hub with `train_out ≥ 4`. The 50% subset is by alternating rank.
- There is no matched random control and no interval in that code. The analogue-free statement for a static feed-forward graph is right. PREREG's phrase "出现次数 ≥ 4" is loose (it is out-count as actor).
- A stronger and fair point that NOTES could make: the multiplier is not a robust effect even in the source project.

## Suggested NOTES edits
- Stage 5: state that `active` removes 93% vs 40% of code slots; that six of eight registered contrasts are on the circular task; and that the "更新得更多" mechanism is untested.
- 5b: replace "hub 有小而可测的作用" by "hub effect on door_class is small and is reproduced by an odour-activity ranking; the pre-lesion primary contrast is equivalent". Add that family 6 and 7 compare different channel sets (shuffled fan-out is flat).
- Soften "bridger 在所有设置里都没有效应".

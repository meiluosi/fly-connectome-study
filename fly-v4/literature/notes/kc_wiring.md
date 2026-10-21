# PN->KC wiring in the Drosophila mushroom body: randomness, structure, and individual variability

Read-status key: FULL = full text fetched (WebFetch summaries of the page, so numbers are as reported by the fetch tool, possibly partial for very long pages); PARTIAL = only part of the full text was retrievable; ABSTRACT = abstract/metadata/search snippets only; NOT READ = nothing retrieved. Numbers below are from the fetched text unless marked "UNVERIFIED (background knowledge)".

## Is PN->KC wiring random or structured? (Caron 2013, Eichler 2017, Li 2020, Zheng 2018/2022)

### Takeaway
Caron 2013 found no detectable structure beyond a non-uniform glomerular input distribution (n=200 KCs, one per fly). Later dense EM data (FAFB: Zheng 2018/2022; hemibrain: Li 2020) found modest but statistically significant deviations from the matched random null. These are concentrated in alpha/beta and alpha'/beta' KCs and involve a food-responsive "core community" of PNs. The accurate summary is "approximately random, with small, class-specific, non-uniform structure", not "exactly random".

### Cited Findings
- **Caron, Ruta, Abbott, Axel (2013), "Random convergence of olfactory inputs in the Drosophila mushroom body", Nature 497:113-117, doi:10.1038/nature12063. Read: FULL (PMC author manuscript).** [PMC4148081](https://pmc.ncbi.nlm.nih.gov/articles/PMC4148081)
  - 200 KCs traced, one per fly. 100 random KCs gave 84 alpha/beta, 14 alpha'/beta', 2 gamma. A further 100 gamma KCs were targeted via a Fruitless driver.
  - Each KC had 2-11 claws, mean 7. On average about 3 glomerular inputs were identified per KC (claws were filled sequentially). Text reports 683 inputs (654 from AL glomeruli); analyses use 665 connections. Totals are not fully reconciled.
  - 49 of 51 glomeruli were sampled (DA3 and VL1 absent). Input was non-uniform: DA1 and DC3 were most frequent at 5.1% each. The authors attribute this to bouton number/size differences.
  - Tests used 1,000 shuffled datasets that preserve the non-uniform glomerular distribution (so the null is not uniform-random). Only 11/200 KCs got two inputs from the same glomerulus and none got three. This did not differ significantly from shuffles. Of 1,378 possible glomerular pairs, 508 occurred and 310 of these occurred in only one KC. DA1-DC3 co-occurred in 9 KCs. Pair/trio/quartet co-occurrence was "consistent with shuffled data", but the fetched text says data "not shown".
  - No preferential patterns by sensillar type, odour tuning, calyx/LH overlap, zonal organization, PN lineage or Fruitless expression. SVD found no structure beyond the non-uniform distribution. Most comparisons are qualitative ("no significant difference") without explicit p-values. The only reported p-value is alpha/beta vs gamma, p<0.001. Analyses were then run per class with no difference found, and the data were pooled.
  - Caveats stated by the authors: one KC per fly, so they cannot exclude determined inputs for some KC subsets. Glomerular identification was by a single observer. Power to detect small structure is limited.
- **Eichler et al. (2017), "The complete connectome of a learning and memory centre in an insect brain", Nature 548:175-182, doi:10.1038/nature23455. Read: ABSTRACT/secondary only** (Nature page redirected to login, bioRxiv PDF returned 403, no PMC copy found). Via [IDEAS/RePEc record](https://ideas.repec.org/a/nat/nature/v548y2017i7666d10.1038_nature23455.html) and search snippets: most larval KCs receive random combinations of inputs, while a subset receives stereotyped input from single PNs; a model shows this improves a stimulus-discrimination task for an output neuron. A later paper reports L1 larva has about 100 KCs, each receiving 1-6 uPN inputs ([PMC13537232](https://pmc.ncbi.nlm.nih.gov/articles/PMC13537232/), snippet only). A preprint snippet says single-claw KCs occurred more often than a Gaussian would predict ([Zheng 2020 bioRxiv](https://www.biorxiv.org/content/10.1101/2020.04.17.047167v1.full), snippet only; its full text returned 403). Quantitative details not verified.
- **Zheng, Li, et al. (2018), "A complete electron microscopy volume of the brain of adult Drosophila melanogaster" (FAFB), Cell 174:730-743, doi:10.1016/j.cell.2018.06.019. Read: ABSTRACT only** (PMC returned a reCAPTCHA page). Abstract-level claims: all KC inputs mapped, a new cell type (MB-CP2), postsynaptic partners of KC dendrites, and "unexpected clustering of olfactory projection neurons". [PMC6063995](https://pmc.ncbi.nlm.nih.gov/articles/PMC6063995) via [Janelia news](https://www.janelia.org/news/complete-fly-brain-imaged-at-nanoscale-resolution) snippet. No quantitative detail verified.
- **Zheng, Li, Lauritzen, Bock, et al. (2022), "Structured sampling of olfactory input by the fly mushroom body", Current Biology (NOT eLife; the user's "eLife/Cell" attribution is wrong for the 2022 paper), PMC9413950. Read: FULL, first ~100k of 180k characters.** DOI not captured in the fetch; verify before citing. [PMC9413950](https://pmc.ncbi.nlm.nih.gov/articles/PMC9413950)
  - Reconstructed PN inputs to 7,102 claws of 1,356 randomly sampled KCs (about 62% of right calyx claws). Mean 5.2 claws per KC (SD 1.6). About 2,200 KCs per hemisphere, about 150 PNs from 51 glomeruli. About 91% of claws were from uniglomerular olfactory PNs.
  - Core community of PNs made 1,916 claws against a random-bouton null mean of 1,421.7 (SD 35.7), z=13.8. Core types nearly all respond to food-related odorants. Core boutons had 17.4+/-9.3 claws per bouton vs 11.5+/-7.4 for others. Food-responsive PNs averaged 15.66 vs 10.53 claws per bouton and 162.95 vs 100.06 claws per glomerulus (p<2.5e-5).
  - Structure is concentrated in alpha/beta and alpha'/beta' KCs, with little in gamma KCs.
  - **Important qualifier:** a "local random" null (random within a radius, preserving bouton spatial position) gave 1,890.6+/-22.5 claws to core boutons vs 1,916 observed, and the over-convergence essentially disappeared. Core boutons are spatially closer together (10.9+/-6.8 vs 18.6+/-7.4 um). So much of the structure is explainable by spatial proximity of boutons plus local random sampling.
  - Hemibrain re-analysis showed a similar core community. PN-type output fractions correlate with FAFB, r^2=0.83. Subsampling FAFB to Caron-sized data (about half of claws in 200 KCs) made the core community undetectable. This is a power explanation for why Caron saw no structure.
  - Larvae: no over-convergence, and larvae have only the gamma-type class.
  - The authors state the extent of over-convergence and the exact core membership likely vary between individuals. No quantitative variability data are given.
- **Li, Lindsey, Marin, Otto, Dreher, Dempsey, Stark, Bates, Pleijzier, ... Rubin, Waddell, Litwin-Kumar, et al. (2020), "The connectome of the adult Drosophila mushroom body provides insights into function", eLife 9:e62576, doi:10.7554/eLife.62576. Read: PARTIAL** (about chars 100k-200k of the eLife page plus the first 100k of PMC; section "Randomness and structure in sensory inputs to KCs" captured, Results text before and after not seen). [eLife](https://elifesciences.org/articles/62576), [PMC7909955](https://pmc.ncbi.nlm.nih.gov/articles/PMC7909955). Note the user listed Li 2020 as eLife 57443, which was a wrong guess on my side; 62576 is correct.
  - About 2,000 KCs per hemisphere. KCs get input from "an average of six PNs" (intro) and an average 5.6 claws in the CA (results section). Each claw is innervated by a single PN. About 150 PNs, 51 glomeruli, generally 3-4 PNs per glomerulus innervating the MB. 126 PNs at a 25-synapse threshold innervate the CA. Over 90% of main-calyx sensory input is olfactory. About 8% of KCs get predominantly visual input. 14 KC types (10 main plus four gamma-s types); e.g. 590 KCg-m, 99 KCg-d.
  - Null model: shuffle each KC's connections so that KCs sample uPNs in proportion to each uPN's total connections, keeping per-KC claw count. Connectivity binarized at 5 synapses before PCA. Three PCs clearly exceeded the random model. Alpha'/beta' and alpha/beta KCs are skewed to highly represented glomeruli, especially DP1m and DM1. Gamma KC input is more uniform. Authors say the null should allow uPN probabilities to depend on KC type.
  - Spatial shuffling: same-glomerulus boutons are closer than different-glomerulus boutons. Participation ratio / dimension is lower in real data than in shuffled models, but the effect is "modest", appears above about 10 um, is strongest for alpha/beta and alpha'/beta', minimal for gamma, and does not noticeably persist at the level of KC outputs to MBONs.
  - The paper frames Caron 2013 and Eichler 2017 as suggesting no apparent structure and Zheng 2020 as finding PN convergence inconsistent with random sampling. Synapses per claw, food-odour analysis, and per-KC-type PN fractions were not in the captured text.
- **Takemura et al. (2017), "A connectome of a learning and memory center in the adult Drosophila brain", eLife 6:e26975, doi:10.7554/eLife.26975. Read: PARTIAL (first 100k of 336k chars).** [eLife](https://elifesciences.org/articles/26975). This is the alpha-lobe FIB-SEM reconstruction, not the hemibrain, and contains no PN->KC connectivity (PNs not in the reconstructed set). Of note for downstream: 949 alpha/beta KCs, about 89,000 presynaptic sites; KC->MBON synapses 80-93% in convergent groupings.
- **Scheffer et al. (2020), "A connectome and analysis of the adult Drosophila central brain", eLife 9:e57443, doi:10.7554/eLife.57443. Read: PARTIAL (first 100k of 474k chars).** (The URL I first tried, 57443, is this paper, not Li 2020.) [eLife](https://elifesciences.org/articles/57443). MB neuropil: 2,315 neurons (2,003 excluding DANs). About 9.5 million T-bars and 64 million PSDs overall. Only one bit of this was relevant to PN->KC.

### Inferences
- The original "random" claim and the later "structured" claim are not strictly contradictory. Caron tested against a null that already included non-uniform glomerular frequency and had low power (about half the claws of 200 KCs, one per fly). Zheng 2022 shows the structure is undetectable at that sample size.
- Effect sizes are small: Li 2020 calls dimension reduction modest and absent downstream at MBON level. Zheng's local random null explains the over-convergence. So "close to random" is defensible for a computational model if clarified as "random with non-uniform glomerular probabilities, KC-type-specific biases and a spatial/food-PN bias".
- Reported structure sits in alpha/beta and alpha'/beta' KCs, so whole-population models that pool KC types can miss it.

### Gaps
- Eichler 2017 and Zheng 2018 full text: not retrievable (paywall/captcha). Quantitative claims for these are unverified.
- Li 2020 results text on claws per KC type, synapses per claw and food-odour findings not seen.
- Caron "not shown" pair/trio data: no explicit statistics available.

## Individual and dataset variability (FlyWire vs hemibrain; Schlegel 2024; Dorkenwald 2024; male CNS)

### Takeaway
Cell-type counts and strong connections are broadly consistent between FlyWire (female, TEM) and hemibrain (female, FIB-SEM), but weights vary within and across animals, and the MB principal neurons (KCs) were singled out as highly variable. I found no verified source that reports glomerulus-level PN->KC input totals as conserved across individuals. I also did not retrieve the data to quantify PN->KC variability directly.

### Cited Findings
- **Dorkenwald et al. (2024), "Neuronal wiring diagram of an adult brain", Nature 634:124-138, doi:10.1038/s41586-024-07558-y. Read: PARTIAL, via the bioRxiv v2 PMC copy (PMC10327113, chars 0-200k of 236k); the Nature page was blocked.** [PMC10327113](https://pmc.ncbi.nlm.nih.gov/articles/PMC10327113)
  - Companion paper reports "high variability for principal neurons of the mushroom body". Earlier work found some MB connectivity close to random and later work deviations from randomness.
  - FlyWire: 127,978 neurons, 53 million synapses (the preprint's counts; the final Nature paper differs). Hemibrain: about 20,000 uncropped neurons, 14 million synapses. Cell-type counts and strong connections "largely in agreement" (Schlegel matching). Presynapse attachment 92.3%, postsynapse attachment 43.9%. False negatives dominate; threshold >4 synapses. Synapses were automatically predicted, not manually proofread. Natural variability plus reconstruction noise "tend to be modest", and strong connections are expected to be more reproducible. No numbers on KC counts or left/right reproducibility were given in the captured text.
- **Schlegel et al. (2024), "Whole-brain annotation and multi-connectome cell typing of Drosophila", Nature 634:139-152, doi:10.1038/s41586-024-07686-5. Read: ABSTRACT only** (Nature page redirected). [carta.anthropogeny.org record](https://carta.anthropogeny.org/node/330521), [IDEAS](https://ideas.repec.org/a/nat/nature/v634y2024i8032d10.1038_s41586-024-07686-5.html). 8,453 cell types (3,643 from hemibrain, 4,581 new). About one-third of hemibrain-proposed types could not be reliably re-identified in FlyWire. Abstract claims "functional homeostasis in the mushroom body", where absolute excitatory input changes while E/I balance is maintained. A secondary snippet says the most common MB cell type is almost twice as numerous in FlyWire as in hemibrain (I did not verify this against the paper; it is probably the KC population but could be a different count basis).
- **Male CNS connectome (Janelia; bioRxiv 2025).** Read: Janelia project page snippet only ([janelia.org](https://www.janelia.org/node/70079)). Reports 262 sex-specific and 114 sexually dimorphic cell types (4.8% of central brain). No MB / KC / PN->KC data retrieved. I could not find the bioRxiv full text, so full citation not verified.

### Inferences
- If KC counts per hemisphere differ by up to about 2x across connectomes (unverified), then KC in-degree and glomerulus-level input totals cannot be assumed constant. This conflicts with the project statement that glomerulus input totals are conserved. At minimum the claim is unsupported.

### Gaps
- No verified quantitative PN->KC per-glomerulus comparison between FlyWire, hemibrain, and male CNS. This needs the Schlegel/Dorkenwald full text or neuPrint/FlyWire data.
- Left vs right hemisphere reproducibility numbers for the MB: not found.
- Synapse-detection differences specific to PN->KC (as opposed to whole-brain rates above): not found.

## Does structured wiring help computation? (Zheng 2022, Eichler 2017, Litwin-Kumar 2017, Gruntman & Turner 2013)

### Takeaway
Theory and the Zheng 2022 model say random mixing is near-optimal for discrimination. Structure helps only when signals are routed through the over-represented community. This supports a project finding of no advantage for real vs shuffled wiring in generic learning tasks.

### Cited Findings
- **Zheng 2022 (above)**: discrimination model with 2,200 KCs, 10 stimulus odours, 10,000 trials per network, 100 network instantiations. Random-glomerulus networks performed best. Non-random networks performed worse, but recovered when signal was channeled through community PNs. Zheng 2022 reports no dimensionality measurement of its own in the captured text. [PMC9413950](https://pmc.ncbi.nlm.nih.gov/articles/PMC9413950)
- **Li 2020**: real data have modestly lower dimension than spatially shuffled models, with no persistent effect at KC->MBON level (above). [PMC7909955](https://pmc.ncbi.nlm.nih.gov/articles/PMC7909955) Together this means real structure slightly reduces rather than increases dimension in that analysis.
- **Eichler 2017**: model claims single-PN-input KCs improve discrimination (abstract-level only, ABSTRACT).
- **Litwin-Kumar, Harris, Axel, Sompolinsky, Abbott (2017), "Optimal degrees of synaptic connectivity", Neuron 93:1153-1164, doi:10.1016/j.neuron.2017.01.030. Read: ABSTRACT only** (PDF text was unreadable). [HUJI record](https://cris.huji.ac.il/en/publications/optimal-degrees-of-synaptic-connectivity/). Representation dimension peaks at in-degrees matching anatomy for cerebellar granule cells and Drosophila KCs; sparse wiring beats dense; dense wiring becomes advantageous when input synapses undergo supervised plasticity. A talk abstract says they checked against larval MB EM. I could not verify the numerical optimum (UNVERIFIED background: roughly 4-7 claws).
- **Gruntman & Turner (2013), "Integration of the olfactory code across dendritic claws of single mushroom body neurons", Nat Neurosci 16:1821-1829, doi:10.1038/nn.3547. Read: ABSTRACT + author manuscript opening only.** [PMC3908930](https://pmc.ncbi.nlm.nih.gov/articles/PMC3908930). Claws of one KC respond to different odours; a single KC fires only when several claws are stimulated simultaneously. This supports the coincidence-detection / thresholded readout rationale. It is not a test of random vs structured wiring.

### Inferences
- The hypothesis "real wiring offers no advantage over shuffled wiring" is consistent with Zheng 2022 (random networks best) and Li 2020 (real structure slightly reduces dimension).
- A plausible way for real structure to matter is task-specific routing through the food-related core PNs, a task-relevance effect rather than a dimension effect.

### Gaps
- Endo or other 2023-2025 modelling papers on real vs shuffled MB wiring were not searched or found.
- Litwin-Kumar numbers and Eichler model numbers unverified.

## Justification of ~2000 KCs, ~5-7 inputs per KC, and the top-k nonlinearity

### Takeaway
KC count (about 2,000-2,200), claws per KC (5.2 to 7 depending on dataset and method), and thresholded coincidence detection are supported by the sources. The "top-k" is a model abstraction of APL-mediated global inhibition, and I did not find a source that directly justifies a hard top-k.

### Cited Findings
- KC count: about 2,000 per hemisphere (Li 2020, PMC7909955); about 2,200 per hemisphere (Zheng 2022).
- Claws per KC: 5.2 +/- 1.6 (FAFB, Zheng 2022, n=1,356 KCs), 5.6 (hemibrain, Li 2020 results text), "an average of six PNs" (Li 2020 intro), 7 (mean of 2-11, Caron 2013, using a different counting method with sequential filling). The three datasets differ by about 35% on this number, which counters the claim of tight conservation.
- Thresholded coincidence: a single KC fires only when several claws are simultaneously stimulated (Gruntman & Turner 2013, abstract); Li 2020 ties this to global feedback inhibition and sparse odour representations.
- Optimality of in-degree: Litwin-Kumar 2017 (abstract-level; see above).

### Inferences
- Because the three datasets give 5.2-7 mean claws per KC, claim ranges of "~5-7" are appropriate, but do not treat the exact value as fixed.

### Gaps
- Direct source for top-k (APL inhibition giving fixed fraction of about 5-10% active KCs): not retrieved in this session. UNVERIFIED background: Honegger 2011, Lin 2014.

## Project claim audit

- **"KC wiring is close to random"**: partially supported but qualified. Supported by Caron 2013, Eichler 2017 (abstract), and the modest effect sizes in Li 2020 (small dimension difference, no effect downstream). Contradicted in the strict sense by Zheng 2022 (z=13.8 core-community over-convergence, KC-type-dependent bias) and Li 2020 (3 PCs exceeding the null; alpha/beta and alpha'/beta' skewed to DP1m, DM1). Suggested wording: "approximately random given non-uniform glomerular and KC-type-dependent probabilities, with small structured deviations, mostly in alpha/beta and alpha'/beta' KCs."
- **"Real wiring has heterogeneous in-degree and synapse counts"**: in-degree heterogeneity is supported (2-11 claws in Caron 2013; SD 1.6 around mean 5.2 in Zheng 2022; 1-6 in larvae). Synapse-count heterogeneity per claw was NOT found in any fetched text. Treat as unsupported by my reading, not contradicted. Also note thresholds (5 synapses in Li 2020, >4 in FlyWire) shape what is counted as an edge.
- **"Glomerulus-level input totals are conserved across individuals"**: not supported by any source I read. Dorkenwald says MB principal neurons are highly variable (via the companion paper, not read directly). Zheng 2022 says core-community extent and membership likely vary across individuals. Caron's own conclusion is that the same odour activates the same KC ensemble within a fly but different ensembles across flies. Schlegel's abstract suggests the absolute amount of excitatory MB input varies across brains while E/I balance is maintained. FAFB vs hemibrain PN-type output fractions correlate with r^2=0.83 (Zheng 2022), which means substantial but incomplete agreement, not conservation.

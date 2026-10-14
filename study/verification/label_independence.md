# Label independence check: MBON/DAN compartment labels

## Verdict
(a) DAN->MBON: PARTIALLY CIRCULAR (mostly independent at origin, not fully). Confidence: moderate (~65%).
(b) KC->MBON: INDEPENDENT at origin, weakly confirmatory only. Confidence: moderate (~65%).

## Evidence
1. Origin (light microscopy). Aso et al. 2014 defined MBON/DAN types and compartments from split-GAL4 anatomy, not synapses. The paper defines a type as neurons "indistinguishable morphology" across ~7000 lines; dendrites of MBON types tile "spatially stereotyped compartments"; DAN axons were assigned to compartments by arbor location. Synaptic connectivity was not the primary criterion. https://pmc.ncbi.nlm.nih.gov/articles/PMC4273437/ (read via fetch summary).
2. EM transfer. Takemura 2017 identified MBONs/DANs by comparing "morphologies to existing images" from light microscopy; connectivity gave "further confirmation", and neurite entry points were also used. https://pmc.ncbi.nlm.nih.gov/articles/PMC5550281/. Connectivity was therefore a secondary check (e.g. MBONs lack presynapses, APL presents to KCs). A DAN->MBON same-compartment check could have been part of that confirmation. This is the main circularity route.
3. Li et al. 2020 (hemibrain): typical MBONs were confirmed by comparing LM images with hemibrain skeletons; 14 additional "atypical" MBON types were found in EM. Atypical types (and possibly new PAM/PPL1 splits) were plausibly defined using EM morphology plus connectivity. I could NOT fetch the Methods (eLife and bioRxiv blocked), so how atypical/new types were clustered is unverified. https://elifesciences.org/articles/62576 (only search-snippet content).
4. Schlegel 2024 (FlyWire): hemibrain labels were transferred by matching, not re-derived. https://www.nature.com/articles/s41586-024-07686-5. Matching used NBLAST morphology plus connectivity-based cross-checks (the latter not verified by me).
5. MaleCNS (Berg et al. 2026, Cell). The download page and search snippets gave no typing methods ("See manuscript methods"). I could not retrieve the paper's text. https://male-cns.janelia.org/download/. Presumably the MB types were carried over from hemibrain by morphology and connectivity matching; unverified.
6. Local files (read-only). hemibrain_meta.csv has no notes column covering MB typing (notes hold only hemilineage/paper tags). mb_annotations_malecns.csv has columns bodyId, role, type, instance, compartment, side; the compartment is parsed from the instance string, e.g. MBON14(a3)_R. There is no provenance field saying how the label was assigned. Some DANs (PPL201, PPL202, PPL108, many PAM) carry no compartment label.

## Reasoning
- The compartment term in the name is anatomical by definition: where the MBON dendrite or DAN axon sits along the KC lobes. Those positions are in turn defined by KC axon segments, so the name embeds KC-lobe geometry.
- DAN->MBON: a DAN and an MBON share a compartment because both arbors lie in the same lobe zone. That is a real anatomical fact and the labels were set by LM, so most of the 91% is a genuine finding. Residual circularity: EM identification used synaptic confirmation, and ambiguous cells in EM (atypical MBONs, multi-compartment DANs such as "y1pedc", "B1>a") could have been placed using their DAN or KC contacts. Part of the 91% vs ~11% gap may also be a shared-geometry effect (both are anatomical co-location), not independent evidence of a functional rule.
- KC->MBON: KC input to an MBON is the same anatomical co-location (MBON dendrite along KC axons). The labels were not derived from KC synapse counts, so the KC-overlap analysis is not circular by construction. It can still be confirmatory for the same geometry reason, and EM confirmation may have used KC contacts for ambiguous MBONs.

## Suggested limitations wording
"Compartment labels come from light-microscopy anatomy (Aso et al. 2014) and were carried to EM by morphological matching, with synaptic connectivity used as a secondary check. DAN->MBON same-compartment enrichment therefore partly reflects shared anatomy, and some EM-based identity confirmation may have used these connections, so the 91% should be read as a consistency check, not a fully independent test. KC->MBON overlap measures are likewise anchored to the same compartment geometry. FlyWire labels are transferred from the hemibrain, and MaleCNS typing methods could not be verified here."

## Suggested robustness check
Restrict to the 21 typical MBONs and the 20 classic DAN types (LM-defined) and recompute 91% vs shuffle; if it holds, the circularity concern is small.

Unverified: Li 2020 Methods, Berg 2026 methods, Schlegel connectivity-matching detail.

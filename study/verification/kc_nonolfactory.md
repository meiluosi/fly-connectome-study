# Verification: KCg-d and KCab-p are mainly non-olfactory (visual) KCs

Verdict: SUPPORTED for the visual-input claim, with nuance on the exact inputs and on "zero". Confidence: high for the main claim, moderate for fine detail. Web fetches returned summaries, not full text, so quotes are as returned and should be spot-checked.

## Sources
1. Li et al. 2020 eLife, hemibrain MB connectome. https://elifesciences.org/articles/62576 (read via https://pmc.ncbi.nlm.nih.gov/articles/PMC7909955/)
   - "The dendrites of γd KCs form the ventral accessory calyx" (vACA). About 99 KCg-d.
   - "The dendrites of α/βp KCs form the dorsal accessory calyx" (dACA).
   - "These accessory calyces receive non-olfactory input."
   - "About 8% of KCs" get predominantly visual input; these are the two classes (KCg-d and KCab-p).
   - Thermo/hygrosensory PN input is a different group: KCg-t (about 8 cells) in the anterior main calyx. It is not KCab-p or KCg-d.
2. Vogt et al. 2016 eLife. https://elifesciences.org/articles/14009
   - Two visual projection neuron (VPN) types connect the optic lobes to the vAC (the ventral accessory calyx, which is KCg-d's dendritic field).
   - It is a light-microscopy/behaviour study and does not give a connectome-level breakdown.
3. Ganguly et al. 2024 Nat Commun, FlyWire/hemibrain visual inputs to KCs. https://www.nature.com/articles/s41467-024-49616-z (read via https://pmc.ncbi.nlm.nih.gov/articles/PMC11228034/)
   - 8% of KCs receive predominantly visual input.
   - Direct VPNs dominate input to KCg-d. Indirect visual input via local visual interneurons (LVINs) dominates KCab-p.
   - Key caveat: "Five identified KCγ-d's did not receive any inputs from VPNs or LVINs." They received olfactory PN input instead.
   - Visual KCg-d get 1-7 inputs (median 3) versus 5-6 for olfactory KCs.
4. Schlegel et al. 2024 (FlyWire). I did not read it. FlyWire follows hemibrain type names, so KCg-d and KCab-p (KCapbp) are expected to match. Unverified.
5. Berg et al. 2026 MaleCNS (Cell). https://www.cell.com/cell/fulltext/S0092-8674(26)00942-6, bioRxiv https://www.biorxiv.org/content/10.1101/2025.10.09.680999v1. I found no KC-specific statements and did not read the full text.

## Nuance
- KCg-d: mainly visual, via direct VPNs, in the vACA.
- KCab-p: mainly visual, but indirect, via LVINs, in the dACA. The same two papers support it as non-olfactory and visual. I found no source calling KCab-p thermo/hygrosensory.
- "Non-olfactory" is the right word for the calyces. It is not safe to say "no olfactory input ever": a few KCg-d (5 in FlyWire) take olfactory PN input, and some KCs have mixed inputs.
- Naming: KCg-d = gamma-dorsal; KCab-p = KCapbp = alpha/beta-posterior. Hemibrain/FlyWire also use KCg-m, KCg-s, KCab-c, KCab-s, KCa'b'.

## Your numbers
- Zero-ALPN KCs in 82% of KCg-d and 60% of KCab-p fit the biology. These types are about 8% of KCs; 99 KCg-d is roughly the expected count.
- The 18% of KCg-d and 40% of KCab-p that do have ALPN input are plausibly the small olfactory or mixed minority. The 5 olfactory KCg-d in FlyWire fit the KCg-d side.
- Your 128 zero-ALPN KCs (88 + 39 + 1) are about 6% of 2045, close to the expected visual share.
- Zero ALPN input is a necessary but not sufficient marker of the visual types. The one KCa'b' with zero ALPN input is an exception worth checking. Check its inputs for VPN, LVIN, or a missing or low synapse count.
- To confirm, verify in MaleCNS that the zero-ALPN KCs' upstream partners are VPNs/LVINs, using the accessory-calyx ROIs.

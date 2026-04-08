---
title: "Introduction"
teaching: 15
exercises: 0
questions:
- "What is the physics motivation for measuring B<sup>0</sup><sub>s</sub>→μ<sup>+</sup>μ<sup>−</sup>?"
- "What is the overall analysis strategy?"
objectives:
- "Understand why B<sup>0</sup><sub>s</sub>→μ<sup>+</sup>μ<sup>−</sup> is a sensitive probe of new physics."
- "Know the key ingredients of the branching fraction measurement."
- "Understand the role of the normalization channel."
keypoints:
- "B<sup>0</sup><sub>s</sub>→μ<sup>+</sup>μ<sup>−</sup> is a FCNC decay heavily suppressed in the SM — new physics can enhance it."
- "The branching fraction is extracted from a simultaneous fit across BDT categories."
- "B<sup>+</sup>→J/ψK<sup>+</sup> serves as the normalization channel to cancel many systematic uncertainties."
---

## Physics motivation

<!-- TODO: paste/expand from TWiki introduction section -->

The decay B<sup>0</sup><sub>s</sub>→μ<sup>+</sup>μ<sup>−</sup> is a Flavour-Changing Neutral
Current (FCNC) process. In the Standard Model it is loop- and helicity-suppressed, giving a
branching fraction of:

**BF(B<sup>0</sup><sub>s</sub>→μ<sup>+</sup>μ<sup>−</sup>) ≈ 3.66 × 10<sup>−9</sup>**

Many beyond-SM scenarios (SUSY, leptoquarks, extra dimensions) predict significant deviations
from this value, making it one of the most sensitive indirect probes of new physics at the LHC.

## Analysis strategy

<!-- TODO: paste from TWiki -->

The measurement follows the strategy of the CMS Run-2 paper [BPH-21-006](https://cms-results.web.cern.ch/cms-results/public-results/publications/BPH-21-006/index.html):

1. Select B<sub>s</sub>→μμ candidates and classify them into **8 BDT categories** based on signal/background discrimination.
2. Model the **signal PDF** using a double Gaussian + Crystal Ball shape fitted to MC.
3. Model **background PDFs**: combinatorial (Bernstein), peaking (KDE from MC), semileptonic (KDE from MC).
4. Fit the **normalization channel** B<sup>+</sup>→J/ψK<sup>+</sup> in data to extract the observed yield and efficiency.
5. Perform a **simultaneous unbinned maximum likelihood fit** across all 8 categories to extract BF(B<sub>s</sub>→μμ).

## Branching fraction formula

The branching fraction is extracted via:

$$
\text{BF}(B_s \to \mu\mu) = \frac{N_{B_s}}{N_{B^+}} \cdot \frac{\varepsilon_{B^+}}{\varepsilon_{B_s}} \cdot \frac{f_u}{f_s} \cdot \text{BF}(B^+ \to J/\psi K^+)
$$

where f<sub>u</sub>/f<sub>s</sub> is the ratio of B<sup>+</sup> to B<sup>0</sup><sub>s</sub> production fractions.

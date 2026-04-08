---
layout: lesson
root: .
permalink: index.html
---

This exercise is based on the CMS measurement of the B<sup>0</sup><sub>s</sub>→μ<sup>+</sup>μ<sup>−</sup>
decay branching fraction and effective lifetime using the Run-2 dataset
([BPH-21-006](https://cms-results.web.cern.ch/cms-results/public-results/publications/BPH-21-006/index.html)).

We will build an unbinned maximum likelihood fitter using **RooFit** to extract decay branching
fractions — following the real analysis strategy from end to end.

> ## Important
>
> **Do NOT run these scripts on the LPC interactive nodes.**
> They use hard-coded EOS paths that will crash an interactive session.
> Use a condor job or a dedicated analysis node instead.
{: .callout}

> ## Prerequisites
>
> Basic familiarity with ROOT and Python (or C++) is assumed.
> You should have a valid CERN/LPC account and access to EOS.
{: .prereq}

---

### Schedule

| Episode | Topic |
|---------|-------|
| [Setup](setup.html) | Environment setup and data files |
| [1. Introduction]({{ page.root }}{% link _episodes/01-introduction.md %}) | Physics overview and analysis strategy |
| [2. Signal MC Fit]({{ page.root }}{% link _episodes/02-signal-mc-fit.md %}) | Fitting B<sup>+</sup>→J/ψK<sup>+</sup> MC with a double Gaussian |
| [3. Normalization Channel]({{ page.root }}{% link _episodes/03-normalization.md %}) | Fitting B<sup>+</sup>→J/ψK<sup>+</sup> and B<sub>s</sub>→J/ψφ data |
| [4. Background PDFs]({{ page.root }}{% link _episodes/04-backgrounds.md %}) | Building peaking, semileptonic, and combinatorial background models |
| [5. Final Fit]({{ page.root }}{% link _episodes/05-final-fit.md %}) | Simultaneous fit across categories and branching fraction extraction |

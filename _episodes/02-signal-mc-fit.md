---
title: "Signal MC Fit"
teaching: 10
exercises: 40
questions:
- "How do we model the B+→J/ψK+ signal peak?"
- "How do we apply MC-derived shape parameters to data?"
objectives:
- "Fit a double Gaussian model to B+→J/ψK+ MC."
- "Understand mean shift and resolution scale corrections."
- "Fit the full signal+background model to data."
keypoints:
- "The signal shape is fixed from MC, with a floating mean shift and resolution scale fitted in data."
- "The combinatorial background uses an exponential; the J/ψ+X tail uses an error function."
---

## Task 2.1 — Double Gaussian fit to MC (category 0)

Fit a double Gaussian model to the B<sup>+</sup>→J/ψK<sup>+</sup> MC in category 0.
The invariant mass range is 5.0–5.8 GeV.

<!-- TODO: add figure from task_2_1 output -->

> ## Task 2.1
>
> Open `task_2_1.py` (or `task_2_1.C`) and run the double Gaussian fit to MC.
> Record the fitted parameters — you will use them as starting values in later tasks.
>
> ```python
> python task_2_1.py
> ```
{: .challenge}

## Task 2.2 — Fit data with fixed signal shape

Use the MC-derived signal shape (fixed parameters) and fit the B<sup>+</sup>→J/ψK<sup>+</sup>
data with a signal + combinatorial + J/ψ+X background model.

<!-- TODO: add figure from task_2_2 output -->

> ## Task 2.2
>
> Run `task_2_2.py`. The signal PDF parameters are hard-coded from the Task 2.1 MC fit result.
> Observe the fit quality and check the yield.
{: .challenge}

## Task 2.3 — Fit data with mean shift and resolution scale corrections

Introduce two free parameters:
- `sig_shift`: a common mean shift applied to both Gaussians
- `sig_scale`: a common resolution scale factor applied to both sigmas

These correct for known data/MC differences.

<!-- TODO: add figure from task_2_3 output -->

> ## Task 2.3
>
> Run `task_2_3.py`. Compare the fitted `sig_shift` and `sig_scale` to unity/zero.
> Are the data/MC corrections significant?
{: .challenge}

## Task 2.4 — Repeat for category 1

Repeat Tasks 2.1–2.3 for BDT category 1: fit the MC first, then fit the data with corrections.

<!-- TODO: add figure from task_2_4 output -->

> ## Task 2.4
>
> Run `task_2_4.py`. Note that the MC parameters are different for category 1.
{: .challenge}

## Task 2.5 — Bs→J/ψφ signal fit

Repeat the MC+data fit for the B<sub>s</sub>→J/ψφ channel (mass peak near 5.37 GeV).

<!-- TODO: add figure from task_2_5 output -->

> ## Task 2.5
>
> Run `task_2_5.py`. Note the different mass peak position and the simpler background
> (no J/ψ+X tail needed for the B<sub>s</sub>→J/ψφ channel).
{: .challenge}
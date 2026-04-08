---
title: "Normalization Channel"
teaching: 10
exercises: 30
questions:
- 'How do we fit the normalization channel $B^+ \to J/\psi K^+$?'
- 'How do we extract the $B^+ \to J/\psi K^+$ yield and efficiency?'
- "How do we compute the fs/fu production fraction ratio?"
objectives:
- 'Fit the $B^+ \to J/\psi K^+$ data and MC to extract signal yield and shape parameters.'
- 'Fit the $B_s \to J/\psi\phi$ channel to extract the Bs yield.'
- "Compute fs/fu from the ratio of the two channel yields."
keypoints:
- 'The normalization channel $B^+ \to J/\psi K^+$ cancels many systematic uncertainties.'
- 'fs/fu is measured from data using $B_s \to J/\psi\phi$ and $B^+ \to J/\psi K^+$.'
---

## Task 3.1 — $B^+ \to J/\psi K^+$ normalization fit

<!-- TODO: describe the $B^+ \to J/\psi K^+$ fit in data across all BDT categories -->

> ## Task 3.1
>
> Run `task_3_1.py` to fit the $B^+ \to J/\psi K^+$ invariant mass distribution in data.
> Record the signal yield and efficiency for each category.
>
> ```python
> python task_3_1.py
> ```
{: .challenge}

## Task 3.2 — $B_s \to J/\psi\phi$ yield fit

<!-- TODO: describe the $B_s \to J/\psi\phi$ fit used to measure fs/fu -->

> ## Task 3.2
>
> Run `task_3_2.py` to fit the $B_s \to J/\psi\phi$ invariant mass distribution.
> This gives the Bs yield needed to compute the fs/fu ratio.
{: .challenge}

## Task 3.3 — Computing fs/fu

<!-- TODO: describe the arithmetic for fs/fu and its uncertainty -->

> ## Task 3.3
>
> Run `task_3_3.py`. This script does pure arithmetic — no ROOT needed.
> It uses the yields from Tasks 3.1 and 3.2 to compute fs/fu with propagated uncertainty.
{: .challenge}
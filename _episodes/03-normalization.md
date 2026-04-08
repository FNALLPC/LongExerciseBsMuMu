---
title: "Normalization Channel"
teaching: 10
exercises: 30
questions:
- "How do we fit the normalization channel B+→J/ψK+?"
- "How do we extract the B+→J/ψK+ yield and efficiency?"
- "How do we compute the fs/fu production fraction ratio?"
objectives:
- "Fit the B+→J/ψK+ data and MC to extract signal yield and shape parameters."
- "Fit the Bs→J/ψφ channel to extract the Bs yield."
- "Compute fs/fu from the ratio of the two channel yields."
keypoints:
- "The normalization channel B+→J/ψK+ cancels many systematic uncertainties."
- "fs/fu is measured from data using Bs→J/ψφ and B+→J/ψK+."
---

## Task 3.1 — B+→J/ψK+ normalization fit

<!-- TODO: describe the B+→J/ψK+ fit in data across all BDT categories -->

> ## Task 3.1
>
> Run `task_3_1.py` to fit the B+→J/ψK+ invariant mass distribution in data.
> Record the signal yield and efficiency for each category.
>
> ```python
> python task_3_1.py
> ```
{: .challenge}

## Task 3.2 — Bs→J/ψφ yield fit

<!-- TODO: describe the Bs→J/ψφ fit used to measure fs/fu -->

> ## Task 3.2
>
> Run `task_3_2.py` to fit the Bs→J/ψφ invariant mass distribution.
> This gives the Bs yield needed to compute the fs/fu ratio.
{: .challenge}

## Task 3.3 — Computing fs/fu

<!-- TODO: describe the arithmetic for fs/fu and its uncertainty -->

> ## Task 3.3
>
> Run `task_3_3.py`. This script does pure arithmetic — no ROOT needed.
> It uses the yields from Tasks 3.1 and 3.2 to compute fs/fu with propagated uncertainty.
{: .challenge}

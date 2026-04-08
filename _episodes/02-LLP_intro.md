---
title: "Long-lived Particles (LLPs)"
teaching: 10
exercises: 120
questions:
- "What is a long-lived particle?"
- "What is a particle proper decay lengths and lab frame decay lengths?"
- "How often does an LLP decay in the muon detectors?"
objectives:
- "Understand particle lifetime"
- "Reweight LLP lifetime given a signal sample with fixed LLP lifetime"
- "Calculate the geometric acceptance of the endcap muon detector for different LLP lifetimes"
keypoints:
- Particle proper decay lengths follow an exponential decay.
- Long-lived particles for LHC searches generally have mean proper decay lengths of ~mm to ~km scale that create displaced signatures in the sub-detectors
- LLP lifetime can be reweighted to avoid generating many signal samples with different LLP lifetimes
- The probability that an LLP decays in a sub-detector depends on the LLP mean proper decay lengths, so searches for LLPs with different sub-detectors (tracker, calorimeter, and muon detectors) provide complementary coverage to LLPs
---



> ## After following the instructions in the setup:
>
> ~~~
> cd <YOUR WORKING DIRECTORY>/CMSSW_14_1_0_pre4/src/MDS_CMSDAS/scripts
> source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh
> jupyter notebook --no-browser --port=8888 --ip 127.0.0.1
> ~~~
> {: .language-bash}
>
> This will open a jupyter notebook tree with various notebooks. 
{: .callout}

## Particle lifetime

Particle decay is a Poisson process, and so the probability that a particle survives for time t (in their own time frame) before decaying is given by an exponential distribution whose time constant depends on the particle's mean proper decay time($\tau$):

$N(t) = e^{-t/\tau}$


Long-lived particles in CMS are generally considered to have $c\tau$ of ~mm to ~km scale that have non-negligible propability to decay in subdetectors (trackers, calorimeters, and muon detectors), creating displaced signatures.

In this exercise, we will plot the particle proper decay length, from the generator-level LLP information (lab-frame decay vertex and velocity) to verify the exponential behavior.

> ## Open a notebook
>
> For this part, open the notebook called `LLP_lifetimes.ipynb` and run `Ex0` and `Ex1` to calculate and plot the LLP proper decay length and perform exponential fit.
{: .checklist}


> ## Discussion 2.1
>
> Are you able to extract the LLP proper decay length from the exponential fit? 
> Does it agree with the expectation?
{: .discussion}

## Particle lifetime reweighting
Since the particle lifetime is usually an unknown parameter. We will interpret our search in a large range of particle lifetimes.

However, to avoid having to generate a large number of signal Monte Carlo samples with different LLP lifetimese, we can reweight the particle lifetime from a signal sample with a given lifetime to a new designated particle lifetime.

For example, we have only generated signal samples with particle lifetimes of 0.1, 1, 10, and 100m, we will use those signal samples to reweight to intermediate particle lifetimes (e.g. 0.5, 5, 50 m)

In this exercise, we will go through how to reweight the particle lifetimes.

> ## Open a notebook
>
> For this part, open the notebook called `LLP_lifetimes.ipynb`.
> Run `Ex2` to reweight the particle lifetimes and plot the proper decay length distribution before and after reweighting to verify the reweighting is done properly.
{: .checklist}


> ## Discussion 2.2
>
> Why do we reweight from a larger lifetime to a smaller lifetime? 
> What happens when we do the opposite (reweight from smaller lifetime to larger lifetime)?
{: .discussion}

## Probability of LLP decaying in Endcap Muon Detectors

In this section, we will calculate the probability of LLP decaying in the endcap muon detectors for different LLP lifetimes and observe how the probability changes with the lifetime.

> ## Open a notebook
>
> For this part, open the notebook called `LLP_lifetimes.ipynb` and run `Ex3` 
{: .checklist}
In this exercise, you will first define the geometric decay region of the muon system.

You can find the dimension and layout of the CMS muon system in Fig. 4.1.1 on page 141 of the [Muon Detector Technical Design Report](https://cds.cern.ch/record/343814?ln=en) 

You will calculate the probability of LLP decaying in the endcap muon detectors for LLP mean proper decay lenegths (0.1, 1, 10, 100m) that have been generated.

Then you will call the reweighting function that you've written in the previous exercise to calculate the probability, which we call geometric acceptance, for other intermediate proper decay lengths.

Finally, you will plot the geometric acceptance with respect to the LLP mean proper decay lengths.

> ## Discussion 2.3
> Do you understand the shape of the geometric acceptance vs. LLP mean proper decay lengths plot?
> 
> Why is the peak at 2m, much smaller than the distance between the muon detectors and the interaction point?
> 
{: .discussion}

{% include links.md %}


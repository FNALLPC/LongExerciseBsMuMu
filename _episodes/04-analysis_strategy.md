---
title: "Analysis Strategy"
teaching: 15
exercises: 120
questions:
- "What trigger do we use?"
- "What selections do we make to select for signal clusters and reject background clusters?"
- "What are the remaining background compositions for MDS?"

objectives:
- "Understand the background from punch-through jets, muon bremsstrahlung and low pT pileup particles"
- "Understand key variables that are used to remove background and final discriminating variables used to extract signal and estimate background"

keypoints:
- "Due to the lack of dedicated trigger, we use the high MET trigger in Run 2 to trigger on the signal"
- "The background from main collision comes from punch-through jet and muon bremsstrahlung and are killed by dedicated jet and muon vetos and active vetos using the first muon detector station"
- "The remaining irreducible background comes from low pT particles from pileup events and clear out-of-time pileup contributions can be observed from cluster time distribution"
- "Two final discriminating variables that are independent for background will be used to extract signal and estimate background"
---

## Benchmark model
The MDS signature is model independent, but to develop an analysis strategy we use the higgs portal as a benchmark model, where the Feynman diagram shown below.

We choose this model because its one of the more difficult model probe at the LHC, with no stable BSM particles to produce large MET and the final state objects from the higgs are generally low pT.
This model is also used commonly across many CMS physics searches for sensitivity comparison


> ## Figure 4.1
> <img src="../fig/twinhiggs.png" alt="" style="width: 400px;"/>
> Feynman diagram of the higgs portal model, where a pair of LLPs (S) are produced from the Higgs and the LLPs can decay to fermions.
{: .callout}

## Trigger strategy selections

Trigger selection is the beginning of any CMS analysis.

As mentioned in the introductory slides, there's no dedicated trigger for this signature in Run2.

We are using `MET > 200 GeV` due to the lack of dedicated trigger on the MDS object.

As a result, in order for signal events to pass the large MET trigger
 - the Higgs is recoiled against a high pT jet
 - When the LLPs decays beyond calorimeters, the decay
 - Since the Higgs has a high pT, the MET will be large

This results in the following event topology for signals:

> ## Figure 4.2
> <img src="../fig/trigger.png" alt="" style="width: 600px;"/>
> Diagram demonstrating the signal topology.
> The Higgs is recoiled against an ISR (Initial-State Radiation) jet in a back-to-back configuration.
> The Higgs decay immediately into 2 LLPs.
> When LLPs are decaying in the Muon System or beyond, this will result in MET.
>
> Make sure you understand this event topology.
{: .callout}

> ## Check your understanding
>
> For this part, open the notebook called `analysis_strategy.ipynb`
> You will
>  - confirm that pT of the Higgs matches the size of MET in the event.
>  - compute the trigger efficiency for signals
>
> The typical trigger efficiency for signals is around 1%
{: .checklist}

## Event selections

The event selections for this search are kept at minimal to be as model independent as possible.

We only apply the MET trigger and an *offline* MET cut of 200 GeV, due to the use of the high-MET skim dataset.

To select for a signal-like cluster from an LLP, we will investigate a number of variables that are used in the analysis that remove punch-through jet and muon brem background in the following sections.

## Cluster-level selections

> ## Open a notebook
>
> For this part, open the notebook called `analysis_strategy.ipynb` and run `Ex0` to load the ntuples, apply event level selections, and load the relevant branches.
{: .checklist}

At the cluster-level, we don't apply any selections for data, while for signal we select clusters that are matched to generator-level LLPs that decay in the muon detectors.

At the event-level, we only apply the MET trigger, offline MET cut, and the required MET filters that are already encoded in the `metFilters` variable.

### Punch-through Jet and Muon Bremsstrahlung Background

The dominant background from the main collision comes from punch-through jets that are not fully contained in the calorimeters and high pT muons that could create bremsstrahlung showers in the muon detectors. To remove those background, we reject clusters by matching them to reconstructed jets and muon.
The pT of the jet/muon that the cluster is matched to are saved in objects called `cscRechitClusterJetVetoPt` and `cscRechitClusterMuonVetoPt`.
In this exercise you will plot the two variables for signal and background and apply a selection on the two variables to remove clusters from jets and muons.

> ## Open a notebook
>
> For this part, open the notebook called `analysis_strategy.ipynb` and run `Ex1` to plot the two variables `cscRechitClusterJetVetoPt` and `cscRechitClusterMuonVetoPt`.
{: .checklist}


> ## Discussion 4.1
>
> Does the shape make sense to you? Why does signal has small values and background has larger values? The analysis apply a cut of `cscRechitClusterJetVetoPt<10` and `cscRechitClusterMuonVetoPt<20`, do you agree with these selections?
{: .discussion}


### Cluster Hits in ME11 and ME12

Additionally, punch-through jets or muon bremsstrahlung showers might not get reconstructed as jets and muons.
To fully remove these background, we remove clusters that have hits in the first CSC stations (ME11/ME12) that have little shielding in front.

In this exercise you will plot the number of ME11/ME12 hits in clusters for signal and background and apply a selection on the two variables to remove clusters from jets and muons.

> ## Open a notebook
>
> For this part, open the notebook called `analysis_strategy.ipynb` and run `Ex2` to plot the number of ME11/ME12 hits in clusters
{: .checklist}


> ## Discussion 4.2
>
> Does the shape make sense to you? Why does signal has small values and background has larger values? Why does the background have peaks at around 6 and 12? The analysis requires clusters to have no hits in ME11 and ME12, does you agree with the selection?
> 
{: .discussion}



### Cluster $\eta$ 

After we removed punch-through jets and muon brems, we observed that there are a lot more backgorund in higer $\eta$ region, where the muon reconstruction efficiency is lower and more pileup particles are present to create clusters.

In this exercise you will plot the cluster $\eta$ for signal and background and apply a selection on the variable to remove clusters from high $\eta$ region.

> ## Open a notebook
>
> For this part, open the notebook called `analysis_strategy.ipynb` and run `Ex3` to plot the cluster $\|\eta\|$.
{: .checklist}


> ## Discussion 4.3
>
> Does the shape make sense to you? The analysis requires clusters to have $ \| \eta \| < 2$, does you agree with the selection?
> 
{: .discussion}


### Cluster time

The remaining background clusters after punch-through jet and muon brem showers from the main collision are removed, are from low pT particles in pileup events.
To verify this, you will plot the cluster time for signal and background in this exercise to check for any out-of-time pileup contributions in data.

> ## Open a notebook
>
> For this part, open the notebook called `analysis_strategy.ipynb` and run `Ex4` to plot the cluster time.
{: .checklist}


> ## Discussion 4.4
>
> Does the shape make sense to you? Why is data spaced at 25 ns?
> 
{: .discussion}

> ## Discussion 4.5
>
> Does the data distribution change with and without the vetoes applied? If it does, do you know why?
> 
{: .discussion}
In the analysis, we apply a selection requiring the cluster time to be between -5 ns and -12.5 ns as the signal region.
Additionally, to make use of the out-of-time background clusters, we define a background-enriched early out-of-time (OOT) validation region for the background estimation method used for this analysis, which we will go through in the next episode.



### Cluster $N_{\text{hits}}$ and $\Delta\phi\text{(cluster, MET)}$

The final discriminating variables that we will use to extract the signal and estimate background are the number of hits in the cluster ($N_{\text{hits}}$) and the azimuthal angle between the cluster and MET ( $\Delta\phi\text{(cluster, MET)}$).
The background estimation method will be described in more detail in the next episode.
In this exercise, we will just plot the distributions of the two variables, to understand the shape of the two variables.

> ## Open a notebook
>
> For this part, open the notebook called `analysis_strategy.ipynb` and run `Ex5` to plot the two variables.
{: .checklist}



> ## Question 4.1
>
> Why does the $\Delta\phi\text{(cluster, MET)}$ peak at 0 for signal, but flat for background distribution?
{: .challenge}

> ## Solution 4.1
> For signal, the cluster corresponds to the LLP direction and MET corresponds to the higgs direction, so the two objects are aligned as you can see from Figure 4.2.
> 
> For background, clusters are produced from underlying events, while MET is calculated from primary event, so the two objects are independent.
> 
> Additionally, since $\Delta\phi\text{(cluster, MET)}$ is flat for background, it is also independent to $N_{\text{hits}}$.
> 
> This independence is a key property that we will make use of in the next episode to develop the background estimation method.
{: .solution}

> ## Discussion 4.7
>
> In the analysis, we apply a selection requiring the $N_{\text{hits}}>130$ and  $\| \Delta\phi\text{(cluster, MET)}\| < 0.75$. Do you agree with the selections?
> 
{: .discussion}

Now we have defined the set of selections to select signal clusters, next we will go over how to estimate the background yield with a fully data-driven method without using MC simulation.

{% include links.md %}


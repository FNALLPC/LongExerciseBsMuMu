---
title: "MDS Reconstruction"
teaching: 30
exercises: 180
questions:
- "What is Muon Detector Shower (MDS)?"
- "How are MDS reconstructed?"
objectives:
- "Understand how are MDS reconstructed: the input, the algorithm, the output"
- "Visualize MDS reconstruction"
- "Calculate cluster properties"
- "Calculate MDS reconstruction efficiency with respect to LLP decay position"
keypoints:
- "MDS is a cluster of rechits in the muon system, clustered by the DBSCAN algorithm"
- "MDS properties are computed from the input rechits(e.g. position,time & station) and are very powerful of rejecting background"
- "MDS reconstruction efficiency depends on where the LLP decays with respect to the steel, since the decay particles require small amount of steel to initiate the shower and are detected only in the active gas chambers"
---
## Ingredient of MDS: Rechits 
MDS is a cluster of rechits in the muon system. 
The main reason for using rechit is that rechit provides sufficient **granularity** to capture the high-multiplicity nature of the showers coming from LLPs.

### What is a rechit?

CSCs consist of arrays of positively-charged anode wires crossed with negatively-charged copper cathode strips within a gas volume.
 
When muons pass through, they knock electrons off the gas atoms, which flock to the anode wires creating an avalanche of electrons. 

Positive ions move away from the wire and towards the copper cathode, also inducing a charge pulse in the strips, at right angles to the wire direction.

Because the strips and the wires are perpendicular, we get two position coordinates for each passing particle.

> ## Figure 3.1
> <img src="{{ page.root }}/fig/CSC_chamber.png" alt="" style="width: 400px;"/>
> Illustration of a CSC chamber.
{: .callout}

> ## Discussion 3.1 :rechits
>
> Can you think of some of the properties of a rechit?
> 
> > ## Solution:
> > The most relevant ones for MDS are: position(x,y,z,eta,phi) and time. 
> > 
> {: .solution} 
>
> Are there disadvantage/limitation for using rechit as the inputs of MDS?
> > ## Solution:
> > 
> > The reconstruction of rechits from the anode/cathode pulses are **designed** for a **single muon**, thus it can miss some details about how the shower is developed.
> > 
> > A dedicated machine learning algorithm maybe able to extract those details for even better MDS reconstruction.
> > 
> > Since **multiplicity** is the most important feature of MDS, the limitation of using rechits is very minimal.
> {: .solution} 
{: .discussion}

### How are CSC chambers arranged?

CSC chambers are arranged into 4 different stations, interleaved with the steel of the flux-return yoke.
> ## Figure 3.2
> <img src="{{ page.root }}/fig/MuonSystem.png" alt="" style="width: 600px;"/>
> Illustration of CMS Muon System.
{: .callout}

> ## Open a notebook
>
> For this part, open the notebook called `MDS_reconstruction.ipynb` to learn how to access and visualize the rechits.
{: .checklist}


## Clustering algorithm

DBSCAN(Density-Based Spatial Clustering of Applications with Noise) is a widely-used, generic clustering algorithm.

It has two parameters, `minPts` for minimum points to be a cluster and `dR` for the distance between points. 

For clustering MDS, the rechits are the input points and we are clustering in the `eta-phi` space.

We choose `minPts = 50, dR = 0.2`. `minPts = 50` because it's more than 2x of the typical number of hits created by a muon in CSC(< 24 hits).

> ## Figure 3.3
> <img src="{{ page.root }}/fig/DBSCAN-Illustration.png" alt="" style="width: 400px;"/>
> Illustration of DBSCAN algorithm.
> In this diagram, minPts = 4. 
>
> Point A and the other red points are core points, because the area surrounding these points in an ε radius contain at least 4 points (including the point itself). Because they are all reachable from one another, they form a single cluster.
>
> Points B and C are not core points, but are reachable from A (via other core points) and thus belong to the cluster as well. 
>
> Point N is a noise point that is neither a core point nor directly-reachable. 
{: .callout}

### Cluster properties  

Cluster properties are computed from **constituent** rechits. Here are the descriptions of some key cluster properties:
 - Cluster position: average of input rechit positions
 - Cluster time: average of input rechit wire time and strip time 
 - Cluster nStation10: number of stations with at least 10 input rechits in this cluster
 - Cluster avgStation10: average station number weighted by number of rechits, using stations with at least 10 input rechits
 - Cluster nME11/12: number of rechits coming from ME11 or ME12 in this cluster

> ## Exercise: compute cluster properties
>
> Following the definitions above, complete the function `computeCluster`, `computeStationProp` and `computeME11_12`.
> 
{: .challenge}

> ## Exercise: plot cluster properties 
>
> Plot the cluster properties of background and signal clusters.
> 
> To compute for signal clusters,
> - run the `DBScan` functions with signal rechits
> - store the output in a new variable called `s_cls`
> - add an addition line in `samples` for plotting
>
> Try to read and understand the plotting code as well. 
{: .challenge}


> ## Discussion 3.2: cluster properties 
>
> Which variables can be used to distinguish between signal and background? 
> 
> > ## Solution:
> > You should be able to see the `N_rechits`, `time`, and `ME11_12` distributions are very different between signal and background.
> >
> > Placing some cuts on these variables should give us separation of signal events from background! 
> > 
> {: .solution} 
{: .discussion}


## MDS reconstruction efficiency

When an LLP decay in CSC, we want to know 
 - *how often* it can make an MDS cluster (this is cluster efficiency) and
 - *where* does the LLP decay when this happens
 
In this part, we will make a plot of MDS efficiency as a function LLP decay position and try to understand it. 

> ## Open a notebook
>
> For this part, continue to the section `MDS reconstruction efficiency for signal` to calculate the MDS reconstruction efficiency with respect to the LLP decay position.
{: .checklist}


> ## Discussion 3.3
>
> Why does the efficiency drops off at the two ends of the muon detectors?
> 
> How does the efficiency varies between the muon stations? Do you understand why?
> 
> Make a 2D histogram to confirm your understanding!
> 
{: .discussion}
{% include links.md %}


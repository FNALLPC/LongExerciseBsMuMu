---
title: "Event Display (optional)"
teaching: 0
exercises: 60
questions:
- "How to make event displays of interesting signal simulation?"
objectives:
- "Learn to make and inspects event displays with cmsShow"
keypoints:
- "Event displays allow us to view all available collections visually and scrutinize event topologies that are not possible with ntuples"
---

In this episode you will look at event display of signal simulation events that pass the signal region selectionns

cmsShow is the program used to view event displays using a web-based GUI. 

We have created a ROOT file that contains the RECO format of the events passing the signal region selection.


## Open the events with cmsShow

Go to [cmsShow](https://fireworks.cern.ch). Enter the file path: `/eos/user/c/christiw/CMSDAS_MDS/ggH_HToSSTobbbb_MH-125_MS-40_ctau-1000_Fall17_nhits600_nStation1.root` and then click on "Load file EOS".
You will now see a graphical interface like this:
> ## Figure 7.1
> <img src="../fig/event_display_web.png" alt="" style="width: 600px;"/>
> Event display of a signal event from cmsShow.
{: .callout}

By default the `csc2DRecHits` are not included in the display, go to Add Collectionon the left to add the rechits collections!
Now you can skim through the events that you have selected to see if the clusters appear as you've expected.

> ## Discussion 7.1
>
> What PF objects do you see in the events? Does the kinematics of these objects agree with what you are expecting?
> I.e. is the MET greater than 200 GeV, is the $\Delta\phi$ between the MET and the cluster what you are expecting? How many hits are there in the cluster? Does the cluster pass the jet/muon veto cut that you applied? 
> 
{: .discussion}

{% include links.md %}


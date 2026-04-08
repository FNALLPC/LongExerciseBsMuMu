---
title: "Results and Statistical Analysis"
teaching: 0
exercises: 180
questions:
- "What is the unblinded result?"
- "How to constrain the ABCD relationship for background in datacards?"
objectives:
- "Understand how to make datacard and constrain the ABCD relationship for background in the datacards"
- "Run Higgs Combine to get Asymptotic limits on BR from the datacards"
- "Produce limit plot with respect to LLP mean proper decay length"
keypoints:
- "We can use Higgs Combine to perform statistical analysis and set limits"
- "The value of the limits depend significantly on the LLP mean proper decay length, as the probability of LLP decaying in the muon system strongly correlates with the LLP lifetimes"
---

## Create datacards

Now that we have a well-developed analysis stratey and robus background estimation method, we are ready to produce datacards, look at the unblinded result and perform statistical analysis.

In this exercise, we will walk you through to apply all the signal region selections, add systematic uncertainties and and write the signal and background yield in the ABCD plane to datacards.

> ## Open a notebook
>
> For this part, open the notebook called `create_datacard.ipynb` to load the ntuples, apply signal region selection, add systematic uncertainties, and write the signal and background yield in the ABCD plane to datacards.
{: .checklist}


> ## Discussion 6.1
>
> Do you understand the example datacards? Where is the ABCD relationship constrained for background?
> 
{: .discussion}

> ## Question 6.1
> Do you know what does the rateParam `norm` do and why do we add the rateParam to change the normalization of the signal yield?
{: .challenge}

> ## Solution 6.1
> The rateParam in principle can shift the normalization of the signal yield if its allowed to float during the fit.
> However, we will freeze the rateParam when we run Combine by adding arguments `--freezeParameters norm --setParameters norm=0.001`
> The reason we add a rateParam and scale the signal is because the signal yield varies from O(1) to O(1000) for signals with different LLP lifetimes.
> However, Combine only works well when the fitted signal strength is between 1 to 15, so we scale the signal yield up/down so that the fitted signal strength fits in that range, and we multiply scale factor back when we plot the limits.
{: .solution}




## Results

Based on the unblinded data, we can perform a background-only fit to see if the observation agrees with the background prediction.


Run the followiing command to install Higgs Combine:
~~~
cd ${CMSSW_BASE}/src
cmsenv
git -c advice.detachedHead=false clone --depth 1 --branch v10.4.2 https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
scramv1 b clean; scramv1 b -j$(nproc --ignore=2) # always make a clean build, with n - 2 cores on the system
~~~
{: .language-bash}

Choose any of the datacards that you've produced and run the following commands:

~~~
combine -M MultiDimFit datacard.txt --saveWorkspace -n Snapshot --freezeParameters r,norm --setParameters r=0,norm=0.001

combine -M FitDiagnostics  --snapshotName MultiDimFit --bypassFrequentistFit higgsCombineSnapshot.MultiDimFit.mH120.root --saveNormalizations --saveShapes --saveWithUncertainties
~~~
{: .language-bash}

You will get an output file called `fitDiagnosticsTest.root`.
Open the ROOT file and navigate to the TH1F in `shapes_fit_b/chA/total_background` by running the following command:
~~~
root -l fitDiagnosticsTest.root
shapes_fit_b->cd()
chA->cd()
total_background->GetBinContent(1) # this will print the background prediction
total_background->GetBinError(1) # this will print the uncertainty on the background prediction

~~~
{: .language-bash}

Does the background prediction agree with the observation?

{: .language-bash}

## Run Higgs Combine to compute limits


To run the Asymptotic frequentist limits we can use the following command (replace `test.txt` with your datacard path):
~~~
combine -M AsymptoticLimits test.txt --freezeParameters norm --setParameters norm=1
# a good rule of thumb for norm is to set it equal to 1./sigA, where sigA is the signal yield in bin A
~~~
{: .language-bash}

The program will print the limit on the signal strength r (number of signal events / number of expected signal events) e .g. Observed Limit: r < XXX @ 95% CL , the median expected limit Expected 50.0%: r < XXX, and edges of the 68% and 95% ranges for the expected limits.
The program will also create a ROOT file `higgsCombineTest.AsymptoticLimits.mH120.root` containing a ROOT tree limit that contains the limit values that we will use later to produce limits plots.

Since we have normalized our signal yield to assume BR(h$\rightarrow$ SS) = 1, the limit on the signal strength r from Combine essentially tells us the limit on BR(h$\rightarrow$ SS), modulo the normalization in signal yield.

> ## Open a script
>
> For this part, open the python script `scripts/run_combine.py` to run over all of the datacards that you produced in the previous exercise and save all the ROOT files in a directory.
>
> * You will have to update the directory of the datacards in the script*
{: .checklist}


## Make limit plots

In this exercise, we will use the limits that were saved in ROOT files produced in the previous exercise to calculate the limit on BR(h $\rightarrow$ SS) with respect to the LLP mean proper decay lengths. 

> ## Open a notebook
>
> For this part, open the notebook called `limitPlot.ipynb` to plot the expected and observed limits. See if the limit agrees with the one showed on slide 25 of the introduction slides.
{: .checklist}



> ## Discussion 6.1
>
> Did you expect the shape of the limit to look like this? Why does the sensitivity decreases for very long or very short lifetimes?
> 
{: .discussion}

> ## Exercise 
> Now that you have the limit plot for 40 GeV, try to see if you can create datacards, run combine, and make limits plot for 15 and 55 GeV.
> Try to plot them in the same canvas, like the one in slide 25 of the introduction slide.
> 
{: .discussion}


{% include links.md %}




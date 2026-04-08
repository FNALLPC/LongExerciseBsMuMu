---
title: Setup
---

# Run exercises in cmslpc

Open a terminal/console, connect to cmslpc-el9 and prepare your working area:

~~~
kinit username@FNAL.GOV
ssh -L localhost:8888:localhost:8888 <YOUR USERNAME>@cmslpc-el9.fnal.gov
~~~
{: .language-bash}


If you haven't done it yet, go to your `nobackup` area (`/uscms_data/d3/<YOUR USERNAME>/`) and create a folder for the CMSDAS exercises. Once you are there you can setup the CMSSW environment and clone our repository:

~~~
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv

git clone git@github.com:FNALLPC/MDS_CMSDAS.git -b 2026
cd MDS_CMSDAS 
~~~

## Useful tips

You can make an `alias` for that command in your `~/.bashrc` file
~~~
alias sourcelcg='source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh'
~~~
{: .language-bash}
then you can just do 
~~~
sourcelcg
~~~
after you login.
{: .language-bash}


{% include links.md %}

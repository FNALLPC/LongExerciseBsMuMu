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
{: .language-bash}


The following commands one has to do it *everytime you log in into a new session*. They load the
environment and the packages needed for the exercises and open a jupyter notebook:
~~~
source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh
jupyter notebook --no-browser --port=8888 --ip 127.0.0.1
~~~
{: .language-bash}

> ## Remember
> The port number `8888` needs to match the port number you log-in to `cmslpc`.
> 
> If someone has taken the `8888` port on the cmslpc node, you will need to use another one. 
{: .callout}

If these two lines are running sucessfully, you should see something like this:
~~~

[I 12:55:39.283 NotebookApp] Serving notebooks from local directory: /uscms_data/d3/christiw/MDSDAS_test/CMSSW_14_1_0_pre4/src/MDS_CMSDAS
[I 12:55:39.283 NotebookApp] Jupyter Notebook 6.4.0 is running at:
[I 12:55:39.283 NotebookApp] http://127.0.0.1:8888/?token=230ce3a068580ce4d808fde4b44c8575ebe4ae0fbb7d4b4f
[I 12:55:39.283 NotebookApp]  or http://127.0.0.1:8888/?token=230ce3a068580ce4d808fde4b44c8575ebe4ae0fbb7d4b4f
[I 12:55:39.283 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 12:55:39.321 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///uscms/homes/c/christiw/.local/share/jupyter/runtime/nbserver-412704-open.html
    Or copy and paste one of these URLs:
        http://127.0.0.1:8888/?token=230ce3a068580ce4d808fde4b44c8575ebe4ae0fbb7d4b4f
     or http://127.0.0.1:8888/?token=230ce3a068580ce4d808fde4b44c8575ebe4ae0fbb7d4b4f
~~~
{: .output}

Copy and paste one of the last two urls in your favorite browser and now you can continue with the lesson 1 (Episode 1).


## Useful tips

Since we launch jupyter server frequently, you can make an `alias` for that command in your `~/.bashrc` file
~~~
alias sourcelcg='source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh'
alias launchJupyter='jupyter notebook --no-browser --port=8888 --ip 127.0.0.1'
~~~
{: .language-bash}
then you can just do 
~~~
sourcelcg
launchJupyter
~~~
after you login.
{: .language-bash}


{% include links.md %}

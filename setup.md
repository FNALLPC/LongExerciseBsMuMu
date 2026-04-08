---
title: Setup
root: .
layout: page
---

## Environment

This exercise runs at the LPC (Fermilab). You need:

- A valid CMSLPC account with access to EOS
- CMSSW (for the reconstruction part)
- A ROOT installation with RooFit (included in CMSSW or standalone CMSSW environment)

### Setting up CMSSW

```bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_13_0_13
cd CMSSW_13_0_13/src
cmsenv
```

### Getting the exercise scripts

```bash
git clone git@github.com:FNALLPC/LongExerciseBsMuMu.git
cd LongExerciseBsMuMu
git checkout 2027
```

## Data files

All input ROOT files are on EOS at:

```
root://cmseos.fnal.gov//store/user/cmsdas/2025/long_exercises/long-ex-bs-mumu/
```

Key files used in the exercise:

| File | Description |
|------|-------------|
| `bupsikData.root` | B<sup>+</sup>→J/ψK<sup>+</sup> data |
| `bupsikMc.root` | B<sup>+</sup>→J/ψK<sup>+</sup> MC |
| `bspsiphiData.root` | B<sub>s</sub>→J/ψφ data |
| `bspsiphiMc.root` | B<sub>s</sub>→J/ψφ MC |
| `bsmmMc.root` | B<sub>s</sub>→μμ signal MC |
| `bmmData-blind.root` | Blinded B<sub>s</sub>→μμ data (sidebands only) |
| `bmmSoup10.root` | Toy data soup for final fit |
| `bdmmMc.root` | B<sup>0</sup>→μμ peaking background MC |
| `bstohhMcBg.root`, `bdtohhMcBg.root` | Hadronic background MCs |
| `bskmunuMcBg.root`, `bdpimunuMcBg.root` | Semileptonic background MCs |

> ## Note on EOS paths
>
> These files can only be accessed from the LPC interactive nodes or batch jobs.
> The scripts use `xrootd` (`root://cmseos.fnal.gov//...`) to read them remotely.
{: .callout}

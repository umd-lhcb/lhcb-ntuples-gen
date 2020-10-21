## Rationale

- The main limitation for local `DaVinci` docker is: Raw data files (`.dst`)
  need to be downloaded locally. Given that the size of `.dst` files is on the
  order of TBs, this method is only used for developing `DaVinci` scripts and
  first-order validation

- On `lxplus`, several official `DaVinci` versions are provided. However, there
  are some drawbacks:

    1. `.dst` files still need to be downloaded to some `lxplus` user directory
    2. While `DaVinci` is running, the connection to `lxplus` must be kept alive

LHCb collaboration provides a solution: Submitting and running `DaVinci` jobs on
a GRID. The advantages are:

1. GRID know how to access `.dst` files directly, thus there's no need to manually
   download them. Instead, users need to specify the links (`LFN`s) to desired
   `.dst` files

2. While the GRID `DaVinci` jobs are running, there's no need to keep a
   connection to `lxplus`.


## Preparation

### Setup LHCb GRID certificate

Following [this twiki](https://twiki.cern.ch/twiki/bin/view/LHCb/FAQ/Certificate) to:

1. Apply for a GRID certificate
2. Setup the certificate on `lxplus`

!!! note
    The twiki claimed that a new user must physically go to CERN's user office
    to be able to apply for a new cert via [ca.cern.ch](https://ca.cern.ch/ca).
    But I didn't have to do that.

### Compile a local `DaVinci` on `lxplus`

We are using some non-official `TupleTool`, so we need to compile `DaVinci` on lxplus.

First, we need to figure out the runtime dependency for our version of DaVinci: {{ davinci_ver }}.


There is a **central** Ganga job submitter that should handle **all** job
submissions for **all** reconstruction scripts in **all** folders. The script
is located at:
```
scripts/ganga/ganga_jobs.py
```

This script can only run on `lxplus` nodes. The general syntax is:
```
ganga_jobs.py <reco_script> <cond_files>
```

For instance, for run 1 $R(D^{(*)})$ signal Monte Carlo:
```
ganga_jobs.py ../../run1-rdx/reco_Dst_D0.py ../../run1-rdx/cond/cond-mc-2012-md-sim08a.py -p mu -P Pythia6 -d Bd2DstTauNu
```

!!! note
    The last three flags: `-p`, `-P`, and `-d` are optional. They have default values.

!!! note
    The usage of `ganga_jobs.py` is described by:
    ```
    ganga_jobs.py --help
    ```

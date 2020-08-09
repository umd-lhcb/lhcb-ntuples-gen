# lhcb-ntuples-gen [![Build status](https://travis-ci.com/umd-lhcb/lhcb-ntuples-gen.svg?build)](https://travis-ci.com/umd-lhcb/lhcb-ntuples-gen)
This is a special branch for comparing DaVinci scripts made by Phoebe and
Yipeng. We use DaVinci/v36r1p2 on the lxplus7 to do the comparison.

- `reco_Dst-debug-phoebe.py`: Phoebe's script is taken from [version `0.1`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/0.1/2012-b2D0MuXB2DMuNuForTauMuLine/ntuple_options-sample.py),
   of this project, with data conditions removed and automatic formatting by
   `black`.

- `reco_Dst-debug-yipeng.py`: Yipeng's script is taken from [version `0.7`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/0.7/run1-b2D0MuXB2DMuNuForTauMuLine/reco_Dst-debug.py)
  of this project, with tweaks for DaVinci-backward-compatibility.


## To run these scripts on `lxplus`

1. Checkout the `test-comp-davinci` branch
2. `cd` into `run1-b2D0MuXB2DMuNuForTauMuLine` folder
3. Put the following 2012 MagDown data to the subfolder `data/data-2012-md`:
    ```
    00041836_00006100_1.semileptonic.dst
    00041836_00011435_1.semileptonic.dst
    00041836_00013110_1.semileptonic.dst
    ```

4. Execute the following command
    ```
    ./run.sh reco_Dst-debug-phoebe.py conds/cond-std-2012.py
    ./run.sh reco_Dst-debug-yipeng.py conds/cond-std-2012.py
    ```

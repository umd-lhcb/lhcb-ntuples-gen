# RDX run 1 validation: Phoebe vs us, 2011 MD

!!! info
    The **bold number** with a link indicates that this number is consistent
    with a previous study, with the previous study linked.

    If a number is **bold** but w/o a link, it shares the link for the number
    to its left.


## $D^*$, right-sign, Phoebe step-1+1.5 vs us

!!! note
    - Before the slanted _step-1.5_ line, the numbers are from Phoebe's step-1.
    - The `*` is considered immaterial
        - For Phoebe's ntuple, we remove the VELO only slow $\pi$
        - For us, this is already removed at DaVinci level

!!! info
    - It is known that PID and isolation BDT values have changed between
      DaVinci versions
    - Also, the vertexing has changed. This is manifested in the
      _Offline $D^* \mu$ combo_ cuts.
        - The cuts are defined in [here](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/45069ec62bae102c2e397d1f42594de30e6ce7df/include/functor/rdx/cut.h#L222-L245).
        - Notably, we have _vertex $\chi^2/dof$_ cuts, like
          `b0_endvtx_chi2/b0_endvtx_ndof < 6.0`.

| Cut                                           | Phoebe  | us      | Phoebe $\epsilon$  | us $\epsilon$      | $\epsilon$ ratio   |
|-----------------------------------------------|---------|---------|--------------------|--------------------|--------------------|
| Total events                                  | 208846  | 216987  | -                  | -                  | -                  |
| Select 2011 MD data*                          | 195535  | 216987  | 93.6               | 100.0              | 1.07               |
| L0                                            | 189422  | 210166  | 96.9               | 96.9               | 1.00               |
| Hlt1                                          | 185980  | 206226  | 98.2               | 98.1               | 1.00               |
| Hlt2                                          | 183194  | 203010  | 98.5               | 98.4               | 1.00               |
| $D^0$ PID                                     | 178517  | 197740  | 97.4               | 97.4               | 1.00               |
| Offline $D^0$ cuts (no PID no mass window)    | 146240  | 160219  | 81.9               | 81.0               | 0.99               |
| $\mu$ PID$\mu$ cut                            | 146240  | 160219  | 100.0              | 100.0              | 1.00               |
| Offline $\mu$ cuts (no PID)                   | 138166  | 151326  | 94.5               | 94.4               | 1.00               |
| Offline $D^* \mu$ combo cuts (no mass window) | 137097  | 140528  | 99.2               | 92.9               | 0.94               |
| _step-1.5_                                    | [**136645**](https://github.com/umd-lhcb/rdx-run2-analysis/blob/master/docs/cuts/cut_validation.md#2011-magdown-real-data-d-phoebe-vs-us-global-cuts-only)  | **140528**  | 99.6               | 92.9               | 0.93               |
| Fit variable range cuts                       | 132754  | 136478  | 97.2               | 97.1               | 1.00               |
| $\mu$ other PID cuts                          | 126514  | 135038  | 95.3               | 98.9               | 1.04               |
| $D^*$ mass window                             | 110017  | 112535  | 87.0               | 83.3               | 0.96               |
| $B^0$ mass window                             | 110010  | 112528  | 100.0              | 100.0              | 1.00               |
| $BDT_{iso} < 0.15$                            | 78903   | 72628   | 71.7               | 64.5               | 0.90               |
| ISO final                                     | [**74301**](https://github.com/umd-lhcb/rdx-run2-analysis/blob/master/docs/cuts/cut_validation.md#skim-cuts)  | 72628   | 94.2               | 100.0              | 1.06               |


## $D^*$, wrong-sign $\mu$, Phoebe step-1+1.5 vs us

| Cut                                           | Phoebe  | us      | Phoebe $\epsilon$  | us $\epsilon$      | $\epsilon$ ratio   |
|-----------------------------------------------|---------|---------|--------------------|--------------------|--------------------|
| Total events                                  | 26705   | 31939   | -                  | -                  | -                  |
| Select 2011 MD data*                          | 24945   | 31939   | 93.4               | 100.0              | 1.07               |
| L0                                            | 24120   | 30876   | 96.7               | 96.7               | 1.00               |
| Hlt1                                          | 23451   | 30008   | 97.2               | 97.2               | 1.00               |
| Hlt2                                          | 22872   | 29218   | 97.5               | 97.4               | 1.00               |
| $D^0$ PID                                     | 22256   | 28390   | 97.3               | 97.2               | 1.00               |
| Offline $D^0$ cuts (no PID no mass window)    | 11925   | 14643   | 53.6               | 51.6               | 0.96               |
| $\mu$ PID$\mu$ cut                            | 11925   | 14643   | 100.0              | 100.0              | 1.00               |
| Offline $\mu$ cuts (no PID)                   | 11665   | 14332   | 97.8               | 97.9               | 1.00               |
| Offline $D^* \mu$ combo cuts (no mass window) | 11529   | 11796   | 98.8               | 82.3               | 0.83               |
| _step-1.5_                                    | [**12219**](https://github.com/umd-lhcb/rdx-run2-analysis/blob/master/docs/cuts/cut_validation.md#2011-magdown-wrong-sign-mu-d-phoebe-vs-us-global-cuts-only)  | **11796**   | 99.6               | 82.3               | 0.83               |
| Fit variable range cuts                       | 10819   | 10369   | 88.5               | 87.9               | 0.99               |
| $\mu$ other PID cuts                          | 7796    | 9918    | 72.1               | 95.7               | 1.33               |
| $D^*$ mass window                             | 5495    | 5594    | 70.5               | 56.4               | 0.80               |
| $B^0$ mass window                             | 5486    | 5586    | 99.8               | 99.9               | 1.00               |
| $BDT_{iso} < 0.15$                            | 1419    | 1248    | 25.9               | 22.3               | 0.86               |


## $D^*$, wrong-sign slow $\pi$, Phoebe step-1+1.5 vs us

| Cut                                           | Phoebe  | us      | Phoebe $\epsilon$  | us $\epsilon$      | $\epsilon$ ratio   |
|-----------------------------------------------|---------|---------|--------------------|--------------------|--------------------|
| Total events                                  | 34556   | 44187   | -                  | -                  | -                  |
| Select 2011 MD data*                          | 31850   | 44187   | 92.2               | 100.0              | 1.08               |
| L0                                            | 30785   | 42712   | 96.7               | 96.7               | 1.00               |
| Hlt1                                          | 29563   | 41079   | 96.0               | 96.2               | 1.00               |
| Hlt2                                          | 28683   | 39843   | 97.0               | 97.0               | 1.00               |
| $D^0$ PID                                     | 27678   | 38413   | 96.5               | 96.4               | 1.00               |
| Offline $D^0$ cuts (no PID no mass window)    | 21291   | 30013   | 76.9               | 78.1               | 1.02               |
| $\mu$ PID$\mu$ cut                            | 21291   | 30013   | 100.0              | 100.0              | 1.00               |
| Offline $\mu$ cuts (no PID)                   | 20403   | 28649   | 95.8               | 95.5               | 1.00               |
| Offline $D^* \mu$ combo cuts (no mass window) | 20240   | 21165   | 99.2               | 73.9               | 0.74               |
| _step-1.5_                                    | [**19409**](https://github.com/umd-lhcb/rdx-run2-analysis/blob/master/docs/cuts/cut_validation.md#2011-magdown-wrong-sign-slow-pi-d-phoebe-vs-us-global-cuts-only)  | **21165**   | 99.7               | 73.9               | 0.74               |
| Fit variable range cuts                       | 18710   | 20343   | 96.4               | 96.1               | 1.00               |
| $\mu$ other PID cuts                          | 17511   | 20043   | 93.6               | 98.5               | 1.05               |
| $D^*$ mass window                             | 3194    | 3386    | 18.2               | 16.9               | 0.93               |
| $B^0$ mass window                             | 3193    | 3385    | 100.0              | 100.0              | 1.00               |
| $BDT_{iso} < 0.15$                            | 1548    | 1446    | 48.5               | 42.7               | 0.88               |

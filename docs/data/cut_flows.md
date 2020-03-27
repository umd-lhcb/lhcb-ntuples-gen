## $R(D^{*})$ cut flow comparison between run 1 and 2

### Generation steps

1. Extract DaVinci-level cut efficiencies with [`davinci_log_parser.py`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/utils/davinci_log_parser.py):
    ```
    ./davinci_log_parser.py <output_yaml_filename> <input_log1> <input_log2> ...
    ```
2. Run the [`cut_flow-run1.py`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/run1-b2D0MuXB2DMuNuForTauMuLine/cut_flow/cut_flow-run1.py) and [`cut_flow-run2.py`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/run2-b2D0MuXB2DMuForTauMuLine/cut_flow/cut_flow-run2.py). Note that all required files are hard-coded in the scripts.
3. Generate cut flow table with:
    ```
    make cutflow-RDst
    ```
    Please refer to the [`Makefile`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/Makefile) on the implementation details.


### Cut flow table

| cut name                                     | run 1 yield   | run 2 yield   | run 1 efficiency   | run 2 efficiency   | double ratio   |
|----------------------------------------------|---------------|---------------|--------------------|--------------------|----------------|
| Total events                                 | 502736        | 520046        | -                  | -                  | -              |
| Stripped $D^0 \mu^-$                         | 10422         | 13807         | 0.02073±0.00020    | 0.02655±0.00022    | 1.281±0.016    |
| $D^0 \rightarrow K^- \pi^+$ (tigter $K \pi$) | 10080         | 13398         | 0.9672±0.0018      | 0.9704±0.0015      | 1.0033±0.0025  |
| $D^{*+} \rightarrow D^0 \pi^+$               | 5987          | 7893          | 0.5939±0.0049      | 0.5891±0.0043      | 0.992±0.011    |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$         | 5498          | 6454          | 0.9183±0.0037      | 0.8177±0.0044      | 0.8904±0.0060  |
| Refit $\bar{B}^0$ decay tree                 | 5197          | 6139          | 0.9453±0.0032      | 0.9512±0.0028      | 1.0063±0.0045  |
| L0                                           | 488           | 579           | 0.0842±0.0038      | 0.0859±0.0035      | 1.020±0.062    |
| Hlt1                                         | 419           | 579           | 0.859±0.017        | 1.0000±0.0032      | 1.165±0.024    |
| Hlt2                                         | 310           | 579           | 0.740±0.023        | 1.0000±0.0032      | 1.352±0.042    |
| $\mu$ PID                                    | 310           | 527           | 1.0000±0.0059      | 0.910±0.013        | 0.910±0.014    |
| $\text{IsoBDT}_{\Upsilon(\text{4s})} < 0.15$ | 241           | 392           | 0.777±0.026        | 0.744±0.020        | 0.957±0.041    |
| $m_{\Upsilon(\text{4s})} < 5280$             | 241           | 392           | 1.0000±0.0076      | 1.0000±0.0047      | 1.0000±0.0089  |
| Total ratio                                  | -             | -             | 0.000479±0.000033  | 0.000754±0.000040  | 1.57±0.14      |

!!! note
    - With run 1 `DaVinci` script plus the run 2 stripping condition, we find
      2016 (run 2 year) ntuple contains ~5x candidates than that of 2012 (run 1
      year). See [released figures in this project](https://github.com/umd-lhcb/RDRDstRun2AnalysisPreservation/releases/latest).
    - The luminosity between 2016 and 2012 are similar. We figured this out with DaVinci and DIRAC.
    - We have a factor of 2 from the cross section. See [this paper](https://arxiv.org/pdf/1612.05140.pdf)
    - This leaves a factor of 2.5. We are expecting ~1.7.
    - Meanwhile, cut flow generated with very similar script and cocktail MC
      data agrees with the expected ~1.7 factor.
    - This table uses **full** run 1 and 2 cocktail MC.

!!! info
    - Run 1 stripping conditions can be found at [`Strippingb2D0MuXB2DMuNuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping21/semileptonic/strippingb2d0muxb2dmunufortaumuline.html)
    - Run 2 stripping conditions can be found at [`Strippingb2D0MuXB2DMuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping28r2/semileptonic/strippingb2d0muxb2dmufortaumuline.html)

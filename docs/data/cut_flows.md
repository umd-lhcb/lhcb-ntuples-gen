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


### Cut flow table with cocktail MC

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
    - This table uses **full MagDown** run 1 and 2 cocktail MC.

!!! info
    - Run 1 stripping conditions can be found at [`Strippingb2D0MuXB2DMuNuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping21/semileptonic/strippingb2d0muxb2dmunufortaumuline.html)
    - Run 2 stripping conditions can be found at [`Strippingb2D0MuXB2DMuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping28r2/semileptonic/strippingb2d0muxb2dmufortaumuline.html)


### Cut flow table with real data

| cut name                                     | run 1 yield   | run 2 yield   | run 1 efficiency    | run 2 efficiency      | double ratio        |
|----------------------------------------------|---------------|---------------|---------------------|-----------------------|---------------------|
| Total events                                 | 129986930     | 486980122     | -                   | -                     | -                   |
| Stripped $D^0 \mu^-$                         | 7576232       | 35543709      | 0.058285±0.000020   | 0.072988±0.000012     | 1.25227±0.00048     |
| $D^0 \rightarrow K^- \pi^+$ (tigter $K \pi$) | 7574988       | 35529720      | 0.9998358±0.0000048 | 0.9996064±0.0000033   | 0.9997706±0.0000058 |
| $D^{*+} \rightarrow D^0 \pi^+$               | 1642940       | 7337335       | 0.21689±0.00015     | 0.206513±0.000068     | 0.95215±0.00072     |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$         | 1190313       | 4510320       | 0.72450±0.00035     | 0.61471±0.00018       | 0.84846±0.00048     |
| Refit $\bar{B}^0$ decay tree                 | 1110480       | 4117698       | 0.93293±0.00023     | 0.91295±0.00013       | 0.97858±0.00028     |
| L0                                           | 99719         | 409798        | 0.08023±0.00024     | 0.08558±0.00013       | 1.0667±0.0036       |
| Hlt1                                         | 86378         | 409798        | 0.8662±0.0011       | 1.0000000±0.0000045   | 1.1544±0.0014       |
| Hlt2                                         | 66875         | 409798        | 0.7742±0.0014       | 1.0000000±0.0000045   | 1.2916±0.0024       |
| $\mu$ PID                                    | 66875         | 275695        | 1.000000±0.000027   | 0.67276±0.00073       | 0.67276±0.00073     |
| $\text{IsoBDT}_{\Upsilon(\text{4s})} < 0.15$ | 46820         | 183843        | 0.7001±0.0018       | 0.66683±0.00090       | 0.9525±0.0027       |
| $m_{\Upsilon(\text{4s})} < 5280$             | 45990         | 179910        | 0.98227±0.00063     | 0.97861±0.00034       | 0.99627±0.00073     |
| Total ratio                                  | -             | -             | 0.0003538±0.0000016 | 0.00036944±0.00000087 | 1.0442±0.0054       |

!!! note
    - This table uses **full MagDown** 2012 and 2016 real data.
    - The ntuples used to generated the comparison plot have 258438 (2012) and
      1218948 (2016) events.
    - The main difference between the cut flow ntuples and the plotting ntuples
      is:
      Cut flow ntuples use **stripping line $\mu$** but plotting ntuples use
      **all available $\mu$**.

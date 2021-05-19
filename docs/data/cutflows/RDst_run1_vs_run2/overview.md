# $R(D^*)$ cutflow overview

## Generation steps

1. Extract DaVinci-level cut efficiencies with [`davinci_log_parser.py`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/scripts/davinci_log_parser.py):
    ```
    ./davinci_log_parser.py <output_yaml_filename> <input_log1> <input_log2> ...
    ```

    !!! note
        `<output_yaml_filename>` is the generated file. Same below.

        For input logs files, wildcard `*` is supported. So instead of
        providing a list of log files, you can just provide a single
        **pattern** that matches to all log files.

        Example usage:
        ```
        ./davinci_log_parser.py input-run1.yml $INPUT_DIR/53/*/output/*.log
        ```

2. Generate cut flow table with:
    ```
    make cutflow-rdst
    ```
    Please refer to the [`rdx.mk`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/postprocess/make/rdx.mk) on the implementation details.


## Cutflow table with cocktail MC

| cut name                                     | run 1 yield   | run 2 yield   | run 1 efficiency   | run 2 efficiency   | double ratio   |
|----------------------------------------------|---------------|---------------|--------------------|--------------------|----------------|
| Total events                                 | 502736        | 520046        | -                  | -                  | -              |
| Stripped $D^0 \mu^-$                         | 10422         | 13807         | 0.02073±0.00020    | 0.02655±0.00022    | 1.281±0.016    |
| $D^0 \rightarrow K^- \pi^+$ (tighter $K\pi$) | 10080         | 13397         | 0.9672±0.0018      | 0.9703±0.0015      | 1.0032±0.0025  |
| $D^{*+} \rightarrow D^0 \pi^+$               | 5988          | 7891          | 0.5940±0.0049      | 0.5890±0.0043      | 0.992±0.011    |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$         | 5500          | 6449          | 0.9185±0.0037      | 0.8173±0.0044      | 0.8898±0.0060  |
| Refit $\bar{B}^0$ decay tree                 | 5482          | 6423          | 0.99673±0.00096    | 0.99597±0.00095    | 0.9992±0.0014  |
| L0                                           | 2463          | 3529          | 0.4493±0.0068      | 0.5494±0.0063      | 1.223±0.023    |
| Hlt1                                         | 1819          | 3529          | 0.7385±0.0091      | 1.00000±0.00052    | 1.354±0.017    |
| Hlt2                                         | 1242          | 3529          | 0.683±0.011        | 1.00000±0.00052    | 1.465±0.024    |
| $\mu$ PID                                    | 1174          | 3131          | 0.9452±0.0072      | 0.8872±0.0055      | 0.9386±0.0093  |
| $\text{IsoBDT}_{B^0} < 0.15$                 | 910           | 2342          | 0.775±0.013        | 0.7480±0.0080      | 0.965±0.019    |
| $B^0$ cuts                                   | 910           | 2340          | 1.0000±0.0020      | 0.9991±0.0011      | 0.9991±0.0023  |
| $K$ cuts                                     | 897           | 1915          | 0.9857±0.0051      | 0.8184±0.0083      | 0.8302±0.0094  |
| $\pi$ cuts                                   | 888           | 1587          | 0.9900±0.0045      | 0.8287±0.0090      | 0.8371±0.0099  |
| $\pi_{soft}$ cuts                            | 888           | 1587          | 1.0000±0.0021      | 1.0000±0.0012      | 1.0000±0.0024  |
| $D^0$ cuts                                   | 863           | 1454          | 0.9718±0.0067      | 0.9162±0.0075      | 0.943±0.010    |
| $D^*$ cuts                                   | 782           | 1323          | 0.906±0.011        | 0.9099±0.0081      | 1.004±0.015    |
| Total ratio                                  | -             | -             | 0.001555±0.000057  | 0.002544±0.000071  | 1.636±0.076    |

!!! note
    - With run 1 `DaVinci` script plus the run 2 stripping condition, we find
      2016 (run 2 year) ntuple contains ~5x candidates than that of 2012 (run 1
      year). See [released figures in this project](https://github.com/umd-lhcb/RDRDstRun2AnalysisPreservation/releases/latest).
    - The luminosity between 2016 and 2012 are similar. We figured this out with DaVinci and DIRAC.
    - We have a factor of 2 from the cross section. See [this paper](https://arxiv.org/pdf/1612.05140.pdf)
    - This leaves a factor of 2.5. We are expecting ~1.7.
    - Cut flow generated with very similar script and cocktail MC data agrees
      with **the result from real data**.
    - This table uses **full MagDown** run 1 and 2 cocktail MC.
    - **ALL** numbers are number of events, **NOT** number of candidates.

!!! info
    - Run 1 stripping conditions can be found at [`Strippingb2D0MuXB2DMuNuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping21/semileptonic/strippingb2d0muxb2dmunufortaumuline.html)
    - Run 2 stripping conditions can be found at [`Strippingb2D0MuXB2DMuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping28r2/semileptonic/strippingb2d0muxb2dmufortaumuline.html)


## Cutflow table with cocktail MC, bare

| cut name                             | run 1 yield   | run 2 yield   | run 1 efficiency   | run 2 efficiency   | double ratio    |
|--------------------------------------|---------------|---------------|--------------------|--------------------|-----------------|
| Total events                         | 502736        | 520046        | -                  | -                  | -               |
| $D^0 \rightarrow K^- \pi^+$          | 89441         | 94498         | 0.18680±0.00056    | 0.19328±0.00056    | 1.0347±0.0043   |
| $D^{*+} \rightarrow D^0 \pi^+$       | 89277         | 94412         | 0.99817±0.00015    | 0.99909±0.00011    | 1.00093±0.00019 |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$ | 47858         | 51329         | 0.6181±0.0017      | 0.6082±0.0017      | 0.9840±0.0039   |
| L0                                   | 18742         | 16392         | 0.3916±0.0022      | 0.3194±0.0021      | 0.8155±0.0070   |
| Hlt1                                 | 9201          | 16383         | 0.4909±0.0037      | 0.99945±0.00025    | 2.036±0.015     |
| Hlt2                                 | 3761          | 8232          | 0.4088±0.0052      | 0.5025±0.0039      | 1.229±0.018     |
| Stripping (partial)                  | 1303          | 4168          | 0.3465±0.0079      | 0.5063±0.0055      | 1.461±0.037     |
| $\mu$ PID                            | 1229          | 3672          | 0.9432±0.0071      | 0.8810±0.0052      | 0.9340±0.0090   |
| $\text{IsoBDT}_{B^0} < 0.15$         | 921           | 2593          | 0.749±0.013        | 0.7062±0.0077      | 0.942±0.019     |
| $B^0$ cuts                           | 921           | 2516          | 1.0000±0.0020      | 0.9703±0.0037      | 0.9703±0.0042   |
| $K$ cuts                             | 907           | 2050          | 0.9848±0.0052      | 0.8148±0.0080      | 0.8274±0.0092   |
| $\pi$ cuts                           | 901           | 1668          | 0.9934±0.0039      | 0.8137±0.0090      | 0.8191±0.0096   |
| $\pi_{soft}$ cuts                    | 901           | 1668          | 1.0000±0.0020      | 1.0000±0.0011      | 1.0000±0.0023   |
| $D^0$ cuts                           | 870           | 1519          | 0.9656±0.0072      | 0.9107±0.0075      | 0.943±0.010     |
| $D^*$ cuts                           | 803           | 1402          | 0.923±0.010        | 0.9230±0.0074      | 1.000±0.014     |
| Total ratio                          | -             | -             | 0.001597±0.000058  | 0.002696±0.000073  | 1.688±0.077     |

!!! note
    - We removed all kinematic cuts and loosened some vertex quality cuts when generating bare ntuples.
    - This table uses **full MagDown** run 1 and 2 cocktail MC.
    - Additional step 2 cuts are applied here.
    - **ALL** numbers are number of events.


## Cutflow table with real data

| cut name                                     | run 1 yield   | run 2 yield   | run 1 efficiency    | run 2 efficiency      | double ratio        |
|----------------------------------------------|---------------|---------------|---------------------|-----------------------|---------------------|
| Total events                                 | 129986930     | 486980122     | -                   | -                     | -                   |
| Stripped $D^0 \mu^-$                         | 7576232       | 35543709      | 0.058285±0.000020   | 0.072988±0.000012     | 1.25227±0.00048     |
| $D^0 \rightarrow K^- \pi^+$ (tighter $K\pi$) | 7574988       | 35529720      | 0.9998358±0.0000048 | 0.9996064±0.0000033   | 0.9997706±0.0000058 |
| $D^{*+} \rightarrow D^0 \pi^+$               | 1642940       | 7337335       | 0.21689±0.00015     | 0.206513±0.000068     | 0.95215±0.00072     |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$         | 1190313       | 4510320       | 0.72450±0.00035     | 0.61471±0.00018       | 0.84846±0.00048     |
| Refit $\bar{B}^0$ decay tree                 | 1173783       | 4434577       | 0.98611±0.00011     | 0.983207±0.000060     | 0.99705±0.00012     |
| L0                                           | 639358        | 2813588       | 0.54470±0.00046     | 0.63447±0.00023       | 1.1648±0.0011       |
| Hlt1                                         | 510855        | 2813586       | 0.79901±0.00050     | 0.99999929±0.00000093 | 1.25154±0.00078     |
| Hlt2                                         | 372095        | 2813584       | 0.72838±0.00062     | 0.99999929±0.00000093 | 1.3729±0.0012       |
| $\mu$ PID                                    | 350558        | 1796976       | 0.94212±0.00038     | 0.63868±0.00029       | 0.67792±0.00041     |
| $\text{IsoBDT}_{B^0} < 0.15$                 | 244617        | 1215751       | 0.69779±0.00077     | 0.67655±0.00035       | 0.9696±0.0012       |
| $B^0$ cuts                                   | 241038        | 1196904       | 0.98537±0.00025     | 0.98450±0.00011       | 0.99912±0.00027     |
| $K$ cuts                                     | 237327        | 901003        | 0.98460±0.00025     | 0.75278±0.00039       | 0.76455±0.00044     |
| $\pi$ cuts                                   | 234090        | 699341        | 0.98636±0.00024     | 0.77618±0.00044       | 0.78691±0.00048     |
| $\pi_{soft}$ cuts                            | 234090        | 699341        | 1.0000000±0.0000078 | 1.0000000±0.0000026   | 1.0000000±0.0000083 |
| $D^0$ cuts                                   | 220336        | 608678        | 0.94124±0.00049     | 0.87036±0.00040       | 0.92469±0.00064     |
| $D^*$ cuts                                   | 183786        | 504923        | 0.83412±0.00079     | 0.82954±0.00048       | 0.9945±0.0011       |
| Total ratio                                  | -             | -             | 0.0014139±0.0000033 | 0.0010368±0.0000015   | 0.7333±0.0020       |

!!! note
    - This table uses **full MagDown** 2012 and 2016 real data.
    - The main differences between the cut flow ntuples and the plotting
      ntuples are:
      - Cut flow ntuples use **stripping line $\mu$** but plotting ntuples use
        **all available $\mu$**.
      - Cut flow ntuples contain additional Hlt1 cuts.
    - **ALL** numbers are number of events.

!!! warn
    The first few entries are extracted from the DaVinci log, and should not be
    trusted for data cutflow.

    This is because here the _Total events_ are the events passing one of a
    couple of stripping lines, so it's not the actual _total number of events_.

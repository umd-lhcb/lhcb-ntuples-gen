## Generation steps

1. Extract DaVinci-level cut efficiencies with [`davinci_log_parser.py`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/utils/davinci_log_parser.py):
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

2. Run the [`cutflow-run1.py`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/run1-b2D0MuXB2DMuNuForTauMuLine/cutflow/cutflow-run1.py) and [`cutflow-run2.py`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/run2-b2D0MuXB2DMuForTauMuLine/cutflow/cutflow-run2.py).

    !!! note
        The `<output_yaml_filename>` generated in the previous step is used as
        `<input_yaml_filename>` in this step.

        These scripts take the following arguments:
        ```
        cutflow_script <cutflow_ntuple> <input_yaml_filename> <output_yaml_filename>
        ```

        Example usage:
        ```
        ./cut_flow-run2.py ../ntuples/cutflow-Dst/BCands_Dst-yipeng-cutflow_mc-2016-mag_down.root input-run2.yml output-run2.yml
        ```

3. Generate cut flow table with:
    ```
    make cutflow-RDst
    ```
    Please refer to the [`Makefile`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/Makefile) on the implementation details.


## Cutflow table with cocktail MC

| cut name                                     | run 1 yield   | run 2 yield   | run 1 efficiency   | run 2 efficiency   | double ratio   |
|----------------------------------------------|---------------|---------------|--------------------|--------------------|----------------|
| Total events                                 | 502736        | 520046        | -                  | -                  | -              |
| Stripped $D^0 \mu^-$                         | 10422         | 13807         | 0.02073±0.00020    | 0.02655±0.00022    | 1.281±0.016    |
| $D^0 \rightarrow K^- \pi^+$ (tighter $K\pi$) | 10080         | 13397         | 0.9672±0.0018      | 0.9703±0.0015      | 1.0032±0.0025  |
| $D^{*+} \rightarrow D^0 \pi^+$               | 5988          | 7891          | 0.5940±0.0049      | 0.5890±0.0043      | 0.992±0.011    |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$         | 5500          | 6449          | 0.9185±0.0037      | 0.8173±0.0044      | 0.8898±0.0060  |
| Refit $\bar{B}^0$ decay tree                 | 5482          | 6423          | 0.99673±0.00096    | 0.99597±0.00095    | 0.9992±0.0014  |
| L0                                           | 2589          | 3681          | 0.4723±0.0068      | 0.5731±0.0062      | 1.213±0.022    |
| Hlt1                                         | 1884          | 3681          | 0.7277±0.0090      | 1.00000±0.00050    | 1.374±0.017    |
| Hlt2                                         | 1283          | 3681          | 0.681±0.011        | 1.00000±0.00050    | 1.468±0.024    |
| $\mu$ PID                                    | 1212          | 3258          | 0.9447±0.0071      | 0.8851±0.0055      | 0.9369±0.0091  |
| $\text{IsoBDT}_{B^0} < 0.15$                 | 925           | 2384          | 0.763±0.013        | 0.7317±0.0079      | 0.959±0.019    |
| $B^0$ cuts                                   | 925           | 2382          | 1.0000±0.0020      | 0.9992±0.0011      | 0.9992±0.0023  |
| $K$ cuts                                     | 912           | 1946          | 0.9859±0.0050      | 0.8170±0.0082      | 0.8286±0.0093  |
| $\pi$ cuts                                   | 903           | 1607          | 0.9901±0.0045      | 0.8258±0.0090      | 0.8340±0.0098  |
| $D^0$ cuts                                   | 877           | 1083          | 0.9712±0.0067      | 0.674±0.012        | 0.694±0.013    |
| $D^*$ cuts                                   | 785           | 974           | 0.895±0.011        | 0.8994±0.0099      | 1.005±0.017    |
| Total ratio                                  | -             | -             | 0.001561±0.000057  | 0.001873±0.000062  | 1.199±0.059    |

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
| $D^0$ cuts                           | 870           | 1125          | 0.9656±0.0072      | 0.674±0.012        | 0.698±0.013     |
| $D^*$ cuts                           | 803           | 1036          | 0.923±0.010        | 0.9209±0.0088      | 0.998±0.015     |
| Total ratio                          | -             | -             | 0.001597±0.000058  | 0.001992±0.000063  | 1.247±0.060     |

!!! note
    - We removed all kinematic cuts and loosened some vertex quality cuts when generating bare ntuples.
    - This table uses **full MagDown** run 1 and 2 cocktail MC.
    - Additional step 2 cuts are applied here.
    - **ALL** numbers are number of events, **NOT** number of candidates.


## Cutflow table with real data

| cut name                                     | run 1 yield   | run 2 yield   | run 1 efficiency    | run 2 efficiency      | double ratio        |
|----------------------------------------------|---------------|---------------|---------------------|-----------------------|---------------------|
| Total events                                 | 129986930     | 486980122     | -                   | -                     | -                   |
| Stripped $D^0 \mu^-$                         | 7576232       | 35543709      | 0.058285±0.000020   | 0.072988±0.000012     | 1.25227±0.00048     |
| $D^0 \rightarrow K^- \pi^+$ (tighter $K\pi$) | 7574988       | 35529720      | 0.9998358±0.0000048 | 0.9996064±0.0000033   | 0.9997706±0.0000058 |
| $D^{*+} \rightarrow D^0 \pi^+$               | 1642940       | 7337335       | 0.21689±0.00015     | 0.206513±0.000068     | 0.95215±0.00072     |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$         | 1190313       | 4510320       | 0.72450±0.00035     | 0.61471±0.00018       | 0.84846±0.00048     |
| Refit $\bar{B}^0$ decay tree                 | 1173783       | 4434577       | 0.98611±0.00011     | 0.983207±0.000060     | 0.99705±0.00012     |
| L0                                           | 674011        | 3047616       | 0.57422±0.00045     | 0.68724±0.00022       | 1.1968±0.0010       |
| Hlt1                                         | 533012        | 3047614       | 0.79081±0.00049     | 0.99999934±0.00000086 | 1.26453±0.00079     |
| Hlt2                                         | 385887        | 3047610       | 0.72397±0.00061     | 0.9999987±0.0000010   | 1.3813±0.0012       |
| $\mu$ PID                                    | 363598        | 1902951       | 0.94224±0.00038     | 0.62441±0.00028       | 0.66268±0.00039     |
| $\text{IsoBDT}_{B^0} < 0.15$                 | 249209        | 1255079       | 0.68540±0.00077     | 0.65954±0.00034       | 0.9623±0.0012       |
| $B^0$ cuts                                   | 245522        | 1235316       | 0.98521±0.00024     | 0.98425±0.00011       | 0.99903±0.00027     |
| $K$ cuts                                     | 241736        | 926079        | 0.98458±0.00025     | 0.74967±0.00039       | 0.76141±0.00044     |
| $\pi$ cuts                                   | 238433        | 716253        | 0.98634±0.00024     | 0.77343±0.00043       | 0.78414±0.00048     |
| $D^0$ cuts                                   | 224236        | 478165        | 0.94046±0.00049     | 0.66759±0.00055       | 0.70986±0.00069     |
| $D^*$ cuts                                   | 184564        | 387659        | 0.82308±0.00081     | 0.81072±0.00057       | 0.9850±0.0012       |
| Total ratio                                  | -             | -             | 0.0014199±0.0000033 | 0.0007960±0.0000013   | 0.5606±0.0016       |

!!! note
    - This table uses **full MagDown** 2012 and 2016 real data.
    - The main differences between the cut flow ntuples and the plotting
      ntuples are:
      - Cut flow ntuples use **stripping line $\mu$** but plotting ntuples use
        **all available $\mu$**.
      - Cut flow ntuples contain additional Hlt1 cuts.

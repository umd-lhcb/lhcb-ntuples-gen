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

| cut name                                      | run 1 yield   | run 2 yield   | run 1 efficiency   | run 2 efficiency   | double ratio   |
|-----------------------------------------------|---------------|---------------|--------------------|--------------------|----------------|
| Total events                                  | 502736        | 520046        | -                  | -                  | -              |
| Stripped $D^0 \mu^-$                          | 10422         | 13807         | 0.02073±0.00020    | 0.02655±0.00022    | 1.281±0.016    |
| $D^0 \rightarrow K^- \pi^+$ (tighter $K \pi$) | 10080         | 13397         | 0.9672±0.0018      | 0.9703±0.0015      | 1.0032±0.0025  |
| $D^{*+} \rightarrow D^0 \pi^+$                | 5988          | 7891          | 0.5940±0.0049      | 0.5890±0.0043      | 0.992±0.011    |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$          | 5500          | 6449          | 0.9185±0.0037      | 0.8173±0.0044      | 0.8898±0.0060  |
| Refit $\bar{B}^0$ decay tree                  | 5199          | 6136          | 0.9453±0.0032      | 0.9515±0.0028      | 1.0066±0.0045  |
| L0                                            | 2589          | 3681          | 0.4467±0.0066      | 0.5469±0.0061      | 1.224±0.023    |
| Hlt1                                          | 1884          | 3681          | 0.7277±0.0090      | 1.00000±0.00050    | 1.374±0.017    |
| Hlt2                                          | 1283          | 3681          | 0.681±0.011        | 1.00000±0.00050    | 1.468±0.024    |
| $\mu$ PID                                     | 1283          | 3431          | 1.0000±0.0014      | 0.9321±0.0044      | 0.9321±0.0046  |
| $\text{IsoBDT}_{\Upsilon(\text{4s})} < 0.15$  | 979           | 2516          | 0.763±0.012        | 0.7333±0.0077      | 0.961±0.019    |
| $m_{\Upsilon(\text{4s})} < 5280$              | 979           | 2514          | 1.0000±0.0019      | 0.9992±0.0010      | 0.9992±0.0021  |
| Total ratio                                   | -             | -             | 0.001947±0.000064  | 0.004834±0.000098  | 2.482±0.096    |

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

| cut name                                      | run 1 yield   | run 2 yield   | run 1 efficiency   | run 2 efficiency   | double ratio    |
|-----------------------------------------------|---------------|---------------|--------------------|--------------------|-----------------|
| Total events                                  | 502736        | 520046        | -                  | -                  | -               |
| $D^0 \rightarrow K^- \pi^+$ (tighter $K \pi$) | 89441         | 94498         | 0.18680±0.00056    | 0.19328±0.00056    | 1.0347±0.0043   |
| $D^{*+} \rightarrow D^0 \pi^+$                | 89277         | 94412         | 0.99817±0.00015    | 0.99909±0.00011    | 1.00093±0.00019 |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$          | 7780          | 6010          | 0.1005±0.0011      | 0.07122±0.00089    | 0.709±0.012     |
| L0                                            | 99725         | 111916        | 0.4267±0.0010      | 0.33438±0.00081    | 0.7837±0.0027   |
| Hlt1                                          | 42851         | 111806        | 0.4297±0.0016      | 0.99902±0.00010    | 2.3250±0.0085   |
| Hlt2                                          | 17863         | 46599         | 0.4169±0.0024      | 0.4168±0.0015      | 0.9998±0.0067   |
| Stripping                                     | 6144          | 13839         | 0.3440±0.0036      | 0.2970±0.0021      | 0.863±0.011     |
| $\mu$ PID                                     | 6144          | 12964         | 1.00000±0.00030    | 0.9368±0.0021      | 0.9368±0.0021   |
| $\text{IsoBDT}_{\Upsilon(\text{4s})} < 0.15$  | 4355          | 8911          | 0.7088±0.0059      | 0.6874±0.0041      | 0.9697±0.0099   |
| $m_{\Upsilon(\text{4s})} < 5280$              | 4355          | 8903          | 1.00000±0.00042    | 0.99910±0.00044    | 0.99910±0.00061 |
| Total ratio                                   | -             | -             | 0.00866±0.00013    | 0.01712±0.00018    | 1.976±0.037     |


## Cutflow table with real data

| cut name                                     | run 1 yield   | run 2 yield   | run 1 efficiency    | run 2 efficiency      | double ratio        |
|----------------------------------------------|---------------|---------------|---------------------|-----------------------|---------------------|
| Total events                                 | 129986930     | 486980122     | -                   | -                     | -                   |
| Stripped $D^0 \mu^-$                         | 7576232       | 35543709      | 0.058285±0.000020   | 0.072988±0.000012     | 1.25227±0.00048     |
| $D^0 \rightarrow K^- \pi^+$ (tigter $K \pi$) | 7574988       | 35529720      | 0.9998358±0.0000048 | 0.9996064±0.0000033   | 0.9997706±0.0000058 |
| $D^{*+} \rightarrow D^0 \pi^+$               | 1642940       | 7337335       | 0.21689±0.00015     | 0.206513±0.000068     | 0.95215±0.00072     |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$         | 1190313       | 4510320       | 0.72450±0.00035     | 0.61471±0.00018       | 0.84846±0.00048     |
| Refit $\bar{B}^0$ decay tree                 | 1110480       | 4117698       | 0.93293±0.00023     | 0.91295±0.00013       | 0.97858±0.00028     |
| L0                                           | 674011        | 3047616       | 0.54226±0.00044     | 0.63643±0.00022       | 1.1736±0.0010       |
| Hlt1                                         | 533012        | 3047614       | 0.79081±0.00049     | 0.99999934±0.00000086 | 1.26453±0.00079     |
| Hlt2                                         | 385887        | 3047610       | 0.72397±0.00061     | 0.9999987±0.0000010   | 1.3813±0.0012       |
| $\mu$ PID                                    | 385887        | 2019777       | 1.0000000±0.0000047 | 0.66274±0.00027       | 0.66274±0.00027     |
| $\text{IsoBDT}_{\Upsilon(\text{4s})} < 0.15$ | 264931        | 1329826       | 0.68655±0.00074     | 0.65840±0.00033       | 0.9590±0.0011       |
| $m_{\Upsilon(\text{4s})} < 5280$             | 261200        | 1310660       | 0.98592±0.00023     | 0.98559±0.00010       | 0.99967±0.00026     |
| Total ratio                                  | -             | -             | 0.0020094±0.0000039 | 0.0026914±0.0000023   | 1.3394±0.0029       |

!!! note
    - This table uses **full MagDown** 2012 and 2016 real data.
    - The ntuples used to generated the comparison plot have 258438 (2012) and
      1218948 (2016) events.
    - The main differences between the cut flow ntuples and the plotting
      ntuples are:
      - Cut flow ntuples use **stripping line $\mu$** but plotting ntuples use
        **all available $\mu$**.
      - Cut flow ntuples contain additional Hlt1 cuts.

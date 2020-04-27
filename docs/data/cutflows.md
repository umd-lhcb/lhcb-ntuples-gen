## $R(D^{*})$ cut flow comparison between run 1 and 2

### Generation steps

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
        ./davinci_log_parser.py test_output.yml $INPUT_DIR/53/*/output/*.log
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
        ./cut_flow-run2.py ../ntuples/cutflow-Dst/BCands_Dst-yipeng-cutflow_mc-2016-mag_down.root input-run2-data.yml output-run2-data.yml
        ```

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
| Refit $\bar{B}^0$ decay tre                 | 5197          | 6139          | 0.9453±0.0032      | 0.9512±0.0028      | 1.0063±0.0045  |
| L0                                           | 2587          | 3687          | 0.4465±0.0066      | 0.5472±0.0061      | 1.226±0.023    |
| Hlt1                                         | 1882          | 3687          | 0.7275±0.0090      | 1.00000±0.00050    | 1.375±0.017    |
| Hlt2                                         | 1282          | 3687          | 0.681±0.011        | 1.00000±0.00050    | 1.468±0.024    |
| $\mu$ PID                                    | 1282          | 3437          | 1.0000±0.0014      | 0.9322±0.0044      | 0.9322±0.0046  |
| $\text{IsoBDT}_{\Upsilon(\text{4s})} < 0.15$ | 977           | 2517          | 0.762±0.012        | 0.7323±0.0077      | 0.961±0.019    |
| $m_{\Upsilon(\text{4s})} < 5280$             | 977           | 2515          | 1.0000±0.0019      | 0.9992±0.0010      | 0.9992±0.0021  |
| Total ratio                                  | -             | -             | 0.001943±0.000064  | 0.004836±0.000098  | 2.489±0.096    |

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


### Cut flow table with real data

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

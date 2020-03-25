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
| cut name                               | run 1 yield   | run 2 yield   | run 1 efficiency   | run 2 efficiency   | double ratio      |
|----------------------------------------|---------------|---------------|--------------------|--------------------|-------------------|
| Total candidates                       | 35131         | 26633         | -                  | -                  | -                 |
| Stripped $B$                           | 749           | 754           | 0.02132±0.00079    | 0.0283±0.0010      | 1.328±0.070       |
| $D^0 \rightarrow K^- \pi^+$            | 725           | 720           | 0.9680±0.0078      | 0.9549±0.0088      | 0.987±0.012       |
| $D^{*+} \rightarrow D^0 \pi^+$         | 437           | 410           | 0.603±0.019        | 0.569±0.019        | 0.945±0.043       |
| $B^0 \rightarrow D^{*+} \tau^-$        | 410           | 333           | 0.938±0.014        | 0.812±0.021        | 0.866±0.026       |
| Refit $B^0$ decay tree                 | 391           | 321           | 0.954±0.013        | 0.964±0.013        | 1.011±0.019       |
| L0                                     | 39            | 33            | 0.091±0.016        | 0.096±0.019        | 1.06±0.28         |
| Hlt1                                   | 32            | 33            | 0.821±0.083        | 1.000±0.054        | 1.22±0.14         |
| Hlt2                                   | 25            | 33            | 0.781±0.097        | 1.000±0.054        | 1.28±0.17         |
| $\mu$ PID                              | 25            | 31            | 1.000±0.071        | 0.939±0.074        | 0.939±0.099       |
| $\Upsilon(\text{4s})$ isolation cut    | 19            | 24            | 0.76±0.12          | 0.77±0.10          | 1.02±0.20         |
| $m_{\Upsilon(\text{4s})}$ cut          | 19            | 24            | 1.000±0.092        | 1.000±0.074        | 1.00±0.12         |
| Total ratio                            | -             | -             | 0.00054±0.00015    | 0.00090±0.00022    | 1.67±0.63         |


!!! note
    - With run 1 `DaVinci` script plus the run 2 stripping condition, we find
      2016 (run 2 year) ntuple contains ~5x candidates than that of 2012 (run 1
      year). See [released figures in this project](https://github.com/umd-lhcb/RDRDstRun2AnalysisPreservation/releases/latest).
    - The luminosity between 2016 and 2012 are similar. We figured this out with DaVinci and DIRAC.
    - We have a factor of 2 from the cross section. See [this paper](https://arxiv.org/pdf/1612.05140.pdf)
    - This leaves a factor of 2.5. We are expecting ~1.7.
    - Meanwhile, cut flow generated with very similar script and cocktail MC
      data agrees with the expected ~1.7 factor.

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
| cut name             | run 1 yield   | run 2 yield   | run 1 efficiency    | run 2 efficiency    | double ratio        |
|----------------------|---------------|---------------|---------------------|---------------------|---------------------|
| Total events         | 35131         | 26633         | 1.0000000±0.0000522 | 1.0000000±0.0000688 | 1.0000000±0.0000863 |
| `StrippedBCands`     | 749           | 754           | 0.021320±0.000794   | 0.02831±0.00105     | 1.3279±0.0697       |
| `SelMyD0`            | 725           | 720           | 0.96796±0.00777     | 0.95491±0.00884     | 0.9865±0.0121       |
| `SelMyDst`           | 437           | 410           | 0.6028±0.0189       | 0.5694±0.0191       | 0.9447±0.0434       |
| `SelMyB0`            | 410           | 333           | 0.9382±0.0137       | 0.8122±0.0212       | 0.8657±0.0259       |
| `SelMyRefitB02DstMu` | 391           | 321           | 0.9537±0.0128       | 0.9640±0.0133       | 1.0108±0.0194       |
| Step 2 cuts          | 328           | 238           | 0.7646±0.0222       | 0.6959±0.0268       | 0.9102±0.0438       |
| L0                   | 29            | 24            | 0.0884±0.0185       | 0.1008±0.0233       | 1.141±0.356         |
| Hlt1                 | 24            | 24            | 0.8276±0.0993       | 1.0000±0.0735       | 1.208±0.170         |
| Hlt2                 | 19            | 24            | 0.792±0.116         | 1.0000±0.0735       | 1.263±0.207         |
| Total ratio          | -             | -             | 0.000541±0.000154   | 0.000901±0.000223   | 1.666±0.628         |

!!! note
    - With run 1 `DaVinci` script plus the run 2 stripping condition, we find
      2016 (run 2 year) ntuple contains ~5x candidates than that of 2012 (run 1
      year). See [released figures in this project](https://github.com/umd-lhcb/RDRDstRun2AnalysisPreservation/releases/latest).
    - The luminosity between 2016 and 2012 are similar. We figured this out with DaVinci and DIRAC.
    - We have a factor of 2 from the cross section. See [this paper](https://arxiv.org/pdf/1612.05140.pdf)
    - This leaves a factor of 2.5. We are expecting ~1.7.
    - Meanwhile, cut flow generated with very similar script and cocktail MC
      data agrees with the expected ~1.7 factor.

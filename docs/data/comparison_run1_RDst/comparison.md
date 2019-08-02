In general, we find the unique events [^1] in both ntuples, then see if they
occur in both ntuples, and find their:

1. absolute difference
2. normalized difference, with one of them used as normalization


[^1]: Typically by the combination of `runNumber` and `eventNumber`.


## Comparison between `BCands_Dst-data-2012-mag_down-stage2` and `BCands_Dst-data-2012-mag_down-davinci_v42r8p1-subset`

* Phoebe used [this DaVinci script](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/0.1/2012-b2D0MuXB2DMuNuForTauMuLine/ntuple_options-sample.py)
  to generate her ntuple, with `DaVinci v36r1p2`. The generated ntuple can be
  found at:
    ```
    <project_root>/2012-b2D0MuXB2DMuNuForTauMuLine/data/sample/YCands_Dstar-2012-mag_down-data.root
    ```

* We used [our script](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/2012-b2D0MuXB2DMuNuForTauMuLine/ntuple_options.py)[^2], and
  `DaVinci v42r8p1`. The ntuple can be found at:

    ```
    <project_root>/2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root
    ```


[^2]: Based on Phoebe's original script.

### `D0_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/D0_P_diff.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/D0_P_diff_norm.png) |

### `Dst_2010_minus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Dst_2010_minus_P_diff.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Dst_2010_minus_P_diff_norm.png) |

### `Kplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Kplus_P_diff.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Kplus_P_diff_norm.png) |

### `Kplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Kplus_PX_diff.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Kplus_PX_diff_norm.png) |

### `Kplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Kplus_PY_diff.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Kplus_PY_diff_norm.png) |

### `Kplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Kplus_PZ_diff.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Kplus_PZ_diff_norm.png) |

### `muplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/muplus_P_diff.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/muplus_P_diff_norm.png) |

### `muplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/muplus_PX_diff.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/muplus_PX_diff_norm.png) |

### `muplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/muplus_PY_diff.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/muplus_PY_diff_norm.png) |

### `muplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/muplus_PZ_diff.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/muplus_PZ_diff_norm.png) |

### `FitVar_Mmiss2`
| difference [?] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/FitVar_Mmiss2_diff_manuel_phoebe.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/FitVar_Mmiss2_diff_norm_manuel_phoebe.png) |

### `FitVar_q2`
| difference [?] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/FitVar_q2_diff_manuel_phoebe.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/FitVar_q2_diff_norm_manuel_phoebe.png) |

### `FitVar_El`
| difference [?] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/FitVar_El_diff_manuel_phoebe.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/FitVar_El_diff_norm_manuel_phoebe.png) |

### `Y_ISOLATION_BDT`
| difference [?] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Y_ISOLATION_BDT_diff_manuel_phoebe.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Y_ISOLATION_BDT_diff_norm_manuel_phoebe.png) |

### `Y_ISOLATION_BDT2`
| difference [?] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Y_ISOLATION_BDT2_diff_manuel_phoebe.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Y_ISOLATION_BDT2_diff_norm_manuel_phoebe.png) |

### `Y_ISOLATION_BDT3`
| difference [?] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Y_ISOLATION_BDT3_diff_manuel_phoebe.png) | ![](data-2012-mag_down-stage2_vs_data-2012-mag_down-davinci_v42r8p1-subset/Y_ISOLATION_BDT3_diff_norm_manuel_phoebe.png) |

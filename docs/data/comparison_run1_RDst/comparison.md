In general, we find the unique events [^1] in both ntuples, then see if they
occur in both ntuples, and find their:

1. absolute difference
2. normalized difference, with one of them used as normalization


[^1]: Typically by the combination of `runNumber` and `eventNumber`.


## Comparison between 2012 data
The files being compared are:

* `BCands_Dst-phoebe-data-2012-mag_down-step2.root`
* `BCands_Dst-yipeng-data-2012-mag_down-davinci_v42r8p1-subset.root`


!!! note
    * Phoebe used [this DaVinci script](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/0.1/2012-b2D0MuXB2DMuNuForTauMuLine/ntuple_options-sample.py)
      to generate her ntuple, with `DaVinci v36r1p2`.

    * We used [our script](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/0.3/2012-b2D0MuXB2DMuNuForTauMuLine/ntuple_options.py)[^2], and
      `DaVinci v42r8p1`.


[^2]: Based on Phoebe's original script.

### `D0_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/D0_P_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/D0_P_diff_norm.png) |

### `Dst_2010_minus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/Dst_2010_minus_P_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/Dst_2010_minus_P_diff_norm.png) |

### `Kplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/Kplus_P_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/Kplus_P_diff_norm.png) |

### `Kplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/Kplus_PX_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/Kplus_PX_diff_norm.png) |

### `Kplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/Kplus_PY_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/Kplus_PY_diff_norm.png) |

### `Kplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/Kplus_PZ_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/Kplus_PZ_diff_norm.png) |

### `muplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/muplus_P_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/muplus_P_diff_norm.png) |

### `muplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/muplus_PX_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/muplus_PX_diff_norm.png) |

### `muplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/muplus_PY_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/muplus_PY_diff_norm.png) |

### `muplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/muplus_PZ_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/muplus_PZ_diff_norm.png) |

### `FitVar_Mmiss2`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/FitVar_Mmiss2_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/FitVar_Mmiss2_diff_norm.png) |

### `FitVar_q2`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/FitVar_q2_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/FitVar_q2_diff_norm.png) |

### `FitVar_El`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/FitVar_El_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/FitVar_El_diff_norm.png) |

### `Y_ISOLATION_BDT`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/Y_ISOLATION_BDT_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/Y_ISOLATION_BDT_diff_norm.png) |

### `Y_ISOLATION_BDT2`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/Y_ISOLATION_BDT2_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/Y_ISOLATION_BDT2_diff_norm.png) |

### `Y_ISOLATION_BDT3`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-phoebe_vs_yipeng/Y_ISOLATION_BDT3_diff.png) | ![](data-2012-mag_down-phoebe_vs_yipeng/Y_ISOLATION_BDT3_diff_norm.png) |


## Comparison between `DaVinci` version
Files used:

* `BCands_Dst-phoebe-data-2012-mag_down-davinci_v36r1p2-subset.root`
* `BCands_Dst-yipeng-data-2012-mag_down-davinci_v42r8p1-subset.root`

### `D0_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/D0_P_diff.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/D0_P_diff_norm.png) |

### `Dst_2010_minus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Dst_2010_minus_P_diff.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Dst_2010_minus_P_diff_norm.png) |

### `Kplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Kplus_P_diff.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Kplus_P_diff_norm.png) |

### `Kplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Kplus_PX_diff.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Kplus_PX_diff_norm.png) |

### `Kplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Kplus_PY_diff.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Kplus_PY_diff_norm.png) |

### `Kplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Kplus_PZ_diff.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Kplus_PZ_diff_norm.png) |

### `muplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/muplus_P_diff.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/muplus_P_diff_norm.png) |

### `muplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/muplus_PX_diff.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/muplus_PX_diff_norm.png) |

### `muplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/muplus_PY_diff.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/muplus_PY_diff_norm.png) |

### `muplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/muplus_PZ_diff.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/muplus_PZ_diff_norm.png) |

### `Y_ISOLATION_BDT`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_BDT_diff.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_BDT_diff_norm.png) |

### `Y_ISOLATION_BDT2`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_BDT2_diff.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_BDT2_diff_norm.png) |

### `Y_ISOLATION_BDT3`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_BDT3_diff.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_BDT3_diff_norm.png) |

### `Y_ISOLATION_Type`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_Type_dv36r1p2.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_Type_dv42r8p1.png) |

### `Y_ISOLATION_Type2`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_Type2_dv36r1p2.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_Type2_dv42r8p1.png) |

### `Y_ISOLATION_Type3`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_Type3_dv36r1p2.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_Type3_dv42r8p1.png) |

### `Y_ISOLATION_Type4`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_Type4_dv36r1p2.png) | ![](data-2012-mag_down-dv36r1p2_vs_dv42r8p1/Y_ISOLATION_Type4_dv42r8p1.png) |


## Comparison between MC (Pythia 6)
Files used:

* `BCands_Dst-phoebe-mc-mag_down-py6-step2.root`
* `BCands_Dst-yipeng-mc-mag_down-py6-sim08a-subset.root`

### `D0_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](mc-py6-mag_down-phoebe_vs_yipeng/D0_P_diff.png) | ![](mc-py6-mag_down-phoebe_vs_yipeng/D0_P_diff_norm.png) |

### `Kplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](mc-py6-mag_down-phoebe_vs_yipeng/Kplus_P_diff.png) | ![](mc-py6-mag_down-phoebe_vs_yipeng/Kplus_P_diff_norm.png) |

### `FitVar_Mmiss2`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](mc-py6-mag_down-phoebe_vs_yipeng/FitVar_Mmiss2_diff.png) | ![](mc-py6-mag_down-phoebe_vs_yipeng/FitVar_Mmiss2_diff_norm.png) |

### `FitVar_q2`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](mc-py6-mag_down-phoebe_vs_yipeng/FitVar_q2_diff.png) | ![](mc-py6-mag_down-phoebe_vs_yipeng/FitVar_q2_diff_norm.png) |

### `FitVar_El`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](mc-py6-mag_down-phoebe_vs_yipeng/FitVar_El_diff.png) | ![](mc-py6-mag_down-phoebe_vs_yipeng/FitVar_El_diff_norm.png) |

### `Y_ISOLATION_BDT`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](mc-py6-mag_down-phoebe_vs_yipeng/Y_ISOLATION_BDT_diff.png) | ![](mc-py6-mag_down-phoebe_vs_yipeng/Y_ISOLATION_BDT_diff_norm.png) |

### `Y_ISOLATION_BDT2`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](mc-py6-mag_down-phoebe_vs_yipeng/Y_ISOLATION_BDT2_diff.png) | ![](mc-py6-mag_down-phoebe_vs_yipeng/Y_ISOLATION_BDT2_diff_norm.png) |

### `Y_ISOLATION_BDT3`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](mc-py6-mag_down-phoebe_vs_yipeng/Y_ISOLATION_BDT3_diff.png) | ![](mc-py6-mag_down-phoebe_vs_yipeng/Y_ISOLATION_BDT3_diff_norm.png) |

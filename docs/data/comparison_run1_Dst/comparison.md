In general, we find the unique events [^1] in both ntuples, then see if they
occur in both ntuples, and find their:

1. absolute difference
2. normalized difference, with one of them used as normalization

Unless specified, all ntuples are located in `run1-b2D0MuXB2DMuNuForTauMuLine/samples`.


[^1]: Typically by the combination of `runNumber` and `eventNumber`.


## Comparison between data
The files being compared are, located in `run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst`:

* `BCands_Dst-phoebe-data-2012-mag_down.root`
* `BCands_Dst-yipeng-data-2012-mag_down.root`

!!! note
    * Phoebe used [this DaVinci script](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/0.1/2012-b2D0MuXB2DMuNuForTauMuLine/ntuple_options-sample.py)
      to generate her ntuple, with `DaVinci v36r1p2`.

    * We used [our script](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/0.3/2012-b2D0MuXB2DMuNuForTauMuLine/ntuple_options.py)[^2], and
      `DaVinci v42r8p1`.


[^2]: Based on Phoebe's original script.

### `D0_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/D0_P_diff.png) | ![](data-phoebe_vs_yipeng/D0_P_diff_norm.png) |

### `Dst_2010_minus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Dst_2010_minus_P_diff.png) | ![](data-phoebe_vs_yipeng/Dst_2010_minus_P_diff_norm.png) |

### `Kplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Kplus_P_diff.png) | ![](data-phoebe_vs_yipeng/Kplus_P_diff_norm.png) |

### `Kplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Kplus_PX_diff.png) | ![](data-phoebe_vs_yipeng/Kplus_PX_diff_norm.png) |

### `Kplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Kplus_PY_diff.png) | ![](data-phoebe_vs_yipeng/Kplus_PY_diff_norm.png) |

### `Kplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Kplus_PZ_diff.png) | ![](data-phoebe_vs_yipeng/Kplus_PZ_diff_norm.png) |

### `muplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/muplus_P_diff.png) | ![](data-phoebe_vs_yipeng/muplus_P_diff_norm.png) |

### `muplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/muplus_PX_diff.png) | ![](data-phoebe_vs_yipeng/muplus_PX_diff_norm.png) |

### `muplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/muplus_PY_diff.png) | ![](data-phoebe_vs_yipeng/muplus_PY_diff_norm.png) |

### `muplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/muplus_PZ_diff.png) | ![](data-phoebe_vs_yipeng/muplus_PZ_diff_norm.png) |

### `Y_ISOLATION_BDT`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Y_ISOLATION_BDT_diff.png) | ![](data-phoebe_vs_yipeng/Y_ISOLATION_BDT_diff_norm.png) |

### `Y_ISOLATION_BDT2`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Y_ISOLATION_BDT2_diff.png) | ![](data-phoebe_vs_yipeng/Y_ISOLATION_BDT2_diff_norm.png) |

### `Y_ISOLATION_BDT3`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Y_ISOLATION_BDT3_diff.png) | ![](data-phoebe_vs_yipeng/Y_ISOLATION_BDT3_diff_norm.png) |

### `Y_ENDVERTEX_X`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_X_diff.png) | ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_X_diff_norm.png) |

### `Y_ENDVERTEX_Y`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_Y_diff.png) | ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_Y_diff_norm.png) |

### `Y_ENDVERTEX_Z`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_Z_diff.png) | ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_Z_diff_norm.png) |


## Comparison between `DaVinci` `v36r1p2` and `v42r8p1`
Files used:

* `BCands_Dst-phoebe-data-dv36-subset.root`
* `BCands_Dst-yipeng-data-dv42-subset.root`

### `D0_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/D0_P_diff.png) | ![](data-dv36_vs_dv42/D0_P_diff_norm.png) |

### `Dst_2010_minus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/Dst_2010_minus_P_diff.png) | ![](data-dv36_vs_dv42/Dst_2010_minus_P_diff_norm.png) |

### `Kplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/Kplus_P_diff.png) | ![](data-dv36_vs_dv42/Kplus_P_diff_norm.png) |

### `Kplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/Kplus_PX_diff.png) | ![](data-dv36_vs_dv42/Kplus_PX_diff_norm.png) |

### `Kplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/Kplus_PY_diff.png) | ![](data-dv36_vs_dv42/Kplus_PY_diff_norm.png) |

### `Kplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/Kplus_PZ_diff.png) | ![](data-dv36_vs_dv42/Kplus_PZ_diff_norm.png) |

### `muplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/muplus_P_diff.png) | ![](data-dv36_vs_dv42/muplus_P_diff_norm.png) |

### `muplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/muplus_PX_diff.png) | ![](data-dv36_vs_dv42/muplus_PX_diff_norm.png) |

### `muplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/muplus_PY_diff.png) | ![](data-dv36_vs_dv42/muplus_PY_diff_norm.png) |

### `muplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/muplus_PZ_diff.png) | ![](data-dv36_vs_dv42/muplus_PZ_diff_norm.png) |

### `Y_ISOLATION_BDT`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/Y_ISOLATION_BDT_diff.png) | ![](data-dv36_vs_dv42/Y_ISOLATION_BDT_diff_norm.png) |

### `Y_ISOLATION_BDT2`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/Y_ISOLATION_BDT2_diff.png) | ![](data-dv36_vs_dv42/Y_ISOLATION_BDT2_diff_norm.png) |

### `Y_ISOLATION_BDT3`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/Y_ISOLATION_BDT3_diff.png) | ![](data-dv36_vs_dv42/Y_ISOLATION_BDT3_diff_norm.png) |

### `Y_ISOLATION_Type`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42/Y_ISOLATION_Type_dv36.png) | ![](data-dv36_vs_dv42/Y_ISOLATION_Type_dv42.png) |

### `Y_ISOLATION_Type2`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42/Y_ISOLATION_Type2_dv36.png) | ![](data-dv36_vs_dv42/Y_ISOLATION_Type2_dv42.png) |

### `Y_ISOLATION_Type3`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42/Y_ISOLATION_Type3_dv36.png) | ![](data-dv36_vs_dv42/Y_ISOLATION_Type3_dv42.png) |

### `Y_ISOLATION_Type4`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42/Y_ISOLATION_Type4_dv36.png) | ![](data-dv36_vs_dv42/Y_ISOLATION_Type4_dv42.png) |


## Comparison between `DaVinci` `v36r1p2` and `v42r8p1`, without VELO pions
Files used:

* `BCands_Dst-phoebe-data-dv36-subset-no_velo_pions.root`
* `BCands_Dst-yipeng-data-dv42-subset-no_velo_pions.root`

### `Y_ISOLATION_Type`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type_dv36-no_velo_pions.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type_dv42-no_velo_pions.png) |

### `Y_ISOLATION_Type2`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type2_dv36-no_velo_pions.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type2_dv42-no_velo_pions.png) |

### `Y_ISOLATION_Type3`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type3_dv36-no_velo_pions.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type3_dv42-no_velo_pions.png) |

### `Y_ISOLATION_Type4`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type4_dv36-no_velo_pions.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type4_dv42-no_velo_pions.png) |


## Comparison between `DaVinci` `v36r1p2` and `v42r8p1`, without refitting
Files used:

* `BCands_Dst-phoebe-data-2012-mag_down-dv36-subset-no_refit.root`
* `BCands_Dst-yipeng-data-2012-mag_down-dv42-subset-no_refit.root`

### `D0_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/D0_P_diff.png) | ![](data-dv36_vs_dv42-no_refit/D0_P_diff_norm.png) |

### `Dst_2010_minus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Dst_2010_minus_P_diff.png) | ![](data-dv36_vs_dv42-no_refit/Dst_2010_minus_P_diff_norm.png) |

### `Kplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Kplus_P_diff.png) | ![](data-dv36_vs_dv42-no_refit/Kplus_P_diff_norm.png) |

### `Kplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Kplus_PX_diff.png) | ![](data-dv36_vs_dv42-no_refit/Kplus_PX_diff_norm.png) |

### `Kplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Kplus_PY_diff.png) | ![](data-dv36_vs_dv42-no_refit/Kplus_PY_diff_norm.png) |

### `Kplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Kplus_PZ_diff.png) | ![](data-dv36_vs_dv42-no_refit/Kplus_PZ_diff_norm.png) |

### `muplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/muplus_P_diff.png) | ![](data-dv36_vs_dv42-no_refit/muplus_P_diff_norm.png) |

### `muplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/muplus_PX_diff.png) | ![](data-dv36_vs_dv42-no_refit/muplus_PX_diff_norm.png) |

### `muplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/muplus_PY_diff.png) | ![](data-dv36_vs_dv42-no_refit/muplus_PY_diff_norm.png) |

### `muplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/muplus_PZ_diff.png) | ![](data-dv36_vs_dv42-no_refit/muplus_PZ_diff_norm.png) |

### `Y_ISOLATION_BDT`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_BDT_diff.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_BDT_diff_norm.png) |

### `Y_ISOLATION_BDT2`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_BDT2_diff.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_BDT2_diff_norm.png) |

### `Y_ISOLATION_BDT3`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_BDT3_diff.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_BDT3_diff_norm.png) |

### `Y_ISOLATION_Type`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type_dv36-no_refit.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type_dv42-no_refit.png) |

### `Y_ISOLATION_Type2`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type2_dv36-no_refit.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type2_dv42-no_refit.png) |

### `Y_ISOLATION_Type3`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type3_dv36-no_refit.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type3_dv42-no_refit.png) |

### `Y_ISOLATION_Type4`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type4_dv36-no_refit.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type4_dv42-no_refit.png) |

### `ISOLATION_TRACK1`

!!! note
    The version should be interpreted in this way: `v36r1p2` means matching
    `v36` tracks with `v42` tracks as references.

    Also, for track $i$, if the match is 100%, then all datapoints should be at
    $i$.

    Track 0 indicates no match at all.

| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/ISOLATION_TRACK1_dv36.png) | ![](data-dv36_vs_dv42-no_refit/ISOLATION_TRACK1_dv42.png) |

### `ISOLATION_TRACK2`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/ISOLATION_TRACK2_dv36.png) | ![](data-dv36_vs_dv42-no_refit/ISOLATION_TRACK2_dv42.png) |

### `ISOLATION_TRACK3`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/ISOLATION_TRACK3_dv36.png) | ![](data-dv36_vs_dv42-no_refit/ISOLATION_TRACK3_dv42.png) |


## Comparison between MC (Pythia 6)
Files used, located in `run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/mc`:

* `BCands-phoebe-mc-mag_down-py6-Bd2DstTauNu.root`
* `BCands-yipeng-mc-mag_down-py6-sim08a-Bd2DstTauNu.root`

### `D0_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](mc-py6-phoebe_vs_yipeng/D0_P_diff.png) | ![](mc-py6-phoebe_vs_yipeng/D0_P_diff_norm.png) |

### `Kplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](mc-py6-phoebe_vs_yipeng/Kplus_P_diff.png) | ![](mc-py6-phoebe_vs_yipeng/Kplus_P_diff_norm.png) |

### `Y_ISOLATION_BDT`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](mc-py6-phoebe_vs_yipeng/Y_ISOLATION_BDT_diff.png) | ![](mc-py6-phoebe_vs_yipeng/Y_ISOLATION_BDT_diff_norm.png) |

### `Y_ISOLATION_BDT2`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](mc-py6-phoebe_vs_yipeng/Y_ISOLATION_BDT2_diff.png) | ![](mc-py6-phoebe_vs_yipeng/Y_ISOLATION_BDT2_diff_norm.png) |

### `Y_ISOLATION_BDT3`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](mc-py6-phoebe_vs_yipeng/Y_ISOLATION_BDT3_diff.png) | ![](mc-py6-phoebe_vs_yipeng/Y_ISOLATION_BDT3_diff_norm.png) |

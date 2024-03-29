# $R(D^*)$ variables, run 1

In general, we find the unique events [^1] in both ntuples, then see if they
occur in both ntuples, and find their:

1. absolute difference
2. normalized difference, with one of them used as normalization


[^1]: Typically by the combination of `runNumber` and `eventNumber`.


## Comparison between data
The files being compared are, located in `ntuples/run1-Dst`:

* `ntuples/ref-rdx-run1/Dst-std/Dst--19_09_05--std--data--2012--md--phoebe.root` (Phoebe)
* `ntuples/pre-0.9.0/Dst-std/Dst--19_09_05--std--data--2012--md.root` (Yipeng)

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
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Y_ISOLATION_BDT_diff.png) | ![](data-phoebe_vs_yipeng/Y_ISOLATION_BDT_diff_norm.png) |

### `Y_ISOLATION_BDT2`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Y_ISOLATION_BDT2_diff.png) | ![](data-phoebe_vs_yipeng/Y_ISOLATION_BDT2_diff_norm.png) |

### `Y_ISOLATION_BDT3`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-phoebe_vs_yipeng/Y_ISOLATION_BDT3_diff.png) | ![](data-phoebe_vs_yipeng/Y_ISOLATION_BDT3_diff_norm.png) |

### `Y_ENDVERTEX_X`
| difference [mm] | difference (normalized) | distributions [mm] |
|---|---|---|
| ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_X_diff.png) | ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_X_diff_norm.png) | ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_X_dist.png) |

### `Y_ENDVERTEX_Y`
| difference [mm] | difference (normalized) | distributions [mm] |
|---|---|---|
| ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_Y_diff.png) | ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_Y_diff_norm.png) | ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_Y_dist.png) |

### `Y_ENDVERTEX_Z`
| difference [mm] | difference (normalized) | distributions [mm] |
|---|---|---|
| ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_Z_diff.png) | ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_Z_diff_norm.png) | ![](data-phoebe_vs_yipeng/Y_ENDVERTEX_Z_dist.png) |

### `Y_OWNPV_X`
| difference [mm] | difference (normalized) | distributions [mm] |
|---|---|---|
| ![](data-phoebe_vs_yipeng/Y_OWNPV_X_diff.png) | ![](data-phoebe_vs_yipeng/Y_OWNPV_X_diff_norm.png) | ![](data-phoebe_vs_yipeng/Y_OWNPV_X_dist.png) |

### `Y_OWNPV_Y`
| difference [mm] | difference (normalized) | distributions [mm] |
|---|---|---|
| ![](data-phoebe_vs_yipeng/Y_OWNPV_Y_diff.png) | ![](data-phoebe_vs_yipeng/Y_OWNPV_Y_diff_norm.png) | ![](data-phoebe_vs_yipeng/Y_OWNPV_Y_dist.png) |

### `Y_OWNPV_Z`
| difference [mm] | difference (normalized) | distributions [mm] |
|---|---|---|
| ![](data-phoebe_vs_yipeng/Y_OWNPV_Z_diff.png) | ![](data-phoebe_vs_yipeng/Y_OWNPV_Z_diff_norm.png) | ![](data-phoebe_vs_yipeng/Y_OWNPV_Z_dist.png) |


## Comparison between `DaVinci` `v36r1p2` and `v42r8p1`
Files used:

* `run1-rdx/samples/Dst--19_07_12--std--data--2012--md--dv36-subset.root`
* `run1-rdx/samples/Dst--19_07_12--std--data--2012--md--dv42-subset.root`

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
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/Y_ISOLATION_BDT_diff.png) | ![](data-dv36_vs_dv42/Y_ISOLATION_BDT_diff_norm.png) |

### `Y_ISOLATION_BDT2`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42/Y_ISOLATION_BDT2_diff.png) | ![](data-dv36_vs_dv42/Y_ISOLATION_BDT2_diff_norm.png) |

### `Y_ISOLATION_BDT3`
| difference (DL) | difference (normalized) |
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

* `run1-rdx/samples/Dst--19_09_11--std--data--2012--md--dv36-subset-no_velo_pions.root`
* `run1-rdx/samples/Dst--19_09_11--std--data--2012--md--dv42-subset-no_velo_pions.root`

### `Y_ISOLATION_BDT`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_BDT_diff.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_BDT_diff_norm.png) |

### `Y_ISOLATION_BDT2`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_BDT2_diff.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_BDT2_diff_norm.png) |

### `Y_ISOLATION_BDT3`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_BDT3_diff.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_BDT3_diff_norm.png) |

### `Y_ISOLATION_Type`
#### Raw
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type_dv36.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type_dv42.png) |

#### Matched diff

!!! note
    These are the difference in track _type_ for momentum-matched tracks in
    events matched by the `event` and `run` numbers.  The momentum matching is
    performed for each track $i = 1,2,3$ in release r=`v36`, `v42` by finding a
    track in the opposite release for any index $1$, $2$, or $3$ whose
    difference in every 4-momentum component is smaller than 10 eV.

    The version should be interpreted in this way: `v36r1p2` means `v42` track
    type is used as a reference, and the difference is calculated with:
    $TrackType_{v42} - TrackType_{v36}$.

| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type_matched_diff_dv36.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type_matched_diff_dv42.png) |

### `Y_ISOLATION_Type2`
#### Raw
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type2_dv36.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type2_dv42.png) |

#### Matched diff
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type2_matched_diff_dv36.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type2_matched_diff_dv42.png) |

### `Y_ISOLATION_Type3`
#### Raw
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type3_dv36.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type3_dv42.png) |

#### Matched diff
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type3_matched_diff_dv36.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type3_matched_diff_dv42.png) |

### `Y_ISOLATION_Type4`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type4_dv36.png) | ![](data-dv36_vs_dv42-no_velo_pions/Y_ISOLATION_Type4_dv42.png) |

### `ISOLATION_TRACK1`

!!! note
    `ISOLATION_TRACK{1,2,3}` represent the best 3 tracks selected by the BDT.
    A value of $1$ represents `ISOLATION_TRACK1`. $2$ and $3$ are interpreted
    in the same way.
    A value of $0$ indicates no match at all.
    A value of $-2$ indicates no actual track exists, and is only assigned
    when the BDT score is $-2$.

    The version should be interpreted in this way: `v36r1p2` means matching a
    `v36` track with all 3 `v42` tracks with the same UID. The `v42` tracks act
    as references.

    Also, for track $i$, if the match is 100%, then all datapoints should be at
    $i$.

| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/ISOLATION_TRACK1_dv36.png) | ![](data-dv36_vs_dv42-no_velo_pions/ISOLATION_TRACK1_dv42.png) |

### `ISOLATION_TRACK2`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/ISOLATION_TRACK2_dv36.png) | ![](data-dv36_vs_dv42-no_velo_pions/ISOLATION_TRACK2_dv42.png) |

### `ISOLATION_TRACK3`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_velo_pions/ISOLATION_TRACK3_dv36.png) | ![](data-dv36_vs_dv42-no_velo_pions/ISOLATION_TRACK3_dv42.png) |


## Comparison between `DaVinci` `v36r1p2` and `v42r8p1`, without refitting
Files used:

* `run1-rdx/samples/Dst--19_10_04--std--data--2012--md--dv36-subset-no_refit.root`
* `run1-rdx/samples/Dst--19_09_26--std--data--2012--md--dv42-subset-no_refit.root`

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
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_BDT_diff.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_BDT_diff_norm.png) |

### `Y_ISOLATION_BDT2`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_BDT2_diff.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_BDT2_diff_norm.png) |

### `Y_ISOLATION_BDT3`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_BDT3_diff.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_BDT3_diff_norm.png) |

### `Y_ISOLATION_Type`
#### Raw
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type_dv36.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type_dv42.png) |

#### Matched diff
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type_matched_diff_dv36.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type_matched_diff_dv42.png) |

### `Y_ISOLATION_Type2`
#### Raw
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type2_dv36.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type2_dv42.png) |

#### Matched diff
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type2_matched_diff_dv36.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type2_matched_diff_dv42.png) |

### `Y_ISOLATION_Type3`
#### Raw
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type3_dv36.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type3_dv42.png) |

#### Matched diff
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type3_matched_diff_dv36.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type3_matched_diff_dv42.png) |

### `Y_ISOLATION_Type4`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type4_dv36.png) | ![](data-dv36_vs_dv42-no_refit/Y_ISOLATION_Type4_dv42.png) |

### `ISOLATION_TRACK1`
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

### `TRACK_TYPE1_CHI2`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/TRACK_TYPE1_CHI2_dv36.png) | ![](data-dv36_vs_dv42-no_refit/TRACK_TYPE1_CHI2_dv42.png) |

### `TRACK_TYPE3_CHI2`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/TRACK_TYPE3_CHI2_dv36.png) | ![](data-dv36_vs_dv42-no_refit/TRACK_TYPE3_CHI2_dv42.png) |

### `TRACK_TYPE4_CHI2`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/TRACK_TYPE4_CHI2_dv36.png) | ![](data-dv36_vs_dv42-no_refit/TRACK_TYPE4_CHI2_dv42.png) |

### Track type difference vs. BDT score difference
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit/ISOLATION_TRACK_vs_BDT_dv36.png) | ![](data-dv36_vs_dv42-no_refit/ISOLATION_TRACK_vs_BDT_dv42.png) |


## Comparison between `DaVinci` `v36r1p2` and `v45r3`, without refitting
Files used:

* `run1-rdx/samples/Dst--19_10_04--std--data--2012--md--dv36-subset-no_refit.root`
* `run1-rdx/samples/Dst--19_11_14--std--data--2012--md--dv45-subset-no_refit.root`

### `D0_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/D0_P_diff.png) | ![](data-dv36_vs_dv45-no_refit/D0_P_diff_norm.png) |

### `Dst_2010_minus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Dst_2010_minus_P_diff.png) | ![](data-dv36_vs_dv45-no_refit/Dst_2010_minus_P_diff_norm.png) |

### `Kplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Kplus_P_diff.png) | ![](data-dv36_vs_dv45-no_refit/Kplus_P_diff_norm.png) |

### `Kplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Kplus_PX_diff.png) | ![](data-dv36_vs_dv45-no_refit/Kplus_PX_diff_norm.png) |

### `Kplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Kplus_PY_diff.png) | ![](data-dv36_vs_dv45-no_refit/Kplus_PY_diff_norm.png) |

### `Kplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Kplus_PZ_diff.png) | ![](data-dv36_vs_dv45-no_refit/Kplus_PZ_diff_norm.png) |

### `muplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/muplus_P_diff.png) | ![](data-dv36_vs_dv45-no_refit/muplus_P_diff_norm.png) |

### `muplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/muplus_PX_diff.png) | ![](data-dv36_vs_dv45-no_refit/muplus_PX_diff_norm.png) |

### `muplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/muplus_PY_diff.png) | ![](data-dv36_vs_dv45-no_refit/muplus_PY_diff_norm.png) |

### `muplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/muplus_PZ_diff.png) | ![](data-dv36_vs_dv45-no_refit/muplus_PZ_diff_norm.png) |

### `Y_ISOLATION_BDT`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_BDT_diff.png) | ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_BDT_diff_norm.png) |

### `Y_ISOLATION_BDT2`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_BDT2_diff.png) | ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_BDT2_diff_norm.png) |

### `Y_ISOLATION_BDT3`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_BDT3_diff.png) | ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_BDT3_diff_norm.png) |

### `Y_ISOLATION_Type`
#### Raw
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type_dv36.png) | ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type_dv45.png) |

#### Matched diff
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type_matched_diff_dv36.png) | ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type_matched_diff_dv45.png) |

### `Y_ISOLATION_Type2`
#### Raw
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type2_dv36.png) | ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type2_dv45.png) |

#### Matched diff
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type2_matched_diff_dv36.png) | ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type2_matched_diff_dv45.png) |

### `Y_ISOLATION_Type3`
#### Raw
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type3_dv36.png) | ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type3_dv45.png) |

#### Matched diff
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type3_matched_diff_dv36.png) | ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type3_matched_diff_dv45.png) |

### `Y_ISOLATION_Type4`
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type4_dv36.png) | ![](data-dv36_vs_dv45-no_refit/Y_ISOLATION_Type4_dv45.png) |

### `ISOLATION_TRACK1`
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/ISOLATION_TRACK1_dv36.png) | ![](data-dv36_vs_dv45-no_refit/ISOLATION_TRACK1_dv45.png) |

### `ISOLATION_TRACK2`
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/ISOLATION_TRACK2_dv36.png) | ![](data-dv36_vs_dv45-no_refit/ISOLATION_TRACK2_dv45.png) |

### `ISOLATION_TRACK3`
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/ISOLATION_TRACK3_dv36.png) | ![](data-dv36_vs_dv45-no_refit/ISOLATION_TRACK3_dv45.png) |

### `TRACK_TYPE1_CHI2`
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/TRACK_TYPE1_CHI2_dv36.png) | ![](data-dv36_vs_dv45-no_refit/TRACK_TYPE1_CHI2_dv45.png) |

### `TRACK_TYPE3_CHI2`
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/TRACK_TYPE3_CHI2_dv36.png) | ![](data-dv36_vs_dv45-no_refit/TRACK_TYPE3_CHI2_dv45.png) |

### `TRACK_TYPE4_CHI2`
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/TRACK_TYPE4_CHI2_dv36.png) | ![](data-dv36_vs_dv45-no_refit/TRACK_TYPE4_CHI2_dv45.png) |

### Track type difference vs. BDT score difference
| `v36r1p2` | `v45r3` |
|---|---|
| ![](data-dv36_vs_dv45-no_refit/ISOLATION_TRACK_vs_BDT_dv36.png) | ![](data-dv36_vs_dv45-no_refit/ISOLATION_TRACK_vs_BDT_dv45.png) |


## Comparison between `DaVinci` `v42r8p1` and `v45r3`, without refitting
Files used:

* `run1-rdx/samples/Dst--19_09_26--std--data--2012--md--dv42-subset-no_refit.root`
* `run1-rdx/samples/Dst--19_11_14--std--data--2012--md--dv45-subset-no_refit.root`

### `D0_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/D0_P_diff.png) | ![](data-dv42_vs_dv45-no_refit/D0_P_diff_norm.png) |

### `Dst_2010_minus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Dst_2010_minus_P_diff.png) | ![](data-dv42_vs_dv45-no_refit/Dst_2010_minus_P_diff_norm.png) |

### `Kplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Kplus_P_diff.png) | ![](data-dv42_vs_dv45-no_refit/Kplus_P_diff_norm.png) |

### `Kplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Kplus_PX_diff.png) | ![](data-dv42_vs_dv45-no_refit/Kplus_PX_diff_norm.png) |

### `Kplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Kplus_PY_diff.png) | ![](data-dv42_vs_dv45-no_refit/Kplus_PY_diff_norm.png) |

### `Kplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Kplus_PZ_diff.png) | ![](data-dv42_vs_dv45-no_refit/Kplus_PZ_diff_norm.png) |

### `muplus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/muplus_P_diff.png) | ![](data-dv42_vs_dv45-no_refit/muplus_P_diff_norm.png) |

### `muplus_PX`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/muplus_PX_diff.png) | ![](data-dv42_vs_dv45-no_refit/muplus_PX_diff_norm.png) |

### `muplus_PY`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/muplus_PY_diff.png) | ![](data-dv42_vs_dv45-no_refit/muplus_PY_diff_norm.png) |

### `muplus_PZ`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/muplus_PZ_diff.png) | ![](data-dv42_vs_dv45-no_refit/muplus_PZ_diff_norm.png) |

### `Y_ISOLATION_BDT`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_BDT_diff.png) | ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_BDT_diff_norm.png) |

### `Y_ISOLATION_BDT2`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_BDT2_diff.png) | ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_BDT2_diff_norm.png) |

### `Y_ISOLATION_BDT3`
| difference (DL) | difference (normalized) |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_BDT3_diff.png) | ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_BDT3_diff_norm.png) |

### `Y_ISOLATION_Type`
#### Raw
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type_dv42.png) | ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type_dv45.png) |

#### Matched diff
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type_matched_diff_dv42.png) | ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type_matched_diff_dv45.png) |

### `Y_ISOLATION_Type2`
#### Raw
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type2_dv42.png) | ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type2_dv45.png) |

#### Matched diff
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type2_matched_diff_dv42.png) | ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type2_matched_diff_dv45.png) |

### `Y_ISOLATION_Type3`
#### Raw
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type3_dv42.png) | ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type3_dv45.png) |

#### Matched diff
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type3_matched_diff_dv42.png) | ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type3_matched_diff_dv45.png) |

### `Y_ISOLATION_Type4`
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type4_dv42.png) | ![](data-dv42_vs_dv45-no_refit/Y_ISOLATION_Type4_dv45.png) |

### `ISOLATION_TRACK1`
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/ISOLATION_TRACK1_dv42.png) | ![](data-dv42_vs_dv45-no_refit/ISOLATION_TRACK1_dv45.png) |

### `ISOLATION_TRACK2`
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/ISOLATION_TRACK2_dv42.png) | ![](data-dv42_vs_dv45-no_refit/ISOLATION_TRACK2_dv45.png) |

### `ISOLATION_TRACK3`
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/ISOLATION_TRACK3_dv42.png) | ![](data-dv42_vs_dv45-no_refit/ISOLATION_TRACK3_dv45.png) |

### `TRACK_TYPE1_CHI2`
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/TRACK_TYPE1_CHI2_dv42.png) | ![](data-dv42_vs_dv45-no_refit/TRACK_TYPE1_CHI2_dv45.png) |

### `TRACK_TYPE3_CHI2`
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/TRACK_TYPE3_CHI2_dv42.png) | ![](data-dv42_vs_dv45-no_refit/TRACK_TYPE3_CHI2_dv45.png) |

### `TRACK_TYPE4_CHI2`
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/TRACK_TYPE4_CHI2_dv42.png) | ![](data-dv42_vs_dv45-no_refit/TRACK_TYPE4_CHI2_dv45.png) |

### Track type difference vs. BDT score difference
| `v42r8p1` | `v45r3` |
|---|---|
| ![](data-dv42_vs_dv45-no_refit/ISOLATION_TRACK_vs_BDT_dv42.png) | ![](data-dv42_vs_dv45-no_refit/ISOLATION_TRACK_vs_BDT_dv45.png) |


## Comparison between `DaVinci` `v36r1p2` and `v42r8p1`, without refitting nor momentum rescaling
Files used:

* `run1-rdx/samples/Dst--19_10_11--std--data--2012--md--dv36-subset-no_refit_no_rescale.root`
* `run1-rdx/samples/Dst--19_10_11--std--data--2012--md--dv42-subset-no_refit_no_rescale.root`

### `D0_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/D0_P_diff.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/D0_P_diff_norm.png) |

### `Dst_2010_minus_P`
| difference [MeV] | difference (normalized) |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/Dst_2010_minus_P_diff.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/Dst_2010_minus_P_diff_norm.png) |

### `Y_ISOLATION_Type`
#### Raw
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type_dv42.png) |

#### Matched diff
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type_matched_diff_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type_matched_diff_dv42.png) |

### `Y_ISOLATION_Type2`
#### Raw
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type2_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type2_dv42.png) |

#### Matched diff
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type2_matched_diff_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type2_matched_diff_dv42.png) |

### `Y_ISOLATION_Type3`
#### Raw
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type3_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type3_dv42.png) |

#### Matched diff
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type3_matched_diff_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type3_matched_diff_dv42.png) |

### `Y_ISOLATION_Type4`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type4_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/Y_ISOLATION_Type4_dv42.png) |

### `ISOLATION_TRACK1`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/ISOLATION_TRACK1_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/ISOLATION_TRACK1_dv42.png) |

### `ISOLATION_TRACK2`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/ISOLATION_TRACK2_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/ISOLATION_TRACK2_dv42.png) |

### `ISOLATION_TRACK3`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/ISOLATION_TRACK3_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/ISOLATION_TRACK3_dv42.png) |

### `TRACK_TYPE1_CHI2`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/TRACK_TYPE1_CHI2_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/TRACK_TYPE1_CHI2_dv42.png) |

### `TRACK_TYPE3_CHI2`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/TRACK_TYPE3_CHI2_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/TRACK_TYPE3_CHI2_dv42.png) |

### `TRACK_TYPE4_CHI2`
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/TRACK_TYPE4_CHI2_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/TRACK_TYPE4_CHI2_dv42.png) |

### Track type difference vs. BDT score difference
| `v36r1p2` | `v42r8p1` |
|---|---|
| ![](data-dv36_vs_dv42-no_refit-no_rescale/ISOLATION_TRACK_vs_BDT_dv36.png) | ![](data-dv36_vs_dv42-no_refit-no_rescale/ISOLATION_TRACK_vs_BDT_dv42.png) |


## Comparison between MC (Pythia 6)
Files used, located in `run1-rdx/ntuples/mc`:

* `ntuples/ref-rdx-run1/Dst-mc/Dst--19_09_26--mc--Bd2DstTauNu--2012--md--py6-phoebe.root`
* `ntuples/pre-0.9.0/Dst-mc/Dst--19_09_26--mc--Bd2DstTauNu--2012--md--py6-sim08a.root`

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

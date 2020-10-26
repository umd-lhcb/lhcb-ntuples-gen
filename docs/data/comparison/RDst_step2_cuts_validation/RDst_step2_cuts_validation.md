We took Phoebe's $D^*$ step-2 ntuple located at:
```
ntuples/ref-rdx-run1/Dst-mix/Dst--20_07_02--mix--all--2011-2012--md-mu--phoebe.root
```
and [extracted the ISO sample](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/d5cbd869542a1f610c089e6d0d4d36b5d9a764a5/postprocess/ref-rdx-run1/rdst-2011-mix.yml) as a reference.

Then, we apply [most step-2 cuts](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/d5cbd869542a1f610c089e6d0d4d36b5d9a764a5/postprocess/rdx-run1/rdx-run1.yml) to our newly generated 2011 MagDown ntuple:
```
ntuples/0.9.2-2011_production/Dst_D0--20_10_12--std--LHCb_Collision11_Beam3500GeV-VeloClosed-MagDown_Real_Data_Reco14_Stripping21r1_90000000_SEMILEPTONIC.DST.root
```
for comparison.

There are ~79k candidates in Phoebe's, ~72k in ours. This is a mystery to be solved.


### `el`
| difference [GeV] | difference (normalized) | distributions [GeV] |
|---|---|---|
| ![](data-iso_phoebe_vs_us/el_diff.png) | ![](data-iso_phoebe_vs_us/el_diff_norm.png) | ![](data-iso_phoebe_vs_us/el_dist.png) |

### `mm2`
| difference [GeV^2^] | difference (normalized) | distributions [GeV^2^] |
|---|---|---|
| ![](data-iso_phoebe_vs_us/mm2_diff.png) | ![](data-iso_phoebe_vs_us/mm2_diff_norm.png) | ![](data-iso_phoebe_vs_us/mm2_dist.png) |

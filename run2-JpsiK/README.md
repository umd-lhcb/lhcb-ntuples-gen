## Production of `B -> J/Psi K` ntuples

We reweight the production kinematics of `B` mesons with a sample of `B -> J/Psi K` events reconstructed in
DaVinci with the `run2-JpsiK/reco_JpsiK.py` script. No cuts are applied at this level. In data we use
the `StrippingBetaSBu2JpsiKDetached` stripping line, and 
[`B -> JPsi K` MC (12143001)](https://gitlab.cern.ch/lhcb-datapkg/Gen/DecFiles/-/blob/v30r103/dkfiles/Bu_JpsiK,mm=DecProdCut.dec).

The DaVinci ntuples are processed with the following commands inside `workflows`

```shell
cd workflows
./JpsiK.py JpsiK-ntuple-run2-data
./JpsiK.py JpsiK-ntuple-run2-mc
```

This script runs `babymaker` to rename and remove branches as specified in
`postprocess/JpsiK-run2/JpsiK-run2.yml`, and applies the following cuts

- `b_L0MuonDecision_TOS && b_Hlt1TrackMuonDecision_TOS && b_Hlt2DiMuonDetachedHeavyDecision_TOS`
- `mu_pt > 2000` for at least one of the muons satisfying L0
- `mu_pt > 500 && amu_pt > 500 && k_pt > 500`
- `b_m > 5150 && b_m < 5350`
- `j_mm > 3060 && j_mm < 3140`
- `b_dira > 0.9995 && b_min_ip_ch2 < 12 && b_endvtx_chi2 < 18`
- `j_fd_chi2 > 25 && mu_min_ip_chi2 > 4 && amu_min_ip_chi2 > 4`
- `k_pid_k > 4 && mu_pid_mu > 2 && amu_pid_mu > 2`
- Truthmatch for MC

Three sets of precalculated weights are applied
- PID for the muons and kaon from `P x eta x nTracks` histograms in `run2-JpsiK/reweight/pid/root-run2-JpsiK_oldcut`
- Tracking from `P x eta` histograms in `run2-JpsiK/reweight/tracking/root-run2-general`
- `B` kinematics from `PV x tracks` and `pT x eta` histograms in `run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_oldcut`

## Reweighting of `B` kinematics with `B -> J/Psi K`

To find the `B` kinematics reweighting we perform a fit to the invariant mass of the `B` meson with
`run2-JpsiK/fit/fit_and_sweight.py`. This fit provides the s-weights that implement the background
subtraction. The histograms are then produced with `run2-JpsiK/fit/gen_weights.py`.

The recipes can take 10 minutes and are run with

```shell
cd run2-JpsiK
./fit/find_jpsik_weights.py -d ../ntuples/0.9.8-JpsiK_L0/JpsiK-std-step2/ \
    -m ../ntuples/0.9.8-JpsiK_L0/JpsiK-mc-step2/
```

The output weightfile should then be placed in the proper folder
```shell
cp -f gen//run2-JpsiK-2016-md-B-ndof_ntracks__pt_eta.root \
  reweight/JpsiK/root-run2-JpsiK_oldcut/run2-JpsiK-2016-md-B-ndof_ntracks__pt_eta.root
```
With this file in place, the step 2 ntuples can be regenerated with the new `wjk` weights as
described above. This file is also used by the non JpsiK MC ntuples.
   
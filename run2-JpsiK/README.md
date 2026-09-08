## Production of `B -> J/Psi K` ntuples

We reweight the production kinematics of `B` mesons with a sample of `B -> J/Psi K` events reconstructed in
DaVinci with the `run2-JpsiK/reco_JpsiK.py` script. No cuts are applied at this level.
In data we use the `StrippingBetaSBu2JpsiKDetached` stripping line.
For MC, the
[`B -> JPsi K` MC (12143001)](https://gitlab.cern.ch/lhcb-datapkg/Gen/DecFiles/-/blob/v30r103/dkfiles/Bu_JpsiK,mm=DecProdCut.dec) sample is used,
reconstructed using a similar sequence as the data stripping, but without PID (to be able to use PIDCalib and include data-MC corrections).

The DaVinci ntuples are processed with the following commands inside `workflows`

```shell
cd workflows
./JpsiK.py JpsiK-ntuple-run2-data
./JpsiK.py JpsiK-ntuple-run2-mc
```

This script runs `babymaker` to rename and remove branches as specified in
`postprocess/JpsiK-run2/JpsiK-run2.yml`, and applies the following cuts

- `j_L0DiMuonDecision_TOS && b_Hlt1TrackMuonDecision_TOS && b_Hlt2DiMuonDetachedHeavyDecision_TOS`
- `mu_pt * amu_pt > 2.35 GeV2` (Can be relaxed for 2017/18. See Table 1 in [LHCb-DP-2019-001](https://iopscience.iop.org/article/10.1088/1748-0221/14/04/P04013).)
- `mu_pt > 500 && amu_pt > 500 && k_pt > 500`
- `b_m > 5150 && b_m < 5450`
- `j_mm > 3060 && j_mm < 3140`
- `b_dira > 0.9995 && b_min_ip_ch2 < 12 && b_endvtx_chi2 < 18`
- `j_fd_chi2 > 25 && mu_min_ip_chi2 > 4 && amu_min_ip_chi2 > 4`
- `mu_is_mu && amu_is_mu`
- `k_pid_k > 4 && mu_pid_mu > 2 && amu_pid_mu > 2` (via PIDCalib weights for MC)
- Truthmatch for MC

Two additional sets of weights are found and used
<!-- - PID for the muons and kaon from `P x eta x nTracks` histograms in `run2-JpsiK/reweight/pid/root-run2-JpsiK_oldcut` -->
- Tracking from `P x eta` histograms in `run2-JpsiK/reweight/tracking/root-run2-general`
- `B` kinematics from `PV x tracks` and `pT x eta` histograms in `run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_oldcut` (can use only after `B` kinematic/occupancy reweighting completed, of course)

## Reweighting of `B` kinematics with `B -> J/Psi K`

To find the `B` kinematic/occupancy reweighting we perform a fit to the invariant mass of the `B` meson with
`run2-JpsiK/fit/fit_and_sweight.py`. This fit provides the s-weights that implement the background
subtraction. The histograms are then produced with `run2-JpsiK/fit/gen_weights.py`.

The recipes can take 10 minutes (per year) and are run with

```shell
./fit/find_jpsik_weights.py
#     -d ../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/JpsiK-data/step2/ \
#     -m ../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/JpsiK-mc/step2/
```

(if trouble importing tensorflow, ensure you've somehow run `export LD_LIBRARY_PATH	:=	${STUB_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH}` in your nix shell).

The output weight files should then be placed in the proper folders.
These weights get used for both `JpsiK` and rdx

```shell
cp gen/run2-JpsiK-*-md-B-ndof_ntracks__pt_eta.root reweight/JpsiK/root-run2-JpsiK_PIDweights_IsMuonCut/
cp gen/run2-JpsiK-*-md-B-ndof_ntracks__pt_eta.root ../run2-rdx/reweight/JpsiK/root-run2-JpsiK/
```

With these files in place, the step 2 ntuples can be regenerated with the new `wjk` weights (as
described above for `JpsiK`).
The reprocessing of JpsiK with the new wjk is needed to produce validation plots with `studies/plot-JpsiK_kinematic_reweighting/plot_JpsiK_reweighting.py`.

# lhcb-ntuples-gen [![github CI](https://github.com/umd-lhcb/lhcb-ntuples-gen/workflows/CI/badge.svg?branch=master)](https://github.com/umd-lhcb/lhcb-ntuples-gen/actions?query=workflow%3ACI)

ntuples generation with DaVinci and in-house offline components.
Please refer to [project wiki](https://umd-lhcb.github.io/lhcb-ntuples-gen/)
for more details about installation, usage, and data sources of this project.

## Quick set up

Type in a terminal

```shell
git clone git@github.com:umd-lhcb/lhcb-ntuples-gen
cd lhcb-ntuples-gen
git remote add julian git@lhcb.physics.umd.edu:lhcb-ntuples-gen
git remote add glacier git@10.229.60.85:lhcb-ntuples-gen
git annex init --version=7
git submodule update --init  # Do this before git annex sync to avoid potential mess-up of submodule pointers!
git annex sync

nix develop  ## Can take an hour
make install-dep
make install-dep-pip ## To install packages needed for JpsiK reweighting, including zfit
```

## Generation of step-1 ntuples (DaVinci)

Development of the DaVinci scripts can be done locally in your laptop by running our `docker`
image of DaVinci. Install `docker` as described in the
[wiki](https://umd-lhcb.github.io/lhcb-ntuples-gen/ntupling/installation/#install-docker-to-run-davinci-locally) and pull the image with
```shell
docker pull umdlhcb/lhcb-stack-cc7:DaVinci-v45r6-SL
```

For instance, to test the standard data script you would first pull the example `.dst` files,
would then enter `docker`, and run the script
```shell
git annex get run2-rdx/data/data-2016-md/00102837*
make docker-dv
cd run2-rdx
./run.sh conds/cond-std-2016.py
```

After your script does what you want, you are ready to send ganga jobs to the LHCb grid
as detailed in the [wiki](https://umd-lhcb.github.io/lhcb-ntuples-gen/ntupling/grid_job/#grid-job-preparation-and-submission-on-lxplus).

## Generation of step-2 ntuples (babies)

The step-1 ntuples coming out of DaVinci are processed with the
[babymaker](https://pybabymaker.readthedocs.io/en/latest/scripts/babymaker.html), a neat script that allows
for easy branch renaming and deleting, as well as cut selection and calculation of new branches. This is
configured in YAML files.

For instance, the tracker-only MC ntuples used to produce the fit templates use [`postprocess/rdx-run2/rdx-run2_oldcut.yml`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/postprocess/rdx-run2/rdx-run2_oldcut.yml).
These ntuples are currently produced by first downloading the step-1 ntuples from the `annex`. Since these are
over 1 TB, this is typically done in `glacier` inside a `tmux`
```shell
tmux
git annex get ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only
```
The generation of the step-2 babies can be quite slow, currently taking about two days to run, mainly because of the normalization (and likely becaue HAMMER FF weights are recalculated each time--**TODO** to avoid this, these ought to be cached by saving them to the subfolders in `ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only`). The ntupling is run with the following (specific options can be found inside `workflows/rdx.py`):
```shell
tmux
cd workflows
## Takes 37 hours, output is 422GB
./rdx.py rdx-ntuple-run2-mc-to-sig-norm    2>&1 | tee step2-ntuple_mc-to-sig-norm.log
## Takes 75 min, output is 58GB
./rdx.py rdx-ntuple-run2-mc-to-ddx         2>&1 | tee step2-ntuple_mc-to-ddx.log
## Takes 11hours, output is 81GB
./rdx.py rdx-ntuple-run2-mc-to-dstst       2>&1 | tee step2-ntuple_mc-to-dstst.log
## Takes 45 min, output is 2.7GB
./rdx.py rdx-ntuple-run2-mc-to-d_s         2>&1 | tee step2-ntuple_mc-to-d_s.log
## Takes 45 min, output is 23GB
./rdx.py rdx-ntuple-run2-mc-to-dstst-heavy 2>&1 | tee step2-ntuple_mc-to-dstst-heavy.log
## Takes ??, output is 10GB
./rdx.py rdx-ntuple-run2-data              2>&1 | tee step2-ntuple_data.log
## Takes 65 min, output is 22GB
./rdx.py rdx-ntuple-run2-mu_misid          2>&1 | tee step2-ntuple_mu_misid.log
## Takes 65 min, output is 22GB
./rdx.py rdx-ntuple-run2-mu_misid-vmu      2>&1 | tee step2-ntuple_mu_misid-vmu.log
```

This generation relies on various auxiliary ntuples and weights. **Some aux ntuples need to be generated prior to running the above commands**. Namely:

- `B` occupancy/kinematic MC correction weights (from `B -> J/psi K` events)--described in [`run2-JpsiK/README.md`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/run2-JpsiK/README.md)--are stored in `run2-rdx/reweight/JpsiK/root-run2-JpsiK`
- Long track reco eff MC correction weights (from `J/psi -> mu mu` events)--described a bit more in [this comment](https://github.com/umd-lhcb/lhcb-ntuples-gen/issues/80#issue-948098584); makes use of LHCb's TrackCalib package--are stored in `run2-rdx/reweight/tracking/root-run2-general`
- PID weights to implement the PID cuts (`DLLK`, `DLLmu`, `DLLe`, `isMuon`, `uBDT`) and skim PID selections (`NNK`, `NNghost`) present in data for our tracker-only MC--makes use of LHCb's PIDCalib (we also have a [local fork](https://github.com/umd-lhcb/pidcalib2) to incorporate `uBDT`); generated with these shell scripts for [mu PID](https://github.com/umd-lhcb/pidcalib2/blob/90ba3cf9333839033ea89b36f9e368acc0978b6a/efficiency_gen/rdx-run2-ubdt.sh), [K/pi PID](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/b2a4095d4d0efb4cd988bffca4cd4f1209b90b96/run2-rdx/reweight/pid/run2-rdx_oldcut.sh), [skim sel PID](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/b2a4095d4d0efb4cd988bffca4cd4f1209b90b96/run2-rdx/reweight/pid/run2-rdx_iso_oldcut.sh) and with all efficiencies [shifted positive](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/b2a4095d4d0efb4cd988bffca4cd4f1209b90b96/scripts/shift_histo_efficiencies.py)--are stored in `run2-rdx/reweight/pid/root-run2-rdx_oldcut-shifted`
- Vertex smearing weights to compensate for the incomplete MC final reweighting of vertex resolution (smears the `B` flight vector according to data-driven corrections)--currently run1 corrections used, stored in `run2-rdx/reweight/vertex/smearing_vec.root` (weights calculated in our `vertex-resolution` repo)
- misID efficiencies and DiF smearing weights, used in misID unfolding (calculated in and then applied using a script in our `misid-unfold` repo) are stored in `run2-rdx/reweight/misid/histos`

The other auxiliary ntuples are calculated on the fly if not cached:

- Form-factor weights, calculated in `Hammer` (via code in our `hammer-reweight` repo) and applied to signal, normalization, and `D**(s)`
- Trigger emulation weights to implement `L0Hadron TOS`, `L0Global TIS`, `HLT1` triggers for our tracker-only MC, calculated in our `TrackerOnlyEmu` repo

The step-2 ntuples (outputted to `ntuple_merged` folders) can then be copied to `rdx-run2-analysis/ntuples` and annexed, and will be used in that
repository to produce the fit templates and other studies.

### Updating PID weights in Monte Carlo

MC weights are saved in histograms that we store
in [`run2-rdx/reweight/pid/root-run2-rdx_oldcut-shifted`](https://github.com/umd-lhcb/lhcb-ntuples-gen/tree/e8d90f19de802f3fb786486cbf28db7914201dc1/run2-rdx/reweight/pid/root-run2-rdx_oldcut-shifted). These histograms
are calculated with the `pidcalib2` package. We have three sets of scripts
- `pidcalib2/efficiency_gen/rdx-run2-ubdt.sh` for the muon PID, that is to be run in `glacier` and takes 15 min to run.
- `lhcb-ntuples-gen/reweight/pid/run2-rdx_oldcut.sh` for the kaon and pion PID, run in `lxplus` and takes 50 min to run.
- `misid-unfold/spec/rdx-run2.yml` for the misID unfold species.

If you want add new weights, you should calculate the histogram, copy it to that folder, and include
a branch by modifying `run2-rdx/reweight/pid/run2-rdx_oldcut.yml`.

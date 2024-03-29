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
```
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
The ntupling is run with the following, that overall take about two days to run. The comments
list how long each command takes and the gigabytes the produced folder in `gen/` is
```shell
tmux
cd workflows
## Takes 45 min, 2.7G
./rdx.py rdx-ntuple-run2-mc-to-d_s         | tee step2-ntuple_mc-to-d_s.log
## Takes 45 min, 23G
./rdx.py rdx-ntuple-run2-mc-to-dstst-heavy | tee step2-ntuple_mc-to-dstst-heavy.log
## Takes 75 min, 58G
./rdx.py rdx-ntuple-run2-mc-to-ddx         | tee step2-ntuple_mc-to-ddx.log
## Takes ~hours, ~80G
./rdx.py rdx-ntuple-run2-mc-to-dstst       | tee step2-ntuple_mc-to-dstst.log
## Takes 37 hours, 422G
./rdx.py rdx-ntuple-run2-mc-to-sig-norm    | tee step2-ntuple_mc-to-sig-norm.log     
```

This generation relies on a host of auxiliary ntuples and weights that in the case of `B` kinematics weights
from `B -> J/Psi K` events, described in
[`run2-JpsiK/README.md`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/run2-JpsiK/README.md), need
to be pre-calculated.

The other auxiliary ntuples are calculated on the fly if not cached

- Form-factor weights calculated in `Hammer` and applied to signal, normalization, and `D**(s)`.
- PID weights calculated in `PIDCalib2`.
- Trigger emulation weights.

The step-2 ntuples are then stored in the `annex` of `rdx-run2-analysis/ntuples`, and used in that
repository to produce the fit templates and other studies.

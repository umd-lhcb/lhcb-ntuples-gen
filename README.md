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

## Generation of step-2 ntuples (babies)

The step-1 ntuples coming out of DaVinci are processed with the
[babymaker](https://pybabymaker.readthedocs.io/en/latest/scripts/babymaker.html), a neat script that allows
for easy branch renaming and deleting, as well as cut selection and calculation of new branches. This is
configured in YAML files.

For instance, the tracker-only MC ntuples used to produce the fit templates use [`postprocess/rdx-run2/rdx-run2_oldcut.yml`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/postprocess/rdx-run2/rdx-run2_oldcut.yml).
These ntuples are currently produced by first downloading the step-1 ntuples from the `annex`. Since these are
over 1 TB, this is typically done in `glacier`
```shell
git annex get ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only
```
Then, run
```shell
cd workflows
./rdx.py rdx-ntuple-run2-mc-to-sig-norm
./rdx.py rdx-ntuple-run2-mc-to-ddx
./rdx.py rdx-ntuple-run2-mc-to-dstst
./rdx.py rdx-ntuple-run2-mc-to-dstst-heavy
./rdx.py rdx-ntuple-run2-mc-to-d_s
```

This generation relies on a host of auxiliary ntuples and weights that need to be pre-calculated.
- Form-factor weights calculated in `Hammer` and applied to signal, normalization, and `D**(s)`.
- PID weights calculated in `PIDCalib2`.
- `B` kinematics weights from `B -> J/Psi K` events, described in
[`run2-JpsiK/README.md`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/run2-JpsiK/README.md).
- Trigger emulation weights.

The step-2 ntuples are then stored in the `annex` of `rdx-run2-analysis/ntuples`.

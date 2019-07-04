Welcome to the wiki for `lhcb-ntuples-gen`. In this section, you'll find useful
information on installing required dependencies for this project, as well the
usage of some tools, such as `git-annex`, that will be used in this project.

This project requires the following vesion control software to be installed in
your system:

* `git`: for source code version control
* `git-annex` (that supports `v7` repository format): for data file version
  control

To install these programs, please follow [this section](installation/#install-version-control-software).

The ntuples[^1] generation is separated into **2 steps**:

1. Use `DaVinci` to generate ntuples from raw data[^2].
   Follow [this section](installation/#install-dependencies-for-davinci) to install required programs.
2. Use `babymaker` frame work to do slimming, skimming, and additional
   calculation on previous ntuples, generating new ntuples.
   Use [this section](installation/#install-dependencies-for-babymaker) for installation.

!!! note
    These two steps have separate dependencies. If you only need to run one
    step, just follow the installation instruction for that particular step.


[^1]: `.root` files that can be processed by `DaVinci`, `ROOT`, and many other tools.
[^2]: `.dst` files that directly come from CERN.

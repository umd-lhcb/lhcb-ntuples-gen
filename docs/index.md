Welcome to the wiki for `lhcb-ntuples-gen`, the repository that generates the
ntuples for some LHCb analyses at UMD, currently just run 2 $R(D^{(*)})$
analysis. In this section, you'll find useful information for installing the
required dependencies for this project, as well as the usage of some tools,
such as `git-annex`, that will be used in this project.


## Ntuple generation
The ntuples[^1] generation is separated into **2 steps**:

1. Use `DaVinci` to generate ntuples from raw data[^2].
   Follow [this section](ntupling/installation/#install-docker-to-run-davinci-locally) to install required programs.
   Use [this manual](ntupling/step1_davinci.md) to learn how to use `DaVinci` locally.
2. Use `babymaker` frame work to do slimming, skimming, and additional
   calculation on previous ntuples, generating new ntuples.
   Use [this section](ntupling/installation/#install-babymaker) for installation.
   The `babymaker` manual can be found [here](ntupling/step2_babymaker.md).

!!! note
    These two steps have separate dependencies. If you only need to run one
    step, just follow the installation instruction for that particular step.


## Modifying this wiki
This wiki is written in a series of markdown files (`.md`) committed to the
[docs](https://github.com/umd-lhcb/lhcb-ntuples-gen/tree/master/docs) folder of the
`lhcb-ntuples-gen` repository. The structure of the wiki is defined in
[`mkdocs.yml`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/mkdocs.yml). This file contains the
title of each page in the wiki, and the markdown file that defines that page.

To modify the wiki just modify `mkdocs.yml` or the `.md` files, and commit the changes to the repo. In about
a minute Travis will deploy the new website to [https://umd-lhcb.github.io/lhcb-ntuples-gen/](https://umd-lhcb.github.io/lhcb-ntuples-gen/).

To view the website locally (for instance, before committing), you will need to install `mkdocs` and
the `material` theme
```
pip3 install --user -r docs/requirements.txt
```
Then, from `lhcb-ntuples-gen` you generate the website at the local address [http://127.0.0.1:8000](http://127.0.0.1:8000) with the command
```
mkdocs serve
```

## Version control systems (VCS)
This project requires the following VCS to be installed in your system:

* `git`: for source code version control
* `git-annex` (that supports `v7` repository format): for data file version
  control

To install these programs, please follow [this section](ntupling/installation/#install-vcs-git-and-git-annex).
In addition, we provide [a brief introduction](software_manuals/git_annex) on the usage of `git-annex`.


[^1]: `.root` files that can be processed by `DaVinci`, `ROOT`, and many other tools.
[^2]: `.dst` files that directly come from CERN.

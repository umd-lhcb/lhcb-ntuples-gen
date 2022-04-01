Welcome to the wiki for `lhcb-ntuples-gen`, the repository that generates the
ntuples for some LHCb analyses at UMD, currently just run 2 $R(D^{(*)})$
analysis. In this section, you'll find useful information for installing the
required dependencies for this project, as well as the usage of some tools,
such as `git-annex`, that will be used in this project.


## Generation of analysis ntuples
The ntuples[^1] generation is separated into:

1. **STEP 1**: Use LHCb's `DaVinci` to generate ntuples from raw LHCb data[^2].
   Follow [this section](ntupling/installation/#install-docker-to-run-davinci-locally) to install required programs.
   Use [this manual](ntupling/step1_davinci.md) to learn how to use `DaVinci` locally.
   Follow [this section](ntupling/grid_job.md) to learn submitting `DaVinci`
   jobs to the GRID.
2. **STEP 2**: Use `babymaker` frame work to do slimming, skimming, and additional
   calculation on previous ntuples, generating new ntuples.
   Follow [these two](ntupling/installation/#install-nix) [sections](ntupling/installation/#install-babymaker) for installation.
   A general guide for generating step-2 ntuple can be found [here](ntupling/step2_babymaker.md).

!!! note
    These two steps have separate dependencies. If you only need to run one
    step, just follow the installation instruction for that particular step.

!!! info
    - The step-1 and step-2 ntuples have [the following](ntupling/nomenclature.md)
      naming conventions.
    - For some tips on the general development of this project, see [here](ntupling/dev.md)


## Directory structures

```shell
.
├── archive      # storage for plots, csv, and some old code
├── docs
├── ganga
├── gen          # output produced by make rules, e.g. ntuple, cutflow MD
├── include      # headers
│   └── functor
│       └── rdx  # RDX-specific headers
├── lib
│   └── python   # Python submodules, e.g. pyBabyMaker
├── ntuples      # storage for (mostly) GRID-produced ntuples
├── postprocess
│   ├── cpp_templates  # C++ templates for babymaker
│   ├── rdx-run1
│   ├── rdx-run2
│   ├── ref-rdx-run1   # For Phoebe's sample ntuples
│   └── skims          # For branch removal at lxplus level
├── run1-rdx     # DaVinci scripts, sample ntuples for RDX run 1
├── run2-rdx     # ^^^^ for RDX run 2
├── scripts      # plotting, cutflow, and utility scripts
├── studies      # One-off studies
└── workflows    # workflows for ntuple production, cutflow, etc.
    └── rdx
```


## Modifying this wiki
This wiki is written in a series of markdown files (`.md`) committed to the
[`docs`](https://github.com/umd-lhcb/lhcb-ntuples-gen/tree/master/docs) folder of the
`lhcb-ntuples-gen` repository. The structure of the wiki is defined in
[`mkdocs.yml`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/mkdocs.yml).
This file contains the title of each page in the wiki, and the markdown file
that defines that page.

To modify the wiki just modify `mkdocs.yml` or the `.md` files, and commit the
changes to the repo. In about a minute _Github Action_ will deploy the new
website to
[https://umd-lhcb.github.io/lhcb-ntuples-gen/](https://umd-lhcb.github.io/lhcb-ntuples-gen/).

To view the website locally (for instance, before committing), you will need to
install `mkdocs` and the `material` theme
```
pip install --user -r docs/requirements.txt
```
Then, from `lhcb-ntuples-gen` you generate the website at the local address
[http://127.0.0.1:8000](http://127.0.0.1:8000) with the command
```
mkdocs serve
```

!!! note
    If you have problems installing `mkdocs`, you can also install it and run it inside
    [nix](ntupling/installation/#install-nix) with

    ```shell
    nix develop  # Enter the nix shell in lhcb-ntuples-gen
    pip install -r docs/requirements.txt
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

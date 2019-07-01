# lhcb-ntuples-gen
ntuple processing scripts. For some tips and tricks, please refer to the "Wiki"
section of the project.


## DaVinci
For each stripping line, `ntuple_options.py` is the DaVinci script that
generates a ntuple.


## `babymaker`
All ntuple postprocessing are done in the `babymaker` framework.

### Prerequisite
Install `gcc`, `root`, `clang-format` (which normally comes with `clang`) and
`python`. Then install required `Python` packages with:
```
pip install -r requirements.txt
```

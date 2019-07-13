# lhcb-ntuples-gen [![Build status](https://travis-ci.com/umd-lhcb/lhcb-ntuples-gen.svg?build)](https://travis-ci.com/umd-lhcb/lhcb-ntuples-gen)
ntuples generation with DaVinci and babymaker.
Please refer to [project wiki](https://umd-lhcb.github.io/lhcb-ntuples-gen/)
for more details about installation, usage, and data sources of this project.


## Utilities
In `utils` folder, we have some utility `ROOT` macros.

### `extract_uid.cxx`
This utility extracts shared events between two files that are unique to each
one of them:
```
root -q -l 'extract_uid.cxx("file1", "file2", "output", "tree1", "tree2")'
```

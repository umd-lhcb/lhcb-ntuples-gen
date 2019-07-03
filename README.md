# lhcb-ntuples-gen
ntuple processing scripts. For some tips and tricks, please refer to the "Wiki"
section of the project.


## DaVinci
For each stripping line, `ntuple_options.py` is the DaVinci script that
generates a ntuple.


## Postprocess
All ntuple postprocessing are done in the `babymaker` framework.

### Prerequisite
Install `gcc`, `root`, `clang-format` (which normally comes with `clang`) and
`python`. Then install required `Python` packages with:
```
pip install -r requirements.txt
```


## Sample files
Here we track the original filenames and their providers in the `*/sample` folder.

### 2012-b2D0MuXB2DMuNuForTauMuLine

| name in this repo | original name | provider | MD5 sum |
|---|---|---|---|
| `YCands_D0-2012-mag_down-data.root` | ? | P. Hamilton | `73bfbc7b9d0e1eea19572fa42b28ebc6` |
| `YCands_Dstar-2012-mag_down-data.root` | `newTFYCands_DATA_2012_MD.root` | P. Hamilton | `16c4750761d75b8b37e5bff521139887` |

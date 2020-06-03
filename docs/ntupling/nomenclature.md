These rules should be checked by a script automatically.

## General guidelines
- These filenames are case-sensitive
- No whitespace or `\` permitted. Replace them with `_`
- Fields must be separated with `--`


## Filenames

### Step 1 ntuples
Step 1 ntuple filenames, DaVinci logs, and ganga jobs should follow the following form:
```
<reco_sample>--<date>--<type>--<Dirac_path>.root
```

!!! note
    Below are the definitions of each field.

    - `reco_sample`: For instance `Dst`, `D0`, `DstPi`, `DstplusPi`, etc. They may all be merged into a single tree
    - `date`: Generation date. Formatted: `YY_MM_DD`
    - `type`: Descriptor, for instance `cutflow_mc`
    - `Dirac_path>: The full Dirac path for the sample, replacing `\` and whitespace with `_`

!!! example
    An ntuple name looks like this:
    ```
    Dst--20_05_08--cutflow_mc--MC_2011_11874091_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged.root
    ```

### Step 2 ntuples

Step 2 ntuple filenames should follow the following form:
```
<reco_sample>--<date>--<type>--<sample>--<year>--<polarity>--<additional_flags>.root
```

!!! note
    Below are the definitions of each field.

    - `reco_sample`: For instance `Dst`, `D0`, `DstPi`, etc. They may all be merged into a single tree
    - `date`: Generation date. Formatted: `YY_MM_DD`
    - `type`: Descriptor, for instance `cutflow_mc`
    - `sample`: Sample or samples in ntuple, eg `data`, `DstplusTauNu` or `All` if all samples merged
    - `year`: Year the data/MC is recorded/generated. Format: `YYYY`
    - `polarity`: `md` (magnet down) or `mu` (magnet up)
    - `additional_flags`: Optional. Ordered in the following way. Legal ones are:
        - `DaVinci` version (e.g. `dv36`)
        - `Pythia` version (e.g. `py6`)
        - Simulation condition (e.g. `sim08a`)
        - Other short descriptions (e.g. `no_refit_no_rescale`)
        - Literal `subset` for indicating only a subset of raw data used
        - Literal `step2` for indicating step-2 ntuples

!!! example
    An ntuple name looks like this:
    ```
    Dst--20_02_02--DstplusMuNu--mc--2012--md--dv36-py6-sim08a.root
    ```


## Folder structure for storage

Each ntuple production (defined by the same code) is to be placed in one folder
named `<code_tag>-<Descriptor>`, with subfolders containing divisions in terms
of `reco_sample` and `mc/data`. For example, the folder structure could look
like

```
0.8.6-cutflow/Dst-cutflow_mc
0.8.6-cutflow/Dst-cutflow_data

0.9.0-FirstFull/Dst-mc
0.9.0-FirstFull/Dst-data
0.9.0-FirstFull/D0-mc
0.9.0-FirstFull/D0-data
0.9.0-FirstFull/Dst-cutflow_mc

0.9.1-TriggerFix/Dst-mc
```

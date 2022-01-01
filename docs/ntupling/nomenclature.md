These rules are checked by [a script](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/test/test_filename_convention.py) automatically.

## General guidelines

- These filenames are case-sensitive
- No whitespace or `\` permitted. Replace them with `_`
- Fields must be separated with `--`



## Filenames
### Step 1 ntuples

Step 1 ntuple filenames, DaVinci logs, and ganga jobs should follow this form:
```
<particles>--<date>--<reco_mode>--[additional_flags]--<lfn>--[index]--[aux].root
```

!!! note
    Below are the definitions of each field. Optional fields are marked with
    `[]` instead of `<>`.

    - `particles`: For instance `Dst`, `D0`, `Dst_D0`, etc.
    - `date`: Generation date. Formatted: `YY_MM_DD`.
    - `reco_mode`: Reconstruction mode, for instance `cutflow_mc` or `std`.
    - `additional_flags`: Optional. Additional descriptions, such as `tracker_only`.
    - `lfn`: The full DIRAC LFN of the sample, replacing `\` and whitespace with `_`.
    - `index`: Optional. Index of the split sample. Ideally padding so ntuples.
        in the same folder have the same length.
    - `aux`: Optional. Reserved for auxiliary ntuples. Start with `aux`. e.g. `aux_ubdt`.

!!! example
    A ntuple name looks like this:
    ```
    Dst--20_05_08--cutflow_mc--bare--MC_2011_11874091_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged.root
    ```

    For split (unmerged) ntuples:
    ```
    Dst_D0--21_10_16--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST--406-dv.root
    ```


### Step 2 ntuples

Step 2 ntuple filenames should follow this form:
```
<particles>--<date>--<reco_mode>--<decay_mode>--<year>--<polarity>--[additional_flags]--[index].root
```

!!! note
    Sample ntuples that are stored in the `samples` folder of each stripping
    line folder is considered _step 2_!

!!! note
    Below are the definitions of the fields not defined above.

    - `decay_mode`: Brief description of the reco'ed sample. e.g. `data`,
        `cocktail`, `DstplusTauNu`, `11574021`, or `all` if all samples merged
    - `year`: Year the data/MC is recorded/generated. Format: `YYYY`. If
        multiple years needed, separate them with `-`.
    - `polarity`: `md` (magnet down), `mu` (magnet up), or `md-mu`.

!!! example
    An ntuple name looks like this:
    ```
    Dst--20_02_02--mc--DstplusMuNu--2012--md--dv36-py6-sim08a.root
    ```

    For split (unmerged) ntuples:
    ```
    D0--21_12_31--mc--11574021--2016--md--tracker_only--003.root
    ```


### Condition files

Condition files should follow this filename:

```
cond-<type>-<year>-[polarity]-[additional_flags].py
```

All fields obey the same definitions as listed in previous sections.

!!! note
    Condition files are located in `conds` folder of each stripping line folder.

!!! note
    The `<polarity>` and `<additional_flags>` fields are optional for condition files.


### Log files

Log files should follow this naming convention:
```
<particles>-<date>-<reco_mode>-[additional_flags].log
```

All fields obey the same definitions as listed in previous sections.

!!! note
    Log files are located in `logs` folder of each stripping line folder.



## Folder structure for storage
### Production ntuples

Each ntuple production (defined by the same code) is to be placed in one folder
named `<code_tag>-<description>`, with subfolders containing divisions in terms
of `reco_sample` and `mc/data`. For example, the folder structure could look
like:

```
0.9.0-cutflow/Dst-cutflow_mc

0.9.1-partial_refit/Dst-mc
0.9.1-partial_refit/Dst-data
0.9.1-partial_refit/D0-mc
0.9.1-partial_refit/D0-data
0.9.1-partial_refit/Dst-cutflow_mc

...
```


### DST folders

DST folders should follow this naming convention:
```
<reco_sample>-<year>-<polarity>-[additional_flags]
```

All fields obey the same definitions as listed in previous sections. This time,
the first three fields are mandatory.

!!! note
    DST folders are located in `data` folder of each stripping line folder.

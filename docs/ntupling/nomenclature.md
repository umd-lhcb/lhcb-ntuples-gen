These rules should be checked by a script automatically.

## Filenames

### Ntuples
Ntuples should have the following form:
```
<date>-<particle_name>-<reconstruction_mode>-<year>-<polarity>-<additional_flags>.root
```

!!! note
    Below are the definitions of each field.

    - `date`: Generation date. Formatted: `YYMMDD`
    - `particle_name`: Currently, either `Dst` or `D0`
    - `reconstruction_mode`: Currently, legal ones are:
        - `data`
        - `mc`
        - `cutflow_data`
        - `cutflow_mc`
    - `year`: Year the data/MC is recorded/generated. Format: `YYYY`
    - `polarity`: `md` (magnet down) or `mu` (magnet up)
    - `additional_flags`: Optional. Ordered in the following way. Legal ones are:
        - `DaVinci` version (e.g. `dv36`)
        - `Pythia` version (e.g. `py6`)
        - Simulation condition (e.g. `sim08a`)
        - Decay mode (e.g. `Bd2DstTauNu`)
        - Other short descriptions (e.g. `no_refit_no_rescale`)
        - Literal `subset` for indicating only a subset of raw data used
        - Literal `step2` for indicating step-2 ntuples

!!! note
    These filenames are case-sensitive! Below are the requirements for filename:

    - No whitespace permitted. Replace whitespace with `_`
    - Fields must be separated with `-`
    - No `-` permitted within each field

!!! example
    A legal ntuple name looks like this:
    ```
    200202-Dst-mc-2012-md-dv36-py6-sim08a-Bd2DstTauNu.root
    ```


## File storage

### Ntuples

- For grid-generated ntuples, store in the `ntuples` folder in the project root.
    Note that a subfolder of the form:
    ```
    YYMMDD-<particle_name>-<reconstruction_mode>
    ```
    should be created and ntuples should be placed **inside** the subfolder.

    !!! example
        ```
        ntuples/200202-Dst-data/200202-Dst-data-2016-md.root
        ```

- For locally-generated sample ntuples, store in the `samples` folder in the
    corresponding stripping line folder.


## Ganga job name

Ganga job name should be identical to the filename of the ntuples to be generated.

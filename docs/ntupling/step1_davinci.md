`DaVinci` is the LHCb package that runs preliminary selections and calculations
on the raw `.dst` data, and produces `.root` files. It is often run on LHC
remote Linux nodes `lxplus`.


## Running `DaVinci` locally
However, it is much more convenient to have a local `DaVinci` environment in a
docker with a configuration that is easily shared. After the docker is pulled
as described in the [dependencies](./installation.md#install-docker-to-run-
davinci-locally), it is launched from inside the project root with:
```
make docker-dv
```

This command mounts the project root into the docker, so it has access to all
the code in `lhcb-ntuples-gen` and allows you to modify it outside of the
docker.

Launch `DaVinci` with additional `TupleTool` with this command, inside
`docker`:
```
run gaudirun.py <ntuple_options1> <ntuple_options2> ...
```

We often have scripts that facilitate this. For instance, to run on Run 2
data, type in the `docker`:
```
cd run2-b2D0MuXB2DMuForTauMuLine
git annex get data/data-2016-md  # ~4.7 GB, this will take several minutes
./run.sh reco_Dst_D0.py conds/cond-std-2016.py
```

!!! note
    - The first argument, `reco_Dst_D0.py`, is the script that makes the
        $D^{*+}(\to D^0(\to K^+\pi^-)\pi^+)\mu^-$ reconstruction. It also sets
        how many events to run at most (`EvtMax`) and the print frequency
        (`PrintFreq`).

    - The second argument, `conds/cond-std-2016.py`, sets the type of
        input data (Data or MC), the input files and the name of the output
        file (`std.root` in this case).

!!! info
    For more info about `docker` usage, refer to [this guide](../software_manuals/davinci/docker_image_usage.md).

    For more info about `Makefile`, refer to [this guide](./dev.md#makefile).


## Running `DaVinci` on the `GRID`
We need to build a `DaVinci` on `lxplus` to add our `TupleTool`.
This version will then be sent to the `GRID` by `ganga`.

!!! info
    - For `DaVinci-{{ davinci_sl_ver }}`, refer to [this script](https://github.com/umd-lhcb/docker-images/blob/master/lhcb-stack-cc7/compile_dv.sh) for build instructions.
    - For `DaVinci-v42r8p1-SL` (obsolete), refer to [this `Dockerfile`](https://github.com/umd-lhcb/docker-images/blob/davinci-v42r8p1/lhcb-stack-cc7/Dockerfile-DaVinci-SL).

Then, for each of the stripping line folder inside this project, there should be a
Python scripted named `ganga_jobs.py`. The general syntax is:
```
ganga ganga_jobs.py <cond_files>
```
For instance, for signal Monte Carlo:
```
ganga ganga_jobs.py cond/cond-mc-2012-md-sim08a.py
```

The general usage of `ganga_jobs.py` is described by:
```
ganga ganga_jobs.py --help
```

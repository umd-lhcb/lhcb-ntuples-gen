!!! info
    `DaVinci` is the LHCb package that runs preliminary selections and calculations
    on the raw `.dst` data, and produces `.root` files. It is often run on LHC
    remote Linux nodes `lxplus`.

It is much more convenient to have a local `DaVinci` environment in a
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
If you want to modify the `TupleTools` used in DaVinci, check the `README` on local development at
[https://github.com/umd-lhcb/TupleToolSemiLeptonic/tree/master](https://github.com/umd-lhcb/TupleToolSemiLeptonic/tree/master).

We often have scripts that facilitate this. For instance, to run on Run 2
data, type in the `docker`:
```
cd run2-rdx
./run.sh conds/cond-std-2016.py
```

!!! warning
    The required `.dst` files need to be downloaded via `git-annex` **OUTSIDE**
    docker:
    ```
    cd run2-rdx
    git annex get data/data-2016-md  # ~4.7 GB, this will take several minutes
    ```

!!! note
    - Inside the run script, the `reco_Dst_D0.py` script in the same directory is
        called for $D^{*+}(\to D^0(\to K^+\pi^-)\pi^+)\mu^-$ reconstruction. 
        It also sets how many events to run at most (`EvtMax`) and the print frequency
        (`PrintFreq`). To use a different reco script, edit `run.sh`.

    - The argument, `conds/cond-std-2016.py`, sets the type of
        input data (Data or MC), the input files and the name of the output
        file (`std.root` in this case).

!!! info
    For more info about `docker` usage, refer to [this guide](../software_manuals/davinci/docker_image_usage.md).

    For more info about `Makefile`, refer to [this guide](./dev.md#makefile).

`DaVinci` is a LHCb software package that run various preliminary selections
and calculations on the raw `.dst` file, and produce a `.root` file.

Normally it is run on LHCb remote Linux nodes `lxplus`. However, it is much
more convenient to have a local `DaVinci` environment.


## Launch a `DaVinci` container
To launch a `DaVinci` `docker` container, type in:
```
docker run --rm -it -v <src_path>:/data -e UID=$(id -u) -e GID=$(id -g) --net=host umdlhcb/lhcb-stack-cc7:DaVinci-{{ davinci_sl_ver }}
```
note that `<src_path>` should be an absolute path pointing to the folder that we want to mount inside the container.

If you are in the folder you want to mount, you can just type:
```
docker run --rm -it -v `pwd`:/data -e UID=$(id -u) -e GID=$(id -g) --net=host umdlhcb/lhcb-stack-cc7:DaVinci-{{ davinci_sl_ver }}
```

!!! note
    `docker` _images_ are read-only. When we launch a `docker` _container_, a
    writable layer is placed on top of the image.


## Use DaVinci inside container
The command is very similar to the one used on `lxplus`:
```
lb-run DaVinci/latest gaudirun.py <ntuple_options1> <ntuple_options2> ...
```
since we have only 1 version of `DaVinci` inside the container,
`DaVinci/latest` would always work.


## Additional `TupleTool`
The `docker` image with `-SL` suffix also contains a special `DaVinci` version
that contains additional `TupleTool`[^1] for semileptonic analysis.
To access the special `DaVinci`, just substitute `lb-run DaVinci/latest` with
`run`. For instance:
```
run gaudirun.py <ntuple_options1> <ntuple_options2> ...
```

!!! note
    To make our lives easier, a `run.sh` command is typically created in each
    stripping lines, such as:
    ```
    <project_root>/2012-b2D0MuXB2DMuNuForTauMuLine/gen.sh
    ```

    If you see this file, take a look at it to see the availabe commands, and
    run it inside the `docker` container:
    ```bash
    ./run.sh <path_to_cond_file> <path_to_reco_file>  # inside docker
    ```
    optionally, a `debug` flag can be supplied so that only the first couple of
    events will be considered.


[^1]: Such as `TupleToolApplyIsolation` and `TupleToolTauMuDiscVars`.


## Remove old docker images
To list all local `docker` images:
```
docker images
```

If you download a newer version of `docker` image, and want to remove the old
ones to save disk space, you can:
```
docker rmi <docker_image_tag>
docker image prune
```
here `<docker_image_tag>` should be something like
`umdlhcb/lhcb-stack-cc7:DaVinci-{{ davinci_sl_ver }}`.

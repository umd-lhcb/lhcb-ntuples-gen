## Launch a `DaVinci` container
The shortcut to run a `DaVinci` `docker` in this project is:
```
make docker-dv
```
in the project root.

The `make` rule is actually defined as the following:
```
docker run --rm -it -v `pwd`:/data -e UID=$(id -u) -e GID=$(id -g) --net=host umdlhcb/lhcb-stack-cc7:DaVinci-{{ davinci_sl_ver }}
```

More generally, if you want to mount another folder, with a path `<src_path>`:
```
docker run --rm -it -v <src_path>:/data -e UID=$(id -u) -e GID=$(id -g) --net=host umdlhcb/lhcb-stack-cc7:DaVinci-{{ davinci_sl_ver }}
```

!!! info
    `docker` _images_ are read-only. When we launch a `docker` _container_, a
    writable layer is placed on top of the image.


## Use official `DaVinci` inside container
The command is very similar to the one used on `lxplus`:
```
lb-run DaVinci/latest gaudirun.py <ntuple_options1> <ntuple_options2> ...
```
since we have only 1 version of `DaVinci` inside the container,
`DaVinci/latest` would always work.


## Use locally compiled `DaVinci` inside container
Since we need additional `TupleTool`[^1] in our reconstruction script, we also
provide a locally compiled `DaVinci` inside the container, provided that you
are using a `DaVinci` image with a `-SL` suffix.

To launch this locally compiled `DaVinci`:
```
run gaudirun.py <ntuple_options1> <ntuple_options2> ...
```

!!! note
    To make our lives easier, a `run.sh` command is typically created in each
    stripping lines, such as:
    ```
    run1-b2D0MuXB2DMuNuForTauMuLine/run.sh
    ```

    If you see this file, take a look at it to see the availabe commands, and
    run it inside the `docker` container:
    ```bash
    ./run.sh <path_to_reco_file> <path_to_cond_file>  # inside docker
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

`DaVinci` is a LHCb software package that run various preliminary selections
and calculations on the raw `.dst` file, and produce a `.root` file.

Normally it is run on LHCb remote Linux nodes `lxplus`. However, it is much
more convenient to have a local `DaVinci` environment.


## `DaVinci` `docker` image usage
### Launch a `DaVinci` container
To launch a `DaVinci` `docker` container, type in:
```
docker run --rm -it -v <src_path>:/data -e UID=$(id -u) -e GID=$(id -g) --net=host umdlhcb/lhcb-stack-cc7:DaVinci-v42r8p1-SL
```
note that `<src_path>` should be an absolute path pointing to the folder that we want to mount inside the container.

If you are in the folder you want to mount, you can just type:
```
docker run --rm -it -v `pwd`:/data -e UID=$(id -u) -e GID=$(id -g) --net=host umdlhcb/lhcb-stack-cc7:DaVinci-v42r8p1-SL
```

!!! note
    `docker` _images_ are read-only. When we launch a `docker` _container_, a
    writable layer is placed on top of the image.


### Use DaVinci inside container
The command is very similar to the one used on `lxplus`:
```
lb-run DaVinci/latest gaudirun.py ntuple_options.py
```
since we have only 1 version of `DaVinci` inside the container,
`DaVinci/latest` would always work.


### Additional `TupleTool`
The `docker` image with `-SL` suffix also contains a special `DaVinci` version
that contains additional `TupleTool`[^1] for semileptonic analysis.
To access the special `DaVinci`, just substitute `lb-run DaVinci/latest` with
`run`. For instance:
```
run gaudirun.py ntuple_options.py
```

!!! note
    To make our lives easier, a `run.sh` command is typically created in each
    stripping lines, such as:
    ```
    <project_root>/2012-b2D0MuXB2DMuNuForTauMuLine/gen.sh
    ```

    If you see this file, just run it inside the `docker` container:
    ```bash
    ./run.sh  # inside docker
    ```


[^1]: Such as `TupleToolApplyIsolation` and `TupleToolTauMuDiscVars`.


### Remove old docker images
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
`umdlhcb/lhcb-stack-cc7:DaVinci-v42r8p1-SL`.


## `DaVinci` tips and tricks
### About `GaudiSequencer`
`GaudiSequencer` is an _per-event algorithm_, such as `DecayTreeTuple`, in the
sense that `Gaudi` knows that it should run on every event.

`GaudiSequencer` is used to chain related algorithms, and it's default behavior
is to only run an algorithm if the preceding algorithm _passed_ (this is done
in the `c++` class for the algorithm by returning `StatusCode::SUCCESS`).

This default can be overridden by setting `GaudiSequencer.IgnoreFilterPassed`
to `True`, which will run all the algorithms regardless of whether the preceding
one passed or failed. The list of algorithms to run is defined by the
`GaudiSequencer.Members` list.


### Difference between `MainSequence` and `UserAlgorithms`
* `MainSequence`: Use `DaVinci().addToMainSequence([<a list of algorithms>])`
  to customize the initialization of `DaVinci`. This should be used to provide
  custom functions/TESs[^2] that will be visible to all selection algorithms.

* `UserAlgorithms`: Actual selection algorithms. This is always appended at the
  end of the `MainSequence` of a `DaVinci` session.


[^2]: TES: Transient Event Storage.


### Difference `CC` and `cc` in a decay descriptor
* `LoKi` and `DecayTreeTuple` use uppercase `CC` for charge conjugation.
* `CombineParticles` uses lowercase `cc`.

This is just an inconsistency in the `DaVinci` code base and there's nothing we
can do as a user.


### `TIS` functor
`TIS` is a (undocumented) `LoKi` functor， and it stands for _Trigger
Independent Signal_. There's another similar term: _TOS: Trigger On Signal_.

#### Functor usage
```
TIS(<trigger_line_to_look>, <trigger_decision_storage_location>)
```

!!! note
    `<trigger_decision_storage_location>` is a `TES` location

#### An example from _lhcb-ana-2014-052-v2r1_

```python
INTREE((ABSID == 'mu+') & (TIS('L0.*', 'L0TriggerTisTos')))
```

The line above should be interpreted as following:

1. In the decay tree, find a $\mu$.
2. We look over all `L0.*` trigger lines with `TES` `L0TriggerTisTos`, and
   require to have a trigger independent signal:
    - Since we are triggering on $\mu$, this requires that the trigger cannot
      be due to the $\mu$.
    - Also note that the whole decay tree is just a $\mu$ and a $D$, so it
      means that we are either TOS on $D$, TIS in the **whole** event, or both.

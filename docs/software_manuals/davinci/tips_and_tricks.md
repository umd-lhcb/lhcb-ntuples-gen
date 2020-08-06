## Running old DaVinci on the GRID

The run 1 $R(D^{(*)})$ analysis used DaVinci/v36r1p2. To run that on lxplus7 nodes:

1. Export the following environmental variables to use old runtime:

    ```
    export CMTCONFIG=x86_64-slc6-gcc48-opt
    ```

2. Run old DaVinci with `lb-run`:

    ```
    lb-run DaVinci/v36r1p2 gaudirun.py
    ```


## About `GaudiSequencer`
`GaudiSequencer` is an _per-event algorithm_, such as `DecayTreeTuple`, in the
sense that `Gaudi` knows that it should run on every event.

`GaudiSequencer` is used to chain related algorithms, and it's default behavior
is to only run an algorithm if the preceding algorithm _passed_ (this is done
in the `c++` class for the algorithm by returning `StatusCode::SUCCESS`).

This default can be overridden by setting `GaudiSequencer.IgnoreFilterPassed`
to `True`, which will run all the algorithms regardless of whether the preceding
one passed or failed. The list of algorithms to run is defined by the
`GaudiSequencer.Members` list.


## Difference between `MainSequence` and `UserAlgorithms`
* `MainSequence`: Use `DaVinci().addToMainSequence([<a list of algorithms>])`
  to customize the initialization of `DaVinci`. This should be used to provide
  custom functions/TESs[^2] that will be visible to all selection algorithms.

* `UserAlgorithms`: Actual selection algorithms. This is always appended at the
  end of the `MainSequence` of a `DaVinci` session.


[^2]: TES: Transient Event Storage.


## Difference `CC` and `cc` in a decay descriptor
* `LoKi` and `DecayTreeTuple` use uppercase `CC` for charge conjugation.
* `CombineParticles` uses lowercase `cc`.

This is just an inconsistency in the `DaVinci` code base and there's nothing we
can do as a user.

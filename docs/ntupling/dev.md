## Local development of in-house Python packages
We have made several in-house Python packages, for example:

- [`pyBabyMaker`](https://github.com/umd-lhcb/pyBabyMaker): For producing step-2 ntuples.
- [`pyTuplingUtils`](https://github.com/umd-lhcb/pyTuplingUtils): For simple plotting and cutflow study.

These two packages are included as submodules in this project, so that:

1. We can pinpoint a specific commit of these packages.
2. The development of these packages are often related to this project.
    Including them as submodules makes development easier.

### Initializing `pyBabyMaker` and `pyTuplingUtils` submodules

After initial clone of this project, these submodules can be initialized with:
```
git submodule update --init
```

!!! info
    The `git submodule` only record the pointer to a commit of each submodule,
    no actual content is recorded in the mother project.

    For example, in `lhcb-ntuples-gen`, we only record that `pyBabyMaker`
    should be at commit `a7bb2981`. When we do `submodule update --init`,
    `git` will clone the module and checkout said commit.

### Local development procedure

1. `cd` into the submodule that you want to develop, here we use `pyBabyMaker`
    as an example:

    ```
    cd lib/python/pyBabyMaker
    ```

2. Checkout the `master` branch with `git checkout master`[^1]
3. Do development, and when you want to test something, go back to
    `lhcb-ntuples-gen` project root, and:

    ```
    make install-dep
    ```

    This will install the latest `pyBabyMaker`, with your local changes.

4. Test everything out.
5. After everything works out:
    1. Commit changes inside the `pyBabyMaker` directory.
    2. Inside `pyBabyMaker` directory, push changes to `pyBabyMaker` remote.
    3. Go back to project root, Update pointer to the `pyBabyMaker` commit in
        the mother project.


[^1]: This operation is only valid for newer `git`. Make sure you use an up-to-date `git`!


## `Makefile`
In the [`Makefile`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/Makefile),
we define targets to generate output files and results, such as:

- Step 2 ntuple
- Cutflow study tables

However, `make` rules can be arcane, so if you want to figure out how `make`
would produce a certain target:
```
make --dry-run --always-make <target_name>
```

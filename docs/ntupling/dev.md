## Installing `pyenv` for Python development

We recommend `pyenv` to manage your Python versions and virtual environments.
The two main advantage of using `pyenv`, instead of the Python that comes with
your systems are:

1. No Python package is installed globally to your system Python, this prevents
   conflicting packages to break your system
2. Different versions of the same package can co-exist in different virtual
   environments, making this setup more flexible

First, follow [this instruction](https://github.com/pyenv/pyenv#installation)
to install `pyenv`.

Then, follow [this instruction](https://github.com/pyenv/pyenv-virtualenv#installation)
to install `pyenv-virtualenv`


!!! note
    - Microsoft Windows not supported!
    - If you are using macOS, you can use `homebrew` to install both. Though
      the change in shell configuration file is still needed.
    - Don't forget to change your shell configuration file **manually** after
      installation!
    - After installation, restart your shell.


## Create a virtual environment

First, install a specific version of Python (Python 3.7.7 used here):
```
pyenv install 3.7.7
```

Then create a virtualenv:
```
pyenv virtualenv 3.7.7 ntuples
```

Now go to the project root, and set the local python version:
```
pyenv local ntuples
```

Now, every time you `cd` into the project root, virtual environment `ntuples`
will be automatically activated.


## Local development of in-house Python packages
We have made two in-house Python packages:

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
    2. Optionally, inside `pyBabyMaker` directory, push changes to `pyBabyMaker` remote.
    3. Go back to project root, Update pointer to the `pyBabyMaker` commit in
        the mother project.


[^1]: This operation is only valid for newer `git`. Make sure you use an up-to-date `git`!

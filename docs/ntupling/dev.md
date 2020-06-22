## Installing `pyenv`

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

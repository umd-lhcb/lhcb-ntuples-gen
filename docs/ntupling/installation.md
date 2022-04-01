!!! note
    Before proceeding, send Yipeng or Manuel an [SSH key](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/checking-for-existing-ssh-keys)
    to your system so that we can give you read/write
    permission to `julian`, the `git-annex` server where our ntuples are stored.

Clone the repository and set up the `annex` component[^1].
We have a private server, `julian`, that hosts `git-annex` files.

```shell
git clone git@github.com:umd-lhcb/lhcb-ntuples-gen
cd lhcb-ntuples-gen
#git remote add julian git@129.2.92.92:lhcb-ntuples-gen  # not needed unless you want to copy to julian
git remote add glacier git@10.229.60.85:lhcb-ntuples-gen
git annex init --version=7
git submodule update --init  # Do this before git annex sync to avoid potential mess-up of submodule pointers!
git annex sync

# It is higly recommended to install nix now before proceed! See below for some pointers on how to do it
# If you have nix installed:
#   nix develop
make install-dep
```

Note that these commands will only initialize the files controlled by `git-annex` (several GB in total)
with symbolic links. You typically will download individual files as you need them with
```
git annex get <path_to_file>
```

The set up above also installs in the `lib/python/` folder `pyBabyMaker`,
`pyTuplingUtils`, and other packages that are needed.
Each commit of `lhcb-ntuples-gen` points to specific commits of these packages.
Thus, every time you pull new code in `lhcb-ntuples-gen`, you need to make sure
you have the appropriate commits of the other packages installed with
```
git pull
git submodule update --init --recursive
make install-dep
```

## Install `docker` to run `DaVinci` locally

We use `docker` to run a pre-built `DaVinci` image locally. To install
`docker`:

On Arch Linux run `sudo pacman -S docker` and follow this [Arch wiki entry](https://wiki.archlinux.org/index.php/Docker)
to finish the setup. In macOS, you can install it using homebrew with `brew install docker`

Now it's time to pull (download) the pre-built `DaVinci` docker:
```
docker pull umdlhcb/lhcb-stack-cc7:DaVinci-{{ davinci_sl_ver }}
```


## Install `nix`

All of our C++ dependencies are installed with `nix`. To install `nix`, refer
to [the guide](https://github.com/umd-lhcb/root-curated#install-nix-on-macos)
in `root-curated` repo.

!!! warning
    `nix develop` also provides a Python virtualenv. It is located in
    `.virtualenv` in project root.

    If a major update in `nixpkgs` occurs, Python may also get a significate
    update (e.g. Python 3.8 -> Python 3.9). In this case, the virtualenv may
    stop working.

    In any case, if you see any weired Python problem, simply delete the
    `.virtualenv` folder, then run `nix develop` again: A new virtualenv will
    be re-created.


## `babymaker` code

`babymaker` is part of the `pyBabyMaker` Python package. It requires
`python3` and a couple of `Python` dependencies[^3].

!!! note
    It is strongly recommended to install `clang-format`[^4], so the generated
    `C++` code looks much nicer.

`pyBabyMaker` is included in this project as a submodule. If you follow the
project initialization procedure listed at the beginning of this instruction,
you should already have it installed.

!!! info
    For more info on local development of in-house Python modules (included as
    submodules), refer to [this guide](./dev.md#local-development-of-in-house-python-packages).

## Install VCS (`git` and `git-annex`)

We use `git` to version-control the ntupling code and the wiki, and `git-annex` to version-control
large files, mostly the input `.dst` files or important `.root` outputs. For more details on
`git-annex`, see [this brief introduction](../software_manuals/git_annex.md).

- On Arch Linux, simply issue the following command to install both programs:
    ```
    sudo pacman -S git git-annex
    ```

- On macOS, if you have `homebrew` installed:
    ```
    brew install git git-annex
    ```


[^1]: Windows filesystems don't support symbolic links, which
      makes `git-annex` almost unusable.

      Please use WSL or WSL2, and make sure the project is stored on a Linux
      file system!

[^2]: `gcc` must be recent enough to support `c++17` standard. Effectively,
      `gcc6` or `clang5` (or newer) is required.

      In reality, you typically don't need to worry about this, as
      `nix develop` will prepare you a shell with almost all tools needed for
      this project.

[^3]: These dependencies are listed in `<project_root>/requirements.txt`. It is
      highly recommended to install `pip` to manage Python packages.

      Note that `pyBabyMaker` doesn't rely on ROOT at all.

      It is also highly recommended to use `pyenv` and `pyenv-virtualenv` to
      manage Python enviroments. Please google the installation instructions
      for your OS.

[^4]: `clang-format` usually comes with `clang`. A notable exception is on
      macOS. In that case, just type in `brew install clang-format`.

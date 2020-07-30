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

!!! note
    Before proceed, send us a SSH key so that we can give your read/write
    permission to the `git-annex` server.

Now clone the repository and set up the `annex` component. We have a private server, `julian`, that hosts
`git-annex` files.
```
git clone git@github.com:umd-lhcb/lhcb-ntuples-gen
cd lhcb-ntuples-gen
git remote add julian git@129.2.92.92:lhcb-ntuples-gen
git annex init --version=7
git annex sync julian
```

Note that these commands will only initialize the files controlled by `git-annex` (several GB in total)
with symbolic links. You typically will download individual files as you need them with
```
git annex get <path_to_file>
```


!!! warning "Microsoft Windows not supported, require pre-build image below"
    Windows filesystems don't support symbolic links, which
    makes `git-annex` almost unusable.

    Please use the pre-built image listed in [this section](#use-a-pre-built-virtualbox-image-on-windows) that
    has everything installed.  Note that `VirtualBox` needs to be installed on Ubuntu manually first.

    Alternatively, use WSL or WSL2.



## Install `docker` to run `DaVinci` locally
We use `docker` to run a pre-built `DaVinci` image locally. To install
`docker`:

On Arch Linux run the command below and follow this [Arch wiki entry](https://wiki.archlinux.org/index.php/Docker)
to finish the setup:
```
sudo pacman -S docker
```

On macOS, with `homebrew`:
```
brew install docker
```

Now it's time to pull (download) the pre-built `DaVinci` docker:
```
docker pull umdlhcb/lhcb-stack-cc7:DaVinci-v45r3-SL
```


## Install `babymaker`
`babymaker` is part of the `pyBabyMaker` `Python` package. It requires
`gcc`[^1], `ROOT`, `python3`, and a couple of other `Python` packages[^2].

!!! note
    It is strongly recommended to install `clang-format`[^3], so the generated
    `C++` code looks much nicer.

`pyBabyMaker` is included in this project as a submodule. After cloning this
project for the first time, initialize the submodules with:

```
git submodule update --init
```

Then `pyBabyMaker` can be installed with:
```
make install-dep
```

!!! note
    `make install-dep` will also install `pyTuplingUtils`, a pure `Python`
    library for simple plotting and cutflow study.


[^1]: `gcc` must be recent enough to support `c++17` standard. Effectively,
      `gcc 6` or newer is required.
[^2]: These packages are listed in `<project_root>/requirements.txt`. It is
      highly recommended to install `pip` to manage `Python` packages.

      It is also highly recommended to use `pyenv` and `pyenv-virtualenv` to
      manage `Python` enviroments. Please google the installation instructions
      for your OS.
[^3]: `clang-format` usually comes with `clang`. A notable exception is on
      macOS. In that case, just type in `brew install clang-format`.


## Use a pre-built `VirtualBox` image on Windows
The pre-built `VirtualBox` image is based on Arch Linux.
It contains `git`, `git-annex`;
`docker` (`DaVinci` image _not_ downloaded);
all `babymaker` dependencies (`Python` packages _not_ installed);
`sublime` text editor.

To use the virtual machine image, Please follow these steps on Microsoft
Windows:

1. Download and install the latest `VirtualBox` from [here](https://www.virtualbox.org/wiki/Downloads).
2. Download the pre-built image from [here](https://www.dropbox.com/sh/zyohmvod41pc4oc/AAACD1LOaRjiVM-YdkdLzd_Ca?dl=0)
   (choose the latest date, then download both `.ovf` and `.vmdk` files).
3. Launch `VirtualBox`, click **Tools**, then click **Import**, choose the `ovf`
   file, then proceed with default settings.

!!! info
    Both the username and password of the virtual machine are `vagrant`.

!!! info
    By default the virtual machine can maximally use 4 GB of RAM. If your
    computer has 16 GB or more RAM, it is recommended to allocate 8 GB of RAM
    to the virtual machine.

!!! info
    The virtual machine image already has `docker` installed.

!!! info
    As you may have guessed, the virtual machine image has `gcc`[^1], `ROOT`, `python3`, and a couple
    of other `Python` packages[^2], already installed, including `pip`.

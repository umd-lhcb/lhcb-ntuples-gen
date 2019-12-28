## Install VCS (`git` and `git-annex`)

We use `git` to version-control the ntupling code and the wiki, and `git-annex` to version-control
large files, mostly the input `.dst` files or important `.root` outputs. For more details on
`git-annex`, see [this brief introduction](software_manuals/git_annex).

On Arch Linux, simply issue the following command to install both programs:
```
sudo pacman -S git git-annex
```

On macOS, if you have `homebrew` installed:
```
brew install git git-annex
```

Now clone the repository and set up the `annex` component. We have a private server, `julian`, that hosts
`git-annex` files. You will need to send us a SSH key so that we can give your read/write permission to the
server.
```
git clone git@github.com:umd-lhcb/lhcb-ntuples-gen
cd lhcb-ntuples-gen
git remote add julian git@129.2.92.92:lhcb-ntuples-gen
git annex init --version=7
git annex sync --no-pull julian
git annex sync julian
```
Note that these commands will only initialize the files controlled by `git-annex` (several GB in total)
with symbolic links. You typically will download individual files as you need them with
```
git annex get <path_to_file>
```


!!! warning "Microsoft Windows and Ubuntu not supported, require pre-build image below"
    Windows filesystems don't support symbolic links, which
    makes `git-annex` almost unusable. In Ubuntu there is no easy way to install an up-to-date `git-annex`.

    Please use the pre-built image listed in [this section](#use-a-pre-built-virtualbox-image-on-windows) that
    has everything installed.  Note that `VirtualBox` needs to be installed on Ubuntu manually first.



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
docker pull umdlhcb/lhcb-stack-cc7:DaVinci-v42r8p1-SL
```


## Install dependencies for `babymaker`
`babymaker` is part of the `pyBabyMaker` `Python` package. It requires
`gcc`[^1], `ROOT`, `python3`, and a couple of other `Python` packages[^2].

!!! note
    It is strongly recommended to install `clang-format`[^3], so the generated
    `C++` code looks much nicer.

Install these tools with your choice of package manager. To install
`pyBabyMaker` and other required `Python` packages, you can use the following
command:
```
pip3 install -r --user requirements.txt
```


[^1]: `gcc` must be recent enough to support `c++17` standard. Effectively,
      `gcc 6` or newer is required.
[^2]: These packages are listed in `<project_root>/requirements.txt`. It is
      highly recommended to install `pip` to manage `Python` packages.

      It is also highly recommended to use `pyenv` and `pyenv-virtualenv` to
      manage `Python` enviroments. Please google the installation instructions
      for your OS.
[^3]: `clang-format` usually comes with `clang`. A notable exception is on
      macOS. In that case, just type in `brew install clang-format`.


## Install dependencies for plotting
The comparison plots in this [page]() require `pyTuplingUtils`, which is install as follows
```
git clone git@github.com:umd-lhcb/pyTuplingUtils
cd pyTuplingUtils/
python3 setup.py build
python3 setup.py install
```

## Use a pre-built `VirtualBox` image on Windows and Ubuntu
The pre-built `VirtualBox` image is based on Arch Linux.
It contains `git`, `git-annex`;
`docker` (`DaVinci` image _not_ downloaded);
all `babymaker` dependencies (`Python` packages _not_ installed);
`sublime` text editor.

To use the virtual machine image, Please follow these steps on Microsoft
Windows:

1. Download and install the latest `VirtualBox` from [here](https://www.virtualbox.org/wiki/Downloads).
2. Download the pre-built image from [here](https://www.dropbox.com/sh/83deuk98mb8ckxi/AAAXUIuqiXN6_atuDzx5Whm6a?dl=0) (download both `.ovf` and `.vmdk` files).
3. Launch `VirtualBox`, click **Tools**, then click **Import**, choose the `ovf`
  file, then proceed with default settings.

!!! note
    Both the username and password of the virtual machine are `vagrant`.

!!! note
    By default the virtual machine can maximally use 4 GB of RAM. If your
    computer has 16 GB or more RAM, it is recommended to allocate 8 GB of RAM
    to the virtual machine.
    
!!! note
    The virtual machine image already has `docker` installed.

!!! note
    As you may have guessed, the virtual machine image has `gcc`[^1], `ROOT`, `python3`, and a couple
    of other `Python` packages[^2], already installed, including `pip`.


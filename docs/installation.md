## Install VCS
On Arch Linux, simply issue the following command:
```
sudo pacman -S git git-annex
```

On macOS, if you have `homebrew` installed:
```
brew install git git-annex
```

!!! warning "Microsoft Windows not supported"
    This is because Windows filesystems don't support symbolic links, which
    makes `git-annex` almost unusable.

    If you are a Windows user, please follow [this section](#use-a-pre-built-virtualbox-image-on-windows)
    to set up a Linux virtual machine that has everything installed.

!!! warning "Ubuntu not supported"
    This is because there is no easy way to install an up-to-date `git-annex`.

    Please use the same pre-built image listed in [this section](#use-a-pre-built-virtualbox-image-on-windows).
    Note that `VirtualBox` needs to be installed on Ubuntu manually first.


## Install dependencies for `DaVinci`
We use `docker` to run a pre-built `DaVinci` image locally. To install
`docker`:

On Arch linux:
```
sudo pacman -S docker
```
then follow this [Arch wiki entry](https://wiki.archlinux.org/index.php/Docker)
to finish setup.

On macOS, with `homebrew`:
```
brew install docker
```

!!! note
    The virtual machine image already has `docker` installed.

Now it's time to pull (download) the pre-built `DaVinci` docker:
```
docker pull umdlhcb/lhcb-stack-cc7:DaVinci-v42r8p1-SL
```


## Install dependencies for `babymaker`
`babymaker` requires `gcc`[^1], `ROOT`, `clang-format`[^2], `python3`, and a
couple of `Python` packages[^3].

!!! note
    As you may have guessed it, the virtual machine image has these packages
    installed (including `pip`).

Install these tools with your choice of package manager. To install python
packages, you can use the following command:
```
pip install -r --user requirements.txt
```


[^1]: `gcc` must be recent enough to support `c++17` standard. Effectively,
      `gcc 6` or newer is required.
[^2]: `clang-format` usually comes with `clang`. A notable exception is on
      macOS. In that case, just type in `brew install clang-format`.
[^3]: These packages are listed in `<project_root>/requirements.txt`. It is
      highly recommended to install `pip` to manage `Python` packages.

      It is also highly recommended to use `pyenv` and `pyenv-virtualenv` to
      manage `Python` enviroments. Please google the installation instructions
      for your OS.


## Use a pre-built `VirtualBox` image on Windows
The pre-built `VirtualBox` image is based on Arch Linux.
It contains `git`, `git-annex`;
`docker` (`DaVinci` image _not_ downloaded);
all `babymaker` dependencies (`Python` packages _not_ installed);
`sublime` text editor.

To use the virtual machine image, Please follow these steps on Microsoft
Windows:

1. Download and install the latest `VirtualBox` from [here](https://www.virtualbox.org/wiki/Downloads).
2. Download the pre-built image from [here](https://www.dropbox.com/sh/xfioontn9auv081/AADK5wflwcKy8GA_FD6Xa7Joa?dl=0) (download both `.ovf` and `.vmdk` files).
3. Launch `VirtualBox`, click **Tools**, then click **Import**, choose the `ovf`
  file, then proceed with default settings.

!!! note
    Both the username and password of the virtual machine are `vagrant`.

!!! note
    By default the virtual machine can maximally use 4 GB of RAM. If your
    computer has 16 GB or more RAM, it is recommended to allocate 8 GB of RAM
    to the virtual machine.

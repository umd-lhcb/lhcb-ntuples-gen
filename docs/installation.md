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


## Install dependencies for `babymaker`


## Use a pre-built `VirtualBox` image on Windows
Please following these steps:

* Download and install the latest `VirtualBox` from [here](https://www.virtualbox.org/wiki/Downloads).
* Download the pre-built image from [here](https://www.dropbox.com/sh/xfioontn9auv081/AADK5wflwcKy8GA_FD6Xa7Joa?dl=0) (download both `.ovf` and `.vmdk` files).
* Launch `VirtualBox`, click **Tools**, then click **Import**, choose the `ovf`
  file, and proceed with default settings.

!!! note
    By default the virtual machine can maximally use 4 GB of RAM. If your
    computer has 16 GB or more RAM, it is recommended to allocate 8 GB of RAM
    to the virtual machine.

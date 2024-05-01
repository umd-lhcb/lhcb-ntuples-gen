It is harder to manage large (100 MB or more) files in `git`, as checking them
in/out would take a much longer time. Also, it is undesirable to expose raw
data outside of the collaboration.

We use a `git` addon, `git-annex`, to manage large files. `git-annex` stores all
tracked files under `<project_root>/.git/annex`, and link/copy these files to
the expected locations.

A typical workflow to add a file to the `annex`, commit it, and sync the remotes, is
```
git annex add <file>  ## Moves file to the annex, and replaces it with a soft link in the git repo
git add <file>
git commit -m "Committed <file> (well, a soft link to it)"
git push
git annex copy --to glacier <file>  ## Copies the actual file to glacier
## Make sure you do not have uncommitted changes in the repo, because the sync commits everything
git annex sync 
```

## Initialize `git-annex` repository

!!! info "Before you proceed"
    This needs to be done **only once** for each repository!

We have a private server[^1] that hosts `git` repositories with `git-annex`
capabilities.
After cloning the `umd-lhcb/lhcb-ntuples-gen` repository from github, add our private repository:
```
git remote add julian git@129.2.92.92:lhcb-ntuples-gen
```

!!! note
    Please send us a SSH key so that we can give your read/write permission on
    the `git-annex` repository.

Then we need to initialize the `annex` component:
```
git annex init --version=7
```

!!! warning
    It is important to use a `git-annex` repository of `v7` or newer![^2]

    To upgrade your `git-annex` repository to at least `v7`, issue the
    following command inside your `git` repository:
    ```
    git annex upgrade
    ```

!!! note
    Dropbox will not synchronize any symbolic links, so if the repository is
    placed within your Dropbox folder, and you have multiple computers, the
    symbolic links will be replaced by the actual files on all but the initial
    computers.


[^1]: As of now, the server is sitting on Yipeng's desktop. It is named
      `Julian`, after [Julian Schwinger](https://en.wikipedia.org/wiki/Julian_Schwinger).
[^2]: Please read [this](https://git-annex.branchable.com/tips/unlocked_files/) for the rationale.


## Add files
If you are adding large files that are unlikely to change in the future, such
as `.dst` data files, use the following command:
```
git annex add <path_to_file>
```

!!! note
    **You typically don't need this. It is left here for completeness.**

    `git add` will add files to the `git` repository, **not** `git-annex`
    repository **by default**. Configuration is required to add only `.root`
    files to `git-annex`, and the rest to `git`. This has been done for this
    repository, in:
    ```
    <project_root>/.gitattributes
    ```

    See [this article](https://git-annex.branchable.com/tips/largefiles/)
    for more information on configuring `.gitattributes`.


## Change the content of annexed files
Files added via `git annex add` are read only. For example:
```
echo change > <path_to_annexed_file>
> bash: <annexed_file>: Permission denied
```

To change them, we need to unlock them first:
```
git annex unlock <path_to_annexed_file>
```

Now you can edit the unlocked file as you wish. After editing, use
`git annex add` to keep the changes and lock it again.

!!! note
    When you commit, `git-annex` will notice that you are committing an
    unlocked file, add its new content.
    A pointer to that content is what gets committed to `git`; the actual
    content will go to `git-annex`.

!!! warning
    If you don't need to modify the file after all, or want to discard
    modifications, use `git annex lock`.
    Doing so will result in all modifications discarded. Proceed with care!


Files added via `git add` can be changed just like a regular file.


## Change the name of annexed files
Once a file has been annexed with `git annex add`, the actual file will be
moved automatically by `git-annex` inside `.git` folder in your project, and
`git-annex` will create a symbolic link in-place pointing to that file.

So, if you just want to **rename** the annexed file, **without changing its
content**, just view that symbolic link as a regular file added to `git`.

!!! example
    Consider the following example:

    1. Place `a.root` in `folderA/a.root`.
    2. Annex the file with:
        ```
        git annex add folderA/a.root
        ```
    3. Now `folderA/a.root` will be just a symbolic link, and the actual root
       file is placed in `.git` in your project root
    4. Suppose you want to rename `a.root` to `b.root`. In this case, you can:
        ```
        mv folderA/a.root folderA/b.root
        git add folderA/a.root folderA/b.root  # <-- We are not using annex here!!!
        git commit -a
        ```


## Synchronize files between local and remote repositories

First check that you have committed all changes:
```
git status
```

Make sure **NO** entry looks like this:
```
changes not staged for commit
```

If there are uncommitted local changes, commit then and write sensible
messages. This way, `git annex sync` won't make unwanted commits!

!!! info "Before you proceed"
    Do `git pull origin master` to get latest changes from `origin` first.

Now, you can do this:
```
git annex sync
```

!!! note
    The command above doesn't download the actual data; rather, it only download
    the metadata so that `git annex` _knows_ how to download the actual data.

    The command above will also make sure your local `master` is now identical
    to remote `master`. That's why it's better to do `git pull origin master`
    beforehand to avoid surprises.

!!! error
    By default, `git annex sync` will commit **all previously uncommitted**
    changes before synchronizing!

    This can be disabled on a per-repository basis by:
    ```
    git annex config --set annex.autocommit false
    ```

    Other clones will also be configured properly after they do a:
    `git annex sync`.



If you want to download **every single file** from the `git-annex` repo (which is
probably a couple of GBs), add the `--content` flag in the second step and
download not only the metadata, but also the data:
```
git annex sync --content julian
```


## Download and upload individual files

Downloading is simple:
```
git annex get <path_to_files>
```

So is uploading:
```
git annex copy --to julian <path_to_files>
git annex sync
```

## Drop local files

The following command will remove the local copy of the file **only**, and will
not delete the file from remote[^3]:
```
git annex drop <path_to_files>
```

!!! note
    `git` would still think the working directory is clean, i.e. no change has
    been made.


[^3]: **Deleting files from remote is dangerous!** As the remote might be the
      last copy of the file so we may lose the file permanently.

      Still, if you insist, please refer to the [official guide](https://git-annex.branchable.com/tips/deleting_unwanted_files).


## Check annexed file size

For a single file this can be done via `git annex info`. For example:
```
$ git annex info ntuples/pre-0.9.0/Dst-std/Dst--19_09_05--std--data--2012--md.root
file: ntuples/pre-0.9.0/Dst-std/Dst--19_09_05--std--data--2012--md.root
size: 1.8 gigabytes
key: SHA256E-s1800364650--cb5222668f21032b81ede5f18eb86026e21188c54441917258e8aad4d072f791.root
present: false
```

For directories, we have a home-made wrapper script `scripts/count_root_files.py`. For example:
```
$ ./scripts/count_root_files.py ntuples
   2 .root   total: 171.30 MiB   local:   0.00 KiB   ntuples/0.9.1-partial_refit
   2 .root   total: 171.30 MiB   local:   0.00 KiB   ntuples/0.9.1-partial_refit/Dst_D0-cutflow_mc
   5 .root   total:  47.49 GiB   local:   0.00 KiB   ntuples/ref-rdx-run1
   1 .root   total: 397.92 MiB   local:   0.00 KiB   ntuples/ref-rdx-run1/Dst-mc
   1 .root   total:  29.62 GiB   local:   0.00 KiB   ntuples/ref-rdx-run1/D0-mix
   1 .root   total:   1.70 GiB   local:   0.00 KiB   ntuples/ref-rdx-run1/Dst-std
   1 .root   total:   1.60 GiB   local:   0.00 KiB   ntuples/ref-rdx-run1/D0-std
   1 .root   total:  14.18 GiB   local:   0.00 KiB   ntuples/ref-rdx-run1/Dst-mix
   2 .root   total:   0.98 GiB   local:   0.00 KiB   ntuples/0.9.0-cutflow
   2 .root   total:   0.98 GiB   local:   0.00 KiB   ntuples/0.9.0-cutflow/Dst-cutflow_mc
   7 .root   total:  37.90 GiB   local:   0.00 KiB   ntuples/pre-0.9.0
   2 .root   total:  46.24 MiB   local:   0.00 KiB   ntuples/pre-0.9.0/Dst-cutflow_mc
   2 .root   total:  17.50 GiB   local:   0.00 KiB   ntuples/pre-0.9.0/Dst-cutflow_data
   1 .root   total: 179.56 MiB   local:   0.00 KiB   ntuples/pre-0.9.0/Dst-mc
   2 .root   total:  20.19 GiB   local:   0.00 KiB   ntuples/pre-0.9.0/Dst-std
```

!!! info
    If you are in the `nix` shell, `count_root_files.py` is added to PATH so
    you can call it directly.


## Check annexed file availability

We can use `git annex list` for this. For example:
```
$ git annex list ntuples/0.9.0-cutflow
here
|Julian
||origin
|||web
||||bittorrent
|||||
_X___ ntuples/0.9.0-cutflow/Dst-cutflow_mc/Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root
_X___ ntuples/0.9.0-cutflow/Dst-cutflow_mc/Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root
```

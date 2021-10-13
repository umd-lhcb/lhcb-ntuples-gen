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


## Workflows

Each analysis can have many workflows. For example RDX run 2 has
`rdx.py` and `rdx_cutflows.py` in the `workflows` folder.

!!! example

    In `rdx.py`, we have:

    ```python
    JOBS = {
        # Run 2
        'rdx-ntuple-run2-data-oldcut': lambda name: workflow_data(
            name,
            '../ntuples/0.9.4-trigger_emulation/Dst_D0-std',
            '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
            executor=executor
        ),
        'rdx-ntuple-run2-mc-demo': lambda name: workflow_mc(
            name,
            '../run2-rdx/samples/Dst_D0--21_07_30--mc--Bd2DstMuNu--2016--md--py8-sim09j-dv45-subset.root',
            '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
            output_ntp_name_gen=parse_step2_name,
            executor=executor
        ),
        # Run 1
        'rdx-ntuple-run1-data': lambda name: workflow_data(
            name,
            '../ntuples/0.9.2-2011_production/Dst_D0-std',
            '../postprocess/rdx-run1/rdx-run1.yml',
            use_ubdt=False,
            executor=executor
        ),
        'ref-rdx-ntuple-run1-data': lambda name: workflow_data(
            name,
            '../ntuples/ref-rdx-run1/Dst-mix',
            '../postprocess/ref-rdx-run1/rdst-2011-mix.yml',
            use_ubdt=False,
            output_ntp_name_gen=parse_step2_name,
            executor=executor
        )
    }
    ```

    The actual workflows are defined earlier in the same file.


## External programs used by workflows

### Greg's $\mu$ UBDT adder

The name of the program is `addUBDTBranch`. It's source code, along with its
`Makefile`, is available [here](https://github.com/umd-lhcb/MuonBDTPid/tree/master/src).

Let's back track on how it is made available in our `lhcb-ntuples-gen` environment:

1. In this project's [`flake.nix`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/flake.nix),
we have:

    ```nix
    # snippet only

    inputs = {
      nixpkgs = ...;  # software foundation, including compiles, etc.
      MuonBDTPid.url = "github:umd-lhcb/MuonBDTPid";
    };

    outputs = { nixpkgs, MuonBDTPid, ... }:
        let
          pkgs = import nixpkgs {
            # We make packages defined in MuonBDTPid's overlay available
            overlays = [ MuonBDTPid.overlay ];
          };
        in
        {
          devShell = pkgs.mkShell {
            buildInputs = [
              pkgs.addUBDTBranchWrapped  # Install UBDT adder
            ];
          };
        }
    ```

2. What we learned is that the UBDT adder is defined in `MuonBDTPid`'s
   [overlay](https://github.com/umd-lhcb/MuonBDTPid/blob/master/nix/overlay.nix).
   Let's inspect its content:

    ```nix
    final: prev:

    {
      root5-ubdt = prev.callPackage ./root5 {
        inherit (prev.darwin.apple_sdk.frameworks) Cocoa OpenGL;
        stdenv = if prev.stdenv.cc.isClang then prev.llvmPackages_5.stdenv else prev.gcc8Stdenv;
      };

      addUBDTBranch = prev.callPackage ./addUBDTBranch {
        root = final.root5-ubdt;
        stdenv = if prev.stdenv.cc.isClang then prev.llvmPackages_5.stdenv else prev.gcc8Stdenv;
      };

      addUBDTBranchWrapped = prev.writeScriptBin "addUBDTBranch" ''
        unset LD_LIBRARY_PATH
        unset DYLD_LIBRARY_PATH
        exec ${final.addUBDTBranch}/bin/addUBDTBranchRun2 $@
      '';
    }
    ```

    1. Now we see `addUBDTBranchWrapped` is just a shell script that wraps
       around the executables in `addUBDTBranch`.

        The reason is that when you make ROOT available in a `devShell`, on
        Linux it will set `LD_LIBRARY_PATH` environment variable, which will
        mess up with the `addUBDTBranch` executables. We need to unset it
        first.

    2. Also, `addUBDTBranch` has an input called `root`, which is explicitly
       set to a patched version of ROOT 5 that contains UBDT.

3. Finally, the actual derivation (directive on how to compile it with `nix`) of
   `addUBDTBranch` is defined [here](https://github.com/umd-lhcb/MuonBDTPid/blob/master/nix/addUBDTBranch/default.nix).
   It is actually quite simple but we won't go over it here.

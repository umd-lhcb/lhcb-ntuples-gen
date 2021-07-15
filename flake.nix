{
  description = "ntuple generation with DaVinci and babymaker.";

  inputs = {
    root-curated.url = "github:umd-lhcb/root-curated";
    nixpkgs.follows = "root-curated/nixpkgs";
    flake-utils.follows = "root-curated/flake-utils";

    MuonBDTPid.url = "github:umd-lhcb/MuonBDTPid";
  };

  outputs = { self, nixpkgs, flake-utils, root-curated, MuonBDTPid }:
    {
      overlayPython = import ./nix/overlay-python.nix;
      overlayMkDoc = import ./nix/overlay.nix;
    } //
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config = { allowUnfree = true; };
          overlays = [
            root-curated.overlay
            MuonBDTPid.overlay
            #self.overlayPython
            #self.overlayMkDoc
          ];
        };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
      in
      {
        devShell = pkgs.mkShell {
          name = "lhcb-ntuples-gen";
          buildInputs = with pythonPackages; [
            # for documentation (broken on macOS)
            #pkgs.mkdocs-material

            pkgs.clang-tools # For clang-format
            pkgs.root

            # UBDT adder
            pkgs.addUBDTBranchWrapped

            # Auto completion
            jedi

            # Linters
            flake8
            pylint

            # Python requirements (enough to get a virtualenv going).
            virtualenvwrapper
          ];

          FONTCONFIG_FILE = pkgs.makeFontsConf {
            fontDirectories = with pkgs; [
              corefonts
            ];
          };

          shellHook = ''
            # Allow the use of wheels.
            SOURCE_DATE_EPOCH=$(date +%s)
            VENV=./.virtualenv

            if test ! -d $VENV; then
              virtualenv $VENV
            fi
            source $VENV/bin/activate

            # allow for the environment to pick up packages installed with virtualenv
            export PYTHONPATH=$VENV/${python.sitePackages}/:$PYTHONPATH

            # fix libstdc++.so not found error
            export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH

            # Update PATH
            export PATH=$(pwd)/test:$(pwd)/tools:$(pwd)/ganga:$(pwd)/scripts:$PATH
          '';
        };
      });
}

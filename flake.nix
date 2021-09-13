{
  description = "ntuple generation with DaVinci and babymaker.";

  inputs = {
    root-curated.url = "github:umd-lhcb/root-curated";
    nixpkgs.follows = "root-curated/nixpkgs";
    flake-utils.follows = "root-curated/flake-utils";

    MuonBDTPid.url = "github:umd-lhcb/MuonBDTPid";
    hammer-reweight.url = "github:umd-lhcb/hammer-reweight";
  };

  outputs = { self, nixpkgs, flake-utils, root-curated, MuonBDTPid, hammer-reweight }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config = { allowUnfree = true; };
          overlays = [
            root-curated.overlay
            MuonBDTPid.overlay
            hammer-reweight.overlay
          ];
        };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
      in
      {
        devShell = pkgs.mkShell {
          name = "lhcb-ntuples-gen";
          buildInputs = with pythonPackages; [
            pkgs.clang-tools # For clang-format
            pkgs.root

            # UBDT adder
            pkgs.addUBDTBranchWrapped

            # HAMMER reweighter
            pkgs.hammer-reweight

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

            # Allow for the environment to pick up packages installed with virtualenv
            export PYTHONPATH=$VENV/${python.sitePackages}/:$PYTHONPATH

            # Fix libstdc++.so not found error
            export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH

            # Update PATH
            export PATH=$(pwd)/test:$(pwd)/workflows:$(pwd)/ganga:$(pwd)/scripts:$PATH
          '';
        };
      });
}

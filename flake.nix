{
  description = "ntuple generation with DaVinci and babymaker.";

  inputs = {
    root-curated.url = "github:umd-lhcb/root-curated";
    nixpkgs.follows = "root-curated/nixpkgs";
    flake-utils.follows = "root-curated/flake-utils";

    MuonBDTPid.url = "github:umd-lhcb/MuonBDTPid";
    hammer-reweight.url = "github:umd-lhcb/hammer-reweight";
    misid-unfold.url = "github:umd-lhcb/misid-unfold";

    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
  };

  outputs = { self, nixpkgs, flake-utils, root-curated, MuonBDTPid, hammer-reweight, misid-unfold, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config = { allowUnfree = true; };
          overlays = [
            root-curated.overlay
            MuonBDTPid.overlay
            hammer-reweight.overlay
            misid-unfold.overlay
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
            pkgs.AddUBDTBranchWrapped

            # HAMMER reweighter
            pkgs.hammer-reweight

            # misiD weight adder
            pkgs.misid-unfold

            # Linters
            pylint

            # Python requirements (enough to get a virtualenv going).
            virtualenvwrapper
            numpy  # FIXME: numpy 1.21.3 from PyPI breaks down because it can't find libz.so.1 (from zlib)
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

            # Update PATH
            export PATH=$(pwd)/test:$(pwd)/workflows:$(pwd)/ganga:$(pwd)/scripts:$PATH

            # Filter out tensorflow and zfit warnings
            export TF_CPP_MIN_LOG_LEVEL=2
            export ZFIT_DISABLE_TF_WARNINGS=1
          '';
        };
      });
}

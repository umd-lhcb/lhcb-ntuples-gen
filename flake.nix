{
  description = "ntuple generation with DaVinci and babymaker.";

  inputs = {
    root-curated.url = "github:umd-lhcb/root-curated/lmg_misid_validation_fit";
    nixpkgs.follows = "root-curated/nixpkgs";
    flake-utils.follows = "root-curated/flake-utils";

    MuonBDTPid.url = "github:umd-lhcb/MuonBDTPid";
    hammer-reweight.url = "github:umd-lhcb/hammer-reweight";
    misid-unfold.url = "github:umd-lhcb/misid-unfold";
    vertex-resolution.url = "github:umd-lhcb/vertex-resolution";

    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
  };

  outputs = { self, nixpkgs, flake-utils, root-curated, MuonBDTPid, hammer-reweight, misid-unfold, vertex-resolution, ... }:
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
            vertex-resolution.overlay
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
            pkgs.misid-unfold-applyer

            # vertex resolution smearing
            pkgs.vertex-resolution

            # Linters
            pylint

            # Python requirements (pin as much as possible)
            virtualenvwrapper
            numpy
            matplotlib
            uproot
            statsmodels
            uncertainties
            boost-histogram
            pyyaml
            scikit-learn
            xgboost
            tabulate
            mplhep
            lark-parser
            pathos # multi-process pool
          ];

          FONTCONFIG_FILE = pkgs.makeFontsConf {
            fontDirectories = with pkgs; [
              gyre-fonts
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
            export STUB_LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [pkgs.stdenv.cc.cc]}

            # Filter out tensorflow and zfit warnings
            export TF_CPP_MIN_LOG_LEVEL=2
            export ZFIT_DISABLE_TF_WARNINGS=1

            # matplotlib gloabl config
            export MPLBACKEND=agg  # the backend w/o a UI
            export MPLCONFIGDIR=$(pwd)/.matplotlib
          '';
        };
      });
}

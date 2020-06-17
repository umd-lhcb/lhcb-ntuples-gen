with import <nixpkgs> {};

let
  python = enableDebugging pkgs.python3;
  pythonPackages = python.pkgs;
  root = pkgs.root;
in

pkgs.mkShell {
  name = "lhcb-ntuples-gen";
  buildInputs = with pythonPackages; [
    # Compilers and other build dependencies
    pkgs.stdenv
    root

    # Auto completion
    jedi

    # Linters
    flake8
    pylint

    # Python requirements (enough to get a virtualenv going).
    virtualenvwrapper
  ];

  shellHook = ''
    # Allow the use of wheels.
    SOURCE_DATE_EPOCH=$(date +%s)

    if test -d $HOME/build/python-venv; then
      VENV=$HOME/build/python-venv/lhcb-ntuples-gen
    else
      VENV=./.virtualenv
    fi

    if test ! -d $VENV; then
      virtualenv $VENV
    fi
    source $VENV/bin/activate

    # allow for the environment to pick up packages installed with virtualenv
    export PYTHONPATH=$VENV/${python.sitePackages}/:$PYTHONPATH
  '';
}

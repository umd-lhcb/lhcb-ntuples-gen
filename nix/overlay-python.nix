let
  pythonPackageOverlay = overlay: attr: final: prev: {
    ${attr} = final.lib.fix (py:
      prev.${attr}.override (old: {
        self = py;
        packageOverrides = final.lib.composeExtensions
          (old.packageOverrides or (_: _: { }))
          overlay;
      }));
  };
in
pythonPackageOverlay
  # Must use 'final' here. 'callPackage' doesn't exsit in 'prev'
  (final: prev: {
    mkdocs = final.callPackage ./mkdocs { };
    mkdocs-markdownextradata-plugin = final.callPackage ./mkdocs-markdownextradata-plugin { };
    mkdocs-material-extensions = final.callPackage ./mkdocs-material-extensions { };
    pymdown-extensions = final.callPackage ./pymdown-extensions { };
  }) "python3"

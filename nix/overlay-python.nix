# Conceptually:
#   'self'  <-> 'final'
#   'super' <-> 'prev'
# But we need to use self super literally to make it actually work.
#  ^^^^refers to 'pythonPackageOverlay' function parameters

let
  pythonPackageOverlay = overlay: attr: self: super: {
    ${attr} = self.lib.fix (py:
      super.${attr}.override (old: {
        self = py;
        packageOverrides = self.lib.composeExtensions
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

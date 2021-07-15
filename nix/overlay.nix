final: prev:

let
  pythonOverrides = {
    packageOverrides = self: super: {
      mkdocs = self.callPackage ./mkdocs { };
      mkdocs-markdownextradata-plugin = self.callPackage ./mkdocs-markdownextradata-plugin { };
      mkdocs-material-extensions = self.callPackage ./mkdocs-material-extensions { };
      pymdown-extensions = self.callPackage ./pymdown-extensions { };
    };
  };
in

{
  python3-mkdocs = prev.python3.override pythonOverrides;
  fetchPypi = prev.python38Packages.fetchPypi;
  mkdocs-material = prev.callPackage ./mkdocs-material { python3 = final.python3-mkdocs; };
}

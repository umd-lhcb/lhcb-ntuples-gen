final: prev:

{
  mkdocs-material = prev.callPackage ./mkdocs-material {
    fetchPypi = prev.python38Packages.fetchPypi;
  };
}

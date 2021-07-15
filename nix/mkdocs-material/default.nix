{ python3, fetchPypi }:

with python3.pkgs;

buildPythonApplication rec {
  pname = "mkdocs-material";
  version = "7.1.10";

  src = fetchPypi {
    inherit pname version;
    sha256 = "890e9be00bfbe4d22ccccbcde1bf9bad67a3ba495f2a7d2422ea4acb5099f014";
  };

  propagatedBuildInputs = [
    mkdocs
    mkdocs-markdownextradata-plugin
    mkdocs-material-extensions
    pymdown-extensions
    pygments
    markdown
  ];

  doCheck = false;
}

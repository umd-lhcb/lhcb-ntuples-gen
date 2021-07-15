{ buildPythonPackage, fetchPypi }:

buildPythonPackage rec {
  pname = "mkdocs-material-extensions";
  version = "1.0.1";

  patches = [ ./no_circular_requirement.patch ];

  src = fetchPypi {
    inherit pname version;
    sha256 = "6947fb7f5e4291e3c61405bad3539d81e0b3cd62ae0d66ced018128af509c68f";
  };

  doCheck = false;
}

{ buildPythonPackage, fetchPypi, markdown }:

buildPythonPackage rec {
  pname = "pymdown-extensions";
  version = "8.2";

  src = fetchPypi {
    inherit pname version;
    sha256 = "b6daa94aad9e1310f9c64c8b1f01e4ce82937ab7eb53bfc92876a97aca02a6f4";
  };

  propagatedBuildInputs = [ markdown ];

  doCheck = false;
}

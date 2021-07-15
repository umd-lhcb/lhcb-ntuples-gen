{ buildPythonPackage
, fetchPypi
, click
, jinja2
, markdown
, mergedeep
, pyyaml
, pyyaml-env-tag
, ghp-import
, importlib-metadata
, watchdog
, packaging
}:

buildPythonPackage rec {
  pname = "mkdocs";
  version = "1.2.1";

  src = fetchPypi {
    inherit pname version;
    sha256 = "6e0ea175366e3a50d334597b0bc042b8cebd512398cdd3f6f34842d0ef524905";
  };

  propagatedBuildInputs = [
    click
    jinja2
    markdown
    mergedeep
    pyyaml
    pyyaml-env-tag
    ghp-import
    importlib-metadata
    watchdog
    packaging
  ];

  doCheck = false;
}

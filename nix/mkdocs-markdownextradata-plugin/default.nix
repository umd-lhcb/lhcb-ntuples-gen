{ buildPythonPackage, fetchFromGitHub, mkdocs, pyyaml }:

buildPythonPackage rec {
  pname = "mkdocs-markdownextradata-plugin";
  version = "0.2.4";

  src = fetchFromGitHub {
    owner = "rosscdh";
    repo = pname;
    rev = version;
    sha256 = "wXk3xV+7xwN4udGNAKFR4C/q8hJS7k18XJJxxFmUR5A=";
  };

  propagatedBuildInputs = [ mkdocs pyyaml ];

  doCheck = false;
}

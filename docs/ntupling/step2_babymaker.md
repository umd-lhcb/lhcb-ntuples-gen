`babymaker` is a part of the `pyBabyMaker` library. Please refer to the
[official document](https://pybabymaker.readthedocs.io) for its command line
usage and internal APIs.


## Generating a C++ file with `babymaker`
The general idea is that `babymaker` takes:

* A `YAML` file as configuration, denote as `cfg_yml`
* A C++ "template" that `babymaker` can work on, denote as `cpp_tmpl`
* Main ntuple file that you want to work on, denote as `main_ntp`
* Optionally many friend ntuples that have part of their tree structures
  identical to that of the main, denote as `friend_ntp1`, `friend_ntp2`, ...

To generate our final C++ file:

```shell
babymaker -i <cfg_yml> -n <main_ntp> -f <friend_ntp1> <friend_ntp2> ... -o <output_cpp> -t <cpp_tmpl>
```

Next, the following shell snippet should be enough to get generated C++
compiled in this repo:

```bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
HEADER_DIR=$DIR/../../include
COMPILER=$(root-config --cxx)
CXX_FLAGS=$(root-config --cflags)
LINK_FLAGS=$(root-config --libs)
ADDF_FLAGS="-I${HEADER_DIR}"

cpp_compile() {
    ${COMPILER} ${CXX_FLAGS} ${ADDF_FLAGS} -o baby baby.cpp ${LINK_FLAGS}
}

cpp_compile  # assuming generated C++ file is named 'baby.cpp'
```

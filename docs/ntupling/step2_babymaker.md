`babymaker` is a part of the `pyBabyMaker` library. Please refer to the
[official document](https://pybabymaker.readthedocs.io) for more info.

The general idea is that `babymaker` takes:

* a `YAML` file as configuration
* a `.root` ntuple file to dump its tree structure and data type of each branch
    in the trees.

and generates a `C++` file. The generated file then will be compiled, and the
compiled binary will be used to generate second stage `.root` ntuples.

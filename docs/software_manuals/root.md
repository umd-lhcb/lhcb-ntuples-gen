### Compiling ROOT without `nix` on macOS

For of our repos have a `nix` flake with `ROOT` in it, but if you want to have `ROOT` installed in your mac with the
`HistFactory` pacthes, you can follow the instructions below.

If you alread have a `ROOT` installation, you should delete it first as it often collides with new ones (`rm -rf root_build root_install`).
```
git clone --branch histfactory_patch https://github.com/umd-lhcb/root.git
mkdir root_build root_install && cd root_build
cmake -DCMAKE_INSTALL_PREFIX=../root_install/ -Dsqlite=OFF -Dmysql=OFF -Dx11=ON  -Droofit=ON -Dmt=ON -Dminuit2=ON -Dccache=ON -Dlibcxx=ON -Drpath=ON ../root 
cmake --build . -- install -j6
```

Note:  For `-jN`, `N` should be your number of CPU cores (or fewer).
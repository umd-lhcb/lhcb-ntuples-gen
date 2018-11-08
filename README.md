# lhcb-ntuples-gen
DaVinci scripts for ntuples generation

## Split bookkeep files
The motivation to do this is that we can split long bookkeeping files (~1000
lines) into many smaller files, each has 50 lines, so that we can use
`LHCbDirac` to download these `dst` files from one of these files to our EOS
storage.

Due to limited space of EOS, it is impossible to download all files listed in a
full bookkeeping file.

To split:
```
split --lines=50 bookkeeping.dst
```
The splitted files will have name `x??`.

To download all `dst` files listed in a bookkeeping file:
```
lhcb-proxy-init
lb-run LHCbDIRAC dirac-dms-get-file -D <target_dir> --File=<splitted_bookkeeping_file>
```

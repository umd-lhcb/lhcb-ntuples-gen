## Split book-keeping files
The `.dst` description files downloaded directly from `Dirac` contains a list with
a large number of files (700 files or more). For example, this file contains 1690 lines:
```
/lhcb/LHCb/Collision12/SEMILEPTONIC.DST/00067251/0000/00067251_00001536_1.Semileptonic.dst
/lhcb/LHCb/Collision12/SEMILEPTONIC.DST/00067251/0000/00067251_00001039_1.Semileptonic.dst
/lhcb/LHCb/Collision12/SEMILEPTONIC.DST/00067251/0000/00067251_00000344_1.Semileptonic.dst
/lhcb/LHCb/Collision12/SEMILEPTONIC.DST/00067251/0000/00067251_00000301_1.Semileptonic.dst
/lhcb/LHCb/Collision12/SEMILEPTONIC.DST/00067251/0000/00067251_00000850_1.Semileptonic.dst
/lhcb/LHCb/Collision12/SEMILEPTONIC.DST/00067251/0000/00067251_00000988_1.Semileptonic.dst
/lhcb/LHCb/Collision12/SEMILEPTONIC.DST/00067251/0000/00067251_00001423_1.Semileptonic.dst
/lhcb/LHCb/Collision12/SEMILEPTONIC.DST/00067251/0000/00067251_00000841_1.Semileptonic.dst
...
/lhcb/LHCb/Collision12/SEMILEPTONIC.DST/00067251/0000/00067251_00001096_1.Semileptonic.dst
```

It is impractical to download every single one of them, as we don't have enough
storage space in `lxplus`, even with `EOS`.

To split, we use `split`, a linux tool that should have been installed by default:
```
split --lines=50 <filename.txt>
```
In this case, the `<filename.txt>` will be sliced for every 50 lines, and the
output filenames will be `x??`.


## Download data files with `lxplus`
To download all dst files listed in a bookkeeping file:
```
lhcb-proxy-init
lb-dirac dirac-dms-get-file -D <target_dir> --File <file_with_list_of_lfns>
```

If you know a `LFN`, instead of a file that contains a list of `LFN`s, you can:
```
lb-dirac dirac-dms-get-file -D <target_dir> -l <lfn>
```


## Query MC DDDB and CONDDB tags

!!! warning
    MagUp and MagDown have different tags. Typically you can replace `mu100`
    with `md100`.

Find the production number for a given `.dst` LFN, say:
```
/lhcb/LHCb/Collision12/SEMILEPTONIC.DST/00067251/0000/00067251_00000841_1.Semileptonic.dst
```

It's production number is `67251`.

On lxplus, do the following:
```
lhcb-proxy-init
lb-dirac dirac-bookkeeping-production-information 67251
```

The output contains both DDDB and CONDDB tags.

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


## Query MC DDB and CONDDB tags

!!! warning
    MagUp and MagDown have different tags. Typically you can replace `mu100`
    with `md100`.

For older productions, these tags are directly available in BKK. Just download
the Python version of the `.DST` file from BKK.

For newer productions, the Python file list these tags as:
```python
#-- GAUDI jobOptions generated on Fri May 21 18:19:43 2021
#-- Contains event types :
#--   11574021 - 112 files - 1500395 events - 400.11 GBytes

#--  Extra information about the data processing phases:

#--  Processing Pass: '/Sim09j/Trig0x6139160F/Reco16/Turbo03a/Filtered'

#--  StepId : 143000
#--  StepName : Merge for SL Filtered Productions (muonic B to D(*) tau nu) - DST
#--  ApplicationName : DaVinci
#--  ApplicationVersion : v45r5
#--  OptionFiles : $APPCONFIGOPTS/Merging/DVMergeDST.py;$APPCONFIGOPTS/DaVinci/DataType-2016.py;$APPCONFIGOPTS/Merging/WriteFSR.py;$APPCONFIGOPTS/Merging/MergeFSR.py;$APPCONFIGOPTS/Persistency/Compression-LZMA-4.py;$APPCONFIGOPTS/DaVinci/Simulation.py
#--  DDDB : fromPreviousStep
#--  CONDDB : fromPreviousStep
#--  ExtraPackages : AppConfig.v3r402
#--  Visible : N
```

If you have a MC production ID (e.g. `74509`), you can either:

1. **DIRAC** -> **Data** -> **Production Request**, then input the ID in **Request ID(s)** field
2. On lxplus:

        lb-dirac dirac-bookkeeping-production-information <prod_id>

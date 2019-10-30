`bender` is a tool to interactively explore `.dst` files.

## Find all trigger lines and hit ratios in a `.dst` file
There is a simple one-liner to find these info:
```
lb-run Bender/latest trg-check -n -1 -d 2012 --teslocation /Event/Semileptonic/Phys/b2D0MuXB2DMuNuForTauMuLine/Particles ~/cmtuser/DaVinci_v36r1p2/data/mag_down/00041836_00011435_1.semileptonic.dst
```

!!! note
    * `-n -1` is number of events to run over; `-1` means all. Default is
      `1000`.
    * `-d 2012` specify the data type (year).

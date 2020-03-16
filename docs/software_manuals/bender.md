`bender` is a tool to interactively explore `.dst` files.

## Find all trigger lines and hit ratios in a `.dst` file
There is a simple one-liner to find these info:
```
lb-run Bender/latest trg-check -n -1 -d 2012 --teslocation /Event/Semileptonic/Phys/b2D0MuXB2DMuNuForTauMuLine/Particles <path_to_dst>
```

!!! note
    * `-n -1` is number of events to run over; `-1` means all. Default is
      `1000`.
    * `-d 2012` specify the data type (year).


## Dump TES info from a `.dst` file
```
lb-run Bender/latest dst-dump -d 2016 -f -n 100 <path_to_dst>
```

!!! note
    * `-f` means that try to unpack all TES locations.

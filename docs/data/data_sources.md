## Run 1 muonic $R(D^{(*)})$ data

| stripping line | sample `DIRAC` path |
|---|---|
| [`b2D0MuXB2DMuNuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping21/semileptonic/strippingb2d0muxb2dmunufortaumuline.html) | `/LHCb/Collision12/Beam4000GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping21/90000000/SEMILEPTONIC.DST` |
| [`b2D0MuXFakeB2DMuNuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping21/semileptonic/strippingb2d0muxfakeb2dmunufortaumuline.html) | Same as above |

!!! note
    Both lines are defined in the same file, which can be found
    [here](https://gitlab.cern.ch/lhcb/Stripping/-/blob/Stripping-s28/Phys/StrippingArchive/python/StrippingArchive/Stripping21/StrippingB2DMuForTauMu.py).

    We have to use `Stripping21` instead of `Stripping20` as mentioned in the
    notes, because the latter one is no longer _fully_ exist.

    Also, `Stripping21` contains 2012 data, and `Stripping21r1` contains 2011
    data.

!!! info
    The _Fake_ line contains all cuts as the _Regular_ line, with the following
    differences:

    1. _Fake_ uses `StdAllNoPIDsMuons` whereas _Regular_ uses `StdLooseMuons`
    2. _Fake_ has the $\mu$ cuts of: `(~ISMUON) & (INMUON)`

        _Regular_ has the $\mu$ cuts of: `PIDmu > 2.0`


## Run 1 muonic $R(D^{(*)})$ Monte-Carlo

!!! tip
    In `DIRAC`, make sure to switch from **Simulation Condition** to **Event
    type**. Then the event will be available at `MC/2012/<event_type_uid>`.

### Normalization
| sample | MC ID | decay |
|---|---|---|
| $D^0$ | `12573010` | $B^- \rightarrow D^0 \mu \nu$ |
| $D^0/D^{*+}$ | `11574020` | $B^0 \rightarrow D^{*+} \mu \nu$ |
| $D^0$ | `12573031` | $B^- \rightarrow D^{*0} \mu \nu$ |

### Signal
| sample | MC ID | decay |
|---|---|---|
| $D^0$ | `12573000` | $B^- \rightarrow D^0 \tau \nu$ |
| $D^0/D^{*+}$ | `11574010` | $B^0 \rightarrow D^{*+} \tau \nu$ |
| $D^0$ | `12573021` | $B^- \rightarrow D^{*0} \tau \nu$ |

### $D^{**}$
| sample | MC ID | decay |
|---|---|---|
| $D^0/D^{*+}$ | `12873010` | $B^- \rightarrow D^{**0} \mu \nu \rightarrow D^0$ |
| $D^0/D^{*+}$ | `11873010` | $B^0 \rightarrow D^{**+} \mu \nu \rightarrow D^0$ |
| $D^0/D^{*+}$ | `12873030` | $B^- \rightarrow D^{**0} \tau \nu \rightarrow D^0$ |
| $D^0/D^{*+}$ | `11873030` | $B^0 \rightarrow D^{**+} \tau \nu \rightarrow D^0$ |

### $D^{**}$ heavy
| sample | MC ID | decay |
|---|---|---|
| $D^0$ | `12675010` | $B^- \rightarrow D^{**} (\rightarrow D^0 \pi \pi) \mu \nu$ |
| $D^0$ | `11674400` | $B^0 \rightarrow D^{**} (\rightarrow D^0 \pi \pi) \mu \nu$ |
| $D^0/D^{*+}$ | `12675400` | $B^- \rightarrow D^{**} (\rightarrow D^{*+} \pi \pi) \mu \nu$ |
| $D^0/D^{*+}$ | `11676010` | $B^0 \rightarrow D^{**} (\rightarrow D^{*+} \pi \pi) \mu \nu$ |
| $D^0$ | `12675430` | $B^- \rightarrow D^{**} (\rightarrow D^{*0} \pi \pi) \mu \nu$ |

### $D_s^{**}$
| sample | MC ID | decay |
|---|---|---|
| $D^0$ | `13873000` | $B_s \rightarrow D_s^{**} (\rightarrow D^0 K) \mu \nu$ |
| $D^{*+}$ | `13874000` | $B_s \rightarrow D^{**+} \mu \nu$ |

### $DDX$
| sample | MC ID | decay |
|---|---|---|
| $D^0$ | `11873000` | $B^0 \rightarrow D^0 X_c (\rightarrow \mu \nu X') X$ |
| $D^0$ | `12873000` | $B^+ \rightarrow D^0 X_c (\rightarrow \mu \nu X') X$ |
| $D^0$ | `11873020` | $B^0 \rightarrow D^0 D_s (\rightarrow \tau \nu) X$ |
| $D^0$ | `12873021` | $B^+ \rightarrow D^0 D_s (\rightarrow \tau \nu) X$ |
| $D^{*+}$ | `11874050` | $B^0 \rightarrow D^{*+} X_c (\rightarrow \mu \nu X') X$ |
| $D^{*+}$ | `12874010` | $B^+ \rightarrow D^{*+} X_c (\rightarrow \mu \nu X') X$ |
| $D^{*+}$ | `11874070` | $B^0 \rightarrow D^{*+} D_s (\rightarrow \tau \nu) X$ |
| $D^{*+}$ | `11874030` | $B^+ \rightarrow D^{*+} D_s (\rightarrow \tau \nu) X$ |

### Cocktail sample for cutflow study
| sample | MC ID | decay |
|---|---|---|
| $D^0/D^{*+}$ | `11874091` | $B_d \rightarrow D^0 X \mu \nu$, $D^0 = cocktail$ |


## Run 2 muonic $R(D^{(*)})$ data

| stripping line | sample `DIRAC` path |
|---|---|
| [`b2D0MuXB2DMuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping28r2/semileptonic/strippingb2d0muxb2dmufortaumuline.html) | `/LHCb/Collision16/Beam6500GeV-VeloClosed-MagDown/Real Data/Reco16/Stripping28r1/90000000/SEMILEPTONIC.DST` |
| [`b2D0MuXFakeB2DMuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping28r2/semileptonic/strippingb2d0muxfakeb2dmufortaumuline.html) | Same as above |

!!! note
    As in run 1, both are defined in [the same file](https://gitlab.cern.ch/lhcb/Stripping/-/blob/Stripping-s28/Phys/StrippingArchive/python/StrippingArchive/Stripping28/StrippingSL/StrippingB2DMuForTauMu.py).

!!! warning
    The run 2 stripping line name is **different** from that of run 1!
    The run 2 stripping line omits `Nu`.


## Run 2 muonic $R(D^{(*)})$ Monte-Carlo

!!! info
    The FullSim production IDs are: `74233, 74234, 74494, 74509`.

!!! tips
    To find the MC IDs of a production, go to DIRAC, then navigate:
    **Data** -> **Production Request** -> input the production ID you'd like to
    inspect.

### Normalization
| sample | MC ID | decay |
|---|---|---|
| $D^0$ | `12573012` | $B^- \rightarrow D^0 \mu \nu$ |
| $D^0/D^{*+}$ | `11574021` | $B^0 \rightarrow D^{*+} \mu \nu$ |
| $D^0$ | `12773410` | $B^- \rightarrow D^{*0} \mu \nu$ |

### Signal
| sample | MC ID | decay |
|---|---|---|
| $D^0$ | `12573001` | $B^- \rightarrow D^0 \tau \nu$ |
| $D^0/D^{*+}$ | `11574011` | $B^0 \rightarrow D^{*+} \tau \nu$ |
| $D^0$ | `12773400` | $B^- \rightarrow D^{*0} \tau \nu$ |

### $D^{**}$
| sample | MC ID | decay |
|---|---|---|
| $D^0/D^{*+}$ | `11874430` | $B^0 \rightarrow D^{**+} \mu \nu \rightarrow D^0$ |
| $D^0/D^{*+}$ | `11874440` | $B^0 \rightarrow D^{**+} \tau \nu \rightarrow D^0$ |
| $D^0/D^{*+}$ | `12873450` | $B^- \rightarrow D^{**0} \mu \nu \rightarrow D^0$ |
| $D^0/D^{*+}$ | `12873460` | $B^- \rightarrow D^{**0} \tau \nu \rightarrow D^0$ |

### $D^{**}$ heavy
| sample | MC ID | decay |
|---|---|---|
| $D^0$ | `12675011` | $B^- \rightarrow D^{**} (\rightarrow D^0 \pi \pi) \mu \nu$ |
| $D^0$ | `11674401` | $B^0 \rightarrow D^{**} (\rightarrow D^0 \pi \pi) \mu \nu$ |
| $D^0/D^{*+}$ | `12675402` | $B^- \rightarrow D^{**} (\rightarrow D^{*+} \pi \pi) \mu \nu$ |
| $D^0/D^{*+}$ | `11676012` | $B^0 \rightarrow D^{**} (\rightarrow D^{*+} \pi \pi) \mu \nu$ |
| $D^0$ | `12875440` | $B^- \rightarrow D^{**} (\rightarrow D^{*0} \pi \pi) \mu \nu$ |

### $D_s^{**}$
| sample | MC ID | decay |
|---|---|---|
| $D^0$ | `13874020` | $B_s \rightarrow D_s^{**} (\rightarrow D^0 K) \mu \nu$ |
| $D^{*+}$ | `13674000` | $B_s \rightarrow D^{**+} \mu \nu$ |

### $DDX$
| sample | MC ID | decay |
|---|---|---|
| $D^0$ | `11894600` | $B^0 \rightarrow D^0 X_c (\rightarrow \mu \nu X') X$ |
| $D^0$ | `12893600` | $B^+ \rightarrow D^0 X_c (\rightarrow \mu \nu X') X$ |
| $D^0$ | `11894200` | $B^0 \rightarrow D^0 D_s (\rightarrow \tau \nu) X$ |
| $D^0$ | `12893610` | $B^+ \rightarrow D^0 D_s (\rightarrow \tau \nu) X$ |
| $D^{*+}$ | `11894610` | $B^0 \rightarrow D^{*+} X_c (\rightarrow \mu \nu X') X$ |
| $D^{*+}$ | `12895400` | $B^+ \rightarrow D^{*+} X_c (\rightarrow \mu \nu X') X$ |
| $D^{*+}$ | `11894210` | $B^0 \rightarrow D^{*+} D_s (\rightarrow \tau \nu) X$ |
| $D^{*+}$ | `12895000` | $B^+ \rightarrow D^{*+} D_s (\rightarrow \tau \nu) X$ |

### Cocktail sample for cutflow study
| sample | MC ID | decay |
|---|---|---|
| $D^0/D^{*+}$ | `11874091` | $B_d \rightarrow D^0 X \mu \nu$, $D^0 = cocktail$ |

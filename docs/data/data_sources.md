## Run 1 muonic $R(D^{(*)})$ data

| stripping line (in note) | stripping line (updated) | sample `DIRAC` path |
|---|---|---|
| `Strippingb2D0MuXB2DMuForTaoMuLine` | `Strippingb2D0MuXB2DMuNuForTauMuLine` | `/LHCb/Collision12/Beam4000GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping21/90000000/SEMILEPTONIC.DST`

!!! note
    We have to use `Stripping21` instead of `Stripping20` as mentioned in the
    notes, because the latter one is no longer _fully_ exist.

    Also, `Stripping21` contains 2012 data, and `Stripping21r1` contains 2011
    data.


## Run 1 muonic $R(D^{(*)})$ Monte-Carlo

!!! tip
    In `DIRAC`, make sure to switch from **Simulation Condition** to **Event
    type**. Then the event will be available at `MC/2012/<event_type_uid>`.


### With $D^{**}$ in intermediate product
* `11873030`: $B^0 \rightarrow D^{**} \tau \nu \rightarrow D^0$
* `11873010`: $B^0 \rightarrow D^{**} \mu \nu \rightarrow D^0$
* `13873000`: $B_s \rightarrow D^{**} \mu \nu \rightarrow D^0$
* `12873010`: $B^+ \rightarrow D^{**} \mu \nu \rightarrow D^0$

### With $D^{*}$ in intermediate product
* `11574010`: $B^0 \rightarrow D^* \tau \nu$
* `11574020`: $B^0 \rightarrow D^* \mu \nu$
* `12573020`: $B^+ \rightarrow D^{*0} \tau \nu$
* `12573030`: $B^+ \rightarrow D^{*0} \mu \nu$

### With $D^0$ in intermediate product
* `12573000`: $B^+ \rightarrow D^0 \tau \nu$
* `12573010`: $B^+ \rightarrow D^0 \mu \nu$
* `11873000`: $B^0 \rightarrow D^0 DX \rightarrow \mu X$
* `12873000`: $B^+ \rightarrow D^0 DX \rightarrow \mu X$
* `11873020`: $B^0 \rightarrow D^0 D_s X \rightarrow \tau \nu$
* `12873020`: $B^+ \rightarrow D^0 D_s X \rightarrow \tau \nu$

### Cocktail sample for cut-flow study
* `11874091`: $B_d \rightarrow D^0 X \mu \nu$, $D^0 = cocktail$.


## Run 2 muonic $R(D^{(*)})$ data

| stripping line | sample `DIRAC` path |
|---|---|
| `Strippingb2D0MuXB2DMuForTaoMuLine` | `/LHCb/Collision16/Beam6500GeV-VeloClosed-MagDown/Real Data/Reco16/Stripping28r1/90000000/SEMILEPTONIC.DST`

!!! warning
    The run 2 stripping line name is **different** from that of run 1!
    The run 2 stripping line omits `Nu`.


## Run 2 muonic $R(D^{(*)})$ Monte-Carlo

### Cocktail sample for cut-flow study
* `11874091`: $B_d \rightarrow D^0 X \mu \nu$, $D^0 = cocktail$.

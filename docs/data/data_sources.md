## Samples
Here we track the original filenames and their providers in the `*/sample`
folder.

### `2012-b2D0MuXB2DMuNuForTauMuLine`

| name in this repo | original name | provider | MD5 sum |
|---|---|---|---|
| `YCands_D0-2012-mag_down-data.root` | ? | P. Hamilton | `73bfbc7b9d0e1eea19572fa42b28ebc6` |
| `YCands_Dstar-2012-mag_down-data.root` | `newTFYCands_DATA_2012_MD.root` | P. Hamilton | `16c4750761d75b8b37e5bff521139887` |
| `YCands-davinci_v36r1p2.root` | `ycands_dvv36r1p2.root` | P. Hamilton | `fdb64ca03803a363c484934cff338986` |


## _lhcb-ana-2014-052-v2r1_
### Data
The data source for this analysis note can be found on `DIRAC`:

| stripping line (in note) | stripping line (updated) | `DIRAC` path |
|---|---|---|
| `Strippingb2D0MuXB2DMuForTaoMuLine` | `Strippingb2D0MuXB2DMuNuForTauMuLine` | `/LHCb/Collision12/Beam4000GeV-VeloClosed-Mag{Down,Up}/Real Data/Reco14/Stripping21/90000000/SEMILEPTONIC.DST`

!!! note
    we have to use `Stripping21` instead of `Stripping20` as mentioned in the
    notes, because the latter one is no longer _fully_ exist.

    Also `Stripping21` contains 2012 data, and `Stripping21r1` contains 2011 data.

### Monte-Carlo
In `DIRAC`, make sure to switch from **Simulation Condition** to **Event type**. Then the event will be available at `MC/2012/<event_type_uid>`.

In the analysis note, we used the following event types

| event type |
|---|
| `11574020` |
| `11574010` |
| `11874060` |
| `11874080` |
| `12874040` |
| `12874020` |
| `13874000` |
| `11874050` |
| `11874070` |
| `12874010` |
| `12874030` |

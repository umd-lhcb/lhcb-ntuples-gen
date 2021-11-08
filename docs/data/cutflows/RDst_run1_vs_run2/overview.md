# $R(D^*)$ cutflow overview

## Cutflow table with cocktail MC, bare

| Cut                          | Run 1   | Run 2   | Run 1 $\epsilon$   | Run 2 $\epsilon$   | $\epsilon$ ratio   |
|------------------------------|---------|---------|--------------------|--------------------|--------------------|
| Total events                 | 118213  | 126958  | -                  | -                  | -                  |
| Trig. + Strip.               | 4313    | 13005   | 3.6                | 10.2               | 2.81               |
| Offline $D^0$ cuts           | 3729    | 5808    | 86.5               | 44.7               | 0.52               |
| Offline $\mu$ cuts           | 3307    | 4606    | 88.7               | 79.3               | 0.89               |
| Offline $D^* \mu$ combo cuts | 1975    | 2729    | 59.7               | 59.2               | 0.99               |
| $BDT_{iso} < 0.15$           | 1513    | 1946    | 76.6               | 71.3               | 0.93               |
| Total eff.                   | -       | -       | 1.3                | 1.5                | 1.20               |
| Yield ratio x 0.99           | 1513    | 1946    | -                  | -                  | 1.27               |

!!! note
    - We removed all kinematic cuts and loosened some vertex quality cuts when generating bare ntuples.
    - This table uses **full MagDown** run 1 and 2 cocktail MC.
    - Additional step 2 cuts are applied here.
    - **ALL** numbers are number of events.
    - We applied the same cuts for run 1 and 2.

!!! info
    - Run 1 stripping conditions can be found at [`Strippingb2D0MuXB2DMuNuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping21/semileptonic/strippingb2d0muxb2dmunufortaumuline.html)
    - Run 2 stripping conditions can be found at [`Strippingb2D0MuXB2DMuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping28r2/semileptonic/strippingb2d0muxb2dmufortaumuline.html)


## Cutflow table with cocktail MC, bare, with truth-matched signal, normalization, and $D^{**}$

### Signal

| Cut                          | Run 1   | Run 2   | Run 1 $\epsilon$   | Run 2 $\epsilon$   | $\epsilon$ ratio   |
|------------------------------|---------|---------|--------------------|--------------------|--------------------|
| Total events                 | 118213  | 126958  | -                  | -                  | -                  |
| Signal truth-matching        | 4388    | 4638    | 3.7                | 3.7                | 0.98               |
| Trig. + Strip.               | 151     | 397     | 3.4                | 8.6                | 2.49               |
| Offline $D^0$ cuts           | 120     | 207     | 79.5               | 52.1               | 0.66               |
| Offline $\mu$ cuts           | 110     | 162     | 91.7               | 78.3               | 0.85               |
| Offline $D^* \mu$ combo cuts | 70      | 115     | 63.6               | 71.0               | 1.12               |
| $BDT_{iso} < 0.15$           | 61      | 91      | 87.1               | 79.1               | 0.91               |
| Total eff.                   | -       | -       | 0.05               | 0.07               | 1.39               |
| Yield ratio x 0.99           | 61      | 91      | -                  | -                  | 1.48               |

### Normalization

| Cut                          | Run 1   | Run 2   | Run 1 $\epsilon$   | Run 2 $\epsilon$   | $\epsilon$ ratio   |
|------------------------------|---------|---------|--------------------|--------------------|--------------------|
| Total events                 | 118213  | 126958  | -                  | -                  | -                  |
| Normalization truth-matching | 76567   | 82950   | 64.8               | 65.3               | 1.01               |
| Trig. + Strip.               | 2898    | 8702    | 3.8                | 10.5               | 2.77               |
| Offline $D^0$ cuts           | 2480    | 3868    | 85.6               | 44.4               | 0.52               |
| Offline $\mu$ cuts           | 2182    | 3062    | 88.0               | 79.2               | 0.90               |
| Offline $D^* \mu$ combo cuts | 1613    | 2186    | 73.9               | 71.4               | 0.97               |
| $BDT_{iso} < 0.15$           | 1362    | 1714    | 84.4               | 78.4               | 0.93               |
| Total eff.                   | -       | -       | 1.2                | 1.4                | 1.17               |
| Yield ratio x 0.99           | 1362    | 1714    | -                  | -                  | 1.25               |

### $D^{**}$

| Cut                          | Run 1   | Run 2   | Run 1 $\epsilon$   | Run 2 $\epsilon$   | $\epsilon$ ratio   |
|------------------------------|---------|---------|--------------------|--------------------|--------------------|
| Total events                 | 118213  | 126958  | -                  | -                  | -                  |
| $D^{**}$ truth-matching      | 35827   | 37755   | 30.3               | 29.7               | 0.98               |
| Trig. + Strip.               | 1225    | 3818    | 3.4                | 10.1               | 2.96               |
| Offline $D^0$ cuts           | 1097    | 1699    | 89.6               | 44.5               | 0.50               |
| Offline $\mu$ cuts           | 986     | 1357    | 89.9               | 79.9               | 0.89               |
| Offline $D^* \mu$ combo cuts | 289     | 424     | 29.3               | 31.2               | 1.07               |
| $BDT_{iso} < 0.15$           | 89      | 138     | 30.8               | 32.5               | 1.06               |
| Total eff.                   | -       | -       | 0.08               | 0.11               | 1.44               |
| Yield ratio x 0.99           | 89      | 138     | -                  | -                  | 1.53               |


## Cutflow table with real data

| Cut                          | Run 1   | Run 2   | Run 1 $\epsilon$   | Run 2 $\epsilon$   | $\epsilon$ ratio   |
|------------------------------|---------|---------|--------------------|--------------------|--------------------|
| Total events                 | 216987  | 5349722 | -                  | -                  | -                  |
| Trig. + Strip.               | 202990  | 3043397 | 93.5               | 56.9               | 0.61               |
| Offline $D^0$ cuts           | 153311  | 1077159 | 75.5               | 35.4               | 0.47               |
| Offline $\mu$ cuts           | 143242  | 656044  | 93.4               | 60.9               | 0.65               |
| Offline $D^* \mu$ combo cuts | 115321  | 512969  | 80.5               | 78.2               | 0.97               |
| $BDT_{iso} < 0.15$           | 74535   | 317049  | 64.6               | 61.8               | 0.96               |
| Total eff.                   | -       | -       | 34.3               | 5.9                | 0.17               |
| Yield ratio x 0.35           | 74535   | 317049  | -                  | -                  | 1.51               |

!!! note
    - This table uses **full MagDown** 2011 and 2016 real data.
    - **ALL** numbers are number of events.
    - The _Trig. + Strip._ entries should not be trusted as we don't include
      numbers extracted from DaVinci log.

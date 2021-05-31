# $R(D^*)$ cutflow overview

## Cutflow table with cocktail MC, bare

| cut name                             | run 1 yield   | run 2 yield   | run 1 efficiency   | run 2 efficiency   | double ratio   |
|--------------------------------------|---------------|---------------|--------------------|--------------------|----------------|
| Total events                         | 1025230       | 1035959       | -                  | -                  | -              |
| Relaxed $D^0 \mu$ combo              | 139906        | 144221        | 61.9               | 61.9               | 1.00           |
| $D^{*+} \rightarrow D^0 \pi^+$       | 129550        | 136011        | 92.6               | 94.3               | 1.02           |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$ | 118213        | 126958        | 97.0               | 97.6               | 1.01           |
| L0                                   | 46733         | 42182         | 39.5               | 33.2               | 0.84           |
| Hlt1                                 | 22334         | 29928         | 47.8               | 70.9               | 1.48           |
| Hlt2                                 | 9123          | 15110         | 40.8               | 50.5               | 1.24           |
| Stripping                            | 4313          | 13005         | 47.3               | 86.1               | 1.82           |
| DaVinci $D^* \mu$ cuts               | 2830          | 7837          | 65.6               | 60.3               | 0.92           |
| Offline $D^0$ cuts                   | 1511          | 2371          | 53.4               | 30.3               | 0.57           |
| Offline $\mu$ cuts                   | 1327          | 1880          | 87.8               | 79.3               | 0.90           |
| Offline $D^* \mu$ combo cuts         | 1277          | 1769          | 96.2               | 94.1               | 0.98           |
| Total ratio                          | -             | -             | 0.1                | 0.2                | 1.37           |

!!! note
    - We removed all kinematic cuts and loosened some vertex quality cuts when generating bare ntuples.
    - This table uses **full MagDown** run 1 and 2 cocktail MC.
    - Additional step 2 cuts are applied here.
    - **ALL** numbers are number of events.

!!! info
    - Run 1 stripping conditions can be found at [`Strippingb2D0MuXB2DMuNuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping21/semileptonic/strippingb2d0muxb2dmunufortaumuline.html)
    - Run 2 stripping conditions can be found at [`Strippingb2D0MuXB2DMuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping28r2/semileptonic/strippingb2d0muxb2dmufortaumuline.html)


## Cutflow table with cocktail MC, bare, with truth-matched signal, normalization, and $D^{**}$

### Signal

| cut name                             | run 1 yield   | run 2 yield   | run 1 efficiency   | run 2 efficiency   | double ratio   |
|--------------------------------------|---------------|---------------|--------------------|--------------------|----------------|
| Total events                         | 1025230       | 1035959       | -                  | -                  | -              |
| Relaxed $D^0 \mu$ combo              | 139906        | 144221        | 61.9               | 61.9               | 1.00           |
| $D^{*+} \rightarrow D^0 \pi^+$       | 129550        | 136011        | 92.6               | 94.3               | 1.02           |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$ | 118213        | 126958        | 97.0               | 97.6               | 1.01           |
| Signal truth-matching                | 4388          | 4638          | 3.7                | 3.7                | 0.98           |
| L0                                   | 1633          | 1442          | 37.2               | 31.1               | 0.84           |
| Hlt1                                 | 677           | 947           | 41.5               | 65.7               | 1.58           |
| Hlt2                                 | 310           | 453           | 45.8               | 47.8               | 1.04           |
| Stripping                            | 151           | 397           | 48.7               | 87.6               | 1.80           |
| DaVinci $D^* \mu$ cuts               | 116           | 290           | 76.8               | 73.0               | 0.95           |
| Offline $D^0$ cuts                   | 56            | 102           | 48.3               | 35.2               | 0.73           |
| Offline $\mu$ cuts                   | 52            | 76            | 92.9               | 74.5               | 0.80           |
| Offline $D^* \mu$ combo cuts         | 50            | 74            | 96.2               | 97.4               | 1.01           |
| Total ratio                          | -             | -             | 0.0                | 0.0                | 1.46           |

### Normalization

| cut name                             | run 1 yield   | run 2 yield   | run 1 efficiency   | run 2 efficiency   | double ratio   |
|--------------------------------------|---------------|---------------|--------------------|--------------------|----------------|
| Total events                         | 1025230       | 1035959       | -                  | -                  | -              |
| Relaxed $D^0 \mu$ combo              | 139906        | 144221        | 61.9               | 61.9               | 1.00           |
| $D^{*+} \rightarrow D^0 \pi^+$       | 129550        | 136011        | 92.6               | 94.3               | 1.02           |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$ | 118213        | 126958        | 97.0               | 97.6               | 1.01           |
| Normalization truth-matching         | 76567         | 82950         | 64.8               | 65.3               | 1.01           |
| L0                                   | 29880         | 27255         | 39.0               | 32.9               | 0.84           |
| Hlt1                                 | 14556         | 19556         | 48.7               | 71.8               | 1.47           |
| Hlt2                                 | 5993          | 10104         | 41.2               | 51.7               | 1.25           |
| Stripping                            | 2898          | 8702          | 48.4               | 86.1               | 1.78           |
| DaVinci $D^* \mu$ cuts               | 2280          | 6287          | 78.7               | 72.2               | 0.92           |
| Offline $D^0$ cuts                   | 1227          | 1898          | 53.8               | 30.2               | 0.56           |
| Offline $\mu$ cuts                   | 1068          | 1503          | 87.0               | 79.2               | 0.91           |
| Offline $D^* \mu$ combo cuts         | 1039          | 1420          | 97.3               | 94.5               | 0.97           |
| Total ratio                          | -             | -             | 0.1                | 0.1                | 1.35           |

### $D^{**}$

| cut name                             | run 1 yield   | run 2 yield   | run 1 efficiency   | run 2 efficiency   | double ratio   |
|--------------------------------------|---------------|---------------|--------------------|--------------------|----------------|
| Total events                         | 1025230       | 1035959       | -                  | -                  | -              |
| Relaxed $D^0 \mu$ combo              | 139906        | 144221        | 61.9               | 61.9               | 1.00           |
| $D^{*+} \rightarrow D^0 \pi^+$       | 129550        | 136011        | 92.6               | 94.3               | 1.02           |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$ | 118213        | 126958        | 97.0               | 97.6               | 1.01           |
| $D^{**}$ truth-matching              | 35827         | 37755         | 30.3               | 29.7               | 0.98           |
| L0                                   | 14076         | 12375         | 39.3               | 32.8               | 0.83           |
| Hlt1                                 | 6726          | 8822          | 47.8               | 71.3               | 1.49           |
| Hlt2                                 | 2666          | 4443          | 39.6               | 50.4               | 1.27           |
| Stripping                            | 1225          | 3818          | 45.9               | 85.9               | 1.87           |
| DaVinci $D^* \mu$ cuts               | 423           | 1222          | 34.5               | 32.0               | 0.93           |
| Offline $D^0$ cuts                   | 224           | 366           | 53.0               | 30.0               | 0.57           |
| Offline $\mu$ cuts                   | 203           | 298           | 90.6               | 81.4               | 0.90           |
| Offline $D^* \mu$ combo cuts         | 185           | 273           | 91.1               | 91.6               | 1.01           |
| Total ratio                          | -             | -             | 0.0                | 0.0                | 1.46           |


## Cutflow table with real data

| cut name                                     | run 1 yield   | run 2 yield   | run 1 efficiency    | run 2 efficiency      | double ratio        |
|----------------------------------------------|---------------|---------------|---------------------|-----------------------|---------------------|
| Total events                                 | 129986930     | 486980122     | -                   | -                     | -                   |
| Stripped $D^0 \mu^-$                         | 7576232       | 35543709      | 0.058285±0.000020   | 0.072988±0.000012     | 1.25227±0.00048     |
| $D^0 \rightarrow K^- \pi^+$ (tighter $K\pi$) | 7574988       | 35529720      | 0.9998358±0.0000048 | 0.9996064±0.0000033   | 0.9997706±0.0000058 |
| $D^{*+} \rightarrow D^0 \pi^+$               | 1642940       | 7337335       | 0.21689±0.00015     | 0.206513±0.000068     | 0.95215±0.00072     |
| $\bar{B}^0 \rightarrow D^{*+} \mu^-$         | 1190313       | 4510320       | 0.72450±0.00035     | 0.61471±0.00018       | 0.84846±0.00048     |
| Refit $\bar{B}^0$ decay tree                 | 1173783       | 4434577       | 0.98611±0.00011     | 0.983207±0.000060     | 0.99705±0.00012     |
| L0                                           | 639358        | 2813588       | 0.54470±0.00046     | 0.63447±0.00023       | 1.1648±0.0011       |
| Hlt1                                         | 510855        | 2813586       | 0.79901±0.00050     | 0.99999929±0.00000093 | 1.25154±0.00078     |
| Hlt2                                         | 372095        | 2813584       | 0.72838±0.00062     | 0.99999929±0.00000093 | 1.3729±0.0012       |
| $\mu$ PID                                    | 350558        | 1796976       | 0.94212±0.00038     | 0.63868±0.00029       | 0.67792±0.00041     |
| $\text{IsoBDT}_{B^0} < 0.15$                 | 244617        | 1215751       | 0.69779±0.00077     | 0.67655±0.00035       | 0.9696±0.0012       |
| $B^0$ cuts                                   | 241038        | 1196904       | 0.98537±0.00025     | 0.98450±0.00011       | 0.99912±0.00027     |
| $K$ cuts                                     | 237327        | 901003        | 0.98460±0.00025     | 0.75278±0.00039       | 0.76455±0.00044     |
| $\pi$ cuts                                   | 234090        | 699341        | 0.98636±0.00024     | 0.77618±0.00044       | 0.78691±0.00048     |
| $\pi_{soft}$ cuts                            | 234090        | 699341        | 1.0000000±0.0000078 | 1.0000000±0.0000026   | 1.0000000±0.0000083 |
| $D^0$ cuts                                   | 220336        | 608678        | 0.94124±0.00049     | 0.87036±0.00040       | 0.92469±0.00064     |
| $D^*$ cuts                                   | 183786        | 504923        | 0.83412±0.00079     | 0.82954±0.00048       | 0.9945±0.0011       |
| Total ratio                                  | -             | -             | 0.0014139±0.0000033 | 0.0010368±0.0000015   | 0.7333±0.0020       |

!!! note
    - This table uses **full MagDown** 2012 and 2016 real data.
    - The main differences between the cut flow ntuples and the plotting
      ntuples are:
      - Cut flow ntuples use **stripping line $\mu$** but plotting ntuples use
        **all available $\mu$**.
      - Cut flow ntuples contain additional Hlt1 cuts.
    - **ALL** numbers are number of events.

!!! warn
    The first few entries are extracted from the DaVinci log, and should not be
    trusted for data cutflow.

    This is because here the _Total events_ are the events passing one of a
    couple of stripping lines, so it's not the actual _total number of events_.

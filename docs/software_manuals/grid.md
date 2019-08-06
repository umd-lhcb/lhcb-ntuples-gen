To run `DaVinci` jobs on the `GRID`, please follow these steps.

## Prepare a local `DaVinci`
We need to build a local `DaVinci` to add our tools. This local verison will
then be sent to the `GRID` by `ganga` automatically.

* For `DaVinci-v42r8p1`, please refer to [this `Dockerfile`](https://github.com/umd-lhcb/docker-images/blob/davinci-v42r8p1/lhcb-stack-cc7/Dockerfile-DaVinci-SL)
  for build instructions.


## Send job to the `GRID` with `ganga`
For each of the stripping line folder inside this project, there should be a
`Python` scripted named `ganga_jobs.py`. The general sematics is:
```
ganga ganga_jobs.py <arguments>
```

### `2012-b2D0MuXB2DMuNuForTauMuLine`
```
$ ganga ganga_jobs.py --help
usage: ganga_jobs.py [-h] [--inverse] [--davinci DAVINCI]
                     [-s {py6,py8}] [-p {Up,Down}]
                     {all,data-2012,mc-Bd2DststMuNu2D0,mc-Bd2DststTauNu2D0,mc-Bs2DststMuNu2D0,mc-Bu2DststMuNu2D0,mc-Bd2DstTauNu,mc-Bd2DstMuNu,mc-Bu2Dst0TauNu,mc-Bu2Dst0MuNu,mc-Bu2D0TauNu,mc-Bu2D0MuNu,mc-Bd2D0DX2MuX,mc-Bu2D0DX2MuX,mc-Bd2D0DsX2TauNu,mc-Bu2D0DsX2TauNu}
                     [{all,data-2012,mc-Bd2DststMuNu2D0,mc-Bd2DststTauNu2D0,mc-Bs2DststMuNu2D0,mc-Bu2DststMuNu2D0,mc-Bd2DstTauNu,mc-Bd2DstMuNu,mc-Bu2Dst0TauNu,mc-Bu2Dst0MuNu,mc-Bu2D0TauNu,mc-Bu2D0MuNu,mc-Bd2D0DX2MuX,mc-Bu2D0DX2MuX,mc-Bd2D0DsX2TauNu,mc-Bu2D0DsX2TauNu} ...]

ganga script to process R(D*) run 1 data/MC.

positional arguments:
  {all,data-2012,mc-Bd2DststMuNu2D0,mc-Bd2DststTauNu2D0,mc-Bs2DststMuNu2D0,mc-Bu2DststMuNu2D0,mc-Bd2DstTauNu,mc-Bd2DstMuNu,mc-Bu2Dst0TauNu,mc-Bu2Dst0MuNu,mc-Bu2D0TauNu,mc-Bu2D0MuNu,mc-Bd2D0DX2MuX,mc-Bu2D0DX2MuX,mc-Bd2D0DsX2TauNu,mc-Bu2D0DsX2TauNu}
                        specify data type.

optional arguments:
  -h, --help            show this help message and exit
  --inverse             if this flag is supplied, all types except specified
                        in "type" will be processed.
  --davinci DAVINCI     specify path to local DaVinci build.
  -s {py6,py8}, --simulation {py6,py8}
                        specify simulation (typically Pythia) software package
                        version.
  -p {Up,Down}, --polarity {Up,Down}
                        specify polarity.
```

An example would be:
```
ganga ganga_jobs.py mc-py6-sim08a-Bd2Dsttaunu
```

We use `ganga` and other tools to submit our `DaVinci` jobs to LHCb grid.

## Prepare a local `DaVinci`
We need to build a local `DaVinci` to add our tools. This local verison will
then be sent to the grid by `ganga` automatically.

* For `DaVinci-v42r8p1`, please refer to [this `Dockerfile`](https://github.com/umd-lhcb/docker-images/blob/davinci-v42r8p1/lhcb-stack-cc7/Dockerfile-DaVinci-SL)
  for build instructions.
* For newer version of `DaVinci`, please refer to the [`master` branch `Dockerfile`](https://github.com/umd-lhcb/docker-images/blob/master/lhcb-stack-cc7/Dockerfile-DaVinci-SL)


## Send job to the grid with `ganga`
For each of the stripping line folder inside this project, there should be a
`Python` scripted named `ganga_jobs.py`. The general sematics is:
```
ganga ganga_jobs.py <arguments>
```


### `run1-b2D0MuXB2DMuNuForTauMuLine`
```
$ ganga ganga_jobs.py --help
usage: ganga_jobs.py [-h] [--force] [--davinci DAVINCI]
                     [-b {all,Dst,D0,Dst-cutflow} [{all,Dst,D0,Dst-cutflow} ...]]
                     [-s {all,Pythia6,Pythia8} [{all,Pythia6,Pythia8} ...]]
                     [-c {all,Sim08a,Sim08e,Sim08h,Sim08i} [{all,Sim08a,Sim08e,Sim08h,Sim08i} ...]]
                     [-p {all,Up,Down} [{all,Up,Down} ...]]
                     {all,data-2012-Dst,cocktail-2011-Dst-cutflow,mc-Bd2DststMuNu2D0,mc-Bd2DststTauNu2D0,mc-Bs2DststMuNu2D0,mc-Bu2DststMuNu2D0,mc-Bd2DstTauNu,mc-Bd2DstMuNu,mc-Bu2Dst0TauNu,mc-Bu2Dst0MuNu,mc-Bu2D0TauNu,mc-Bu2D0MuNu,mc-Bd2D0DX2MuX,mc-Bu2D0DX2MuX,mc-Bd2D0
DsX2TauNu,mc-Bu2D0DsX2TauNu}
                     [{all,data-2012-Dst,cocktail-2011-Dst-cutflow,mc-Bd2DststMuNu2D0,mc-Bd2DststTauNu2D0,mc-Bs2DststMuNu2D0,mc-Bu2DststMuNu2D0,mc-Bd2DstTauNu,mc-Bd2DstMuNu,mc-Bu2Dst0TauNu,mc-Bu2Dst0MuNu,mc-Bu2D0TauNu,mc-Bu2D0MuNu,mc-Bd2D0DX2MuX,mc-Bu2D0DX2MuX,mc-Bd2D
0DsX2TauNu,mc-Bu2D0DsX2TauNu} ...]

ganga script to process R(D*) run 1 data/MC.

positional arguments:
  {all,data-2012-Dst,cocktail-2011-Dst-cutflow,mc-Bd2DststMuNu2D0,mc-Bd2DststTauNu2D0,mc-Bs2DststMuNu2D0,mc-Bu2DststMuNu2D0,mc-Bd2DstTauNu,mc-Bd2DstMuNu,mc-Bu2Dst0TauNu,mc-Bu2Dst0MuNu,mc-Bu2D0TauNu,mc-Bu2D0MuNu,mc-Bd2D0DX2MuX,mc-Bu2D0DX2MuX,mc-Bd2D0DsX2TauNu,mc-Bu2D0D
sX2TauNu}
                        specify data type.

optional arguments:
  -h, --help            show this help message and exit
  --force               if this flag is supplied, don't skip existing jobs
                        with the same name.
  --davinci DAVINCI     specify path to local DaVinci build.
  -b {all,Dst,D0,Dst-cutflow} [{all,Dst,D0,Dst-cutflow} ...], --base {all,Dst,D0,Dst-cutflow} [{all,Dst,D0,Dst-cutflow} ...]
                        specify base decay mode (e.g. D* or D0).
  -s {all,Pythia6,Pythia8} [{all,Pythia6,Pythia8} ...], --simulation {all,Pythia6,Pythia8} [{all,Pythia6,Pythia8} ...]
                        specify simulation (typically Pythia) software package
                        version.
  -c {all,Sim08a,Sim08e,Sim08h,Sim08i} [{all,Sim08a,Sim08e,Sim08h,Sim08i} ...], --condition {all,Sim08a,Sim08e,Sim08h,Sim08i} [{all,Sim08a,Sim08e,Sim08h,Sim08i} ...]
                        specify simulation condition.
  -p {all,Up,Down} [{all,Up,Down} ...], --polarity {all,Up,Down} [{all,Up,Down} ...]
                        specify polarity.
```

An example would be:
```
ganga ganga_jobs.py mc-py6-sim08a-Bd2Dsttaunu
```

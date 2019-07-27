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
ganga script to process R(D*) run 1 data/MC.

positional arguments:
  {all,mc-Bd2DstTauNu,mc-Bu2Dst0MuNu,mc-Bu2Dst0TauNu,mc-Bd2DstMuNu,data-2012}
                        specify data type.

optional arguments:
  -h, --help            show this help message and exit
  --inverse             if this flag is supplied, all types except specified
                        in "type" will be processed.
  --davinci DAVINCI     specify path to local DaVinci build.
  -s {py8,py6}, --simulation {py8,py6}
                        specify simulation (typically Pythia) software package
                        version.
  -p [{Up,Down}], --polarity [{Up,Down}]
                        specify polarity.
```

An example would be:
```
ganga ganga_jobs.py mc-py6-sim08a-Bd2Dsttaunu
```

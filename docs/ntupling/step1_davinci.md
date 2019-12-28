`DaVinci` is the LHCb package that runs preliminary selections and calculations on the raw `.dst`
data, and produces `.root` files. It is often run on LHC remote Linux nodes `lxplus`. However, it is much more
convenient to have a local `DaVinci` environment in a docker with a configuration that is easily shared.
After the docker is pulled as described in the [dependencies](ntupling/installation), it is lauched from inside
the repository with
```
cd lhcb-ntuples-gen
docker run --rm -it -v `pwd`:/data -e UID=$(id -u) -e GID=$(id -g) --net=host umdlhcb/lhcb-stack-cc7:DaVinci-v42r8p1-SL
```
This command mounts the current directory (`pwd`) into the docker, so it has access to all the code
in `lhcb-ntuples-gen` and allows you to modify it outside of the docker .

Inside the `docker`, `DaVinci` is run with
`lb-run DaVinci/latest gaudirun.py <ntuple_options1> <ntuple_options2> ...` as in `lxplus`. We often will have
scripts that facilitate this. For instance, to run on Run 2 data (note that downloading the 1-3 GB `.dst`
files from the annex takes several minutes), type in the `docker`
```
cd run2-b2D0MuXB2DMuForTauMuLine
git annex get data/data-2016-mag_down/00069527_00003141_1.semileptonic.dst   # 1.2 GB
git annex get data/data-2016-mag_down/00069529_00017556_1.semileptonic.dst   # 3.5 GB
./run.sh reco_Dst.py conds/cond-data-2016-Dst.py
```

The first argument, `reco_Dst.py`, is the script that makes the $D^{*+}(\to D^0(\to K^+\pi^-)\pi^+)\mu^-$
reconstruction. It also sets how many events to run at most (`EvtMax`) and the print frequency (`PrintFreq`).

The second argument, `conds/cond-data-2016-Dst.py`, sets the type of input data (Data or MC), the input
files and the name of the output file (`BCands_Dst-data.root` in this case).


## Running `DaVinci` on the `GRID`

We need to build a local `DaVinci` to add our tools. This local version will then be sent to the `GRID` by
`ganga` automatically. For `DaVinci-v42r8p1`, refer to [this
`Dockerfile`](https://github.com/umd-lhcb/docker-images/blob/davinci-v42r8p1/lhcb-stack-cc7/Dockerfile-DaVinci-SL)
for build instructions.

Then, for each of the stripping line folder inside this project, there should be a
`Python` scripted named `ganga_jobs.py`. The general syntax is:
```
ganga ganga_jobs.py <arguments>
```
For instance, for signal Monte Carlo
```
ganga ganga_jobs.py mc-py6-sim08a-Bd2Dsttaunu
```

The general usage of `ganga_jobs.py` is described in its help file
```
$ ganga ganga_jobs.py --help
usage: ganga_jobs.py [-h] [--force] [--davinci DAVINCI]
                     [-b {all,Dst,D0} [{all,Dst,D0} ...]]
                     [-s {all,Pythia6,Pythia8} [{all,Pythia6,Pythia8} ...]]
                     [-c {all,Sim08a,Sim08e,Sim08h,Sim08i} [{all,Sim08a,Sim08e,Sim08h,Sim08i} ...]]
                     [-p {all,Up,Down} [{all,Up,Down} ...]]
                     {all,data-2012-Dst,mc-Bd2DststMuNu2D0,mc-Bd2DststTauNu2D0,mc-Bs2DststMuNu2D0,mc-Bu2DststMuNu2D0,mc-Bd2DstTauNu,mc-Bd2DstMuNu,mc-Bu2Dst0TauNu,mc-Bu2Dst0MuNu,mc-Bu2D0TauNu,mc-Bu2D0MuNu,mc-Bd2D0DX2MuX,mc-Bu2D0DX2MuX,mc-Bd2D0DsX2TauNu,mc-Bu2D0DsX2TauNu}
                     [{all,data-2012-Dst,mc-Bd2DststMuNu2D0,mc-Bd2DststTauNu2D0,mc-Bs2DststMuNu2D0,mc-Bu2DststMuNu2D0,mc-Bd2DstTauNu,mc-Bd2DstMuNu,mc-Bu2Dst0TauNu,mc-Bu2Dst0MuNu,mc-Bu2D0TauNu,mc-Bu2D0MuNu,mc-Bd2D0DX2MuX,mc-Bu2D0DX2MuX,mc-Bd2D0DsX2TauNu,mc-Bu2D0DsX2TauNu} ...]

ganga script to process R(D*) run 1 data/MC.

positional arguments:
  {all,data-2012-Dst,mc-Bd2DststMuNu2D0,mc-Bd2DststTauNu2D0,mc-Bs2DststMuNu2D0,mc-Bu2DststMuNu2D0,mc-Bd2DstTauNu,mc-Bd2DstMuNu,mc-Bu2Dst0TauNu,mc-Bu2Dst0MuNu,mc-Bu2D0TauNu,mc-Bu2D0MuNu,mc-Bd2D0DX2MuX,mc-Bu2D0DX2MuX,mc-Bd2D0DsX2TauNu,mc-Bu2D0DsX2TauNu}
                        specify data type.

optional arguments:
  -h, --help            show this help message and exit
  --force               if this flag is supplied, don't skip existing jobs
                        with the same name.
  --davinci DAVINCI     specify path to local DaVinci build.
  -b {all,Dst,D0} [{all,Dst,D0} ...], --base {all,Dst,D0} [{all,Dst,D0} ...]
                        specify base decay mode (e.g. D* or D0).
  -s {all,Pythia6,Pythia8} [{all,Pythia6,Pythia8} ...], --simulation {all,Pythia6,Pythia8} [{all,Pythia6,Pythia8} ...]
                        specify simulation (typically Pythia) software package
                        version.
  -c {all,Sim08a,Sim08e,Sim08h,Sim08i} [{all,Sim08a,Sim08e,Sim08h,Sim08i} ...], --condition {all,Sim08a,Sim08e,Sim08h,Sim08i} [{all,Sim08a,Sim08e,Sim08h,Sim08i} ...]
                        specify simulation condition.
  -p {all,Up,Down} [{all,Up,Down} ...], --polarity {all,Up,Down} [{all,Up,Down} ...]
                        specify polarity.
```


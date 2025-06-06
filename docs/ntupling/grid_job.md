## Rationale

- The main limitation for local `DaVinci` docker is: Raw data files (`.dst`)
  need to be downloaded locally. Given that the size of `.dst` files is on the
  order of TBs, this method is only used for developing `DaVinci` scripts and
  first-order validation
    
- On `lxplus`, several official `DaVinci` versions are provided. However, there
  are some drawbacks:

    1. `.dst` files still need to be downloaded to some `lxplus` user directory
    2. While `DaVinci` is running, the connection to `lxplus` must be kept alive

LHCb collaboration provides a solution: Submitting and running `DaVinci` jobs on
a GRID. The advantages are:

1. GRID know how to access `.dst` files directly, thus there's no need to manually
   download them. Instead, users need to specify the links (`LFN`s) to desired
   `.dst` files

2. While the GRID `DaVinci` jobs are running, there's no need to keep a
   connection to `lxplus`.

The rest of this doc is divided in two parts:

1. GRID job preparation and submission on `lxplus`
2. Offline slimming and annexing of the produced ntuples on a local machine,
   most possibly on `glacier`.


## GRID job preparation and submission on `lxplus`

### Setup LHCb GRID certificate

Following [this twiki](https://twiki.cern.ch/twiki/bin/view/LHCb/FAQ/Certificate) to:

1. Apply for a GRID certificate
2. Setup the certificate on `lxplus`

!!! note
    The twiki claimed that a new user must physically go to CERN's user office
    to be able to apply for a new cert via [ca.cern.ch](https://ca.cern.ch/ca).
    But I didn't have to do that.


### Compile a local `DaVinci` on `lxplus`

We are using some non-official `TupleTool`, so we need to compile `DaVinci` on `lxplus`.

First, we need to figure out the appropriate platform for our version of DaVinci: {{ davinci_ver }}.

```bash
$ lb-run -L DaVinci/{{ davinci_ver }}
WARNING:lb-run:Using default siteroot of /cvmfs/lhcb.cern.ch/lib
x86_64+avx2+fma-centos7-gcc9-opt
x86_64-centos7-gcc9-opt
x86_64-centos7-gcc9-dbg
x86_64-centos7-gcc9-do0

```

For {{davinci_ver}}, we pick the following platform: `{{ davinci_runtime }}`.

Note that `DaVinci {{ davinci_ver }}` only provides CentOS7-based platforms.
However, CentOS7 reached End-of-Life in June 2024 (see [OTG0145248](https://cern.service-now.com/service-portal?id=outage&n=OTG0145248)), and the CentOS7-based `lxplus7` nodes are no longer available.
Consequently, our DaVinci jobs cannot be natively run on the available EL9-based `lxplus` nodes, so we need to use containers.

To setup a CentOS7 container, run the following command (adapted from the [Ganga FAQ](https://twiki.cern.ch/twiki/bin/view/LHCb/FAQ/GangaLHCbFAQ#How_do_I_run_old_Gaudi_applicati)):

```bash
apptainer exec --bind $PWD --env LBENV_SOURCED=  --bind /cvmfs:/cvmfs:ro /cvmfs/lhcb.cern.ch/containers/os-base/centos7-devel/prod/amd64/ bash --rcfile /cvmfs/lhcb.cern.ch/lib/LbEnv
lb-set-platform {{ davinci_runtime }}
export LCG_hostos=x86_64-centos7
```

And then proceed to compile `DaVinci` from inside the container.
First, we should set the chosen platform as the default for `lxplus`. Add to your login shell config:

```bash
export CMTCONFIG={{ davinci_runtime }}
export BINARY_TAG=$CMTCONFIG
```

Now, run [this script](https://github.com/umd-lhcb/docker-images/blob/master/lhcb-stack-cc7/compile_dv.sh)
anywhere on `lxplus` to build a `DaVinci` with our customizations.
The `DaVinci` will be available at `$HOME/build/DaVinciDev_{{ davinci_ver }}`.
Once `DaVinci` is compiled, you can exit the container. 

!!! note
    Our [Ganga script](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/ganga/ganga_jobs.py) also requires specific settings for DaVinci to be run in a container on the grid
    (see the [Ganga FAQ](https://twiki.cern.ch/twiki/bin/view/LHCb/FAQ/GangaLHCbFAQ#How_do_I_run_old_Gaudi_applicati)).
    If at some point we update our DaVinci version and the use of a container is no longer necessary,
    those settings should be removed.


### Configure `ganga`

`ganga` is a command-line interface for LHCb GRID. We need to configure `ganga`
job output directory. On `lxplus`:

1. Run `ganga` once. This should create a `.gangarc` in `$HOME`.
2. Locate `gangadir` option, point it to **your larger AFS storage**, for example:

    ```
    gangadir = /afs/cern.ch/user/s/suny/work/gangadir
    ```

3. Go into your `gangadir`, create a `workspace` symblink pointing to somewhere in your EOS.
   For example:

    ```
    workspace -> /eos/home-s/suny/gangadir-workspace
    ```

4. Copy [`ganga/ganga.sample.py`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/ganga/ganga.sample.py)
   to **`$HOME/.ganga.py` on `lxplus`**.


### Submitting a job with `ganga`

Submitting jobs is very simple, you will simply copy a previous script that has similar features
(eg. data, MC tracker-only), modify it appropriately, and run it. The detailed steps are

1. Log on to `lxplus` and get a proxy with `lhcb-proxy-init`
2. Clone `lhcb-ntuples-gen` and go to the appropriate `jobs` folder, for instance `lhcb-ntuples-gen/run2-rdx/jobs/`
3. Copy a script with similar characteristics and rename it with the current date and some description, [for instance](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/4b27c7dc4dd97aa1ef0efa233fe4aed836c1083a/run2-rdx/jobs/22_02_07-tracker_only_ddx_18to21.sh)

    ```
    cp 22_02_03-tracker_only_Bs.sh 22_02_03-tracker_only_ddx_22to25.sh
    ```

4. Modify the new script appropriately, for instance adding the MC IDs that you want to run. The script automatically sends the MagDown and MagUp for each sample.
5. Run the script, eg.

    ```
    ./22_02_03-tracker_only_ddx_22to25.sh
    ```

6. If there are no errors in the submission, commit the script to `git`

    !!! note
        An error such as

        ```
        GangaDiracError: All the files are only available on
        archive SEs. It is likely the data set has been archived. Contact data
        management to request that it be staged (consider --debug option for
        more information)
        ```

        simply means that the files that you are trying to
        run on do not exist, perhaps because you have a typo.

7. Monitor the status of your jobs by entering interactive `ganga` (simply type `ganga` in `lxplus` after getting a proxy) and typing `jobs`

!!! info "Usage of `ganga_jobs.py`"
    See [this appendix](#general-usage-of-ganga_jobspy).

!!! info "Manage `ganga` job output"
    You need to keep `ganga` running in a `lxplus` session to get up-to-date info
    about your jobs and download output of completed (sub)jobs.


### Update subjob status and force status to be "failed" when necessary

Sometimes ganga would stuck at updating job status. To reset the status for
"completing" and "failed" subjobs, do:

```python
jobs[63].backend.reset(True)
```

If that still doesn't bring a job to a stable state (i.e. "finished" or
"failed"), force the job to fail:

```python
jobs[63].force_status("failed", force=True)
```


### Handling failing subjobs

The GRID job are split into subjobs, enabling parallel execution. Some subjobs may fail. Considering the following `jobs` output in `ganga` shell:

```
[01:30:22]
Ganga In [2]: jobs
Ganga Out [2]:
Registry Slice: jobs (30 objects)
--------------
    fqid |    status |      name | subjobs |    application |        backend |                             backend.actualCE |                       comment |  subjob status
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      62 | completed |Dst_D0--20 |      26 |      GaudiExec |          Dirac |                                         None |                               |       0/0/0/26
      63 |    failed |Dst_D0--20 |    1007 |      GaudiExec |          Dirac |                                         None |                               |     0/1/0/1006
      66 |    failed |Dst_D0--20 |       1 |      GaudiExec |          Dirac |                                         None |                               |        0/1/0/0
      73 | completed |Dst_D0--20 |     772 |      GaudiExec |          Dirac |                                         None |                               |      0/0/0/772
```

Jobs 63 and 66 are marked as `failed` because all of their subjobs are either completed or failed.

To resubmit failed subjobs for, say, `jobs[63]`:

```python
jobs[63].resubmit()
```

However, above won't work unless all sub-jobs are either completed or failed.
To resubmit the failed sub-jobs ASAP:

```python
jobs[63].subjobs.select(status="failed").resubmit()
```

If you forced a "failed" status, some sub-jobs may be in "killed" state. A
simple `job[63].resubmit()` won't resubmit these killed jobs. To resubmit them:

```python
jobs[63].subjobs.select(status="killed").resubmit()
```

There's a helper function to print failed subjobs:

```python
show_subjobs(63)
show_subjobs(63, status='running')  # show subjobs of 'running' status
```

If for some jobs keep failing, consider the backend bad and ban it in:

- `ban_site_for_job` helper function with interactive `ganga`:

    ```python
    ban_site_for_job(63, 'LCG.site.a')
    ban_site_for_job(63, ['LCG.site.a', 'LCG.site.b'])  # you can ban multiple sites at once
    ```

    Then `resubmit` the job using methods described above

- `ganga/ganga_jobs.py` in this repo: In `BannedSites`
- `$HOME/.ganga.py` on `lxplus`: In `remake_uncompleted_job` function parameter

Sometimes it's needed to remake new jobs (say we want to change number of files
per subjob). To do so:

```python
remake_uncompleted_job(63)
```

!!! info
    The `remake_uncompleted_job` creates a new job for each **failed subjob**,
    and add the subjob index to the `comment` property of the new job.

    After the remade job has finished successfuly, merge all of its output `.root`
    files and place it _in the correct_ directory of the failing job.

    Ntuples can be merged with:

    ```
    hadd -fk <name>.root */output/*.root
    ```


## Slimming and annexing of GRID ntuples

### Offline slimming

!!! warning "Before you proceed"

    Clone `lhcb-ntuples-gen` on `glacier` and [setup `git-annex` normally](./installation.md).

    Also don't forget to do `make install-dep` in the nix shell!

We prefer to not merge `.root` files at all. Still, we need to give output files sane
names and slim them to remove unneeded branches.

Yipeng has prepared a `ganga` function that generates a `bash` script to aid the process.
To use it:

!!! warning "Before you proceed"
    The whole procedure takes a long time. It's recommeded to do it inside a `tmux` session.

1. Use `scp` to copy finished jobs to a folder `<glacierntuples>` under in your `$HOME` on `glacier`

    !!! example
        Say your `gangadir` is at `~/eos/gangadir-workspace/suny/LocalXML`, and you
        want to proceed job index `63`, then copy the folder `63` to `glacier`.

2. In `ganga` shell, type in `hadd_completed_job_output(63)`, where `63` is some job index.

    !!! info
        This will generated a `batch_hadd.sh` in `$HOME`. The generated script
        contains commands to merge output `.root` files for **all** completed
        jobs with a index that is greater or equal to the specified index.

    A script named `batch_skim.sh` will be generated in `$HOME` on `lxplus`.

    A sample `batch_skim.sh` is displayed [here](#sample-batch_skimsh).

3. Copy `batch_skim.sh` to your `lhcb-ntuples-gen` root folder on `glacier`,
    then give it execution permission with `chmod +x batch_skim.sh`.

    !!! info "Alternative slimming"
        At some point, we decided to change our folder structure for storing our rdx tuples (to be easier to find files, but note that this procedure won't work for other tuples, eg. `JpsiK`). This can be achieved by either continuing with this procedure and following the (new) step 6, or alternatively you can use `scripts/step1_slim.py` to do this more easily (and also automatically keep track of your total events + failed `ganga` subjobs!). To use this script, with your copied `batch_skim.sh` inside `lhcb-ntuples-gen/`, run

        ```shell
        python scripts/step1_slim.py <ganga_output_dir> <new_slimmed_ntuple_dir> batch_skim.sh
        (eg. python scripts/step1_slim.py ../ntuples_to_merge ntuples/0.9.12-all_years batch_skim.sh)
        ```

        This script automatically chooses `postprocess/skims/rdx_mc.yml` for the slimming. If you run this, the rdx folder structure should be correct, and you can skip steps 4-6.


4. Set the input folder and postprocessing rules as needed in `batch_skim.sh`:

    ```bash
    INPUT_DIR=<glacierntuples>
    SKIM_CONFIG=./postprocess/skims/rdx_mc.yml  # NOTE: Make sure you pick the right one!!!
    ```

    !!! info
        If you don't want to remove any branches, then replace:

        ```shell
        ./ganga/ganga_skim_job_output.py ${OUTPUT_DIR}/$2 ${INPUT_DIR}/$1 ${SKIM_CONFIG}
        ```

        with

        ```shell
        ./ganga/ganga_skim_job_output.py ${OUTPUT_DIR}/$2 ${INPUT_DIR}/$1 ${SKIM_CONFIG} --copy
        ```

        Noting the use of `--copy` flag.

5. Go into a nix shell in your `lhcb-ntuples-gen` with `nix develop`, then in
    the project root, run:

    ```
    ./batch_skim.sh ntuples/<folder_to_ntuple_output>
    ```

    For example, `<folder_to_ntuple_output>` can be:

    ```
    0.9.6-2016-production/Dst_D0-mc-tracker-only
    ```

6. We decided to change our folder naming scheme, so before annexing (in principle this works after annexing too, but it's safer to do it before annexing), if not following the alternative slimming procedure above, run
    
    ```
    python scripts/move_step1_ntuples.py <step1_tuple_dir_old_paths> <output_dir>
    (eg. python scripts/move_step1_ntuples.py ntuples/0.9.100-new_rdx_tuples ntuples/0.9.100-new_rdx_tuples)
    ```

    This script assumes your `rdx-run2-analysis` and `lhcb-ntuples-gen` repos live in the same directories; if they don't, you'll have to specify an additional parameter when running the above command `-s <path_to_rdx-run2-analysis>/fit/spec/histos.yml` (the script references our rdx templates to create the new folder naming scheme).


### Annex ntuples

!!! info
    We decide to use a pull-request-based workflow for ntuple annexation to
    minimize errors.

    ...but if you consider yourself a trusted user (ie. are comfortable enough adding tuples to the annex), you can ignore this section and just annex+commit the tuples on your own.

1. Create a new branch on your `lhcb-ntuples-gen` project on `glacier`, then checkout that branch:

    ```
    git branch <branch_name>
    git checkout <branch_name>
    ```

    !!! example

        ```
        git branch yipeng-ddx_part1
        git checkout yipeng-ddx_part1
        ```

2. Go to the folder that contains your newly slimmed ntuples, then do `git annex add .`
    and commit changes with `git commit . -m <comment>`.

    !!! example

        ```
        cd ntuples/0.9.6-2016-production/Dst_D0-mc-tracker-only
        git annex add .
        git commit . -m "Part 1 of DDX MC"
        ```

3. Push this branch to Github with `git push origin <branch_name>`,
    then create a pull-request.

    !!! info
        If the `git push origin <branch_name>` failed, check your `git` history
        and make sure you **didn't** added ntuples (large files) directly with
        `git add`.

        Github will refuse files larger than 100 MB.

    Once everything checks out, one of **{{ admin }}** will merge the request.

4. Once the request is merged, do the following:

    ```
    git checkout master
    git pull origin master
    ```

    verify that your annexed ntuples are there, then do the following in the
    `lhcb-ntuples-gen` project root:

    ```shell
    git annex sync
    git annex copy . --to glacier
    git annex sync  # YES, you need to do it twice, once before copying, and once after!
    ```

5. Once you finish all these, inform **{{ admin }}**.


!!! info
    For more info on `git-annex` usage, review the
    [`git-annex` entry](../software_manuals/git_annex.md).


## Appendix

### Sample `batch_skim.sh`

```bash
#!/usr/bin/env bash
INPUT_DIR=~/ntuples  # NOTE: Configure this before proceed!!!
SKIM_CONFIG=./postprocess/skims/rdx_mc.yml  # NOTE: Make sure you pick the right one!!!
OUTPUT_DIR=$1
MIN_NTUPLE_SIZE=500  # in KiB

RED='[0;31m'
NC='[0m' # No Color


function check_job () {
  local error=0
  local job_dir=${INPUT_DIR}/$1
  local num_of_subjobs=$2

  echo "Verifying output for Job $1, which has $2 subjobs..."
  # might require GNU find
  local folders=$(find $job_dir -mindepth 1 -maxdepth 1 -type d -regex ".*/[0-9]*" | wc -l)

  if [[ $folders -ne $num_of_subjobs ]]; then
      echo -e "${RED}Found $folders subjobs, which =/= $num_of_subjobs. Terminate now.${NC}"
      exit 1
  fi

  for sj in $(ls $job_dir | grep -E "^[0-9].*$"); do
    local file=$(find $job_dir/$sj/output -name '*.root')

    if [[ -z $file ]]; then
      let "error++"
      echo -e "${RED}subjob $sj: ntuple missing!${NC}"
    else
      local size=$(du -b $file | awk '{print int($1 / 1024)}')  # in KiB
      if [ $size -lt ${MIN_NTUPLE_SIZE} ]; then
        let "error++"
        echo -e "${RED}subjob $sj: ntuple has a size of $size KiB, which is too small!${NC}"
      fi
    fi
  done

  if [ $error -gt 0 ]; then
    echo -e "${RED}Job $1 output verification failed with $error error(s).${NC}"
    exit $error  # exit early to make errors easy to see
  fi

  return $error
}

function concat_job () {
  check_job $1 $2

  if [ $? -eq 0 ]; then
    ./ganga/ganga_skim_job_output.py ${OUTPUT_DIR}/$3 ${INPUT_DIR}/$1 ${SKIM_CONFIG}
  fi
}

concat_job 180 111 Dst_D0--22_02_07--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_11894600_D0TAUNU.SAFESTRIPTRIG.DST.root
```


### General usage of `ganga_jobs.py`

For this repo, there is a **central** `ganga` job submitter that should handle
**all** job submissions for **all** analyses with **all** reconstruction
scripts in **all** folders.
The script is located at: [`ganga/ganga_jobs.py`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/ganga/ganga_jobs.py). For it

The general syntax is:
```
ganga_jobs.py <reco_script> <cond_files>
```

For instance, for run 1 $R(D^{*})$ signal Monte Carlo:
```
ganga_jobs.py run1-rdx/reco_Dst_D0.py run1-rdx/cond/cond-mc-2012-md-sim08a.py -p mu -P Pythia6 -d 11574020
```

!!! note
    - The `-p` and `-P` are optional. They have default values.
    - The `-d` flag has a dummy default of `00000000`. For actual values, consult [data sources](../data/data_sources.md).

!!! info
    The usage of `ganga_jobs.py` is described by:

    ```
    ganga_jobs.py --help
    ```

    Most of submissions are wrapped in shell scripts. Some of them can be found [here](https://github.com/umd-lhcb/lhcb-ntuples-gen/tree/master/run2-rdx/jobs).

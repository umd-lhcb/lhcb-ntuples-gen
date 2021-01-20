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


## Preparation

### Setup LHCb GRID certificate

Following [this twiki](https://twiki.cern.ch/twiki/bin/view/LHCb/FAQ/Certificate) to:

1. Apply for a GRID certificate
2. Setup the certificate on `lxplus`

!!! note
    The twiki claimed that a new user must physically go to CERN's user office
    to be able to apply for a new cert via [ca.cern.ch](https://ca.cern.ch/ca).
    But I didn't have to do that.

### Compile a local `DaVinci` on `lxplus`

We are using some non-official `TupleTool`, so we need to compile `DaVinci` on lxplus.

First, we need to figure out the runtime dependency for our version of DaVinci: {{ davinci_ver }}.
```
lb-run -L DaVinci/v45r4
```

For {{davinci_ver}}, we pick the following runtime: `{{ davinci_runtime }}`.

We should set that runtime as the default for `lxplus`. Add to your login shell config:
```bash
export CMTCONFIG={{ davinci_runtime }}
export BINARY_TAG=$CMTCONFIG
```

Now, following these instruction to build a `DaVinci` with our custom `TupleTool`s:
```bash
mkdir -p build
cd build

DAVINCI_VERSION={{ davinci_ver }}
TUPLETOOL_SL_VERSION={{ davinci_sl_tool_ver }}

# Only do this if you don't have username and email settings configured for git
#git config --global user.name "Physicist"
#git config --global user.email "lhcb@physics.umd.edu"

lb-dev DaVinci/${DAVINCI_VERSION}
cd DaVinciDev_${DAVINCI_VERSION}

git lb-use TupleToolSemiLeptonic https://github.com/umd-lhcb/TupleToolSemiLeptonic.git
git lb-checkout TupleToolSemiLeptonic/${TUPLETOOL_SL_VERSION} Phys/TupleToolSemiLeptonic

make configure && make
```

Now, the `DaVinci` will be available at `$HOME/build/DaVinciDev_{{ davinci_ver }}`.

### Configure `ganga`

`ganga` is a command-line interface for LHCb GRID. We need to configure ganga
job output directory. On `lxplus`:

1. Run `ganga` once. This should create a `.gangarc` in `$HOME`.
2. Locate `gangadir` option, point it to some directory that is large enough.
   The user's EOS directory should do.


## Submitting a job with `ganga`

For this repo, there is a **central** `ganga` job submitter that should handle
**all** job submissions for **all** reconstruction scripts in **all** folders.
The script is located at: [`scripts/ganga/ganga_jobs.py`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/scripts/ganga/ganga_jobs.py).

!!! warning
    - The submitter script can only run on `lxplus` nodes!
    - It is needed to clone this repo on your `lxplus`!

!!! error "Before you proceed"
    When you login to `lxplus`, you need to create a certificate proxy to access GRID.

    Always do the following before doing anything `ganga`-related:
    ```
    lhcb-proxy-init
    ```
    then following instructions on screen.

The general syntax is:
```
ganga_jobs.py <reco_script> <cond_files>
```

For instance, for run 1 $R(D^{*})$ signal Monte Carlo:
```
ganga_jobs.py ../../run1-rdx/reco_Dst_D0.py ../../run1-rdx/cond/cond-mc-2012-md-sim08a.py -p mu -P Pythia6 -d Bd2DstTauNu
```

!!! note
    The last three flags: `-p`, `-P`, and `-d` are optional. They have default values.

!!! note
    The usage of `ganga_jobs.py` is described by:
    ```
    ganga_jobs.py --help
    ```

After a successfully submission, the progress of the job can be checked with ganga:

1. Launch `ganga` from a `lxplus` session
2. In the `ganga` shell, type in `jobs`


## Handling failing subjobs

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

To resubmit failed subjobs for, say, `job[66]`:
```
jobs[66].resubmit()
```


## Manage `ganga` job output

You need to keep `ganga` running in a `lxplus` session to get up-to-date info
about your jobs and download output of completed (sub)jobs.

We prefer to merge all output `.root` files from subjobs. There's a helper
`ganga` function written by Yipeng for that [^1]. To use it:

1. Copy [`scripts/ganga/ganga.sample.py`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/scripts/ganga/ganga.sample.py) to `$HOME/.ganga.py` **on `lxplus`**.

2. In `ganga` shell, type in `hadd_completed_job_output(63)`, where `63` is some job index.

    !!! info
        This will generated a `batch_hadd.sh` in `$HOME`. The generated script
        contains commands to merge output `.root` files for **all** completed
        jobs with a index that is greater or equal to the specified index.

3. Change the `INPUT_DIR` variable of the script to your ganga output workspace

4. `chmod+x batch_hadd.sh`, then run it with `./batch_hadd.sh <output_dir_for_merged_ntuple>`

    !!! note
        The `batch_hadd.sh` script will check the outputs of the jobs so that:

        1. Every single subjob contains a `*.root` file.
        2. The `*.root` file has a size of at least 500 KiB.

    !!! info
        A generated `batch_hadd.sh` looks like this:

        ```bash
        #!/usr/bin/env bash
        INPUT_DIR=/afs/cern.ch/user/s/suny/work/gangadir/workspace/suny/LocalXML
        OUTPUT_DIR=$1
        MIN_NTUPLE_SIZE=500  # in KiB


        function check_job () {
          local error=0
          local job_dir=${INPUT_DIR}/$1

          echo "Verifying output for Job $1..."

          for sj in $(ls $job_dir | grep -E "^[0-9]$"); do
            local file=$(find $job_dir/$sj/output -name '*.root')

            if [[ -z $file ]]; then
              let "error++"
              echo "subjob $sj: ntuple missing!"
            else
              local size=$(du -b $file | awk '{print int($1 / 1024)}')  # in KiB
              if [ $size -lt ${MIN_NTUPLE_SIZE} ]; then
                let "error++"
                echo "subjob $sj: ntuple has a size of $size KiB, which is too small!"
              fi
            fi
          done

          if [ $error -gt 0 ]; then
            echo "Job $1 output verification failed with $error error(s)."
          fi

          return $error
        }

        function concat_job () {
          check_job $1

          if [ $? -eq 0 ]; then
            hadd -fk ${OUTPUT_DIR}/$3 ${INPUT_DIR}/$1/*/output/$2
          fi
        }

        concat_job 73 std.root Dst_D0--20_10_12--std--LHCb_Collision11_Beam3500GeV-VeloClosed-MagDown_Real_Data.root
        ```

5. Finally, rename the merged ntuple in the following way:
    1. The merged ntuple has a filename of 80 characters long. This is because
       the `ganga_jobs.py` trims the job names (which is the same as the ntuple
       name) because `ganga` doesn't allow super long job names.

    2. To figure out the full filename, do a fake submit with
       `ganga_sample_jobs_parser.py`:
        ```
        ganga_sample_jobs_parser.py <reco_script> <cond_files> [optional_flags]
        ```

    3. Use this as the final filename. The **date** should come from the
       trimmed filename, though.

    !!! example
        Suppose after merging, the ntuple name is the following:
        ```
        Dst_D0--21_01_13--mc--MC_2012_Beam4000GeV-2012-MagDown-NoRICHesSim-Nu2.5-Pythia8.root
        ```

        The original filename can be figured out with:
        ```
        ganga_sample_jobs_parser.py run1-rdx/reco_Dst_D0.py run1-rdx/conds/cond-mc-2012-mu-sim09a.py -p md -d Bd2DstMuNu
        ```

        The output would be:

        ```
        Reconstruction script: run1-rdx/reco_Dst_D0.py
        Condition file: run1-rdx/conds/cond-mc-2012-mu-sim09a.py
        Fields from cond file: OrderedDict([('year', '2012'), ('polarity', 'mu'), ('simcond', 'sim09a')])
        LFN: /MC/2012/Beam4000GeV-2012-MagDown-NoRICHesSim-Nu2.5-Pythia8/Sim09a/Trig0x409f0045-NoRichPIDLines/Reco14c/Stripping21Filtered/11574020/DSTTAUNU.SAFESTRIPTRIG.DST
        NTuple name: Dst_D0--21_01_20--mc--MC_2012_Beam4000GeV-2012-MagDown-NoRICHesSim-Nu2.5-Pythia8_Sim09a_Trig0x409f0045-NoRichPIDLines_Reco14c_Stripping21Filtered_11574020_DSTTAUNU.SAFESTRIPTRIG.DST.root
        ```

        Then the final filename should be:
        ```
        Dst_D0--21_01_13--mc--MC_2012_Beam4000GeV-2012-MagDown-NoRICHesSim-Nu2.5-Pythia8_Sim09a_Trig0x409f0045-NoRichPIDLines_Reco14c_Stripping21Filtered_11574020_DSTTAUNU.SAFESTRIPTRIG.DST.root
        ```

    !!! info
        The reason to use the super line filename that is derived directly from
        LFN is:
        The trimmed name lacks important info, such as simulation condition. If
        we don't include them in the filename, eventually they'll be forgotten.

    !!! info
        To rename or relocate already annexed files, treat them as regular
        files added in `git`.

        For more details, refer to [this section](../software_manuals/git_annex.md#change-the-name-of-annexed-files)
        of the `git-annex` manual.


[^1]: There's an official way to merge `.root` files with `ganga`, but the
      method described in the main text offers checks to job output ntuples.

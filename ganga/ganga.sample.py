# NOTE: Copy this file to your lxplus $HOME, and rename it as .ganga.py

###########
# Helpers #
###########

POLARITY = {'Up': 'mag_up', 'Down': 'mag_down'}
SIMULATION = {'Pythia6': 'py6', 'Pythia8': 'py8'}


def normalize_hadd_filename(job):
    # For newer jobs, the canonical job filename is stored in the 'comment'
    # field of the job
    if job.comment:
        return job.comment

    return job.name + '.root'


def get_ntuple_filename(j):
    output_files = j.subjobs(0).outputfiles

    for f in output_files:
        name = f.namePattern
        if 'hist' not in name:
            return name


def gen_hadd_script(instructions, output_script, input_dir, output_dir='$1',
                    min_ntuple_size=500):
    from os.path import expanduser

    header = '''#!/usr/bin/env bash
INPUT_DIR={}
OUTPUT_DIR={}
MIN_NTUPLE_SIZE={}  # in KiB

# User-specific settings, change them according to your environment!
LNG_PATH=$HOME/src/lhcb-ntuples-gen
YAML_PATH=$LNG_PATH/postprocess/skims/rdx_mc.yml
BIN_PATH=$LNG_PATH/scripts

'''.format(input_dir, output_dir, min_ntuple_size)

    functions = '''
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
    python2 $BIN_PATH/haddcut.py ${OUTPUT_DIR}/$3 ${INPUT_DIR}/$1/*/output/$2 \\
        -c $YAML_PATH
  fi
}

'''

    with open(expanduser(output_script), 'w') as f:
        f.write(header)
        f.write(functions)

        for idx, orig_filename, hadd_filename in instructions:
            f.write('concat_job {idx} {orig_filename} {hadd_filename}\n'.format(
                hadd_filename=hadd_filename, idx=idx,
                orig_filename=orig_filename))


##################
# Job operations #
##################

def kill_uncompleted_subjobs(idx):
    for sj in jobs(idx).subjobs:
        if sj.status != 'completed':
            sj.kill()


def collect_input_from_uncompleted_job(idx):
    ds = LHCbDataset()
    for sj in jobs(idx).subjobs.select(status='failed'):
        ds.extend(sj.inputdata)

    return ds


def remake_uncompleted_job(idx, banned_sites=[
        'LCG.NCBJ.pl',
        'LCG.NIPNE-07.ro',
        'LCG.Beijing.cn'
]):
    ds = collect_input_from_uncompleted_job(idx)

    j = jobs(idx).copy()
    j.inputdata = ds
    j.backend.settings['BannedSites'] = banned_sites
    j.submit()


def print_job_hadd_filename(init_idx=0):
    for j in jobs:
        if j.id >= init_idx:
            print('----')
            print('Job {}: {}'.format(j.id, j.status))
            print('hadd filename: {}'.format(normalize_hadd_filename(j)))


def hadd_completed_job_output(
        init_idx=0,
        output_script='~/batch_hadd.sh',
        completed_only=False
):
    input_dir = None

    instructions = []
    for j in jobs:
        if j.id >= init_idx:
            if not input_dir:
                input_dir = '/'.join(j.inputdir.split('/')[:-3])

            if j.status != 'completed':
                print('Warning: job {} has a name {} and status {}'.format(j.id, j.name, j.status))
                if completed_only:
                    print('Skipping...')
                    continue

            instructions.append((j.id, get_ntuple_filename(j),
                                 normalize_hadd_filename(j)))

    gen_hadd_script(instructions, output_script, input_dir)

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


def gen_hadd_script(instructions, output_script, output_dir='$1',
                    min_ntuple_size=500):
    from os.path import expanduser

    header = '''#!/usr/bin/env bash
INPUT_DIR=/dev/null  # NOTE: Configure this before proceed!!!
SKIM_CONFIG=./postprocess/skims/rdx_mc.yml  # NOTE: Make sure you pick the right one!!!
OUTPUT_DIR={}
MIN_NTUPLE_SIZE={}  # in KiB

RED='\033[0;31m'
NC='\033[0m' # No Color

'''.format(output_dir, min_ntuple_size)

    functions = '''
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

'''

    with open(expanduser(output_script), 'w') as f:
        f.write(header)
        f.write(functions)

        for idx, size, name in instructions:
            f.write(f'concat_job {idx} {size} {name}\n')


##################
# Job operations #
##################

def show_subjobs(idx, status='failed'):
    print(jobs(idx).subjobs.select(status=status))


def ban_site_for_job(idx, sites):
    if not isinstance(sites, list):
        sites = [sites]

    for sj in jobs(idx).subjobs.select(status='failed'):
        sj.backend.settings['BannedSites'] += sites


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
], files_per_job=2):
    for failed_sj in jobs[idx].subjobs.select(status='failed'):
        print(f'Remaking failed subjob {failed_sj.fqid}')

        j = failed_sj.copy(unprepare=True)
        j.comment += f'--{failed_sj.fqid}'

        j.splitter = SplitByFiles(filesPerJob=files_per_job)
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
        output_script='~/batch_skim.sh',
        completed_only=False
):
    instructions = []
    for j in jobs:
        if j.id >= init_idx:
            if j.status != 'completed':
                print('Warning: job {} has a name {} and status {}'.format(j.id, j.name, j.status))
                if completed_only:
                    print('Skipping...')
                    continue

            instructions.append((j.id, len(j.subjobs), normalize_hadd_filename(j)))

    gen_hadd_script(instructions, output_script)

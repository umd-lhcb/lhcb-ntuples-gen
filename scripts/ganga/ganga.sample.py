# NOTE: Copy this file to your lxplus $HOME, and rename it as .ganga.py

###########
# Helpers #
###########

POLARITY = {'Up': 'mag_up', 'Down': 'mag_down'}
SIMULATION = {'Pythia6': 'py6', 'Pythia8': 'py8'}


def normalize_hadd_filename(job_name):
    return job_name + '.root'


def get_ntuple_filename(j):
    output_files = j.subjobs(0).outputfiles

    for f in output_files:
        name = f.namePattern
        if 'hist' not in name:
            return name


def gen_hadd_script(instructions, output_script, input_dir, output_dir='$1'):
    from os.path import expanduser
    header = '''#!/bin/bash
INPUT_DIR={}
OUTPUT_DIR={}

'''.format(input_dir, output_dir)

    with open(expanduser(output_script), 'w') as f:
        f.write(header)

        for idx, orig_filename, hadd_filename in instructions:
            f.write('hadd -fk ${{OUTPUT_DIR}}/{hadd_filename} ${{INPUT_DIR}}/{idx}/*/output/{orig_filename}\n'.format(
                hadd_filename=hadd_filename, idx=idx, orig_filename=orig_filename))


##################
# Job operations #
##################

def kill_uncompleted_subjobs(idx):
    for sj in jobs(idx).subjobs:
        if sj.status != 'completed':
            sj.kill()


def remake_uncompleted_job(idx, banned_sites=['LCG.NCBJ.pl', 'LCG.NIPNE-07.ro']):
    ds = LHCbDataset()
    for sj in jobs(idx).subjobs:
        if sj.status != 'completed':
            ds.extend(sj.inputdata)

    j = jobs(idx).copy()
    j.inputdata = ds
    j.backend.settings['BannedSites'] = banned_sites
    j.submit()


def print_job_hadd_filename(init_idx=0):
    for j in jobs:
        if j.id >= init_idx:
            print('----')
            print('Job {}: {}'.format(j.id, j.status))
            print('hadd filename: {}'.format(normalize_hadd_filename(j.name)))


def hadd_completed_job_output(
        init_idx=0,
        output_script='~/batch_hadd.sh',
        input_dir='~/eos/gangadir-workspace/suny/LocalXML',
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

            instructions.append((j.id, get_ntuple_filename(j),
                                 normalize_hadd_filename(j.name)))

    gen_hadd_script(instructions, output_script, input_dir)

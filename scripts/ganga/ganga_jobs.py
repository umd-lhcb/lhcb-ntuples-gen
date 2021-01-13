#!/usr/bin/env ganga
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Jan 13, 2021 at 11:59 AM +0100
#
# Description: A demonstration on ganga option file with parser.
#              This demo runs stand-alone, provided that Python is installed:
#                  python ./ganga_jobs_parser.py [options]
#
#              Alternatively, in lxplus:
#                  ganga ./ganga_job_parser.py [options]

from argparse import ArgumentParser
from itertools import product
from datetime import datetime
from pathlib import Path
from collections import OrderedDict as odict
from os.path import expanduser, realpath, dirname
from os.path import join as path_join
from re import search

# Append current directly to PYTHONPATH so we can load stuff from
# ganga_sample_jobs_parser.py
import sys
sys.path.insert(1, dirname(realpath(__file__)))

# Stuff from ganga_sample_jobs_parser.py
from ganga_sample_jobs_parser import (
    LFN_PATH, MC_PYTHIA, MC_DECAY_MODE, MC_POLARITY,
    gen_date,
    parse_reco_script_name,
    parse_cond_file_name,
    gen_lfn_key,
    gen_lfn_path
)
from ganga_sample_jobs_parser import parse_input as base_parse_input


##########################
# Parameters for data/MC #
##########################

PLATFORM = 'x86_64-centos7-gcc9-opt'
WEIGHT_FILE = 'weights_soft.xml'
FILES_PER_JOB_DATA = 5
FILES_PER_JOB_MC = 2


###########
# Helpers #
###########

def conf_job_app(davinci_path, options):
    app = GaudiExec()
    app.directory = expanduser(davinci_path)
    app.options = options
    app.platform = PLATFORM
    return app


#################################
# Command line arguments parser #
#################################

def parse_input():
    _, parser = base_parse_input()
    parser.add_argument('--force',
                        action='store_true',
                        help='''
if this flag is supplied, don't skip existing jobs with the same name.''')

    parser.add_argument('--davinci',
                        default='~/build/DaVinciDev_v45r4',
                        help='''
specify path to local DaVinci build.''')

    return parser.parse_args()


########
# Main #
########

args = parse_input()

fields, reco_type, additional_flags = parse_cond_file_name(args.cond_file)
reco_sample = parse_reco_script_name(args.reco_script)

# Try to add missing fields required to reconstruct LFNs
lfn, lfn_jobname = gen_lfn_path(
    LFN_PATH[reco_type+'-'+fields['year']], fields,
    odict({'polarity': args.polarity,
           'pythia': args.pythia,
           'decay': args.decay})
)

job_name_fields = [reco_sample, gen_date(), reco_type, lfn_jobname]
if additional_flags:
    job_name_fields.insert(3, additional_flags)
job_name = '--'.join(job_name_fields)[:80]
submitted_jobs = [j.name for j in jobs]

# Only create job if no existing job has the same name or force create
if args.force or job_name not in submitted_jobs:
    print('Preparing job {}'.format(job_name))
    j = Job(name=job_name)

    # Get input data from DIRAC
    data = BKQuery(lfn, dqflag=['OK']).getDataset()
    j.inputdata = data

    # Provide weight file
    weight_file = path_join(dirname(realpath(args.reco_script)), WEIGHT_FILE)
    j.inputfiles = [LocalFile(weight_file)]

    # Use DIRAC backend
    j.backend = Dirac()
    files_per_job = FILES_PER_JOB_MC if 'mc' in reco_type \
        else FILES_PER_JOB_DATA
    j.splitter = SplitByFiles(filesPerJob=files_per_job)
    j.outputfiles = [LocalFile('*.root')]

    # Get path to option files, also prepare DaVinci
    options = [args.cond_file, args.reco_script]
    app = conf_job_app(args.davinci, options)
    j.application = app

    # Submit!
    j.submit()

else:
    print('Job with name {} already exist, skipping...'.format(job_name))

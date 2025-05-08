#!/usr/bin/env ganga
#
# Author: Yipeng Sun, Lucas Meyer Garcia
# License: BSD 2-clause
#
# Description: A demonstration on ganga option file with parser.
#              This demo runs stand-alone, provided that Python is installed:
#                  python ./ganga_jobs_parser.py [options]
#
#              Alternatively, in lxplus:
#                  ganga ./ganga_job_parser.py [options]
#
#              Mostly adapted from ganga_jobs.py

from os.path import expanduser, realpath, dirname, basename, isdir, abspath

# Append current directly to PYTHONPATH so we can load stuff from
# ganga_sample_jobs_parser.py
import sys
sys.path.insert(1, dirname(realpath(__file__)))

# Stuff from ganga_sample_jobs_parser.py
from ganga_sample_jobs_parser import args, lfn, job_name, ntuple_name


#####################
# Parameters for MC #
#####################

DV_VERSION = 'v46r12' # Used in last step (merging) of b-inclusive D* MC (27163974)
PLATFORM = 'x86_64_v2-el9-gcc13-opt'


###########
# Helpers #
###########

def conf_job_app(davinci_path, dv_version, options):
    app = GaudiExec()
    app_dir = abspath( expanduser(f'{davinci_path}/DaVinciDev_{dv_version}') )
    if isdir(app_dir):
        # DaVinci installation already done
        app.directory = app_dir
    else:
        # Need to prepare DaVinci
        path = expanduser(davinci_path)
        print(f"Preparing DaVinci {dv_version} installation at {app_dir}")
        app = prepareGaudiExec('DaVinci', dv_version, myPath=path)
    app.options = options
    app.platform = PLATFORM
    return app


########
# Main #
########

print('Preparing job {}'.format(job_name))
j = Job(name=job_name, comment=ntuple_name)

# Get input data from DIRAC
data = BKQuery(lfn, dqflag=['OK']).getDataset()
j.inputdata = data

# Use DIRAC backend
j.backend = Dirac()

j.splitter = SplitByFiles(filesPerJob=1)
j.outputfiles = [DiracFile('*.root')]

# Get path to option files, also prepare DaVinci
options = [args.cond_file, args.reco_script]
app = conf_job_app('~/build', DV_VERSION, options)
j.application = app

# Submit!
j.submit()

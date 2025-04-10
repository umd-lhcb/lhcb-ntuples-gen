#!/usr/bin/env ganga
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Feb 17, 2022 at 03:33 PM -0500
#
# Description: A demonstration on ganga option file with parser.
#              This demo runs stand-alone, provided that Python is installed:
#                  python ./ganga_jobs_parser.py [options]
#
#              Alternatively, in lxplus:
#                  ganga ./ganga_job_parser.py [options]

from os.path import expanduser, realpath, dirname
from os.path import join as path_join

# Append current directly to PYTHONPATH so we can load stuff from
# ganga_sample_jobs_parser.py
import sys
sys.path.insert(1, dirname(realpath(__file__)))

# Stuff from ganga_sample_jobs_parser.py
from ganga_sample_jobs_parser import args, reco_type, lfn, job_name, ntuple_name


##########################
# Parameters for data/MC #
##########################

PLATFORM = 'x86_64-centos7-gcc9-opt'
WEIGHT_FILE = 'weights_soft.xml'
FILES_PER_JOB_DATA = 60
FILES_PER_JOB_MC = 3


###########
# Helpers #
###########

def conf_job_app(davinci_path, options):
    app = GaudiExec()
    app.directory = expanduser(davinci_path)
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

# Provide weight file
weight_file = path_join(dirname(realpath(args.reco_script)), WEIGHT_FILE)
j.inputfiles = [LocalFile(weight_file)]

# Use DIRAC backend
j.backend = Dirac()
# j.backend.settings['BannedSites'] = [
    # 'LCG.NCBJ.pl',
    # 'LCG.NIPNE-07.ro',
    # 'LCG.Beijing.cn'
# ]

files_per_job = FILES_PER_JOB_MC if 'MC' in lfn else FILES_PER_JOB_DATA

j.splitter = SplitByFiles(filesPerJob=files_per_job)
j.outputfiles = [LocalFile('*.root')]

# Get path to option files, also prepare DaVinci
options = [args.cond_file, args.reco_script]
app = conf_job_app(args.davinci, options)
j.application = app
# Use CentOS7 container.
# For more information, check
# https://twiki.cern.ch/twiki/bin/view/LHCb/FAQ/GangaLHCbFAQ#How_do_I_run_old_Gaudi_applicati
j.application.useApptainer = True
j.application.containerLocation = '/cvmfs/lhcb.cern.ch/containers/os-base/centos7-devel/prod/amd64/'

# Submit!
j.submit()

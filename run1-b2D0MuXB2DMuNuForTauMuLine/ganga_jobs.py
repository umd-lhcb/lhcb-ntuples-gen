#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Jun 05, 2020 at 05:17 PM +0800
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


##########################
# Parameters for data/MC #
##########################

PLATFORM = 'x86_64-centos7-gcc62-opt'
WEIGHT_FILE = './weights_soft.xml'
FILES_PER_JOB_DATA = 5
FILES_PER_JOB_MC = 2

# Example for a fully constructed MC file path:
# '/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20Filtered/11873010/DSTTAUNU.SAFESTRIPTRIG'
LFN_PATH = {
    'std-2012': '/LHCb/Collision12/Beam4000GeV-VeloClosed-Mag{polarity}/Real Data/Reco14/Stripping21/90000000/SEMILEPTONIC.DST',
    'mc-2012': '/MC/2012/Beam4000GeV-2012-Mag{polarity}-Nu2.5-{pythia}/{simcond}/Digi13/Trig0x409f0045/Reco14a/Stripping20Filtered/{decay}/DSTTAUNU.SAFESTRIPTRIG.DST',
    'cutflow_mc-2011': '/MC/2011/Beam3500GeV-2011-Mag{polarity}-Nu2-Pythia8/{simcond}/Digi13/Trig0x40760037/Reco14c/Stripping20r1NoPrescalingFlagged/11874091/ALLSTREAMS.DST',
}
LFN_PATH['cutflow_data-2012'] = LFN_PATH['std-2012']

MC_PYTHIA = ['Pythia6', 'Pythia8']

# Decay mode IDs.
MC_DECAY_MODE = {
    # Dstst
    'Bd2DststMuNu2D0': '11873010',
    'Bd2DststTauNu2D0': '11873030',
    'Bs2DststMuNu2D0': '13873000',
    'Bu2DststMuNu2D0': '12873010',
    # Dst
    'Bd2DstTauNu': '11574010',
    'Bd2DstMuNu': '11574020',
    'Bu2Dst0TauNu': '12573020',
    'Bu2Dst0MuNu': '12573030',
    # D0
    'Bu2D0TauNu': '12573000',
    'Bu2D0MuNu': '12573010',
    'Bd2D0DX2MuX': '11873000',
    'Bu2D0DX2MuX': '12873000',
    'Bd2D0DsX2TauNu': '11873020',
    'Bu2D0DsX2TauNu': '12873020',
}

MC_POLARITY = {
    'mu': 'Up',
    'md': 'Down'
}


###########
# Helpers #
###########

def gen_date(time=datetime.now()):
    return time.strftime('%y_%m_%d')


def parse_reco_script_name(reco_script):
    return '_'.join(Path(reco_script).stem.split('_')[1:])


def parse_cond_file_name(cond_file):
    result = odict({
        'type': None, 'year': None, 'polarity': None, 'simcond': None,
        'additional_flags': None
    })
    fields = Path(cond_file).stem.split('-')[1:]  # Drop the 'cond' prefix.

    for idx, key in enumerate(result.keys()):
        try:
            result[key] = fields[idx]
        except IndexError:
            pass

    # 'type' and 'additional_flags' will be part of the job name, but will not
    # be used in the formatting of the DIRAC LFN path.
    reco_type, additional_flags = result['type'], result['additional_flags']
    result = odict({k: v for k, v in result.items()
                    if v is not None and
                    k != 'type' and k != 'additional_flags'})

    return result, reco_type, additional_flags


def gen_lfn_path(lfn, fields, additional_fields,
                 replacement_rules={
                     'polarity': MC_POLARITY,
                     'decay': MC_DECAY_MODE
                 }):
    for key, rule in replacement_rules.items():
        try:
            fields[key] = rule[fields[key]]
        except Exception:
            pass

    try:
        lfn = lfn.format(**fields)
        lfn_jobname = lfn.replace(' ', '_').replace('/', '_')[1:]  # Remove the prefix '_'
        return lfn, lfn_jobname
    except KeyError:
        if bool(additional_fields):
            key, value = additional_fields.popitem(last=False)
            fields[key] = value
            return gen_lfn_path(lfn, fields, additional_fields)
        raise KeyError


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(description='''
ganga script to process R(D*) run 1 data/MC.''')

    parser.add_argument('reco_script',
                        help='''
specify DaVinci base reconstruction script.''')

    parser.add_argument('cond_file',
                        help='''
specify DaVinci reconstruction condition file.  ''')

    parser.add_argument('--force',
                        action='store_true',
                        help='''
if this flag is supplied, don't skip existing jobs with the same name.''')

    parser.add_argument('--davinci',
                        default='~/build/DaVinciDev_v45r3',
                        help='''
specify path to local DaVinci build.''')

    parser.add_argument('-p', '--polarity',
                        nargs='+',
                        choices=['mu', 'md'],
                        default='md',
                        help='''
specify polarity.''')

    parser.add_argument('-P', '--pythia',
                        nargs='+',
                        choices=MC_PYTHIA,
                        default='Pythia8',
                        help='''
specify Pythia version.''')

    parser.add_argument('-d', '--decay',
                        nargs='+',
                        choices=list(MC_DECAY_MODE.keys()),
                        default=list(MC_DECAY_MODE.keys())[0],
                        help='''
specify decay mode.''')

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

job_name = '--'.join([reco_sample, gen_date(), reco_type, lfn_jobname])
submitted_jobs = [j.name for j in jobs]

# Only create job if no existing job has the same name or force create
if args.force or job_name not in submitted_jobs:
    print('Preparing job {}'.format(job_name))
    j = Job(name=job_name)

    # Get input data from DIRAC
    data = BKQuery(lfn, dqflag=['OK']).getDataset()
    j.inputdata = data

    # Provide weight file
    j.inputfiles = [LocalFile(WEIGHT_FILE)]

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
    print('Job with name {} already exist, skipping...'.format(name))

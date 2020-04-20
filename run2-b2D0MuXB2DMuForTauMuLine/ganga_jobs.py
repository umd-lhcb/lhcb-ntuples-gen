#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Apr 20, 2020 at 08:28 PM +0800
#
# Description: A demonstration on ganga option file with parser.
#              This demo runs stand-alone, provided that Python is installed:
#                  python ./ganga_jobs_parser.py [options]
#
#              Alternatively, in lxplus:
#                  ganga ./ganga_job_parser.py [options]

from argparse import ArgumentParser
from itertools import product
from os.path import expanduser

##########################
# Parameters for data/MC #
##########################

PLATFORM = 'x86_64-centos7-gcc8-opt'
WEIGHT_FILE = './weights_soft.xml'

# Example for a fully constructed MC file path:
# '/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20Filtered/11873010/DSTTAUNU.SAFESTRIPTRIG'
MC_FILE = '/MC/2012/Beam4000GeV-2012-Mag{polarity}-Nu2.5-{simulation}/{condition}/Digi13/Trig0x409f0045/Reco14a/Stripping20Filtered/{decay}/DSTTAUNU.SAFESTRIPTRIG.DST'

MC_SIMULATION = ['Pythia8']

MC_BASE = {
    'Dst': './reco_Dst.py',
    'D0': './reco_D0.py',
}

MC_CONDITION = {
    'Sim09b': './conds/cond-mc-{}-sim09b.py',
}

MC_POLARITIES = {
    'Up': 'mag_up',
    'Down': 'mag_down'
}

# Decay mode IDs.
MC_DSTST_IDS = {
    'Bd2DststMuNu2D0': '11873010',
    'Bd2DststTauNu2D0': '11873030',
    'Bs2DststMuNu2D0': '13873000',
    'Bu2DststMuNu2D0': '12873010',
}

MC_DST_IDS = {
    'Bd2DstTauNu': '11574010',
    'Bd2DstMuNu': '11574020',
    'Bu2Dst0TauNu': '12573020',
    'Bu2Dst0MuNu': '12573030',
}

MC_D0_IDS = {
    'Bu2D0TauNu': '12573000',
    'Bu2D0MuNu': '12573010',
    'Bd2D0DX2MuX': '11873000',
    'Bu2D0DX2MuX': '12873000',
    'Bd2D0DsX2TauNu': '11873020',
    'Bu2D0DsX2TauNu': '12873020',
}

PARAMETERS = {
    'data-2016-Dst': {
        'dirac_path': '/LHCb/Collision16/Beam6500GeV-VeloClosed-Mag{}/Real Data/Reco16/Stripping28r1/90000000/SEMILEPTONIC.DST',
        'options': './conds/cond-data-2016-Dst.py',
        'files_per_job': 5
    },
    'cutflow_data-2016-Dst': {
        'dirac_path': '/LHCb/Collision16/Beam6500GeV-VeloClosed-Mag{}/Real Data/Reco16/Stripping28r1/90000000/SEMILEPTONIC.DST',
        'options': './conds/cond-cutflow_data-2016-Dst.py',
        'files_per_job': 5
    },
    'cutflow_mc-2016-Dst': {
        'dirac_path': '/MC/2016/Beam6500GeV-2016-Mag{}-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping26NoPrescalingFlagged/11874091/ALLSTREAMS.DST',
        'options': './conds/cond-cutflow_mc-mag_down-sim09b-Bd2D0XMuNu-D0_cocktail.py',
        'files_per_job': 8
    },
}

PREDEFINED_PARAMETER_KEYS = list(PARAMETERS.keys())


###########
# Helpers #
###########

# Combine all MC modes into a single dictionary.
MC_MODE_IDS = MC_DSTST_IDS
MC_MODE_IDS.update(MC_DST_IDS)
MC_MODE_IDS.update(MC_D0_IDS)

# Add reconstruction parameters for D*
# for id in MC_MODE_IDS.keys():
#     key = 'mc-{}'.format(id)
#     PARAMETERS[key] = {
#         'files_per_job': 1,
#         'dirac_path': MC_FILE
#     }


def gen_job_name(base, mode, polarity, simulaiton, condition):
    if mode in PREDEFINED_PARAMETER_KEYS:
        # NOTE: Only keep the first two fields!
        # e.g. 'data-2016-Dst' -> 'data-2016'
        mode = '-'.join(mode.split('-')[0:2])
        return '-'.join([base, mode, polarity])

    else:
        return '-'.join([base, mode, polarity, simulaiton, condition])


def gen_decay(mode, reference=MC_MODE_IDS):
    try:
        return MC_MODE_IDS[mode.replace('mc-', '')]
    except KeyError:
        return ''


def gen_dirac_path(raw, polarity, simulation, condition, decay):
    try:
        return raw.format(polarity=polarity, simulation=simulation,
                          condition=condition, decay=decay)
    except IndexError:
        return raw.format(polarity)


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(description='''
ganga script to process R(D*) run 1 data/MC.''')

    parser.add_argument('mode',
                        nargs='+',
                        choices=['all']+list(PARAMETERS.keys()),
                        help='''
specify data type.''')

    parser.add_argument('--force',
                        action='store_true',
                        help='''
if this flag is supplied, don't skip existing jobs with the same name.''')

    parser.add_argument('--davinci',
                        default='~/build/DaVinciDev_v45r3',
                        help='''
specify path to local DaVinci build.''')

    parser.add_argument('-b', '--base',
                        nargs='+',
                        choices=['all']+list(MC_BASE.keys()),
                        default=['Dst'],
                        help='''
specify base decay mode (e.g. D* or D0).''')

    parser.add_argument('-s', '--simulation',
                        nargs='+',
                        choices=['all']+MC_SIMULATION,
                        default=['Pythia6'],
                        help='''
specify simulation (typically Pythia) software package version.''')

    parser.add_argument('-c', '--condition',
                        nargs='+',
                        choices=['all']+list(MC_CONDITION.keys()),
                        default=['Sim08a'],
                        help='''
specify simulation condition.''')

    parser.add_argument('-p', '--polarity',
                        nargs='+',
                        choices=['all']+list(MC_POLARITIES.keys()),
                        default=['Down'],
                        help='''
specify polarity.''')

    return parser.parse_args()


#################
# Configurators #
#################

def conf_job_app(davinci_path, options):
    app = GaudiExec()
    app.directory = expanduser(davinci_path)
    app.options = options
    app.platform = PLATFORM
    return app


########
# Main #
########

args = parse_input()

if args.base == ['all']:
    args.base = list(MC_BASE.keys())
if args.mode == ['all']:
    args.mode = list(PARAMETERS.keys())
if args.polarity == ['all']:
    args.polarity = list(MC_POLARITIES.keys())
if args.simulation == ['all']:
    args.simulation = MC_SIMULATION
if args.condition == ['all']:
    args.condition = list(MC_CONDITION.keys())

for base, mode, polarity, simulaiton, condition in \
        product(
            args.base, args.mode, args.polarity, args.simulation,
            args.condition):
    # College all known job names
    job_names = [j.name for j in jobs]

    # Generate job name
    name = gen_job_name(base, mode, polarity, simulaiton, condition)

    # Only create job if no existing job has the same name or force create
    if args.force or (name not in job_names):
        print('Preparing job {}...'.format(name))
        j = Job(name=name)

        # Get input data
        decay = gen_decay(mode)
        dirac_path = gen_dirac_path(PARAMETERS[mode]['dirac_path'],
                                    polarity, simulaiton, condition, decay)
        data = BKQuery(dirac_path, dqflag=['OK']).getDataset()
        j.inputdata = data

        # Provide weight file
        j.inputfiles = [LocalFile(WEIGHT_FILE)]

        # Use DIRAC backend
        j.backend = Dirac()
        j.splitter = SplitByFiles(filesPerJob=PARAMETERS[mode]['files_per_job'])
        j.outputfiles = [LocalFile('*.root')]

        # Get path to option files, also prepare DaVinci
        base_option_file = MC_BASE[base]
        try:
            options_file = PARAMETERS[mode]['options']
        except KeyError:
            options_file = MC_CONDITION[condition].format(MC_POLARITIES[polarity])
        options = [options_file, base_option_file]
        app = conf_job_app(args.davinci, options)
        j.application = app

        # Submit!
        j.submit()

    else:
        print('Job with name {} already exist, skipping...'.format(name))

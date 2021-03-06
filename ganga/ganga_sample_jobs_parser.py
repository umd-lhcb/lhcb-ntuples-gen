#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Apr 21, 2021 at 03:00 AM +0200
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
from re import search


##########################
# Parameters for data/MC #
##########################

# Example for a fully constructed MC file path:
# '/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20Filtered/11873010/DSTTAUNU.SAFESTRIPTRIG'
LFN_PATH = {
    # run 1 data
    'std-2011': '/LHCb/Collision11/Beam3500GeV-VeloClosed-Mag{polarity}/Real Data/Reco14/Stripping21r1/90000000/SEMILEPTONIC.DST',
    'std-2012': '/LHCb/Collision12/Beam4000GeV-VeloClosed-Mag{polarity}/Real Data/Reco14/Stripping21/90000000/SEMILEPTONIC.DST',
    # run 1 MC
    'mc-2012-sim08': '/MC/2012/Beam4000GeV-2012-Mag{polarity}-Nu2.5-{pythia}/{simcond}/Digi13/Trig0x409f0045/Reco14a/Stripping20Filtered/{decay}/DSTTAUNU.SAFESTRIPTRIG.DST',
    'mc-2012-sim09': '/MC/2012/Beam4000GeV-2012-Mag{polarity}-NoRICHesSim-Nu2.5-{pythia}/{simcond}/Trig0x409f0045-NoRichPIDLines/Reco14c/Stripping21Filtered/{decay}/DSTTAUNU.SAFESTRIPTRIG.DST',
    # run 1 cocktail
    'cutflow_mc-2011-sim08': '/MC/2011/Beam3500GeV-2011-Mag{polarity}-Nu2-Pythia8/{simcond}/Digi13/Trig0x40760037/Reco14c/Stripping20r1NoPrescalingFlagged/11874091/ALLSTREAMS.DST',
    # run 2 data
    'std-2015': '/LHCb/Collision15/Beam6500GeV-VeloClosed-Mag{polarity}/Real Data/Reco15a/Stripping24r2/90000000/SEMILEPTONIC.DST',
    'std-2016': '/LHCb/Collision16/Beam6500GeV-VeloClosed-Mag{polarity}/Real Data/Reco16/Stripping28r1/90000000/SEMILEPTONIC.DST',
    # run 2 MC
    'mc-2016-sim09': '/MC/2016/Beam6500GeV-2016-Mag{polarity}-Nu1.6-25ns-Pythia8/{simcond}/Trig0x6139160F/Reco16/Turbo03a/Filtered/{decay}/D0TAUNU.SAFESTRIPTRIG.DST',
    'mc-2016-sim09-tracker_only': '/MC/2016/Beam6500GeV-2016-Mag{polarity}-TrackerOnly-Nu1.6-25ns-Pythia8/{simcond}/Reco16/Filtered/{decay}/D0TAUNU.SAFESTRIPTRIG.DST',
    # run 2 cocktail
    'cutflow_mc-2016-sim09': '/MC/2016/Beam6500GeV-2016-Mag{polarity}-Nu1.6-25ns-Pythia8/{simcond}/Trig0x6138160F/Reco16/Turbo03/Stripping26NoPrescalingFlagged/11874091/ALLSTREAMS.DST',
}
LFN_PATH['cutflow_data-2012'] = LFN_PATH['std-2012']
LFN_PATH['cutflow_data-2016'] = LFN_PATH['std-2016']

MC_PYTHIA = ['Pythia6', 'Pythia8']
MC_POLARITY = {'mu': 'Up', 'md': 'Down'}
KEY_ADD_FIELDS = [
    'tracker_only'
]


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
    terminating_non_flag_fields = r'^(mu|md|sim\d+[a-z])$'

    if len(fields) >= 3:
        if not bool(search(terminating_non_flag_fields, fields[-1])):
            result['additional_flags'] = fields[-1]
            fields.pop(-1)

    for idx, key in enumerate(result.keys()):
        try:
            result[key] = fields[idx]
        except IndexError:
            pass

    # 'type' and 'additional_flags' will be part of the job name, but will not
    # be used in the formatting of the DIRAC LFN path.
    reco_type, additional_flags = result['type'], result['additional_flags']
    result = odict({k: v for k, v in result.items()
                    if v is not None and k != 'type'})

    return result, reco_type, additional_flags


def gen_lfn_key(reco_type, fields):
    key = reco_type + '-' + fields['year']
    if 'simcond' in fields:
        key += '-' + fields['simcond'][:-1]
    if 'additional_flags' in fields and \
            fields['additional_flags'] in KEY_ADD_FIELDS:
        key += '-' + fields['additional_flags']
    return key


def gen_lfn_path(lfn, fields, additional_fields,
                 replacement_rules={
                     'polarity': MC_POLARITY,
                     'simcond': lambda x: x[0].upper()+x[1:]
                 }):
    for key, rule in replacement_rules.items():
        try:
            fields[key] = rule[fields[key]]
        except TypeError:
            fields[key] = rule(fields[key])
        except KeyError:
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
general ganga job submitter.''')

    parser.add_argument('reco_script',
                        help='''
specify DaVinci base reconstruction script.''')

    parser.add_argument('cond_file',
                        help='''
specify DaVinci reconstruction condition file.  ''')

    parser.add_argument('--davinci',
                        default='~/build/DaVinciDev_v45r6',
                        help='''
specify path to local DaVinci build.''')

    parser.add_argument('-p', '--polarity',
                        choices=['mu', 'md'],
                        default='md',
                        help='''
specify polarity.''')

    parser.add_argument('-P', '--pythia',
                        choices=MC_PYTHIA,
                        default='Pythia8',
                        help='''
specify Pythia version.''')

    parser.add_argument('-d', '--decay',
                        default='00000000',  # This mode doesn't exist!
                        help='''
specify decay mode.''')

    return parser.parse_args()


########
# Main #
########

args = parse_input()

print('Reconstruction script: {}'.format(args.reco_script))
print('Condition file: {}'.format(args.cond_file))

fields, reco_type, additional_flags = parse_cond_file_name(args.cond_file)
reco_sample = parse_reco_script_name(args.reco_script)
#print('Fields from cond file: {}'.format(fields))

# Try to add missing fields required to reconstruct LFNs
lfn_key = gen_lfn_key(reco_type, fields)
lfn, lfn_jobname = gen_lfn_path(
    LFN_PATH[lfn_key], fields,
    odict({'polarity': args.polarity,
           'pythia': args.pythia,
           'decay': args.decay})
)
print('LFN: {}'.format(lfn))

job_name_fields = [reco_sample, gen_date(), reco_type, lfn_jobname]

if additional_flags:
    job_name_fields.insert(3, additional_flags)
ntuple_name = '--'.join(job_name_fields) + '.root'
print('NTuple name: {}'.format(ntuple_name))

if args.decay != '00000000':
    job_name_fields.insert(3, args.decay)
job_name = '--'.join(job_name_fields)[:80]
print('Truncated job name: {}'.format(job_name))

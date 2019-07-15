# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Jul 15, 2019 at 01:12 PM -0400

from argparse import ArgumentParser
from os.path import expanduser


##########################
# Parameters for data/MC #
##########################

PLATFORM = 'x86_64-centos7-gcc62-opt'
BASE_OPTION_FILE = './reco_Dst.py'
WEIGHT_FILE = './weights_soft.xml'
MC_FILE = "/DSTTAUNU.SAFESTRIPTRIG.DST"

MC_CONDS = {
    "py6": "/MC/2012/Beam4000GeV-2012-Mag{}-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20Filtered/",
    "py8": "/MC/2012/Beam4000GeV-2012-Mag{}-Nu2.5-Pythia8/Sim08a/Digi13/Trig0x409f0045/Reco14a/Strip ping20Filtered/"
}

MC_DSTST_IDS = {
    'Bd2Dststmunu2D0': '11873010',
    'Bd2Dststtaunu2D0': '11873030',
    'Bs2Dststmunu2D0': '13873000',
    'Bu2Dststmunu2D0': '12873010',
}

MC_DST_IDS = {
    'Bd2Dsttaunu': '11574010',
    'Bd2Dstmunu': '11574020',
    'Bu2Dst0taunu': '12573020',
    'Bu2Dst0munu': '12573030',
}

MC_D0_IDS = {
    'Bu2D0taunu': '12573000',
    'Bu2D0munu': '12573010',
    'Bd2D0DX2muX': '11873000',
    'Bu2D0DX2muX': '12873000',
    'Bd2D0DsX2taunu': '11873020',
    'Bu2D0DsX2taunu': '12873020',
}

PARAMETERS = {
    'data-2012': {
        'dirac_path': '/LHCb/Collision12/Beam4000GeV-VeloClosed-Mag{}/Real Data/Reco14/Stripping21/90000000/SEMILEPTONIC.DST',
        'options': ['./conds/reco_Dst_conf-data.py'],
        'files_per_job': 4
    },
}

# Add reconstruction parameters for D*
for cond in MC_CONDS.keys():
    for id in MC_DST_IDS.keys():
        key = 'mc-{}-sim08a-{}'.format(cond, id)
        PARAMETERS[key] = {
            'dirac_path': MC_CONDS[cond] + MC_DST_IDS[id] + MC_FILE,
            'options': ['./conds/reco_Dst_conf-mc-{}-sim08a.py'.format(cond)],
            'files_per_job': 1
        }


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(description='''
ganga script to process R(D*) run 1 data/MC.''')

    parser.add_argument('type',
                        choices=['all']+list(PARAMETERS.keys()),
                        help='''
specify data type.''')

    parser.add_argument('--davinci',
                        default='~/build/DaVinciDev_v42r8p1',
                        help='''
specify path to local DaVinci build.''')

    parser.add_argument('-p', '--polarity',
                        nargs='?',
                        choices=['Up', 'Down'],
                        default='Down',
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

if args.type == 'all':
    modes = list(PARAMETERS.keys())
else:
    modes = [args.type]

for m in modes:
    j = Job(name=m)

    options = PARAMETERS[m]['options'] + [BASE_OPTION_FILE]
    app = conf_job_app(args.davinci, options)
    j.application = app

    dirac_path = PARAMETERS[m]['dirac_path'].format(args.polarity)
    data = BKQuery(dirac_path, dqflag=['OK']).getDataset()
    # j.inputdata = data
    j.inputdata = data[0]  # Running on 1 file only.

    # Provide weight file
    j.inputfiles = [LocalFile(WEIGHT_FILE)]

    j.backend = Dirac()
    j.splitter = SplitByFiles(filesPerJob=PARAMETERS[m]['files_per_job'])
    j.outputfiles = [LocalFile('*.root')]

    j.submit()

from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'
# DaVinci().HistogramFile = 'mc-histo.root'

# Additional global flags
DaVinci().MoniSequence += ['TRACKER_ONLY']


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20170721-2-vc-md100"
LHCbApp().DDDBtag = "dddb-20170721-3"


from GaudiConf import IOHelper

# FullSim
# IOHelper().inputFiles([
#     './data/Bd2DstMuNu-2016-md-py8-sim09j-fullsim/00121222_00000002_1.d0taunu.safestriptrig.dst',
#     './data/Bd2DstMuNu-2016-md-py8-sim09j-fullsim/00121222_00000030_1.d0taunu.safestriptrig.dst',
#     './data/Bd2DstMuNu-2016-md-py8-sim09j-fullsim/00121222_00000082_1.d0taunu.safestriptrig.dst'
# ], clear=True)

# Tracker only
IOHelper().inputFiles([
    './data/Bd2DstMuNu-2016-md-py8-sim09j-tracker_only/00120310_00000088_1.d0taunu.safestriptrig.dst',
    './data/Bd2DstMuNu-2016-md-py8-sim09j-tracker_only/00120310_00000093_1.d0taunu.safestriptrig.dst',
    './data/Bd2DstMuNu-2016-md-py8-sim09j-tracker_only/00120310_00000124_1.d0taunu.safestriptrig.dst'
], clear=True)

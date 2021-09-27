from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'
# DaVinci().HistogramFile = 'mc-histo.root'


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20170721-2-vc-md100"
LHCbApp().DDDBtag = "dddb-20170721-3"


from GaudiConf import IOHelper

# FullSim

# Normalization
IOHelper().inputFiles([
    './data/Bd2DstMuNu-2016-md-py8-sim09j-fullsim/00121222_00000002_1.d0taunu.safestriptrig.dst',
    './data/Bd2DstMuNu-2016-md-py8-sim09j-fullsim/00121222_00000030_1.d0taunu.safestriptrig.dst',
    './data/Bd2DstMuNu-2016-md-py8-sim09j-fullsim/00121222_00000082_1.d0taunu.safestriptrig.dst'
], clear=True)

# Signal
# IOHelper().inputFiles([
#     './data/Bd2DstTauNu-2016-md-py8-sim09j-fullsim/00121210_00000016_1.d0taunu.safestriptrig.dst'
# ], clear=True)

# D**
# IOHelper().inputFiles([
#     './data/Bd2DststTauNu-2016-md-py8-sim09j-fullsim/00121651_00000001_1.d0taunu.safestriptrig.dst'
# ], clear=True)

# DD
# IOHelper().inputFiles([
#     './data/Bd2D0DX_MuNu-2016-md-py8-sim09j-fullsim/00121213_00000026_1.d0taunu.safestriptrig.dst',
#     './data/Bd2D0DX_MuNu-2016-md-py8-sim09j-fullsim/00121213_00000028_1.d0taunu.safestriptrig.dst',
#     './data/Bd2D0DX_MuNu-2016-md-py8-sim09j-fullsim/00121213_00000040_1.d0taunu.safestriptrig.dst'
# ], clear=True)

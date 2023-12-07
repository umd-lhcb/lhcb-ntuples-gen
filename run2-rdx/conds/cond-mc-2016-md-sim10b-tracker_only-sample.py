from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'
# DaVinci().HistogramFile = 'mc-histo.root'

# Additional global flags
DaVinci().MoniSequence += ['TRACKER_ONLY']

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-6-vc-md100-Sim10"
LHCbApp().DDDBtag = "dddb-20220927-2016"


from GaudiConf import IOHelper

# Missing DDX modes
IOHelper().inputFiles([
    './data/Bd2D0DX_MuNu-2016-md-py8-sim10b-tracker_only/00202746_00000063_1.d0taunu.safestriptrig.dst',
], clear=True)
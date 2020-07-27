from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'cutflow_mc-dv_strip.root'

# Additional global flags
DaVinci().MoniSequence += ['CUTFLOW', 'DV_STRIP', 'NO_SMEAR']


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20161124-2-vc-md100"
LHCbApp().DDDBtag = "dddb-20150724"


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/Bd2D0XMuNu_D0_cocktail-2016-md-py8-sim09b/00056169_00000005_3.AllStreams.dst',
    './data/Bd2D0XMuNu_D0_cocktail-2016-md-py8-sim09b/00056169_00000013_3.AllStreams.dst',
], clear=True)

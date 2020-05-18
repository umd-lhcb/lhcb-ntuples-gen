from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'Dst-mc.root'

# Additional global flags
DaVinci().MoniSequence += ['CUTFLOW', 'BARE']


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20161124-2-vc-md100"
LHCbApp().DDDBtag = "dddb-20150724"


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/mc-mag_down-py8-sim09b-Bd2D0XMuNu-D0_cocktail/00056169_00000005_3.AllStreams.dst',
    './data/mc-mag_down-py8-sim09b-Bd2D0XMuNu-D0_cocktail/00056169_00000013_3.AllStreams.dst',
], clear=True)

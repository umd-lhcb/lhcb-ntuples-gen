from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'BCands-mc.root'


from Configurables import CondDB

CondDB().useLatestTags("2016")


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20161124-2-vc-md100"
LHCbApp().DDDBtag = "dddb-20150724"


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/mc-mag_down-py8-sim09b-Bd2D0XMuMu-D0_cocktail/00056169_00000005_3.AllStreams.dst',
    './data/mc-mag_down-py8-sim09b-Bd2D0XMuMu-D0_cocktail/00056169_00000013_3.AllStreams.dst',
], clear=True)

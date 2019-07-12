from Configurables import DaVinci

DaVinci().DataType = '2012'
DaVinci().Simulation = True

DaVinci().TupleFile = './gen/BCands_Dst-mc.root'
DaVinci().HistogramFile = './gen/BCands_Dst_histo-mc.root'


from Configurables import CondDB

CondDB().useLatestTags("2012")


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20130503-1-vc-md100"
LHCbApp().DDDBtag = "dddb-20130503-1"


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/mc-py6-sim08a-mag_down/00028778_00000009_1.dsttaunu.safestriptrig.dst',
    './data/mc-py6-sim08a-mag_down/00028778_00000010_1.dsttaunu.safestriptrig.dst',
], clear=True)

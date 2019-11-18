from Configurables import DaVinci

DaVinci().DataType = '2012'
DaVinci().Simulation = True

DaVinci().TupleFile = 'BCands-mc.root'
# DaVinci().HistogramFile = 'BCands_histo-mc.root'


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20130503-1-vc-md100"
LHCbApp().DDDBtag = "dddb-20130503-1"


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/mc-mag_down-py6-sim08a/00028778_00000009_1.dsttaunu.safestriptrig.dst',
    './data/mc-mag_down-py6-sim08a/00028778_00000010_1.dsttaunu.safestriptrig.dst',
], clear=True)

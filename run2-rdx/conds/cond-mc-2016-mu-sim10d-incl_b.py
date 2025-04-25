from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'
# DaVinci().HistogramFile = 'mc-histo.root'

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-6-vc-mu100-Sim10"
LHCbApp().DDDBtag = "dddb-20220927-2016"

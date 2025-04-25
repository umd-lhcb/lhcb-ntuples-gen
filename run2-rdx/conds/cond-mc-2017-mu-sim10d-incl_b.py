from Configurables import DaVinci

DaVinci().DataType = '2017'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'
# DaVinci().HistogramFile = 'mc-histo.root'

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-7-vc-mu100-Sim10"
LHCbApp().DDDBtag = "dddb-20220927-2017"

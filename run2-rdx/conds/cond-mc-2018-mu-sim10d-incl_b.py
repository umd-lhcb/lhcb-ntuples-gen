from Configurables import DaVinci

DaVinci().DataType = '2018'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'
# DaVinci().HistogramFile = 'mc-histo.root'

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-8-vc-mu100-Sim10"
LHCbApp().DDDBtag = "dddb-20210528-8"

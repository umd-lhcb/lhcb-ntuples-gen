from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'
# DaVinci().HistogramFile = 'mc-histo.root'

# Additional global flags
DaVinci().MoniSequence += ['PIPIPI0']

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-6-vc-md100-Sim10"
LHCbApp().DDDBtag = "dddb-20210528-6"

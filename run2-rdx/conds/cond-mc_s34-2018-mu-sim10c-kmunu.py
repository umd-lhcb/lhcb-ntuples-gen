from Configurables import DaVinci

DaVinci().DataType = '2018'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'
# DaVinci().HistogramFile = 'mc-histo.root'

# Additional global flags
DaVinci().MoniSequence += ['KMUNU']

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-8-vc-md100-Sim10"
LHCbApp().DDDBtag = "dddb-20220927-2018"

from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'
# DaVinci().HistogramFile = 'mc-histo.root'

# Additional global flags
DaVinci().MoniSequence += ['PIMUNU']

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20170721-2-vc-md100"
LHCbApp().DDDBtag = "dddb-20170721-3"

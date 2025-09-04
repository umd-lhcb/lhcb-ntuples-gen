from Configurables import DaVinci

DaVinci().DataType = '2017'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'
# DaVinci().HistogramFile = 'mc-histo.root'

# Additional global flags
DaVinci().MoniSequence += ['PIMUNU']

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20190430-1-vc-mu100"
LHCbApp().DDDBtag = "dddb-20170721-3"

from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'

# Additional global flags
DaVinci().MoniSequence += ['KMUNU']

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20170721-2-vc-mu100"
LHCbApp().DDDBtag = "dddb-20170721-3"

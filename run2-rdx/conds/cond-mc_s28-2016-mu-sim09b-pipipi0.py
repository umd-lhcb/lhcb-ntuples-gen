from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'

# Additional global flags
DaVinci().MoniSequence += ['PIPIPI0']

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20161124-2-vc-mu100"
LHCbApp().DDDBtag = "dddb-20150724"

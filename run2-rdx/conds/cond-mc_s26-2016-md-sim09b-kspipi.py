from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'

# Additional global flags
DaVinci().MoniSequence += ['KSPIPI']

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20161124-2-vc-md100"
LHCbApp().DDDBtag = "dddb-20150724"

from Configurables import DaVinci

DaVinci().DataType = '2018'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20190430-vc-md100"
LHCbApp().DDDBtag = "dddb-20170721-3"
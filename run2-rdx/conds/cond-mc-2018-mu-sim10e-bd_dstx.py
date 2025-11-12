from Configurables import DaVinci

DaVinci().DataType = '2018'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-8-vc-mu100-Sim10"
LHCbApp().DDDBtag = "2018-v03.06"

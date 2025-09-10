from Configurables import DaVinci

DaVinci().DataType = '2017'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-7-vc-md100-Sim10"
LHCbApp().DDDBtag = "2017-v03.06"

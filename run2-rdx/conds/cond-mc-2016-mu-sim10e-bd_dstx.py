from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'

from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-6-vc-mu100-Sim10"
LHCbApp().DDDBtag = "2016-v03.06"

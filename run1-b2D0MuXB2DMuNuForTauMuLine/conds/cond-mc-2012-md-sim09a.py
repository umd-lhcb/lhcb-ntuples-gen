from Configurables import DaVinci

DaVinci().DataType = '2012'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20160321-2-vc-md100"
LHCbApp().DDDBtag = "dddb-20150928"

from Configurables import DaVinci

DaVinci().DataType = '2012'
DaVinci().Simulation = True

DaVinci().TupleFile = 'BCands-mc.root'


from Configurables import CondDB

CondDB().useLatestTags("2012")


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20160321-2-vc-mu100"
LHCbApp().DDDBtag = "dddb-20150928"

from Configurables import DaVinci

DaVinci().Simulation = True


from Configurables import CondDB

CondDB().useLatestTags("2012")


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20130503-1-vc-md100"
LHCbApp().DDDBtag = "dddb-20130503-1"

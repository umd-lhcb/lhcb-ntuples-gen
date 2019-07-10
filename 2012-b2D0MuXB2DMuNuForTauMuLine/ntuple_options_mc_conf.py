from Configurables import DaVinci

DaVinci().Simulation = True


from Configurables import CondDB

CondDB().useLatestTags("2012")

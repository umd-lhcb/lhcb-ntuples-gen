from Configurables import DaVinci

DaVinci().DataType = '2018'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-6-vc-md100-Sim10"
LHCbApp().DDDBtag = "dddb-20210528-8" # b-inclusive MB
# LHCbApp().DDDBtag = "dddb-20220927-2018" # MB

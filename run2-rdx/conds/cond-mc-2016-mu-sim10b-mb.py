from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-6-vc-mu100-Sim10"
LHCbApp().DDDBtag = "dddb-20210528-6" # b-inclusive MB
# LHCbApp().DDDBtag = "dddb-20220927-2016" # MB

from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20170721-2-vc-md100"
LHCbApp().DDDBtag = "dddb-20170721-3"


from GaudiConf import IOHelper
from glob import glob

IOHelper().inputFiles(glob('./data/Bu2JpsiK-2016-md-py8-sim09k-fullsim/*.dst'),
                      clear=True)

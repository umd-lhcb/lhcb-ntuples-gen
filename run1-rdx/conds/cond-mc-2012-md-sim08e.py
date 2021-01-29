from Configurables import DaVinci

DaVinci().DataType = '2012'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20130522-1-vc-md100"
LHCbApp().DDDBtag = "dddb-20130929-1"

from GaudiConf import IOHelper

IOHelper().inputFiles([
  './data/Bd2DstMuNu-2012-md-py8-sim08e/00037931_00000001_1.dsttaunu.safestriptrig.dst',
  './data/Bd2DstMuNu-2012-md-py8-sim08e/00037931_00000005_1.dsttaunu.safestriptrig.dst',
], clear=True)

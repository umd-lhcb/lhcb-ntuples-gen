from Configurables import DaVinci

DaVinci().DataType = '2012'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20160321-2-vc-md100"
LHCbApp().DDDBtag = "dddb-20150928"

from GaudiConf import IOHelper

IOHelper().inputFiles([
        './data/Bd2DstMuNu-2012-md-py8-sim09a/00054936_00000051_1.dsttaunu.safestriptrig.dst',
        './data/Bd2DstMuNu-2012-md-py8-sim09a/00054936_00000076_1.dsttaunu.safestriptrig.dst',
], clear=True)

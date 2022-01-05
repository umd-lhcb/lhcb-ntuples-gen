from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = False

DaVinci().TupleFile = 'std.root'
# DaVinci().HistogramFile = 'std-histo.root'


from GaudiConf import IOHelper

# Stripping v28r2
IOHelper().inputFiles([
    './data/data-2016-md/00102837_00000471_1.dimuon.dst',
    './data/data-2016-md/00102837_00000479_1.dimuon.dst',
], clear=True)

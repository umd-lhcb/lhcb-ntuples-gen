from Configurables import DaVinci

DaVinci().DataType = '2015'
DaVinci().Simulation = False

DaVinci().TupleFile = 'std.root'
# DaVinci().HistogramFile = 'std-histo.root'


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/data-2015-md/00102354_00000040_1.semileptonic.dst',
    './data/data-2015-md/00102354_00000905_1.semileptonic.dst',
], clear=True)

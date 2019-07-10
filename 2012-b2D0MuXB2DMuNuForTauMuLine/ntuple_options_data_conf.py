from Configurables import DaVinci

DaVinci().DataType = '2012'
DaVinci().Simulation = False

DaVinci().TupleFile = './gen/YCands-data.root'
DaVinci().HistogramFile = './gen/YCands_histo-data.root'


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/data-mag_down/00041836_00006100_1.semileptonic.dst',  # 95 MB
    './data/data-mag_down/00041836_00011435_1.semileptonic.dst',  # 1.3 GB
    './data/data-mag_down/00041836_00013110_1.semileptonic.dst',  # 2.9 GB
], clear=True)

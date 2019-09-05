from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = False

DaVinci().TupleFile = 'BCands_Dst-data.root'
# DaVinci().HistogramFile = 'BCands_Dst_histo-data.root'


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/data-2016-mag_down/00069609_00007479_1.semileptonic.dst',  # 468 MB
    './data/data-2016-mag_down/00070273_00008958_1.semileptonic.dst',  # 202 MB
    './data/data-2016-mag_down/00069581_00004329_1.semileptonic.dst',  # 3.5 GB
], clear=True)

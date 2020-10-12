from Configurables import DaVinci

DaVinci().DataType = '2011'
DaVinci().Simulation = False

DaVinci().TupleFile = 'std.root'
# DaVinci().HistogramFile = 'std-histo.root'

# Specify tags
# DaVinci().DDDBtag = 'dddb-20130929-1'
# DaVinci().CondDBtag = 'cond-20141007'


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/data-2011-md/00041840_00046559_1.semileptonic.dst',  # 21 MB
], clear=True)

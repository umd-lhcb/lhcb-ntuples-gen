from Configurables import DaVinci

DaVinci().DataType = '2018'
DaVinci().Simulation = False

DaVinci().TupleFile = 'mu_misid.root'
# DaVinci().HistogramFile = 'std-histo.root'

# Additional global flags
DaVinci().MoniSequence += ['MU_MISID']


# from GaudiConf import IOHelper

# IOHelper().inputFiles([
#     './data/data-2016-md/00102837_00003269_1.semileptonic.dst',
#     './data/data-2016-md/00102837_00003459_1.semileptonic.dst',
#     './data/data-2016-md/00103398_00017120_1.semileptonic.dst',
# ], clear=True)

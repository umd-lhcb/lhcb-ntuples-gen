from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = False

DaVinci().TupleFile = 'non_mu_misid.root'
# DaVinci().HistogramFile = 'std-histo.root'

# Additional global flags
DaVinci().MoniSequence += ['NON_MU_MISID']


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/data-2016-md/00069529_00017556_1.semileptonic.dst',  # 1.2 GB
    './data/data-2016-md/00069527_00003141_1.semileptonic.dst',  # 3.5 GB
], clear=True)

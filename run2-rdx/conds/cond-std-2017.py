from Configurables import DaVinci

DaVinci().DataType = '2017'
DaVinci().Simulation = False

DaVinci().TupleFile = 'std.root'
# DaVinci().HistogramFile = 'std-histo.root'


# Optionally force latest, instead of default, tags for real data
# from Configurables import CondDB
# CondDB(Tags={
#     'LHCBCOND': '<latest:2016>',
#     'DDDB':     '<latest:2016>',
#     'DQFLAGS':  '<latest:2016>'
# })


# from GaudiConf import IOHelper --- NOTE: THIS WAS FOR 2016!

# # Stripping v28r1
# # IOHelper().inputFiles([
# #     './data/data-2016-md/00069529_00017556_1.semileptonic.dst',  # 1.2 GB
# #     './data/data-2016-md/00069527_00003141_1.semileptonic.dst',  # 3.5 GB
# # ], clear=True)

# # Stripping v28r2
# IOHelper().inputFiles([
#     './data/data-2016-md/00102837_00003269_1.semileptonic.dst',
#     './data/data-2016-md/00102837_00003459_1.semileptonic.dst',
#     './data/data-2016-md/00103398_00017120_1.semileptonic.dst',
# ], clear=True)

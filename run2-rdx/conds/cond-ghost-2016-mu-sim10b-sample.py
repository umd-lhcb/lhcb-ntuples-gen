from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'ghost.root'
# DaVinci().HistogramFile = 'mc-histo.root'

# Additional global flags
DaVinci().MoniSequence += ['GHOST']


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-6-vc-mu100-Sim10"
LHCbApp().DDDBtag = "dddb-20220927-2016"

from GaudiConf import IOHelper

# FullSim

# D* Inclusive (all mu cuts applied in Filtering)
IOHelper().inputFiles([
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_001.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_002.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_003.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_004.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_005.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_006.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_007.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_008.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_009.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_010.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_011.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_012.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_013.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_014.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_015.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_016.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_017.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_018.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_019.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_020.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_021.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_022.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_023.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_024.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_025.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_026.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_027.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_028.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_029.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_030.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_031.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_032.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_033.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_034.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_035.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_036.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_037.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_038.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_039.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_040.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_041.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_042.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_043.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_044.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_045.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_046.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_047.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_048.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_049.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_050.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_051.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_052.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_053.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_054.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_055.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_056.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_057.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_058.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_059.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_060.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_061.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_062.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_063.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_064.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_065.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_066.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_067.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_068.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_069.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_070.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_071.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_072.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_073.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_074.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_075.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_076.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_077.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_078.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_079.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_080.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_081.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_082.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_083.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_084.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_085.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_086.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_087.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_088.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_089.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_090.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_091.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_092.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_093.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_094.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_095.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_096.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_097.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_098.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_099.dst',
    './samples/23_11_15-11774014-DstIncl-StudySample/Filtered.D0taunu.SafeStripTrig_100.dst'
], clear=True)

# D* Inclusive (mu cuts off in Filtering)
# IOHelper().inputFiles([
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_001.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_002.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_003.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_004.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_005.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_006.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_007.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_008.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_009.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_010.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_011.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_012.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_013.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_014.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_015.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_016.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_017.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_018.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_019.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_020.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_021.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_022.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_023.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_024.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_025.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_026.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_027.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_028.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_029.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_030.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_031.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_032.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_033.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_034.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_035.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_036.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_037.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_038.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_039.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_040.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_041.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_042.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_043.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_044.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_045.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_046.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_047.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_048.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_049.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_050.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_051.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_052.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_053.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_054.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_055.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_056.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_057.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_058.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_059.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_060.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_061.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_062.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_063.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_064.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_065.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_066.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_067.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_068.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_069.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_070.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_071.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_072.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_073.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_074.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_075.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_076.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_077.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_078.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_079.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_080.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_081.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_082.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_083.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_084.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_085.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_086.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_087.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_088.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_089.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_090.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_091.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_092.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_093.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_094.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_095.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_096.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_097.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_098.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_099.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoMuFilterCuts/Filtered.D0taunu.SafeStripTrig-stdMuons-2016-100ev_100.dst'
# ], clear=True)

# D* Inclusive (no Filtering)
# IOHelper().inputFiles([
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_001.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_002.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_003.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_004.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_005.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_006.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_007.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_008.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_009.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_010.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_011.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_012.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_013.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_014.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_015.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_016.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_017.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_018.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_019.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_020.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_021.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_022.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_023.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_024.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_025.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_026.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_027.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_028.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_029.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_030.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_031.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_032.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_033.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_034.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_035.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_036.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_037.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_038.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_039.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_040.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_041.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_042.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_043.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_044.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_045.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_046.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_047.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_048.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_049.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_050.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_051.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_052.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_053.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_054.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_055.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_056.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_057.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_058.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_059.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_060.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_061.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_062.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_063.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_064.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_065.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_066.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_067.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_068.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_069.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_070.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_071.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_072.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_073.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_074.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_075.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_076.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_077.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_078.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_079.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_080.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_081.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_082.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_083.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_084.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_085.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_086.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_087.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_088.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_089.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_090.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_091.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_092.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_093.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_094.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_095.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_096.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_097.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_098.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_099.dst',
#     './samples/24_01_17-11774014-DstIncl-StudySample--NoFilter/Brunel-2016-100ev_100.dst'
# ], clear=True)
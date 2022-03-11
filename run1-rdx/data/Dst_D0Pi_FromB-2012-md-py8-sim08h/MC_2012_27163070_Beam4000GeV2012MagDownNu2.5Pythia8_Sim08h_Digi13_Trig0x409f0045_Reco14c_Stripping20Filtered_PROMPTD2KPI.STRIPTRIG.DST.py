#-- GAUDI jobOptions generated on Fri Mar 11 08:45:55 2022
#-- Contains event types : 
#--   27163070 - 18 files - 257102 events - 64.31 GBytes

#--  Extra information about the data processing phases:

#--  Processing Pass: '/Sim08h/Digi13/Trig0x409f0045/Reco14c/Stripping20Filtered' 

#--  StepId : 127590 
#--  StepName : Merge14 for Stripping20 Charm Filtered Productions (Maguire)  
#--  ApplicationName : DaVinci 
#--  ApplicationVersion : v35r0 
#--  OptionFiles : $APPCONFIGOPTS/Merging/DVMergeDST.py;$APPCONFIGOPTS/DaVinci/DataType-2012.py;$APPCONFIGOPTS/Merging/WriteFSR.py;$APPCONFIGOPTS/Merging/MergeFSR.py 
#--  DDDB : fromPreviousStep 
#--  CONDDB : fromPreviousStep 
#--  ExtraPackages : AppConfig.v3r274 
#--  Visible : N 

from Gaudi.Configuration import * 
from GaudiConf import IOHelper
IOHelper('ROOT').inputFiles([
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000006_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000005_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000007_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000010_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000016_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000011_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000014_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000004_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000003_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000015_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000017_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000002_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000008_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000013_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000012_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000018_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000009_1.promptd2kpi.striptrig.dst',
'LFN:/lhcb/MC/2012/PROMPTD2KPI.STRIPTRIG.DST/00045827/0000/00045827_00000001_1.promptd2kpi.striptrig.dst',
], clear=True)

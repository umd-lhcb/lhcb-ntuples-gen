#-- GAUDI jobOptions generated on Mon Oct 12 19:10:19 2020
#-- Contains event types : 
#--   11574010 - 10 files - 191065 events - 42.60 GBytes

#--  Extra information about the data processing phases:

#--  Processing Pass: '/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20Filtered' 

#--  StepId : 125477 
#--  StepName : Merge14 for Sim08 2012 SLWG Filtered Productions (Ciezarek)  
#--  ApplicationName : DaVinci 
#--  ApplicationVersion : v33r5 
#--  OptionFiles : $APPCONFIGOPTS/Merging/DVMergeDST.py;$APPCONFIGOPTS/DaVinci/DataType-2012.py;$APPCONFIGOPTS/Merging/WriteFSR.py;$APPCONFIGOPTS/Merging/MergeFSR.py 
#--  DDDB : fromPreviousStep 
#--  CONDDB : fromPreviousStep 
#--  ExtraPackages : AppConfig.v3r274 
#--  Visible : N 

from Gaudi.Configuration import * 
from GaudiConf import IOHelper
IOHelper('ROOT').inputFiles([
'LFN:/lhcb/MC/2012/DSTTAUNU.SAFESTRIPTRIG.DST/00028778/0000/00028778_00000001_1.dsttaunu.safestriptrig.dst',
'LFN:/lhcb/MC/2012/DSTTAUNU.SAFESTRIPTRIG.DST/00028778/0000/00028778_00000006_1.dsttaunu.safestriptrig.dst',
'LFN:/lhcb/MC/2012/DSTTAUNU.SAFESTRIPTRIG.DST/00028778/0000/00028778_00000008_1.dsttaunu.safestriptrig.dst',
'LFN:/lhcb/MC/2012/DSTTAUNU.SAFESTRIPTRIG.DST/00028778/0000/00028778_00000009_1.dsttaunu.safestriptrig.dst',
'LFN:/lhcb/MC/2012/DSTTAUNU.SAFESTRIPTRIG.DST/00028778/0000/00028778_00000007_1.dsttaunu.safestriptrig.dst',
'LFN:/lhcb/MC/2012/DSTTAUNU.SAFESTRIPTRIG.DST/00028778/0000/00028778_00000002_1.dsttaunu.safestriptrig.dst',
'LFN:/lhcb/MC/2012/DSTTAUNU.SAFESTRIPTRIG.DST/00028778/0000/00028778_00000010_1.dsttaunu.safestriptrig.dst',
'LFN:/lhcb/MC/2012/DSTTAUNU.SAFESTRIPTRIG.DST/00028778/0000/00028778_00000004_1.dsttaunu.safestriptrig.dst',
'LFN:/lhcb/MC/2012/DSTTAUNU.SAFESTRIPTRIG.DST/00028778/0000/00028778_00000005_1.dsttaunu.safestriptrig.dst',
'LFN:/lhcb/MC/2012/DSTTAUNU.SAFESTRIPTRIG.DST/00028778/0000/00028778_00000003_1.dsttaunu.safestriptrig.dst',
], clear=True)

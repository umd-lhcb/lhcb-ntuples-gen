from Configurables import DecayTreeTuple
from DecayTreeTuple.Configuration import *

isSim = False
year = 2017

# Stream and stripping line we want to use
stream = 'Dimuon'
line = 'Bs2MuMuLinesBu2JPsiKLine'
#line = 'Hb2Charged2BodyB2Charged2BodyLine'
#Create an ntuple to capture D*+ decays from the StrippingLine line
BuTuple = DecayTreeTuple('BuTuple')
#BuTuple = DecayTreeTuple('BuTuple', OutputLevel = 1)
#BuTuple.Decay = '[B+ -> ^K+ ^pi0 {gamma}{gamma}]CC'
#BuTuple.Decay = '[B+ -> ^[J/psi(1S) -> mu+ mu-] ^K+]CC'
BuTuple.Decay = '[B+ -> ^(J/psi(1S) -> ^mu+ ^mu-) ^K+]CC'
#BuTuple.Inputs = [ 'Phys/B2Kpi0Line/Particles' ]
if not isSim: BuTuple.Inputs = ['/Event/{0}/Phys/{1}/Particles'.format(stream,line)]#data
#if isSim: BuTuple.Inputs = ['/Event/Bu2Kpi.Strip/Phys/B2Kpi0Line/Particles']#filteredMC
#BuTuple.Inputs = ['Phys/{0}/Particles'.format(line)]
BuTuple.ToolList += [ ### DEFAULTS: Kinematic, Pid, Geometry, EventInfo
    'TupleToolAngles',
    'TupleToolPrimaries' ]
#TupleToolPrimaries.Verbose() = True

#BuTuple.addTool(TupleToolPrimaries, name = 'PV')
#PV = BuTuple.addTupleTool("TupleToolPrimaries")
#PV.Verbose = True
from Configurables import LoKi__Hybrid__EvtTupleTool, LoKi__Hybrid__DictOfFunctors, LoKi__Hybrid__TupleTool, LoKi__Hybrid__Dict2Tuple, TupleToolDecayTreeFitter
from Configurables import LoKi__Hybrid__DTFDict as DTFDict
LoKiEventTool = BuTuple.addTupleTool("LoKi::Hybrid::EvtTupleTool")
LoKiEventTool.Preambulo = [ 'from LoKiTracks.decorators import *']

LoKiEventTool.VOID_Variables = {
    'nBestTracks' : "CONTAINS('Rec/Track/Best')",
    'nLongTracks' : "TrSOURCE('/Event/Rec/Track/Best', TrLONG) >> TrSIZE",
    'nTracks'     : 'RECSUMMARY( LHCb.RecSummary.nTracks, -1 )',
    'nSPDHits'    : "CONTAINS('Raw/Spd/Digits')"}

#LoKiEventTool.VOID_Variables = {
#    'nBestTracks' : "CONTAINS('Rec/Track/Best')",
#    'nLongTracks' : "TrSOURCE('/Event/Rec/Track/Best', TrLONG) >> TrSIZE",
#    'nLongTracks' : "TrSOURCE('/Event/Bhadron/Rec/Track/Best', TrLONG) >> TrSIZE",
#    'nPVs'        : 'RECSUMMARY( LHCb.RecSummary.nPVs,    -1 )',
#    'nTracks'     : 'RECSUMMARY( LHCb.RecSummary.nTracks, -1 )',
#    'nSPDHits'    : 'RECSUMMARY( LHCb.RecSummary.nSPDhits,-1 )'
#}
BuTuple.addTool(TupleToolDecay, name = 'Bu')
TTTT = BuTuple.Bu.addTupleTool('TupleToolTISTOS')
import sys, os
helperPath = os.path.expandvars( '/afs/cern.ch/work/w/wparker/BKPi/' )
sys.path.append( helperPath )
TTTT.TriggerList  = [ 'L0ElectronDecision',
                      'L0HadronDecision',
                      'L0PhotonDecision' ]
TTTT.TriggerList += [ 'Hlt1TrackMVADecision',
                      'Hlt1TwoTrackMVADecision' ]
#2016
#TTTT.TriggerList += [ 'Hlt2B2Kpi0_B2Kpi0Decision',
#                      'Hlt2B2Kpi0_B2K0pi0Decision']
#2015
TTTT.TriggerList += [ 'Hlt2B2Kpi0Decision',
                      'Hlt2B2K0pi0Decision']

#from triggers import triggerList
#TTTT.TriggerList = triggerList
TTTT.Verbose = True
BuLOKI = BuTuple.Bu.addTupleTool('LoKi::Hybrid::TupleTool')
BuLOKI.Variables = {
    'LOKI_ETA'          : 'ETA',
    'LOKI_MIPCHI2DV_PV' : 'MIPCHI2DV(PRIMARY)', #MIPCHI2 to any PV
    'LOKI_BPVLTIME' : 'BPVLTIME()' #time in ns
                     }
#mapsRoot = '/Event/BhadronCompleteEvent/Phys/B2Kpi0Line/Particles/maps/'
#mapsRoot = '/Event/BhadronCompleteEvent/Phys/B2Kpi0Line/maps/'

##if isSim: mapsRoot = '/Event/Bu2Kpi.Strip/Phys/B2Kpi0Line/maps/'#filteredMC
#if not isSim: mapsRoot = '/Event/Dimuon/Phys/Bs2MuMuLinesBu2JPsiKLine/maps/'#data
#BuVars ={}
#BuVars = {
#    'LOKI_ETA'    : 'ETA',
#    'MTDOCA'      : 'MTDOCA(1)',
#    'MTDOCACHI2'  : 'MTDOCACHI2(1)',
#    'CONE3ANGLE'  :"RELINFO('"+mapsRoot+"coneIso_B/1.7', 'CONEANGLE', -10. )",
#    'CONE3MULT'   :"RELINFO('"+mapsRoot+"coneIso_B/1.7', 'CONEMULT',  -10. )",
#    'CONE3PTASY'  :"RELINFO('"+mapsRoot+"coneIso_B/1.7', 'CONEPTASYM',-10. )",
#    'VTXISONUMVTX':"RELINFO('"+mapsRoot+"vtxIso_B', 'VTXISONUMVTX', -10. )",
#    'VTXISO_ONE'  :"RELINFO('"+mapsRoot+"vtxIso_B', 'VTXISODCHI2ONETRACK',    -10. )",
#    'VTXISO_ONEM' :"RELINFO('"+mapsRoot+"vtxIso_B', 'VTXISODCHI2MASSONETRACK',-10. )",
#    'VTXISO_TWO'  :"RELINFO('"+mapsRoot+"vtxIso_B', 'VTXISODCHI2TWOTRACK',    -10. )",
#    'VTXISO_TWOM' :"RELINFO('"+mapsRoot+"vtxIso_B', 'VTXISODCHI2MASSTWOTRACK',-10. )",
#    'CONE3MULT_K' :"RELINFO('"+mapsRoot+"coneIso_K/1.7', 'CONEMULT',  -10. )",
#    'EWCONE3ANGLE':"RELINFO('"+mapsRoot+"neutralConeIso_B/1.7', 'EWCONEANGLE', -10. )",
#    'EWCONE3NMULT':"RELINFO('"+mapsRoot+"neutralConeIso_B/1.7', 'EWCONENMULT', -10. )"
#    }
### ALWAYS WRITE THIS VAR TO PLACATE TMVA
#if not isSim: BuVars['BKGCAT'] = 'INFO(9028, -10.)'
#BuLOKI.Variables = BuVars
if isSim:
    from Configurables import BackgroundCategory,Calo2MCTool,DaVinciSmartAssociator
    bkg = BuTuple.addTupleTool('TupleToolMCBackgroundInfo')
    bkg.addTool(BackgroundCategory,name='BackgroundCategory')
    bkg.BackgroundCategory.addTool(Calo2MCTool,name='Calo2MCTool')
    bkg.BackgroundCategory.Calo2MCTool.Hypo2Cluster=True
    truth = BuTuple.addTupleTool('TupleToolMCTruth')
    truth.ToolList = [
        'MCTupleToolKinematic',
        'MCTupleToolPID' ]
    truth.addTool(DaVinciSmartAssociator,name='DaVinciSmartAssociator')
    truth.DaVinciSmartAssociator.addTool(Calo2MCTool,name='Calo2MCTool')
    truth.DaVinciSmartAssociator.Calo2MCTool.Hypo2Cluster=True

BuTuple.Branches = { 'Bu'  : '^[B+ -> (J/psi(1S) -> mu+ mu-) K+]CC',
                     'Jpsi'  : '[B+ -> ^(J/psi(1S) -> mu+ mu-) K+]CC',
                     'mup'  : '[B+ -> (J/psi(1S) -> ^mu+ mu-) K+]CC',
                     'mun'  : '[B+ -> (J/psi(1S) -> mu+ ^mu-) K+]CC',
                     'Ku' : '[B+ -> (J/psi(1S) -> mu+ mu-) ^K+]CC'}

BuTuple.Bu.addTupleTool('TupleToolDecayTreeFitter/Jpsimass')
BuTuple.Bu.Jpsimass.Verbose = True
BuTuple.Bu.Jpsimass.daughtersToConstrain = ['J/psi(1S)']
BuTuple.Bu.Jpsimass.UpdateDaughters = True

DictTuple =BuTuple.Bu.addTupleTool(LoKi__Hybrid__Dict2Tuple, "DTFTuple")
DictTuple.addTool(DTFDict,"DTF")
DictTuple.Source = "LoKi::Hybrid::DTFDict/DTF"
DictTuple.NumVar = 30
DictTuple.DTF.daughtersToConstrain=["J/psi(1S)"]
DictTuple.DTF.addTool(LoKi__Hybrid__DictOfFunctors,"dict")
DictTuple.DTF.Source = "LoKi::Hybrid::DictOfFunctors/dict"
DictTuple.DTF.dict.Variables = {
    "DTFDict_Bu_PT"            : "PT",
    "DTFDict_Bu_M"             : "M",
    "DTFDict_Bu_LOKI_BPVLTIME" : "BPVLTIME()",

    "DTFDict_Jpsi_PT"           : "CHILD(PT,'[B+ -> ^(J/psi(1S) -> mu+ mu-) K+]CC')",
    "DTFDict_Jpsi_M"            : "CHILD(M,'[B+ -> ^(J/psi(1S) -> mu+ mu-) K+]CC')",
    "DTFDict_Jpsi_PE"           : "CHILD(E,'[B+ -> ^(J/psi(1S) -> mu+ mu-) K+]CC')",
    "DTFDict_Jpsi_PX"           : "CHILD(PX,'[B+ -> ^(J/psi(1S) -> mu+ mu-) K+]CC')",
    "DTFDict_Jpsi_PY"           : "CHILD(PY,'[B+ -> ^(J/psi(1S) -> mu+ mu-) K+]CC')",
    "DTFDict_Jpsi_PZ"           : "CHILD(PZ,'[B+ -> ^(J/psi(1S) -> mu+ mu-) K+]CC')",
#    "DTFDict_Jpsi_LOKI_MIPCHI2DV_PV"  : "CHILD(MIPCHI2DV(PRIMARY),'[B+ -> ^(J/psi(1S) -> mu+ mu-) K+]CC')",

    "DTFDict_mup_PT"           : "CHILD(PT,'[B+ -> (J/psi(1S) -> ^mu+ mu-) K+]CC')",
    "DTFDict_mup_PE"           : "CHILD(E,'[B+ -> (J/psi(1S) -> ^mu+ mu-) K+]CC')",
    "DTFDict_mup_PX"           : "CHILD(PX,'[B+ -> (J/psi(1S) -> ^mu+ mu-) K+]CC')",
    "DTFDict_mup_PY"           : "CHILD(PY,'[B+ -> (J/psi(1S) -> ^mu+ mu-) K+]CC')",
    "DTFDict_mup_PZ"           : "CHILD(PZ,'[B+ -> (J/psi(1S) -> ^mu+ mu-) K+]CC')",
    "DTFDict_mup_LOKI_MIPCHI2DV_PV"  : "CHILD(MIPCHI2DV(PRIMARY),'[B+ -> (J/psi(1S) -> ^mu+ mu-) K+]CC')",

    "DTFDict_mun_PT"           : "CHILD(PT,'[B+ -> (J/psi(1S) -> mu+ ^mu-) K+]CC')",
    "DTFDict_mun_PE"           : "CHILD(E,'[B+ -> (J/psi(1S) -> mu+ ^mu-) K+]CC')",
    "DTFDict_mun_PX"           : "CHILD(PX,'[B+ -> (J/psi(1S) -> mu+ ^mu-) K+]CC')",
    "DTFDict_mun_PY"           : "CHILD(PY,'[B+ -> (J/psi(1S) -> mu+ ^mu-) K+]CC')",
    "DTFDict_mun_PZ"           : "CHILD(PZ,'[B+ -> (J/psi(1S) -> mu+ ^mu-) K+]CC')",
    "DTFDict_mun_LOKI_MIPCHI2DV_PV"  : "CHILD(MIPCHI2DV(PRIMARY),'[B+ -> (J/psi(1S) -> mu+ ^mu-) K+]CC')",

   }

BuTuple.addTool(TupleToolDecay, name = 'Ku')
TTTT_Ku = BuTuple.Ku.addTupleTool('TupleToolTISTOS')
TTTT_Ku.TriggerList = [ 'Hlt1TrackMVADecision',
                        'Hlt1TwoTrackMVADecision' ]
#TTTT_Ku.TriggerList = [ 'Hlt1DiMuonHighMassDecision',
#    'Hlt1DiMuonLowMassDecision',
#    'Hlt1SingleMuonNoIPDecision',
#    'Hlt1SingleMuonHighPTDecision',
#    'Hlt1SingleElectronNoIPDecision',
#    'Hlt1TrackAllL0Decision',
#    'Hlt1TrackMuonDecision',
#    'Hlt1TrackPhotonDecision',
#    'Hlt1VertexDisplVertexDecision',
#    'Hlt1PhysDecision' ]
TTTT_Ku.Verbose = True
KuTrack = BuTuple.Ku.addTupleTool('TupleToolTrackInfo')
KuLOKI = BuTuple.Ku.addTupleTool('LoKi::Hybrid::TupleTool')
KuLOKI.Variables = {
    'LOKI_ETA'          : 'ETA',
    'LOKI_MIPCHI2DV_PV' : 'MIPCHI2DV(PRIMARY)'
                     }

BuTuple.addTool(TupleToolDecay, name = 'mup')
mupLOKI = BuTuple.mup.addTupleTool('LoKi::Hybrid::TupleTool')
mupLOKI.Variables = {
    'LOKI_ETA'          : 'ETA',
    'LOKI_MIPCHI2DV_PV' : 'MIPCHI2DV(PRIMARY)'
                     }

BuTuple.addTool(TupleToolDecay, name = 'mun')
munLOKI = BuTuple.mun.addTupleTool('LoKi::Hybrid::TupleTool')
munLOKI.Variables = {
    'LOKI_ETA'          : 'ETA',
    'LOKI_MIPCHI2DV_PV' : 'MIPCHI2DV(PRIMARY)'
                     }
#extra info
from Configurables import AddExtraInfo, ConeVariables, VertexIsolation
#from Configurables import AddExtraInfo, ConeVariables, VertexIsolation, TupleToolTest



#MDST
#dtt.Inputs = ['/Phys/[0]/Particles'.format(line)]
from Configurables import DaVinci

# Configure DaVinci
#BuTuple().OutputLevel = VERBOSE
#DaVinci().RedoMCLinks = True
#MessageSvc().Format = "% F%60W%S%7W%R%T %0W%M"
DaVinci().UserAlgorithms += [BuTuple]
#DaVinci().UserAlgorithms += [BuTuple, bhadron_extra]
DaVinci().InputType = 'DST'
DaVinci().TupleFile = 'DVntuple.root'
DaVinci().PrintFreq = 1
DaVinci().DataType = '2017'
if not isSim: DaVinci().Simulation = False
if isSim: DaVinci().Simulation = True
# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation
DaVinci().EvtMax = -1
from Configurables import CondDB
if not isSim: CondDB().useLatestTags("2017")
#CondDB().useLatestTags("2015")
if isSim: DaVinci().DDDBtag   = "dddb-20150724"#2015/6MCrequest
if isSim: DaVinci().CondDBtag = "sim-20161124-vc-md100"#2015MCrequest
#if isSim: DaVinci().CondDBtag = "sim-20161124-2-vc-md100"#2016MCrequest
#DaVinci().DDDBtag   = "dddb-20150724"
#DaVinci().CondDBtag = "cond-20150828"
#DaVinci().CondDBtag = 'sim-20130522-1-vc-md100'
#DaVinci().DDDBtag = 'dddb-20130929-1'
#MDST
#DaVinci().RootInTES = '/Event/{0}'.format(stream)
#DaVinci().RootInTES = '/Event/Bhadron'

from GaudiConf import IOHelper

#Use the local input data
IOHelper().inputFiles([
#'/eos/lhcb/user/w/wparker/ganga/00059560_00000004_1.dimuon.dst'
#'00059560_00000001_1.bhadroncompleteevent.dst'#2016 data
#'000000.Bu2Kpi.Strip.dst' #filtering test 2016MC
#'00056792_00000001_1.bu2kpi.strip.dst'#2016MC
#'00056786_00000001_1.bu2kpi.strip.dst'#2015MC
#'00051527_00000006_3.AllStreams.dst'
#'00049575_00000020_1.bhadroncompleteevent.dst'
#'00053485_00071491_1.bhadroncompleteevent.dst'
], clear=True)


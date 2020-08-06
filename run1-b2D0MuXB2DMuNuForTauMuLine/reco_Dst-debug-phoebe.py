from Gaudi.Configuration import *
import GaudiKernel.SystemOfUnits as Units
from Configurables import DaVinci, LHCbApp, CombineParticles
from PhysSelPython.Wrappers import MergedSelection, Selection, SelectionSequence, DataOnDemand, AutomaticData
from Configurables import CheckPV
from Configurables import ReadHltReport
from Configurables import LoKi__Hybrid__TupleTool
from Configurables import LoKi__HDRFilter as HDRFilter
from Configurables import ChargedProtoParticleMaker
from Configurables import ProtoParticleCALOFilter
from Configurables import CombinedParticleMaker
from Configurables import NoPIDsParticleMaker
from Configurables import TupleToolApplyIsolation
from CommonParticles.Utils import *

DaVinci()
veloprotos = ChargedProtoParticleMaker(name="myProtoPMaker")
veloprotos.Inputs=['Rec/Track/Best']
veloprotos.Output='Rec/ProtoP/myProtoPMaker/ProtoParticles'
DaVinci().appendToMainSequence([veloprotos])

fltr = HDRFilter ('StrippedBCands', Code = "HLT_PASS('Strippingb2D0MuXB2DMuForTauMuLineDecision')", Location ="/Event/Strip/Phys/DecReports")


trigfltr = HDRFilter('TriggeredD0', Code = "HLT_PASS('Hlt2CharmHadD02HH_D02KPiDecision')")

DaVinci().HistogramFile = "YCandTauHistos.root"
DaVinci().TupleFile = "YCands.root"
DaVinci().DataType = "2012"
DaVinci().EvtMax = 250
DaVinci().SkipEvents = 0
DaVinci().PrintFreq = 100
DaVinci().Simulation = True
#DaVinci().EventPreFilters/ = [CheckPV()]
#importOptions('Dstmunu_filteredMC.py')
from Configurables import CondDB
#CondDB().useLatestTags("2012")

#MessageSvc().OutputLevel = DEBUG

#LHCbApp().DDDBtag = "dddb-20130503-1"
#LHCbApp().CondDBtag = "sim-20130503-1-vc-md100"

line = 'Bd2DstarMuNuTight'
location = '/Event/Semileptonic/Phys/'+line+'/Particles'

from Configurables import TrackSmearState


smear = TrackSmearState('StateSmear')
#DaVinci().UserAlgorithms.append(smear)

#K
chargedK = DataOnDemand(Location = 'Phys/StdAllNoPIDsKaons/Particles')

#pi
chargedPi = DataOnDemand(Location = 'Phys/StdAllNoPIDsPions/Particles')

#piNOPID
chargedNOPID = DataOnDemand(Location= 'Phys/StdAllNoPIDsPions/Particles')

#uppiSelMyD0,mulist])
upPi = DataOnDemand(Location = 'Phys/StdNoPIDsUpPions/Particles')

#mu
mulist_pre = DataOnDemand(Location = 'Phys/StdAllNoPIDsMuons/Particles')
from Configurables import TisTosParticleTagger
myTagger = TisTosParticleTagger("MyTagger")
myTagger.Inputs = ["Phys/StdAllNoPIDsMuons/Particles"]
myTagger.TisTosSpecs = {"L0Global%TIS":0}
mulist = Selection("TISMuons", Algorithm=myTagger, RequiredSelections=[mulist_pre])
#mulist = DataOnDemand(Location = 'Phys/StdNoPIDsMuons/Particles')#'Phys/StdAllLooseMuons/Particles')

#D0#
_MyD0 = CombineParticles("MyD0")
_MyD0.Preambulo += ["from LoKiPhysMC.decorators import *",
                   "from LoKiPhysMC.functions import mcMatch"]
_MyD0.DecayDescriptor = "[D0 -> K- pi+]cc"
_MyD0.DaughtersCuts = {"K+" : "(mcMatch('[^K+]CC')) & (PT > 300*MeV) & (MIPCHI2DV(PRIMARY)>45.0) & (TRCHI2DOF < 4)",
                       "pi-" : "(PT > 300*MeV) & (MIPCHI2DV(PRIMARY)>45.0) & (TRCHI2DOF < 4)"
                       }
_MyD0.CombinationCut = "(ADAMASS('D0') < 200*MeV) & (ACHILD(PT,1)+ACHILD(PT,2) > 1*GeV)"
_MyD0.MotherCut = "(mcMatch('[Charm ->K- pi+ {gamma}{gamma}{gamma}]CC')) & (ADMASS('D0') < 100*MeV) & (VFASPF(VCHI2/VDOF) < 100) & (BPVVDCHI2 > 250.0) & (BPVDIRA > 0.9998)"

SelMyD0 = Selection("SelMyD0",Algorithm = _MyD0, RequiredSelections = [chargedK, chargedPi])


#Dmu#
_MyDmup = CombineParticles("MyDmup")
_MyDmup.DecayDescriptor="[B+ -> D0 mu+]cc"
_MyDmup.DaughtersCuts = {"mu-" : "(P > 3*GeV) & (MIPCHI2DV(PRIMARY)>45) & (TRCHI2DOF < 3.0)"}# & (PIDmu > 2)"}
_MyDmup.CombinationCut = "(AM < 10.2*GeV)"
_MyDmup.MotherCut = "(M < 10000*MeV) & (BPVDIRA > 0.9995) & (VFASPF(VCHI2/VDOF)<6)"

#Dmu#
_MyDmum = CombineParticles("MyDmum")
_MyDmum.DecayDescriptor="[B+ -> D0 mu-]cc"
_MyDmum.DaughtersCuts = {"mu-" : "(P > 3*GeV) & (MIPCHI2DV(PRIMARY)>45) & (TRCHI2DOF < 3.0)"}# & (PIDmu > 2)"}
_MyDmum.CombinationCut = "(AM < 10.2*GeV)"
_MyDmum.MotherCut = "(M < 10000*MeV) & (BPVDIRA > 0.9995) & (VFASPF(VCHI2/VDOF)<6)"

SelMyDmup = Selection("SelMyDmup",Algorithm = _MyDmup, RequiredSelections = [SelMyD0,mulist_pre])
SelMyDmum = Selection("SelMyDmum",Algorithm = _MyDmum, RequiredSelections = [SelMyD0,mulist_pre])

SeqStrip = SelectionSequence('SeqStrip', TopSelection = SelMyDmup)#, EventPreSelector=[fltr])
MyPreSelection = SeqStrip.sequence()
SeqWSStrip = SelectionSequence('SeqWSStrip', TopSelection = SelMyDmum)#, EventPreSelector=[fltr])
MyWSPreSelection = SeqWSStrip.sequence()

from PhysConf.Filters import LoKi_Filters
code = "(CONTAINS('"+SelMyDmup.outputLocation()+"') > 0) | (CONTAINS('"+SelMyDmum.outputLocation()+"') > 0)"
DmuFltr=LoKi_Filters(VOID_Code=code)
DmuFltrSeq=DmuFltr.sequence("DmuFltrSeq")


#Dstar#
_MyDst = CombineParticles("MyDstar")
_MyDst.DecayDescriptor = "[D*(2010)+ -> D0 pi+]cc"
_MyDst.DaughtersCuts = {"pi+" : "(MIPCHI2DV(PRIMARY)>0.0) & (TRCHI2DOF < 3)"}
_MyDst.CombinationCut = "(ADAMASS('D*(2010)+') < 220*MeV)"
_MyDst.MotherCut = "(ADMASS('D*(2010)+') < 125*MeV) & (M-MAXTREE(ABSID=='D0',M) < 160*MeV) & (VFASPF(VCHI2/VDOF) < 100)"

SelMyDst = Selection("SelMyDst",Algorithm = _MyDst, RequiredSelections = [SelMyD0, chargedPi, upPi])

from Configurables import FitDecayTrees

refitDst = FitDecayTrees("refitDst", Code = "DECTREE('[D*(2010)+ -> D0 pi+]CC')", UsePVConstraint = False, Inputs = [SelMyDst.outputLocation()])

DTFSel = Selection("DTFSel", Algorithm = refitDst, RequiredSelections = [SelMyDst])

from Configurables import LoKi__Hybrid__PlotTool as PlotTool

#Bd#
_MyBd = CombineParticles("MyBu")
_MyBd.Preambulo += ["from LoKiPhysMC.decorators import *",
                   "from LoKiPhysMC.functions import mcMatch"]
_MyBd.DecayDescriptor = "[B~0 -> D*(2010)+ mu-]cc"
#_MyBd.HistoProduce = True
#_MyBd.addTool(PlotTool("MotherPlots"))
#_MyBd.MotherPlots.Histos = { "AMAXDOCA(FLATTEN((ABSID=='D0') | (ABSID=='mu-')))" : ("DOCA",0,2)}
_MyBd.DaughtersCuts = {"mu-" : "(mcMatch('[^mu+]CC')) & (TRGHOSTPROB < 0.5) & (MIPCHI2DV(PRIMARY)>45) & (TRCHI2DOF < 3.0)"}
_MyBd.CombinationCut = "(AM < 5650*MeV)"
_MyBd.MotherCut = "(M < 5400*MeV) & (BPVDIRA > 0.9995) & (VFASPF(VCHI2/VDOF)<8)"

#BdWS
_MyWSBd = CombineParticles("MyWSBd")
_MyWSBd.DecayDescriptor = "[B~0 -> D*(2010)+ mu+]cc"
_MyWSBd.DaughtersCuts = {"mu+" : "(PT > 100*MeV) & (P > 1*GeV) & (MIPCHI2DV(PRIMARY)>4) & (TRCHI2DOF < 3.0) & (PIDmu > 2)"}
_MyWSBd.CombinationCut = "(AM < 5650*MeV)"
_MyWSBd.MotherCut = "(M < 5400*MeV) & (BPVDIRA > 0.9995)"

#Bd3pi
_MyB2DstPiPiPi = CombineParticles("MyDstPiPiPi")
_MyB2DstPiPiPi.DecayDescriptor = "[B*_00 -> B0 pi+ pi-]cc"
_MyB2DstPiPiPi.DaughtersCuts = {"pi+" : "(TRGHOSTPROB < 0.5) & (MIPCHI2DV(PRIMARY) > 4)"}
_MyB2DstPiPiPi.CombinationCut = "(AM < 5700*MeV) & (AM > 4800*MeV)"
_MyB2DstPiPiPi.MotherCut = "(M < 5500*MeV) & (M > 5000*MeV) & (BPVDIRA > 0.9995) & (VFASPF(VCHI2/VDOF) < 6)"


#SelMyBd = Selection("SelMyBd", Algorithm = _MyBd, RequiredSelections = [DTFSel, mulist_pre])
SelMyBd = Selection("SelMyBd", Algorithm = _MyBd, RequiredSelections = [SelMyDst, mulist_pre])

SelMyWSBd = Selection("SelMyWSBd", Algorithm = _MyWSBd, RequiredSelections = [DTFSel, mulist_pre])


SeqYMaker2 = SelectionSequence('SeqYMaker2', TopSelection = SelMyWSBd)
MySelectionWS = SeqYMaker2.sequence()

from Configurables import FitDecayTrees

refitB2Dstmu = FitDecayTrees("refitB2Dstmu", Code = "DECTREE('[B~0 -> (D*(2010)+ -> (D0->K- pi+) pi+) mu- ]CC')", UsePVConstraint = False, Inputs = [SelMyBd.outputLocation()])
YDTFSel = Selection("YDTFSel", Algorithm = refitB2Dstmu, RequiredSelections = [SelMyBd])

#SeqYMaker = SelectionSequence('SeqYMaker', TopSelection = SelMyBd)#, EventPreSelector=[fltr])
SeqYMaker = SelectionSequence('SeqYMaker', TopSelection = YDTFSel)#, EventPreSelector=[fltr])
MySelection = SeqYMaker.sequence()

SelMyB2DstPiPiPi = Selection("SelMyB2DstPiPiPi",Algorithm = _MyB2DstPiPiPi, RequiredSelections = [chargedPi, SelMyBd])

SeqBdMaker = SelectionSequence('SeqBdMaker', EventPreSelector = [], TopSelection = SelMyB2DstPiPiPi)
MySelectionB2DstPiPiPi = SeqBdMaker.sequence()


algorithm = NoPIDsParticleMaker('StdNoPIDsVeloPions', Particle = 'pion')
algorithm.Input = "Rec/ProtoP/myProtoPMaker/ProtoParticles"
selector = trackSelector(algorithm, trackTypes=['Velo'])

locations = updateDoD(algorithm)
DaVinci().appendToMainSequence([algorithm])

from DecayTreeTuple.Configuration import *

tuple = DecayTreeTuple("YCands")
tuple.ToolList += [
    "TupleToolKinematic",
    "TupleToolTrackInfo",
    "TupleToolAngles",
    "TupleToolPid",
    "TupleToolMuonPid",
    "TupleToolL0Calo"
   ]
from Configurables import TupleToolMCTruth, TupleToolMCBackgroundInfo, BackgroundCategory, TupleToolKinematic, TupleToolTagDiscardDstMu
from Configurables import LoKi__Hybrid__EvtTupleTool as LoKiEvtTool
TTMCBI = tuple.addTupleTool("TupleToolMCBackgroundInfo")
TTMCBI.addTool(BackgroundCategory, name="BackgroundCategory")
TTMCBI.BackgroundCategory.SemileptonicDecay = True
TTMCBI.BackgroundCategory.NumNeutrinos=3
tuple.addTupleTool("TupleToolTISTOS")
tuple.TupleToolTISTOS.TriggerList = ['L0MuonDecision','L0HadronDecision','Hlt1TrackAllL0Decision','Hlt2CharmHadD02HH_D02KPiDecision']
tuple.TupleToolTISTOS.VerboseHlt2 = True
tuple.TupleToolTISTOS.VerboseHlt1 = True
tuple.TupleToolTISTOS.VerboseL0 = True
#isol=tuple.addTupleTool("TupleToolTrackIsolation/Isolation")
#isol.FillAsymmetry = True
#isol.MinConeAngle=0.6
#isol.MaxConeAngle=1.0
#isol.StepSize=0.2
tuple.Decay = "[B~0 -> ^(D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+) ^mu-]CC"
tuple.Inputs = [SeqYMaker.outputLocation()]
tuple.addBranches({
    "Y" : "^([B~0 -> (D*(2010)+ -> (D0 -> K- pi+) pi+) mu-]CC)",
    "D0" : "[B~0 -> (D*(2010)+ -> ^(D0 -> K- pi+) pi+) mu-]CC",
    "piminus" : "[B~0 -> (D*(2010)+ -> (D0 -> K- pi+) ^pi+) mu-]CC",
    "piminus0" : "[B~0 -> (D*(2010)+ -> (D0 -> K- ^pi+) pi+) mu-]CC",
    "Kplus" : "[B~0 -> (D*(2010)+ -> (D0 -> ^K- pi+) pi+) mu-]CC",
    "muplus" : "[B~0 -> (D*(2010)+ -> (D0 -> K- pi+) pi+) ^mu-]CC"})
tuple.Y.addTool(TupleToolTagDiscardDstMu,name="MyDiscardDstMu")
tuple.Y.ToolList+=["TupleToolTagDiscardDstMu/MyDiscardDstMu"]
tuple.Y.addTool(TupleToolApplyIsolation,name="TupleToolApplyIsolationSoft")
tuple.Y.TupleToolApplyIsolationSoft.WeightsFile="weightsSoft.xml"
tuple.Y.ToolList+=["TupleToolApplyIsolation/TupleToolApplyIsolationSoft"]

tuple.addTupleTool(LoKiEvtTool,"LHETT")
tuple.LHETT.Preambulo += ["from LoKiCore.functions import *"]
tuple.LHETT.VOID_Variables = {
    "nTracks" : "CONTAINS ('Rec/Track/Best')",
    "nSPDhits" : "CONTAINS('Raw/Spd/Digits')"
    }
truth=tuple.addTupleTool('TupleToolMCTruth')
truth.ToolList =  [
          "MCTupleToolKinematic",
          "MCTupleToolHierarchy"
          ]

TuplePiPiPi = DecayTreeTuple("B2DstPiPiPi")
TuplePiPiPi.ToolList+=[
    "TupleToolKinematic",
    "TupleToolTrackInfo"
]
TTMCBI2 = TuplePiPiPi.addTupleTool("TupleToolMCBackgroundInfo")
TTMCBI2.addTool(BackgroundCategory, name="BackgroundCategory")
#TTMCBI2.BackgroundCategory.SemileptonicDecay = True
#TTMCBI2.BackgroundCategory.NumNeutrinos=3
TuplePiPiPi.addTupleTool(LoKiEvtTool,"LHETTPiPiPi")
TuplePiPiPi.LHETTPiPiPi.Preambulo += ["from LoKiCore.functions import *"]
TuplePiPiPi.LHETTPiPiPi.VOID_Variables = {
    "nTracks" : "CONTAINS ('Rec/Track/Best')"
    }
TuplePiPiPi.addTupleTool("TupleToolTISTOS")
TuplePiPiPi.TupleToolTISTOS.TriggerList = ['L0MuonDecision','L0HadronDecision','Hlt2CharmHadD02HH_D02KPiDecision']
TuplePiPiPi.Inputs = [SeqBdMaker.outputLocation()]
TuplePiPiPi.Decay = "[B*_0~0 -> (^B~0 -> (^D*(2010)+ -> (^D0 => ^K- ^pi+) ^pi+) ^mu-) ^pi+ ^pi-]cc"

TuplePiPiPi.addBranches({
    "Y" : "[B0]cc : [B0 -> (D*(2010)- -> (D0 -> K- pi+) pi-)]cc",
    "D0" : "[D0]cc : [B0 -> (D*(2010)- -> (^D0 -> K- pi+) pi-)]cc",
    "piminus" : "[B0 -> (D*(2010)- => (D0 -> K- pi+) ^pi-) mu-]cc",
    "piminus0" : "[B0 -> (D*(2010)- => (D0 -> K- ^pi+) pi-) mu-]cc",
    "Kplus" : "[K-]cc : [B0 -> (D*(2010)- => (D0 -> ^K- pi+) pi-)]cc",
    "muplus" : "[[B0]cc -> D*(2010)- ^mu-]cc"})

truth2=TuplePiPiPi.addTupleTool('TupleToolMCTruth')
truth2.ToolList =  [
          "MCTupleToolKinematic",
          "MCTupleToolHierarchy"
          ]


#DaVinci().appendToMainSequence([smear,MyPreSelection, MyWSPreSelection, MySelection, tuple, ReadHltReport()])
DaVinci().appendToMainSequence([smear,MySelection, tuple, ReadHltReport()])

#appConf=ApplicationMgr(OutputLevel=INFO, AppName='myBrunel')

#my gaudipython crap for analysis of brunel output

#import GaudiPython
#appMgr = GaudiPython.AppMgr()
#evt = appMgr.evtSvc()

#appMgr.run(1)




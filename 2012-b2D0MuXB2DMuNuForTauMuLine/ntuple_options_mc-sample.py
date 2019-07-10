from Gaudi.Configuration import *
import GaudiKernel.SystemOfUnits as Units
from Configurables import DaVinci, LHCbApp, CombineParticles
from PhysSelPython.Wrappers import MergedSelection, Selection, SelectionSequence, DataOnDemand, AutomaticData
from Configurables import CheckPV
from Configurables import ReadHltReport
from Configurables import LoKi__Hybrid__TupleTool as lokitool
from Configurables import LoKi__HDRFilter as HDRFilter
from Configurables import ChargedProtoParticleMaker
from Configurables import ProtoParticleCALOFilter
from Configurables import CombinedParticleMaker
from Configurables import NoPIDsParticleMaker
from Configurables import TupleToolApplyIsolation
from Configurables import TupleToolApplyIsolationDD
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
DaVinci().EvtMax = -1#500#50000#500
DaVinci().SkipEvents = 0
DaVinci().PrintFreq = 50
DaVinci().Simulation = True
#DaVinci().EventPreFilters/ = [CheckPV()]
#importOptions('Dstmunu_filteredMC.py')
#from Configurables import CondDB
#CondDB().useLatestTags("2012")

#MessageSvc().OutputLevel = DEBUG

#LHCbApp().DDDBtag = "dddb-20130503-1"
#LHCbApp().CondDBtag = "sim-20130503-1-vc-md100"

mufake=False


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
                   "from LoKiMC.functions import *",
                   "from LoKiPhysMC.functions import *"]
_MyD0.DecayDescriptor = "[D0 -> K- pi+]cc"
_MyD0.DaughtersCuts = {"K+" : "(mcMatch('[^K+]CC')) & (MIPCHI2DV(PRIMARY)> 45.0) & (P>2.0*GeV) & (PT > 300.0 *MeV) & (TRGHOSTPROB < 0.5) & (MCSELMATCH(MCNINANCESTORS(BEAUTY) > 0))",
                       "pi-" : "(PT > 300*MeV) & (P>2.0*GeV) & (PT > 300.0 *MeV)& (MIPCHI2DV(PRIMARY)> 45.0) & (TRGHOSTPROB < 0.5) & (MCSELMATCH(MCNINANCESTORS(BEAUTY) > 0))"
                       }
#_MyD0.DaughtersCuts = {"K+" : "(mcMatch('[^K+]CC')) & (MIPCHI2DV(PRIMARY)> 45.0) & (PT > 300.0 *MeV)",
#                       "pi-" : " (PT > 300.0 *MeV)& (MIPCHI2DV(PRIMARY)> 45.0)"
#                       }
if(mufake):
	_MyD0.DaughtersCuts = {"K+" : "(mcMatch('[^K+]CC')) & (MIPCHI2DV(PRIMARY)> 5.0) & (P>2.0*GeV) & (PT > 300.0 *MeV) & (TRGHOSTPROB < 0.5) & (MCSELMATCH(MCNINANCESTORS(BEAUTY) > 0))",
        	               "pi-" : "(PT > 300*MeV) & (P>2.0*GeV) & (PT > 300.0 *MeV)& (MIPCHI2DV(PRIMARY)> 5.0) & (TRGHOSTPROB < 0.5) & (MCSELMATCH(MCNINANCESTORS(BEAUTY) > 0))"
                	       }
_MyD0.CombinationCut = "(ADAMASS('D0') < 100.0 *MeV) & (ACHILD(PT,1)+ACHILD(PT,2) > 1400.0 *MeV)"
_MyD0.MotherCut = "(mcMatch('[Charm ->K- pi+ {gamma}{gamma}{gamma}]CC')) & (SUMTREE( PT, ISBASIC )> 1400.0 * MeV) &(ADMASS('D0') < 80.0 *MeV) & (VFASPF(VCHI2/VDOF) < 4.0) & (BPVVDCHI2 > 250.0) & (BPVDIRA> 0.9998)"

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
                   "from LoKiPhysMC.functions import *"]
_MyBd.DecayDescriptor = "[B- -> D0 mu-]cc"
#_MyBd.HistoProduce = True
#_MyBd.addTool(PlotTool("MotherPlots"))
#_MyBd.MotherPlots.Histos = { "AMAXDOCA(FLATTEN((ABSID=='D0') | (ABSID=='mu-')))" : ("DOCA",0,2)}
_MyBd.DaughtersCuts = {"mu-" : "(mcMatch('[^mu+]CC')) & (MIPCHI2DV(PRIMARY)> 45.0) &(TRGHOSTPROB < 0.5) & (P> 3.0*GeV) & (MCSELMATCH(MCNINANCESTORS(BEAUTY) > 0))"}
#_MyBd.DaughtersCuts = {"mu-" : "(mcMatch('[^mu+]CC')) & (MIPCHI2DV(PRIMARY)> 45.0) "}
if(mufake):
	_MyBd.DaughtersCuts = {"mu-" : "(MIPCHI2DV(PRIMARY)> 5.0) & (TRGHOSTPROB < 0.5) & (P> 3.0*GeV)"}
#_MyBd.DaughtersCuts = {"mu-" : "(mcMatch('[^mu+]CC')) & (TRGHOSTPROB < 0.5) & (MIPCHI2DV(PRIMARY)>45) & (TRCHI2DOF < 3.0)"}
_MyBd.CombinationCut = "(AM < 10.2*GeV)"
_MyBd.MotherCut = "(MM<10.0*GeV) & (MM>0.0*GeV) & (VFASPF(VCHI2/VDOF)< 6.0) & (BPVDIRA> 0.9995)"

#BdWS
_MyWSBd = CombineParticles("MyWSBd")
_MyWSBd.DecayDescriptor = "[B~0 -> D*(2010)+ mu+]cc"
_MyWSBd.DaughtersCuts = {"mu+" : "(PT > 100*MeV) & (P > 1*GeV) & (MIPCHI2DV(PRIMARY)>4) & (TRCHI2DOF < 3.0) & (PIDmu > 2)"}
_MyWSBd.CombinationCut = "(AM < 5650*MeV)"
_MyWSBd.MotherCut = "(M < 5400*MeV) & (BPVDIRA > 0.9995)"


SelMyBd = Selection("SelMyBd", Algorithm = _MyBd, RequiredSelections = [SelMyD0, mulist_pre])
refitB = FitDecayTrees("refitB", Code = "DECTREE('[B- -> (D0->K- pi+) mu-]CC')", UsePVConstraint = False, Inputs = [SelMyBd.outputLocation()])
DTFSelB = Selection("DTFSelB", Algorithm = refitB, RequiredSelections = [SelMyBd])

SelMyWSBd = Selection("SelMyWSBd", Algorithm = _MyWSBd, RequiredSelections = [DTFSel, mulist_pre])


SeqYMaker2 = SelectionSequence('SeqYMaker2', TopSelection = SelMyWSBd)
MySelectionWS = SeqYMaker2.sequence()

from Configurables import FitDecayTrees

#refitB2Dstmu = FitDecayTrees("refitB2Dstmu", Code = "DECTREE('[B~0 -> D*(2010)+ mu- ]CC')", UsePVConstraint = False, Inputs = [SelMyBd.outputLocation()])
#YDTFSel = Selection("YDTFSel", Algorithm = refitB2Dstmu, RequiredSelections = [SelMyBd])

#refitB2Dmu = FitDecayTrees("refitB2Dmu", Code = "DECTREE('[B- -> D0 mu- ]CC')", UsePVConstraint = False, Inputs = [SelMyBd.outputLocation()])
#YDTFSel2 = Selection("YDTFSel2", Algorithm = refitB2Dmu, RequiredSelections = [SelMyBd])

SeqYMaker = SelectionSequence('SeqYMaker', TopSelection = DTFSelB)#, EventPreSelector=[fltr])
MySelection = SeqYMaker.sequence()

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
    "TupleToolPid"
   ]
from Configurables import TupleToolMCTruth, TupleToolMCBackgroundInfo, BackgroundCategory, TupleToolKinematic, TupleToolTagDiscardDstMu, TupleToolApplyIsolationVetoDst
from Configurables import LoKi__Hybrid__EvtTupleTool as LoKiEvtTool
TTMCBI = tuple.addTupleTool("TupleToolMCBackgroundInfo")
TTMCBI.addTool(BackgroundCategory, name="BackgroundCategory")
TTMCBI.BackgroundCategory.SemileptonicDecay = True
TTMCBI.BackgroundCategory.NumNeutrinos=3
tuple.addTupleTool("TupleToolTISTOS")
tuple.TupleToolTISTOS.TriggerList = ['L0MuonDecision','L0HadronDecision','Hlt2CharmHadD02HH_D02KPiDecision','Hlt1TrackAllL0Decision']
tuple.TupleToolTISTOS.VerboseHlt2 = True
tuple.TupleToolTISTOS.VerboseHlt1 = True
tuple.TupleToolTISTOS.VerboseL0 = True
tuple.Decay = "[B- -> ^(D0 -> ^K- ^pi+) ^mu-]CC"
tuple.Inputs = [SeqYMaker.outputLocation()]
tuple.addBranches({
    "Y" : "^([B- -> (D0 -> K- pi+) mu-]CC)",
    "D0" : "[B- -> ^(D0 -> K- pi+) mu-]CC",
    "piminus0" : "[B- -> (D0 -> K- ^pi+) mu-]CC",
    "Kplus" : "[B- -> (D0 -> ^K- pi+) mu-]CC",
    "muplus" : "[B- -> (D0 -> K- pi+) ^mu-]CC"})
if(mufake==False):
	tuple.Y.addTool(TupleToolApplyIsolationVetoDst,name="TupleToolApplyIsolationSoft")
	tuple.Y.TupleToolApplyIsolationSoft.WeightsFile="weightsSoft.xml"
	tuple.Y.TupleToolApplyIsolationSoft.TrueIDs=True
	tuple.Y.ToolList+=["TupleToolApplyIsolationVetoDst/TupleToolApplyIsolationSoft"]
	#tuple.Y.addTool(TupleToolApplyIsolationDD, name="TTAISDD")
	#tuple.Y.TTAISDD.OutputSuffix="DD"
	#tuple.Y.TTAISDD.WeightsFile="weightsDD.xml"
	#tuple.Y.ToolList+=["TupleToolApplyIsolationDD/TTAISDD"]
tuple.addTupleTool(LoKiEvtTool,"LHETT")
tuple.LHETT.Preambulo += ["from LoKiCore.functions import *"]
tuple.LHETT.VOID_Variables = {
    "nTracks" : "CONTAINS ('Rec/Track/Best')",
    "nSPDhits" : "CONTAINS('Raw/Spd/Digits')"
    }
#tuple.Y.addTupleTool("TupleToolDecayTreeFitter/DTF")
#tuple.Y.DTF.constrainToOriginVertex=False
#tuple.Y.DTF.Verbose=True
#tuple.Y.DTF.UpdateDaughters=True
#tuple.muplus.addTupleTool(lokitool,"TTinfo")
#tuple.muplus.TTinfo.Variables = {"hasTT" : "TrHASTT",
#                    "isTT" : "0 < TrIDC('isTT')"}
#tuple.Y.addTupleTool(lokitool,"MoreMC")
#tuple.Y.MoreMC.Preambulo += ["from LoKiPhysMC.decorators import *",
#                   "from LoKiPhysMC.functions import *"]
#tuple.Y.MoreMC.Variables= {
#			"isDD" : "switch(mcMatch('([ (Beauty) --> (D~0) Xc ... ]CC) '),1,0)"
#			}
tuple.Kplus.ToolList+=["TupleToolL0Calo"]
tuple.piminus0.ToolList+=["TupleToolL0Calo"]

#tuple.Kplus.addTupleTool(lokitool,"KfromB")
#tuple.Kplus.KfromB.Preambulo= ["from LoKiPhysMC.decorators import *",
#                   "from LoKiMC.functions import *",
#                   "from LoKiPhysMC.functions import *"]
#tuple.Kplus.KfromB.Variables={ "fromB" : "switch(MCSELMATCH(MCNINANCESTORS(BEAUTY) > 0),1,0)"}

#tuple.piminus0.addTupleTool(lokitool,"pifromB")
#tuple.piminus0.pifromB.Preambulo=tuple.Kplus.KfromB.Preambulo
#tuple.piminus0.pifromB.Variables={ "fromB" : "switch(MCSELMATCH(MCNINANCESTORS(BEAUTY) > 0),1,0)"}

#tuple.muplus.addTupleTool(lokitool,"mufromB")
#tuple.muplus.mufromB.Preambulo=tuple.Kplus.KfromB.Preambulo
#tuple.muplus.mufromB.Variables={ "fromB" : "switch(MCSELMATCH(MCNINANCESTORS(BEAUTY) > 0),1,0)"}
if(mufake):
	tuple.muplus.ToolList+=["TupleToolANNPIDTraining"]
truth=tuple.addTupleTool('TupleToolMCTruth')
truth.ToolList =  [
          "MCTupleToolKinematic",
          "MCTupleToolHierarchy"
          ]


#DaVinci().appendToMainSequence([smear,MyPreSelection, MyWSPreSelection, MySelection, tuple, ReadHltReport()])
DaVinci().appendToMainSequence([smear,MySelection, tuple, ReadHltReport(RequireObjects=[SeqYMaker.outputLocation()])])

#appConf=ApplicationMgr(OutputLevel=INFO, AppName='myBrunel')

#my gaudipython crap for analysis of brunel output

#import GaudiPython
#appMgr = GaudiPython.AppMgr()
#evt = appMgr.evtSvc()

#appMgr.run(1)




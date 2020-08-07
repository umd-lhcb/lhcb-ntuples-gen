from Gaudi.Configuration import *
import GaudiKernel.SystemOfUnits as Units
from Configurables import DaVinci, LHCbApp, CombineParticles
from PhysSelPython.Wrappers import (
    MergedSelection,
    Selection,
    SelectionSequence,
    DataOnDemand,
    AutomaticData,
)
from Configurables import CheckPV
from Configurables import ReadHltReport
from Configurables import LoKi__HDRFilter as HDRFilter
from Configurables import ChargedProtoParticleMaker
from Configurables import ProtoParticleCALOFilter
from Configurables import CombinedParticleMaker
from Configurables import NoPIDsParticleMaker
from CommonParticles.Utils import *

# MessageSvc().OutputLevel = DEBUG
DaVinci()
veloprotos = ChargedProtoParticleMaker(name="myProtoPMaker")
veloprotos.Inputs = ["Rec/Track/Best"]
veloprotos.Output = "Rec/ProtoP/myProtoPMaker/ProtoParticles"
DaVinci().appendToMainSequence([veloprotos])

controlModes = False
fakeLines = False

if controlModes is True:
    fakeLines = True


fltr = HDRFilter(
    "StrippedBCands",
    Code="HLT_PASS('Strippingb2D0MuXB2DMuNuForTauMuLineDecision')",
    Location="/Event/Strip/Phys/DecReports",
)
if fakeLines:
    fltr = HDRFilter(
        "StrippedBCandsFAKE",
        Code="HLT_PASS('Strippingb2D0MuXFakeB2DMuNuForTauMuLineDecision')",
        Location="/Event/Strip/Phys/DecReports",
    )
# fltr = HDRFilter ('StrippedBCands', Code = "HLT_PASS('StrippingB2D0PiD2HHBeauty2CharmLineDecision')", Location ="/Event/Strip/Phys/DecReports")
if controlModes:
    fltr = HDRFilter(
        "StrippedBCands",
        Code="HLT_PASS('Strippingb2D0HB2DHForTauMuLineDecision')",
        Location="/Event/Strip/Phys/DecReports",
    )


trigfltr = HDRFilter("TriggeredD0", Code="HLT_PASS('Hlt2CharmHadD02HH_D02KPiDecision')")

from Configurables import TrackScaleState as SCALER

scaler = SCALER("StateScale")

DaVinci().HistogramFile = "YCandTauHistos.root"
DaVinci().TupleFile = "YCands.root"
DaVinci().DataType = "2012"
DaVinci().EvtMax = -1  # 25000#250000#250000
DaVinci().SkipEvents = 0
DaVinci().PrintFreq = 100
DaVinci().Simulation = False
# DaVinci().EventPreFilters = [CheckPV()]
# DaVinci().Input=['PFN:./Brunel-10000ev.dst']
from Configurables import CondDB

# CondDB().useLatestTags("2012")

# LHCbApp().DDDBtag = "MC2012-20110727"
# LHCbApp().CondDBtag = "MC2012-20110727-vc-md100"

line = "b2D0MuXB2DMuForTauMuLine"
line = "b2D0MuXB2DMuNuForTauMuLine"
if fakeLines:
    line = "b2D0MuXFakeB2DMuNuForTauMuLine"
location = "/Event/Semileptonic/Phys/" + line + "/Particles"

from Configurables import FilterDesktop, FilterInTrees

strippedGuys = AutomaticData(Location=location)
_smuTISfltr = FilterDesktop(
    "smuTIS", Code="INTREE((ABSID=='mu+') & (TIS('L0.*','L0TriggerTisTos')))"
)
StrippedFilteredGuys = Selection(
    name="smuTISfilterSel", Algorithm=_smuTISfltr, RequiredSelections=[strippedGuys]
)

# seqSFG=SelectionSequence('seqSFG',EventPreSelector=[trigfltr],TopSelection=StrippedFilteredGuys)


# pi
allPi = DataOnDemand(Location="Phys/StdAllLoosePions/Particles")

# uppi
upPi = DataOnDemand(Location="Phys/StdNoPIDsUpPions/Particles")

# K
_chargedK = FilterInTrees("GetK", Code="('K+'==ABSID)")
chargedK = Selection(
    "chargedK", Algorithm=_chargedK, RequiredSelections=[StrippedFilteredGuys]
)

# pi
_chargedPi = FilterInTrees("GetPi", Code="('pi+'==ABSID)")
chargedPi = Selection(
    "chargedPi", Algorithm=_chargedPi, RequiredSelections=[StrippedFilteredGuys]
)

# mu
_mulist = FilterInTrees("GetMu", Code="('mu+'==ABSID)")
mulist = Selection(
    "mulist", Algorithm=_mulist, RequiredSelections=[StrippedFilteredGuys]
)


# D0#
_MyD0 = CombineParticles("MyD0")
_MyD0.DecayDescriptor = "[D0 -> K- pi+]cc"
_MyD0.DaughtersCuts = {
    "K+": "(PT > 300*MeV) & (MIPCHI2DV(PRIMARY)>45.0) & (TRCHI2DOF < 4) & (PIDK > 4) & (TRGHOSTPROB < 0.5)",
    "pi-": "(PT > 300*MeV) & (MIPCHI2DV(PRIMARY)>45.0) & (TRCHI2DOF < 4) & (TRGHOSTPROB < 0.5) & (PIDK < 2)",
}
_MyD0.CombinationCut = "(ADAMASS('D0') < 200*MeV)"
_MyD0.MotherCut = "(ADMASS('D0') < 100*MeV) & (VFASPF(VCHI2/VDOF) < 100)"
_MyD0.ParticleCombiners.update({"": "LoKi::VertexFitter"})

SelMyD0 = Selection(
    "SelMyD0", Algorithm=_MyD0, RequiredSelections=[chargedK, chargedPi]
)


# Dstar#
_MyDst = CombineParticles("MyDstar")
_MyDst.DecayDescriptor = "[D*(2010)+ -> D0 pi+]cc"
_MyDst.DaughtersCuts = {
    "pi+": "(MIPCHI2DV(PRIMARY)>0.0) & (TRCHI2DOF < 3) & (TRGHOSTPROB < 0.25) "
}
_MyDst.CombinationCut = "(ADAMASS('D*(2010)+') < 220*MeV)"
_MyDst.MotherCut = "(ADMASS('D*(2010)+') < 125*MeV) & (M-MAXTREE(ABSID=='D0',M) < 160*MeV) & (VFASPF(VCHI2/VDOF) < 100)"
_MyDst.ParticleCombiners.update({"": "LoKi::VertexFitter"})

SelMyDst = Selection(
    "SelMyDst", Algorithm=_MyDst, RequiredSelections=[SelMyD0, allPi, upPi]
)

from Configurables import FitDecayTrees

refitDst = FitDecayTrees(
    "refitDst",
    Code="DECTREE('[D*(2010)+ -> D0 pi+]CC')",
    UsePVConstraint=False,
    Inputs=[SelMyDst.outputLocation()],
)

DTFSel = Selection("DTFSel", Algorithm=refitDst, RequiredSelections=[SelMyDst])

# Dst2ar#
_MyDst2 = CombineParticles("MyDstar")
_MyDst2.DecayDescriptor = "[D*(2010)- -> D0 pi-]cc"
_MyDst2.DaughtersCuts = {
    "pi+": "(MIPCHI2DV(PRIMARY)>0.0) & (TRCHI2DOF < 3) & (TRGHOSTPROB < 0.25) "
}
_MyDst2.CombinationCut = "(ADAMASS('D*(2010)+') < 220*MeV)"
_MyDst2.MotherCut = "(ADMASS('D*(2010)+') < 125*MeV) & (M-MAXTREE(ABSID=='D0',M) < 160*MeV) & (VFASPF(VCHI2/VDOF) < 100)"

SelMyDst2 = Selection(
    "SelMyDst2", Algorithm=_MyDst2, RequiredSelections=[SelMyD0, allPi, upPi]
)

refitDst2 = FitDecayTrees(
    "refitDst2",
    Code="DECTREE('[D*(2010)- -> D0 pi-]CC')",
    UsePVConstraint=False,
    Inputs=[SelMyDst2.outputLocation()],
)

DTFSel2 = Selection("DTFSel2", Algorithm=refitDst2, RequiredSelections=[SelMyDst2])


# Bd#
_MyBd = CombineParticles("MyBu")
_MyBd.DecayDescriptor = "[B~0 -> D*(2010)+ mu-]cc"
_MyBd.DaughtersCuts = {"mu-": "ALL"}
if fakeLines:
    _MyBd.DaughtersCuts = {"mu-": "ALL"}
_MyBd.CombinationCut = "(AM < 10200*MeV)"
_MyBd.MotherCut = "(M < 10000*MeV) & (BPVDIRA > 0.9995) & (VFASPF(VCHI2/VDOF)<6.0)"
_MyBd.ParticleCombiners.update({"": "LoKi::VertexFitter"})

# BdWS
_MyWSBd = CombineParticles("MyWSBd")
_MyWSBd.DecayDescriptor = "[B~0 -> D*(2010)+ mu+]cc"
_MyWSBd.DaughtersCuts = {"mu+": "ALL"}
if fakeLines:
    _MyWSBd.DaughtersCuts = {"mu+": "ALL"}
_MyWSBd.CombinationCut = "(AM < 10200*MeV)"
_MyWSBd.MotherCut = "(M < 10000*MeV) & (BPVDIRA > 0.9995) & (VFASPF(VCHI2/VDOF)<6.0)"
_MyWSBd.ParticleCombiners.update({"": "LoKi::VertexFitter"})

# BdWS2
_MyWS2Bd = CombineParticles("MyWS2Bd")
_MyWS2Bd.DecayDescriptor = "[B0 -> D*(2010)+ mu+]cc"
_MyWS2Bd.DaughtersCuts = {"mu+": "ALL"}
if fakeLines:
    _MyWS2Bd.DaughtersCuts = {"mu+": "ALL"}
_MyWS2Bd.CombinationCut = "(AM < 10200*MeV)"
_MyWS2Bd.MotherCut = "(M < 10000*MeV) & (BPVDIRA > 0.9995) & (VFASPF(VCHI2/VDOF)<6.0)"
_MyWS2Bd.ParticleCombiners.update({"": "LoKi::VertexFitter"})


# Bd2pi
_MyB2DstPiPi = CombineParticles("MyDstPiPi")
_MyB2DstPiPi.DecayDescriptor = "[B*_0+ -> B0 pi+]cc"
_MyB2DstPiPi.DaughtersCuts = {"pi+": "(TRGHOSTPROB < 0.5) & (MIPCHI2DV(PRIMARY) > 4)"}
_MyB2DstPiPi.CombinationCut = "(AM < 5700*MeV) & (AM > 4800*MeV)"
_MyB2DstPiPi.MotherCut = (
    "(M < 5500*MeV) & (M > 5000*MeV) & (BPVDIRA > 0.9995) & (VFASPF(VCHI2/VDOF) < 9)"
)


# Bd3pi
_MyB2DstPiPiPi = CombineParticles("MyDstPiPiPi")
_MyB2DstPiPiPi.DecayDescriptor = "[B*_00 -> B0 pi+ pi-]cc"
_MyB2DstPiPiPi.DaughtersCuts = {"pi+": "(TRGHOSTPROB < 0.5) & (MIPCHI2DV(PRIMARY) > 4)"}
_MyB2DstPiPiPi.CombinationCut = "(AM < 5700*MeV) & (AM > 4800*MeV)"
_MyB2DstPiPiPi.MotherCut = (
    "(M < 5500*MeV) & (M > 5000*MeV) & (BPVDIRA > 0.9995) & (VFASPF(VCHI2/VDOF) < 9)"
)


SelMyBd = Selection("SelMyBd", Algorithm=_MyBd, RequiredSelections=[SelMyDst, mulist])

# refitY = FitDecayTrees("refitY", Code = "DECTREE('[B~0 -> D*(2010)+ mu-]CC')", UsePVConstraint = False, Inputs = [SelMyBd.outputLocation()])

# DTFYSel = Selection("DTFYSel", Algorithm = refitY, RequiredSelections = [SelMyBd])


SelMyWSBd = Selection(
    "SelMyWSBd", Algorithm=_MyWSBd, RequiredSelections=[SelMyDst, mulist]
)
SelMyWS2Bd = Selection(
    "SelMyWS2Bd", Algorithm=_MyWS2Bd, RequiredSelections=[SelMyDst2, mulist]
)

refitB2Dstmu = FitDecayTrees(
    "refitB2Dstmu",
    Code="DECTREE('[B~0 -> (D*(2010)+ -> (D0->K- pi+) pi+) mu- ]CC')",
    UsePVConstraint=False,
    Inputs=[SelMyBd.outputLocation()],
)
refitB2DstmuWS = FitDecayTrees(
    "refitB2DstmuWS",
    Code="DECTREE('[B~0 -> (D*(2010)+ -> (D0->K- pi+) pi+) mu+ ]CC')",
    UsePVConstraint=False,
    Inputs=[SelMyWSBd.outputLocation()],
)
refitB2DstmuWS2 = FitDecayTrees(
    "refitB2DstmuWS2",
    Code="DECTREE('[B~0 -> (D*(2010)- -> (D0->K- pi+) pi-) mu- ]CC')",
    UsePVConstraint=False,
    Inputs=[SelMyWS2Bd.outputLocation()],
)
YDTFSel = Selection("YDTFSel", Algorithm=refitB2Dstmu, RequiredSelections=[SelMyBd])
YDTFSelWS = Selection(
    "YDTFSelWS", Algorithm=refitB2DstmuWS, RequiredSelections=[SelMyWSBd]
)
YDTFSelWS2 = Selection(
    "YDTFSelWS2", Algorithm=refitB2DstmuWS2, RequiredSelections=[SelMyWS2Bd]
)

SelMyB2DstPiPi = Selection(
    "SelMyB2DstPiPi", Algorithm=_MyB2DstPiPi, RequiredSelections=[chargedPi, SelMyBd]
)
SelMyB2DstPiPiPi = Selection(
    "SelMyB2DstPiPiPi",
    Algorithm=_MyB2DstPiPiPi,
    RequiredSelections=[chargedPi, SelMyBd],
)


SeqBuMaker = SelectionSequence(
    "SeqBuMaker", EventPreSelector=[trigfltr, fltr], TopSelection=SelMyB2DstPiPi
)
MySelectionB2DstPiPi = SeqBuMaker.sequence()
SeqBdMaker = SelectionSequence(
    "SeqBdMaker", EventPreSelector=[trigfltr, fltr], TopSelection=SelMyB2DstPiPiPi
)
MySelectionB2DstPiPiPi = SeqBdMaker.sequence()


from Configurables import FilterDesktop

_dstpifilt = FilterDesktop("dstpifilter", Code="(M > 4600*MeV)")
dstpifiltsel = Selection(
    name="dstpifiltsel", Algorithm=_dstpifilt, RequiredSelections=[SelMyBd]
)
dstpifiltselseq = SelectionSequence("dstpifiltselseq", TopSelection=dstpifiltsel)

SeqYMaker = SelectionSequence(
    "SeqYMaker", EventPreSelector=[trigfltr, fltr], TopSelection=YDTFSel
)
MySelection = SeqYMaker.sequence()
SeqYMaker2 = SelectionSequence(
    "SeqYMaker2", EventPreSelector=[trigfltr, fltr], TopSelection=YDTFSelWS
)
MySelectionWS = SeqYMaker2.sequence()
SeqYMaker3 = SelectionSequence(
    "SeqYMaker3", EventPreSelector=[trigfltr, fltr], TopSelection=YDTFSelWS2
)
MySelectionWS2 = SeqYMaker3.sequence()
MyFiltSelection = dstpifiltselseq.sequence()

algorithm = NoPIDsParticleMaker("StdNoPIDsVeloPions", Particle="pion")
algorithm.Input = "Rec/ProtoP/myProtoPMaker/ProtoParticles"
selector = trackSelector(algorithm, trackTypes=["Velo"])

locations = updateDoD(algorithm)
# DaVinci().appendToMainSequence([algorithm])


from Configurables import LoKi__Hybrid__EvtTupleTool as LoKiEvtTool

from DecayTreeTuple.Configuration import *

tuple1 = DecayTreeTuple("YCands")
tuple1.ToolList += [
    "TupleToolKinematic",
    "TupleToolTrackInfo",
    "TupleToolAngles",
    "TupleToolVtxIsoln",
    "TupleToolPid",
    "TupleToolMuonPid",
    "TupleToolL0Calo",
]
tuple1.addTupleTool(LoKiEvtTool, "LHETT")
tuple1.LHETT.Preambulo += ["from LoKiCore.functions import *"]
tuple1.LHETT.VOID_Variables = {
    "nTracks": "CONTAINS ('Rec/Track/Best')",
    "nSPDhits": "CONTAINS('Raw/Spd/Digits')",
}
from Configurables import TupleToolTISTOS

tuple1.addTupleTool("TupleToolTISTOS")
tuple1.TupleToolTISTOS.TriggerList = [
    "L0MuonDecision",
    "L0HadronDecision",
    "Hlt1TrackAllL0Decision",
    "Hlt2CharmHadD02HH_D02KPiDecision",
    "Hlt2DiMuonDetachedJPsiDecision",
    "Hlt2DiMuonDetachedDecision",
]
tuple1.TupleToolTISTOS.VerboseHlt2 = True
tuple1.TupleToolTISTOS.VerboseHlt1 = True
tuple1.TupleToolTISTOS.VerboseL0 = True
# isol=tuple1.addTupleTool("TupleToolTrackIsolation/Isolation")
# isol.FillAsymmetry = True
# isol.MinConeAngle=0.6
# isol.MaxConeAngle=1.4
# isol.StepSize=0.2
tuple1.Decay = "[B~0 -> ^(D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+) ^mu-]CC"
tuple1.Inputs = [SeqYMaker.outputLocation()]
if controlModes:
    tuple1.Inputs = [dstpifiltselseq.outputLocation()]
tuple1.addBranches(
    {
        "Y": "^([B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) mu+]CC)",
        "Dst_2010_minus": "[B0 -> ^(D*(2010)- -> (D~0 -> K+ pi-) pi-) mu+]CC",
        "D0": "[B0 -> (D*(2010)- -> ^(D~0 -> K+ pi-) pi-) mu+]CC",
        "piminus": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) ^pi-) mu+]CC",
        "piminus0": "[B0 -> (D*(2010)- -> (D~0 -> K+ ^pi-) pi-) mu+]CC",
        "Kplus": "[B0 -> (D*(2010)- -> (D~0 -> ^K+ pi-) pi-) mu+]CC",
        "muplus": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) ^mu+]CC",
    }
)
tuple1.muplus.ToolList += ["TupleToolANNPIDTraining"]


tuple2 = DecayTreeTuple("YCandsWS")
tuple2.ToolList += [
    "TupleToolKinematic",
    "TupleToolTrackInfo",
    "TupleToolAngles",
    "TupleToolVtxIsoln",
    "TupleToolPid",
    "TupleToolMuonPid",
]
tuple2.addTupleTool(LoKiEvtTool, "LHETT2")
tuple2.LHETT2.Preambulo += ["from LoKiCore.functions import *"]
tuple2.LHETT2.VOID_Variables = {"nTracks": "CONTAINS ('Rec/Track/Best')"}
tuple2.addTupleTool("TupleToolTISTOS")
tuple2.TupleToolTISTOS.TriggerList = [
    "L0MuonDecision",
    "L0HadronDecision",
    "Hlt1TrackAllL0Decision",
    "Hlt2CharmHadD02HH_D02KPiDecision",
    "Hlt2DiMuonDetachedJPsiDecision",
    "Hlt2DiMuonDetachedDecision",
]
tuple2.TupleToolTISTOS.VerboseHlt2 = True
tuple2.TupleToolTISTOS.VerboseHlt1 = True
tuple2.TupleToolTISTOS.VerboseL0 = True
# isol2=tuple2.addTupleTool("TupleToolTrackIsolation/Isolation2")
# isol2.FillAsymmetry = True
# isol2.MinConeAngle=0.6
# isol2.MaxConeAngle=1.4
# isol2.StepSize=0.2
tuple2.Decay = "[B~0 -> ^(D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+) ^mu+]CC"
tuple2.Inputs = [SeqYMaker2.outputLocation()]
tuple2.addBranches(
    {
        "Y": "^([B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) mu-]CC)",
        "Dst_2010_minus": "[B0 -> ^(D*(2010)- -> (D~0 -> K+ pi-) pi-) mu-]CC",
        "D0": "[B0 -> (D*(2010)- -> ^(D~0 -> K+ pi-) pi-) mu-]CC",
        "piminus": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) ^pi-) mu-]CC",
        "piminus0": "[B0 -> (D*(2010)- -> (D~0 -> K+ ^pi-) pi-) mu-]CC",
        "Kplus": "[B0 -> (D*(2010)- -> (D~0 -> ^K+ pi-) pi-) mu-]CC",
        "muplus": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) ^mu-]CC",
    }
)
tuple2.muplus.ToolList += ["TupleToolANNPIDTraining"]


tuple3 = DecayTreeTuple("YCandsWS2")
tuple3.ToolList += [
    "TupleToolKinematic",
    "TupleToolTrackInfo",
    "TupleToolAngles",
    "TupleToolVtxIsoln",
    "TupleToolPid",
    "TupleToolMuonPid",
]
tuple3.addTupleTool(LoKiEvtTool, "LHETT3")
tuple3.LHETT3.Preambulo += ["from LoKiCore.functions import *"]
tuple3.LHETT3.VOID_Variables = {"nTracks": "CONTAINS ('Rec/Track/Best')"}
tuple3.addTupleTool("TupleToolTISTOS")
tuple3.TupleToolTISTOS.TriggerList = [
    "L0MuonDecision",
    "L0HadronDecision",
    "Hlt1TrackAllL0Decision",
    "Hlt2CharmHadD02HH_D02KPiDecision",
    "Hlt2DiMuonDetachedJPsiDecision",
    "Hlt2DiMuonDetachedDecision",
]
tuple3.TupleToolTISTOS.VerboseHlt2 = True
tuple3.TupleToolTISTOS.VerboseHlt1 = True
tuple3.TupleToolTISTOS.VerboseL0 = True
# isol3=tuple3.addTupleTool("TupleToolTrackIsolation/Isolation2")
# isol3.FillAsymmetry = True
# isol3.MinConeAngle=0.6
# isol3.MaxConeAngle=1.4
# isol3.StepSize=0.2
tuple3.Decay = "[B~0 -> ^(D*(2010)- -> ^(D0 -> ^K- ^pi+) ^pi-) ^mu-]CC"
tuple3.Inputs = [SeqYMaker3.outputLocation()]
tuple3.addBranches(
    {
        "Y": "^([B0 -> (D*(2010)+ -> (D~0 -> K+ pi-) pi+) mu+]CC)",
        "Dst_2010_minus": "[B0 -> ^(D*(2010)+ -> (D~0 -> K+ pi-) pi+) mu+]CC",
        "D0": "[B0 -> (D*(2010)+ -> ^(D~0 -> K+ pi-) pi+) mu+]CC",
        "piminus": "[B0 -> (D*(2010)+ -> (D~0 -> K+ pi-) ^pi+) mu+]CC",
        "piminus0": "[B0 -> (D*(2010)+ -> (D~0 -> K+ ^pi-) pi+) mu+]CC",
        "Kplus": "[B0 -> (D*(2010)+ -> (D~0 -> ^K+ pi-) pi+) mu+]CC",
        "muplus": "[B0 -> (D*(2010)+ -> (D~0 -> K+ pi-) pi+) ^mu+]CC",
    }
)
tuple3.muplus.ToolList += ["TupleToolANNPIDTraining"]


if controlModes is False:
    DaVinci().appendToMainSequence(
        [
            scaler,
            MySelection,
            MySelectionWS,
            MySelectionWS2,
            algorithm,
            tuple1,
            tuple2,
            tuple3,
        ]
    )

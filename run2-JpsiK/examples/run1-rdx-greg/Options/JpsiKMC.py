from Gaudi.Configuration import *
from Configurables import DaVinci, FilterDesktop, CombineParticles, OfflineVertexFitter
from PhysSelPython.Wrappers import AutomaticData, Selection, SelectionSequence, DataOnDemand
from Configurables import FilterDesktop
from Configurables import LoKiSvc

from Configurables import DecayTreeTuple, LoKi__Hybrid__TupleTool, TupleToolTrigger, TupleToolDecay, TupleToolTISTOS, MCDecayTreeTuple
#from Configurables import MCDecayTreeTuple


#rootInTes = "/Event/Dimuon"
#from PhysConf.MicroDST import uDstConf
#uDstConf ( rootInTes )

from Configurables import ChargedProtoParticleMaker
 
veloprotos = ChargedProtoParticleMaker("ProtoPMaker")
veloprotos.Inputs = ["Rec/Track/Best"]
veloprotos.Output = "Rec/ProtoP/myProtoPMaker/ProtoParticles"

DaVinci().appendToMainSequence( [ veloprotos ])

from Gaudi.Configuration import *
from Configurables       import ProtoParticleCALOFilter, CombinedParticleMaker,NoPIDsParticleMaker

from CommonParticles.Utils import *

from Configurables import TrackSmearState
smear = TrackSmearState('StateSmear')
DaVinci().appendToMainSequence( [ smear ])

 
algorithm = NoPIDsParticleMaker('StdNoPIDsVeloPions',  Particle = 'pion',  )
algorithm.Input = "Rec/ProtoP/myProtoPMaker/ProtoParticles"
selector = trackSelector ( algorithm , trackTypes = ['Velo'] ) 

locations = updateDoD ( algorithm )
DaVinci().appendToMainSequence( [ algorithm ])



name = "dsttaufake"
#DaVinci().EvtMax = 100
DaVinci().PrintFreq = 10000
DaVinci().TupleFile = name+".root"
DaVinci().Simulation   = True
DaVinci().Lumi   = True


from Configurables import CondDB

#sim09
#DaVinci().DDDBtag = "dddb-20150928"
#DaVinci().CondDBtag = "sim-20160321-2-vc-md100"

#sim08e
DaVinci().DDDBtag = "dddb-20130929"
DaVinci().CondDBtag = "sim-20130522-vc-md100"

#sim08a
#DaVinci().DDDBtag = "Sim08-20130503-1"
#DaVinci().CondDBtag = "Sim08-20130503-1-vc-mu100"


DaVinci().DataType = "2012"




from Configurables import TupleToolTrigger, TupleToolTISTOS
from DecayTreeTuple.Configuration import *


_stdKaons = DataOnDemand(Location = "Phys/StdAllNoPIDsKaons/Particles")

_stdMuons = DataOnDemand(Location = "Phys/StdAllNoPIDsMuons/Particles")

_muonFilter = FilterDesktop('muonFilter', Code = "ALL")
MuonFilterSel = Selection(name = 'MuonFilterSel',
                          Algorithm = _muonFilter,
                          RequiredSelections = [ _stdMuons ])
_kaonFilter = FilterDesktop('kaonFilter', Code = "ALL")
KaonFilterSel = Selection(name = 'KaonFilterSel',
                          Algorithm = _kaonFilter,
                          RequiredSelections = [ _stdKaons ])

_makejpsi = CombineParticles("makejpsi_" + name,
			    Preambulo=["from LoKiPhysMC.decorators import *","from LoKiPhysMC.functions import mcMatch"],
                DecayDescriptor = "J/psi(1S) -> mu+ mu-",
                CombinationCut = "(ADOCACHI2CUT(20, ''))",
			    MotherCut = "(VFASPF(VCHI2) < 16.) & (MFIT)",
			    DaughtersCuts = {
				 "mu+" : "mcMatch( '[mu+]cc' )"}
)
seljpsi = Selection ("Seljpsi",
                     Algorithm = _makejpsi,
                     RequiredSelections = [MuonFilterSel])


_Bu_Kmumu = CombineParticles("BLL_" + name,
			    Preambulo=["from LoKiPhysMC.decorators import *","from LoKiPhysMC.functions import mcMatch"],
                            DecayDescriptor = "[B+ -> J/psi(1S) K+]cc",
                            MotherCut = "mcMatch('[B+ => (J/psi(1S) => mu+ mu- )K+]CC')&(BPVLTIME() > 0.2*ps)",
			    DaughtersCuts = {
#				 "mu+" : "mcMatch( '[mu+]cc' )",
				 "K+" : "mcMatch( '[K+]cc' )"},
                            ReFitPVs = False
				)
Bu_Kmumu = Selection ("Sel"+name,
                     Algorithm = _Bu_Kmumu,
                     RequiredSelections = [KaonFilterSel, seljpsi])

seq = SelectionSequence("Seq"+name, 
                          TopSelection = Bu_Kmumu)



tuple1 = DecayTreeTuple()
#tuple1.TupleName="NotDecayTree"
tuple1.NTupleDir=""

tuple1.UseLoKiDecayFinders = False
ToolList=[
     "TupleToolKinematic"
    , "TupleToolPrimaries"
    , "TupleToolMCTruth"
    , "TupleToolEventInfo"
    , "TupleToolTrackInfo"
    , "TupleToolPid"
    , "TupleToolRecoStats"
]

tuple1.ToolList +=  ToolList


tuple1.addBranches({
      "Bplus" :   "[B+]cc : [B+ -> (J/psi(1S) -> mu+ mu-) K+]cc",          
      "Jpsi" :   "[B+ -> (^J/psi(1S) -> mu+ mu-) K+ ]cc",
      "K" :   "[B+ -> (J/psi(1S) -> mu+ mu-) ^K+]cc",
      "muplus" :   "[B+ -> (J/psi(1S) -> ^mu+ mu-) K+]cc",
      "muminus" :   "[B+ -> (J/psi(1S) -> mu+ ^mu-) K+]cc"
})

from Configurables import TupleToolGeometry

tuple1.addTool(TupleToolGeometry, name="TupleToolGeometry")
tuple1.TupleToolGeometry.Verbose = True
#tuple.TupleToolGeometry.OutputLevel = 1
tuple1.ToolList+=["TupleToolGeometry/TupleToolGeometry"]

from Configurables import TupleToolApplyIsolation
tuple1.Bplus.addTool(TupleToolApplyIsolation, name="TupleToolApplyIsolation")
tuple1.Bplus.TupleToolApplyIsolation.OutputSuffix=""
tuple1.Bplus.TupleToolApplyIsolation.WeightsFile="weightsSoft.xml"
tuple1.Bplus.ToolList+=["TupleToolApplyIsolation/TupleToolApplyIsolation"]



TriggerList =[
'L0HadronDecision',
'L0MuonDecision',
'L0DiMuonDecision',

'Hlt1TrackAllL0Decision',
'Hlt1TrackMuonDecision',

	
#'Hlt2CharmHadD02HH_D02KPiDecision',
'Hlt2Topo2BodyBBDTDecision',
'Hlt2Topo3BodyBBDTDecision',
'Hlt2Topo4BodyBBDTDecision',
'Hlt2TopoMu2BodyBBDTDecision',
'Hlt2TopoMu3BodyBBDTDecision',
'Hlt2TopoMu4BodyBBDTDecision',
'Hlt2DiMuonDecision',
'Hlt2DiMuonJPsiDecision',
'Hlt2DiMuonDetachedDecision',
'Hlt2DiMuonDetachedJPsiDecision',
#'Hlt2XcMuXForTauB2D0KPiMuDecision',
]

tuple1.addTupleTool(TupleToolTISTOS,name="TupleToolTISTOS")
tuple1.ToolList+=["TupleToolTISTOS"]
tuple1.TupleToolTISTOS.VerboseL0 = True
tuple1.TupleToolTISTOS.VerboseHlt1 = True
tuple1.TupleToolTISTOS.VerboseHlt2 = True
tuple1.TupleToolTISTOS.TriggerList = TriggerList

tuple1.Decay = "[B+ -> (^J/psi(1S) -> ^mu+ ^mu-) ^K+]cc"


tuple1.Inputs = [seq.outputLocation()]
DaVinci().appendToMainSequence( [seq, tuple1] ) 
#DaVinci().EvtMax = 100

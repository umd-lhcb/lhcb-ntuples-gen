from Gaudi.Configuration import *
from Configurables import DaVinci, FilterDesktop, CombineParticles, OfflineVertexFitter
from PhysSelPython.Wrappers import AutomaticData, Selection, SelectionSequence, DataOnDemand
from Configurables import FilterDesktop
from Configurables import LoKiSvc

from Configurables import DecayTreeTuple, LoKi__Hybrid__TupleTool, TupleToolTrigger, TupleToolDecay, TupleToolTISTOS, MCDecayTreeTuple


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

algorithm = NoPIDsParticleMaker('StdNoPIDsVeloPions',  Particle = 'pion',  )
algorithm.Input = "Rec/ProtoP/myProtoPMaker/ProtoParticles"
selector = trackSelector ( algorithm , trackTypes = ['Velo'] )

locations = updateDoD ( algorithm )
DaVinci().appendToMainSequence( [ algorithm ])


name = "dsttaufake"
DaVinci().PrintFreq = 10000
DaVinci().Lumi   = True


from Configurables import TupleToolTrigger, TupleToolTISTOS
from DecayTreeTuple.Configuration import *


tuple1 = DecayTreeTuple()
#tuple1.TupleName="NotDecayTree"
tuple1.NTupleDir=""

tuple1.UseLoKiDecayFinders = False
ToolList=[
     "TupleToolKinematic"
    , "TupleToolPrimaries"
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
tuple1.ToolList+=["TupleToolGeometry/TupleToolGeometry"]

#from Configurables import TupleToolL0Calo

#tuple1.K.addTool(TupleToolL0Calo, name="TupleToolL0Calo")
#tuple1.K.ToolList+=["TupleToolL0Calo/TupleToolL0Calo"]




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


tuple1.Inputs = ["/Event/Dimuon/Phys/BetaSBu2JpsiKDetachedLine/Particles/"]
DaVinci().appendToMainSequence( [tuple1] )

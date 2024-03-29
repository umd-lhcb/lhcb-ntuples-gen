# Author: Greg Ciezarek, Yipeng Sun, Manuel Franco Sevilla
# License: BSD 2-clause
# Last Change: Mon Feb 21, 2022 at 06:20 PM -0500
#
# Description: Definitions of selection and reconstruction procedures for run 2
#              J/psi K calibration sample.

#####################
# Configure DaVinci #
#####################

from Configurables import DaVinci

DaVinci().InputType = 'DST'
DaVinci().SkipEvents = 0
DaVinci().PrintFreq = 10000

DaVinci().Lumi = not DaVinci().Simulation

# Debug options
DaVinci().EvtMax = -1


###################################
# Customize DaVinci main sequence #
###################################

from Configurables import ChargedProtoParticleMaker
from Configurables import NoPIDsParticleMaker
from CommonParticles.Utils import trackSelector, updateDoD
from PhysSelPython.Wrappers import AutomaticData, Selection, SelectionSequence, DataOnDemand
from Configurables import DaVinci, FilterDesktop, CombineParticles, OfflineVertexFitter

# Provide required information for VELO pions.
ms_all_protos = ChargedProtoParticleMaker(name='MyProtoPMaker')
ms_all_protos.Inputs = ['Rec/Track/Best']
ms_all_protos.Output = 'Rec/ProtoP/MyProtoPMaker/ProtoParticles'

# NOTE: The name 'StdNoPIDsVeloPions' is hard-coded in the tuple tool, so the
#       name should not be changed.
ms_velo_pions = NoPIDsParticleMaker('StdNoPIDsVeloPions', Particle='pion')
ms_velo_pions.Input = ms_all_protos.Output

trackSelector(ms_velo_pions, trackTypes=['Velo'])
updateDoD(ms_velo_pions)

DaVinci().appendToMainSequence([ms_all_protos, ms_velo_pions])


################
# Common tools #
################
# From https://gitlab.cern.ch/lhcb/Stripping/-/blob/v14r3p3/Phys/StrippingSelections/python/StrippingSelections/StrippingB2CC/StrippingB2JpsiXforBeta_s.py
def createSubSel(OutputList, InputList, Cuts ) :
    '''create a selection using a FilterDesktop'''
    filter = FilterDesktop(OutputList+"FD", Code = Cuts)
    return Selection( OutputList,
                  Algorithm = filter,
                  RequiredSelections = [ InputList ] )

def createCombinationSel(OutputList,
                      DecayDescriptor,
                      DaughterLists,
                      DaughterCuts = {} ,
                      PreVertexCuts = "ALL",
                      PostVertexCuts = "ALL",
                      ReFitPVs = True ) :
    '''create a selection using a ParticleCombiner with a single decay descriptor'''
    combiner = CombineParticles(OutputList+"CP", DecayDescriptor = DecayDescriptor,
                                 DaughtersCuts = DaughterCuts,
                                 MotherCut = PostVertexCuts,
                                 CombinationCut = PreVertexCuts,
                                 ReFitPVs = ReFitPVs)
    return Selection ( OutputList,
                       Algorithm = combiner,
                       RequiredSelections = DaughterLists)
    
def createCombinationsSel(OutputList,
                      DecayDescriptors,
                      DaughterLists,
                      DaughterCuts = {} ,
                      PreVertexCuts = "ALL",
                      PostVertexCuts = "ALL",
                      ReFitPVs = True ) :
    '''For taking in multiple decay descriptors'''
    combiner = CombineParticles( DecayDescriptors = DecayDescriptors,
                             DaughtersCuts = DaughterCuts,
                             MotherCut = PostVertexCuts,
                             CombinationCut = PreVertexCuts,
                             ReFitPVs = ReFitPVs)
    return Selection(OutputList,
                   Algorithm = combiner,
                   RequiredSelections = DaughterLists)


##################
# Define ntuples #
##################

from Configurables import DecayTreeTuple
from DecayTreeTuple.Configuration import *


def really_add_tool(tp, tool_name):
    try:
        tp.ToolList.remove(tool_name)
    except (ValueError, AttributeError):
        pass
    finally:
        tool = tp.addTupleTool(tool_name)
    return tool


def tuple_spec_data(name, sel_seq, template,
                    B_meson='b', weights='./weights_soft.xml',
                    tools=[
                        "TupleToolKinematic",
                        "TupleToolPrimaries",
                        "TupleToolEventInfo",
                        "TupleToolTrackInfo",
                        "TupleToolRecoStats"
                    ],
                    trigger_list=[
                        # L0
                        'L0HadronDecision',
                        'L0MuonDecision',
                        'L0DiMuonDecision',
                        'L0ElectronDecision',
                        # HLT 1
                        'Hlt1TrackMVADecision',
                        'Hlt1TwoTrackMVADecision',
                        'Hlt1TrackMuonDecision',
                        # HLT 2
                        'Hlt2DiMuonDetachedHeavyDecision',
                    ]
                    ):
    tp = DecayTreeTuple(name)
    tp.NTupleDir = ''  # From Greg, might be interesting
    tp.TupleName = name

    tp_input = sel_seq if isinstance(sel_seq, str) else sel_seq.outputLocation()
    tp.Inputs = [tp_input]

    tp.setDescriptorTemplate(template)

    tp.ToolList += tools

    tt_pid = really_add_tool(tp, 'TupleToolPid')
    tt_pid.Verbose = True

    tt_geo = really_add_tool(tp, 'TupleToolGeometry')
    tt_geo.Verbose = True

    tt_tistos = really_add_tool(tp, 'TupleToolTISTOS')
    tt_tistos.Verbose = True
    tt_tistos.TriggerList = trigger_list

    tt_l0_calo = really_add_tool(tp, 'TupleToolL0Calo')
    tt_l0_calo.WhichCalo = "HCAL"
    tt_l0_calo.TriggerClusterLocation = "/Event/Trig/L0/Calo"

    tt_app_iso = getattr(tp, B_meson).addTupleTool('TupleToolApplyIsolation')
    tt_app_iso.WeightsFile = weights

    return tp


def tuple_spec_mc(*args, **kwargs):
    tp = tuple_spec_data(*args, **kwargs)

    # Add truth-info
    tt_mc_truth = really_add_tool(tp, 'TupleToolMCTruth')
    tt_mc_truth.ToolList += ['MCTupleToolHierarchy', 'MCTupleToolKinematic']

    return tp

## For data, simply take events from stripping line
if not DaVinci().Simulation:
    line_strip = 'BetaSBu2JpsiKDetachedLine'
    tes_stripped = '/Event/Dimuon/Phys/{}/Particles/'.format(line_strip)
    tp_Bminus = tuple_spec_data(
        'tree',  # our beloved 'tree'
        tes_stripped,
        '${b}[B+ -> ${j}(J/psi(1S) -> ${amu}mu+ ${mu}mu-) ${k}K+]CC'
    ) 
    DaVinci().appendToMainSequence ([tp_Bminus])
    
## Creating new sequence based on the original stripping because in MC we cannot use
## the stripping line, which contains PID cuts
# From https://gitlab.cern.ch/lhcb/Stripping/-/blob/v14r3p3/Phys/StrippingSelections/python/StrippingSelections/StrippingB2CC/StrippingB2JpsiXforBeta_s.py
else:
    jpsikTag = 'jpsik'
    ## Particle lists with no PID requirements
    _stdKaons = DataOnDemand(Location = "Phys/StdAllNoPIDsKaons/Particles")
    _stdMuons = DataOnDemand(Location = "Phys/StdAllNoPIDsMuons/Particles")

    ## Particle filters
    _muonFilter = FilterDesktop('muonFilter', Code = "ALL")
    MuonFilterSel = Selection(name = 'MuonFilterSel',
                              Algorithm = _muonFilter,
                              RequiredSelections = [ _stdMuons ])
    KaonFilterSel = createSubSel( OutputList = "NoIPKaonsForBetaS" + jpsikTag,
                                  InputList = _stdKaons,
                                  Cuts = "mcMatch('[K+]cc') & (TRCHI2DOF < 5 )"  )


    ## J/psi reco
    _makejpsi = CombineParticles("makejpsi_" + jpsikTag,
			                     Preambulo=["from LoKiPhysMC.decorators import *","from LoKiPhysMC.functions import mcMatch"],
                                 DecayDescriptor = "J/psi(1S) -> mu+ mu-",
                                 CombinationCut = "(ADAMASS('J/psi(1S)') < 80.*MeV) & (ADOCACHI2CUT(20, ''))",
			                     MotherCut = "(VFASPF(VCHI2) < 16.) & (MFIT)",
			                     DaughtersCuts = {
				                     "mu+" : "mcMatch('[mu+]cc') & (PT > 0.5*GeV)"}
                                 )
    seljpsi = Selection ("Seljpsi",
                         Algorithm = _makejpsi,
                         RequiredSelections = [MuonFilterSel])

    ## B -> J/psi reco
    Bu2JpsiK = createCombinationSel(OutputList = "Bu2JpsiK" + jpsikTag,
                                    DecayDescriptor = "[B+ -> J/psi(1S) K+]cc",
                                    DaughterLists = [seljpsi, KaonFilterSel],
                                    DaughterCuts  = {"K+": "(PT > 500.*MeV)" },
                                    PreVertexCuts = "in_range(5050,AM,5550)",
                                    PostVertexCuts = "in_range(5150,M,5450) & (VFASPF(VCHI2PDOF) < 10)")
    
    Bu2JpsiKDetached = createSubSel(InputList = Bu2JpsiK, OutputList = Bu2JpsiK.name() + "Detached" + jpsikTag,
                                    Cuts = "(CHILD('Beauty -> ^J/psi(1S) X', PFUNA(ADAMASS('J/psi(1S)'))) < 80 * MeV) & "\
                                    "(DTF_CTAU(0,True) > 0.2*0.299 ) & "\
                                    "(MINTREE('K+'==ABSID, PT) > 500.*MeV)")



    seq = SelectionSequence("Seq"+jpsikTag, TopSelection = Bu2JpsiKDetached)

    ## Setting up TupleTree
    tp_Bminus = tuple_spec_mc(
        'tree',  # our beloved 'tree'
        seq.outputLocation(),
        '${b}[B+ -> ${j}(J/psi(1S) -> ${amu}mu+ ${mu}mu-) ${k}K+]CC'
    )
    
    ## Add selection & tupling sequences to DaVinci
    DaVinci().appendToMainSequence ([seq, tp_Bminus])

    

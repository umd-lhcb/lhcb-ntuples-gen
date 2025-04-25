from Configurables import DecayTreeTuple, CombineParticles, FilterDesktop
from DecayTreeTuple.Configuration import *
from PhysSelPython.Wrappers import Selection, SelectionSequence
from StandardParticles import StdAllNoPIDsKaons, StdAllNoPIDsPions


from Configurables import DaVinci, TrackSmearState
ms_smear = TrackSmearState('StateSmear')
DaVinci().appendToMainSequence([ms_smear])

DaVinci().InputType = 'DST'
DaVinci().PrintFreq = 10000
DaVinci().SkipEvents = 0
DaVinci().Lumi = not DaVinci().Simulation
DaVinci().EvtMax = -1

mc_match_preambulo = [
    'from LoKiMC.functions import *',
    'from LoKiPhysMC.functions import *'
]

# Define truth-matching requirements cuts
fromSignal = 'MCSELMATCH( MCFROMSIGNAL )'
fromD0     = 'MCSELMATCH( MCINANCESTORS( MCABSID == "D0" ) )'
fromDst    = 'MCSELMATCH( MCINANCESTORS( MCABSID == "D*(2010)+" ) )'
fromPi     = 'MCSELMATCH( MCINANCESTORS( MCABSID == "pi+" ) )'
fromK      = 'MCSELMATCH( MCINANCESTORS( MCABSID == "K+" ) )'
isK        = 'mcMatch("[K+]cc")'
isPi       = 'mcMatch("[pi+]cc")'
isKLoose   = f'({isK} | {fromK})'
isPiLoose  = f'({isPi} | {fromPi})'


#################################################################
# D* -> D0(-> K pi) pi ntuples for study K/pi misid corrections #
#################################################################

filter_k_dst  = FilterDesktop('filter_k_dst',  Code=f'ISLONG & {fromSignal} & {fromDst}', Preambulo=mc_match_preambulo)
filter_pi_dst = FilterDesktop('filter_pi_dst', Code=f'ISLONG & {fromSignal} & {fromDst}', Preambulo=mc_match_preambulo)

filtered_k_dst = Selection('filtered_k_dst', Algorithm=filter_k_dst, RequiredSelections=[StdAllNoPIDsKaons])
filtered_pi_dst = Selection('filtered_pi_dst', Algorithm=filter_pi_dst, RequiredSelections=[StdAllNoPIDsPions])

# define D0 -> K pi decay
nameD0 = 'D02KPi'
D02KPiDauCuts = {'K+':  fromD0,
                 'K-':  fromD0,
                 'pi+': fromD0,
                 'pi-': fromD0
}
D02KPiComCut = 'AALL'
D02KPiMotCuts = 'ALL'
D02KPiCombination = CombineParticles(
    nameD0,
    DecayDescriptor='[D0 -> K- pi+]cc',
    MotherCut=D02KPiMotCuts,
    DaughtersCuts=D02KPiDauCuts,
    CombinationCut=D02KPiComCut)
D02KPiCombination.Preambulo += mc_match_preambulo
D02KPi = Selection(
    'Sel' + nameD0,
    Algorithm=D02KPiCombination,
    RequiredSelections=[filtered_k_dst, filtered_pi_dst])

# define D* -> D0 pi decay
nameDst = 'Dst2D0Pi'
Dst2D0PiDauCuts = {'D0':  'ALL',
                   'D~0': 'ALL',
                   'pi+': 'ALL',
                   'pi-': 'ALL'
                  }
Dst2D0PiComCuts = 'AALL'
Dst2D0PiMotCuts = 'ALL'
Dst2D0PiCombination = CombineParticles(
    nameDst,
    DecayDescriptor='[D*(2010)+ -> D0 pi+]cc',
    MotherCut=Dst2D0PiMotCuts,
    DaughtersCuts=Dst2D0PiDauCuts,
    CombinationCut=Dst2D0PiComCuts)
# Dst2D0PiCombination.Preambulo += mc_match_preambulo
Dst2D0Pi = Selection(
    'Sel' + nameDst,
    Algorithm=Dst2D0PiCombination,
    RequiredSelections=[D02KPi, filtered_pi_dst])

# Define decay tree tuple with uBDT input for K candidate
dtt_k = DecayTreeTuple('Dst_D0Pi_ANNK')
dtt_k.setDescriptorTemplate('${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+)]CC')
dtt_k.Inputs = [Dst2D0Pi.outputLocation()]
dtt_k.addTupleTool('TupleToolTISTOS')
dtt_k.addTupleTool('TupleToolRecoStats')
dtt_k.addTupleTool('TupleToolMCBackgroundInfo')
dtt_k.addTupleTool('TupleToolMCTruth')
dtt_k.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolPID',
    'MCTupleToolHierarchy'
]
dtt_k.k.addTupleTool('TupleToolANNPIDTraining')

# Now define decay tree tuple with uBDT input for pi candidate
dtt_pi = DecayTreeTuple('Dst_D0Pi_ANNPi')
dtt_pi.setDescriptorTemplate('${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+)]CC')
dtt_pi.Inputs = [Dst2D0Pi.outputLocation()]
dtt_pi.addTupleTool('TupleToolTISTOS')
dtt_pi.addTupleTool('TupleToolRecoStats')
dtt_pi.addTupleTool('TupleToolMCBackgroundInfo')
dtt_pi.addTupleTool('TupleToolMCTruth')
dtt_pi.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolPID',
    'MCTupleToolHierarchy'
]
dtt_pi.pi.addTupleTool('TupleToolANNPIDTraining') # This is the only difference between the two tuples

sequenceDstD0Pi_k = SelectionSequence(
    'Seq' + nameDst + 'K', TopSelection=Dst2D0Pi, PostSelectionAlgs=[dtt_k])
sequenceDstD0Pi_pi = SelectionSequence(
    'Seq' + nameDst + 'Pi', TopSelection=Dst2D0Pi, PostSelectionAlgs=[dtt_pi])

DaVinci().UserAlgorithms += [sequenceDstD0Pi_k.sequence(), sequenceDstD0Pi_pi.sequence()]


#########################################
# K/pi ntuples for DiF smearing studies #
#########################################

# Loosely select true Kaons satisfying ISMUON
filter_k_dif  = FilterDesktop('filter_k_dif',  Code=f'ISLONG & ISMUON & {isKLoose}', Preambulo=mc_match_preambulo)

filtered_k_dif = Selection('filtered_k_dif', Algorithm=filter_k_dif, RequiredSelections=[StdAllNoPIDsKaons])

dtt_k_dif = DecayTreeTuple('K_DiF')
dtt_k_dif.setDescriptorTemplate('${k}[K+]CC')
dtt_k_dif.Inputs = [filtered_k_dif.outputLocation()]
dtt_k_dif.addTupleTool('TupleToolMCTruth')
dtt_k_dif.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolPID',
    'MCTupleToolHierarchy'
]
dtt_k_dif.k.addTupleTool('TupleToolANNPIDTraining')

sequenceK_dif = SelectionSequence(
    'SeqKDiF', TopSelection=filtered_k_dif, PostSelectionAlgs=[dtt_k_dif])

# Loosely select true Pions satisfying ISMUON
filter_pi_dif = FilterDesktop('filter_pi_dif', Code=f'ISLONG & ISMUON & {isPiLoose}', Preambulo=mc_match_preambulo)

filtered_pi_dif = Selection('filtered_pi_dif', Algorithm=filter_pi_dif, RequiredSelections=[StdAllNoPIDsPions])

dtt_pi_dif = DecayTreeTuple('Pi_DiF')
dtt_pi_dif.setDescriptorTemplate('${pi}[pi+]CC')
dtt_pi_dif.Inputs = [filtered_pi_dif.outputLocation()]
dtt_pi_dif.addTupleTool('TupleToolMCTruth')
dtt_pi_dif.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolPID',
    'MCTupleToolHierarchy'
]
dtt_pi_dif.pi.addTupleTool('TupleToolANNPIDTraining')

sequencePi_dif = SelectionSequence(
    'SeqPiDiF', TopSelection=filtered_pi_dif, PostSelectionAlgs=[dtt_pi_dif])

DaVinci().UserAlgorithms += [sequenceK_dif.sequence(), sequencePi_dif.sequence()]

from Configurables import DecayTreeTuple, CombineParticles, FilterDesktop, BackgroundCategory
from DecayTreeTuple.Configuration import *
from PhysSelPython.Wrappers import Selection, SelectionSequence
from StandardParticles import StdAllNoPIDsKaons, StdAllNoPIDsPions, StdAllNoPIDsMuons


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
isP        = 'mcMatch("[p+]cc")'
isE        = 'mcMatch("[e-]cc")'
isMu       = 'mcMatch("[mu-]cc")'
isGhost    = f'(NINTREE( {isK} | {isPi} | {isP} | {isE} | {isMu} ) < 1)'
isKLoose   = f'({isK} | {fromK})'
isPiLoose  = f'({isPi} | {fromPi})'


#################################################################
# D* -> D0(-> K pi) pi ntuples for study K/pi misid corrections #
#################################################################

filterK  = FilterDesktop('FilterK',  Code=f'ISLONG & {fromSignal} & {fromDst}', Preambulo=mc_match_preambulo)
filterPi = FilterDesktop('FilterPi', Code=f'ISLONG & {fromSignal} & {fromDst}', Preambulo=mc_match_preambulo)

selectionK  = Selection('SelK',  Algorithm=filterK, RequiredSelections=[StdAllNoPIDsKaons])
selectionPi = Selection('SelPi', Algorithm=filterPi, RequiredSelections=[StdAllNoPIDsPions])

# define D0 -> K pi decay
D02KPiDauCuts = {'K-':  fromD0, 'pi+': fromD0}
D02KPiComCuts = 'AALL'
D02KPiMotCuts = 'ALL'
D02KPiCombination = CombineParticles(
    'CombD02KPi',
    DecayDescriptor='[D0 -> K- pi+]cc',
    MotherCut=D02KPiMotCuts,
    DaughtersCuts=D02KPiDauCuts,
    CombinationCut=D02KPiComCuts)
D02KPiCombination.Preambulo += mc_match_preambulo
D02KPi = Selection(
    'SelD02KPi',
    Algorithm=D02KPiCombination,
    RequiredSelections=[selectionK, selectionPi])

# define D* -> D0 pi decay
Dst2D0PiDauCuts = {'D0':  'ALL', 'pi+': 'ALL'}
Dst2D0PiComCuts = 'AALL'
Dst2D0PiMotCuts = 'ALL'
Dst2D0PiCombination = CombineParticles(
    'CombDst2D0Pi',
    DecayDescriptor='[D*(2010)+ -> D0 pi+]cc',
    MotherCut=Dst2D0PiMotCuts,
    DaughtersCuts=Dst2D0PiDauCuts,
    CombinationCut=Dst2D0PiComCuts)
# Dst2D0PiCombination.Preambulo += mc_match_preambulo
Dst2D0Pi = Selection(
    'SelDst2D0Pi',
    Algorithm=Dst2D0PiCombination,
    RequiredSelections=[D02KPi, selectionPi])

# Define decay tree tuple with uBDT input for K candidate
dttDstK = DecayTreeTuple('TupleDstANNK')
dttDstK.setDescriptorTemplate('${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+)]CC')
dttDstK.Inputs = [Dst2D0Pi.outputLocation()]
dttDstK.addTool(BackgroundCategory)
dttDstK.addTupleTool('TupleToolTISTOS')
dttDstK.addTupleTool('TupleToolRecoStats')
dttDstK.addTupleTool('TupleToolMCBackgroundInfo')
dttDstK.addTupleTool('TupleToolMCTruth')
dttDstK.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolPID',
    'MCTupleToolHierarchy'
]
dttDstK.k.addTupleTool('TupleToolANNPIDTraining')

# Now define decay tree tuple with uBDT input for pi candidate
dttDstPi = DecayTreeTuple('TupleDstANNPi')
dttDstPi.setDescriptorTemplate('${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+)]CC')
dttDstPi.Inputs = [Dst2D0Pi.outputLocation()]
dttDstPi.addTool(BackgroundCategory)
dttDstPi.addTupleTool('TupleToolTISTOS')
dttDstPi.addTupleTool('TupleToolRecoStats')
dttDstPi.addTupleTool('TupleToolMCBackgroundInfo')
dttDstPi.addTupleTool('TupleToolMCTruth')
dttDstPi.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolPID',
    'MCTupleToolHierarchy'
]
dttDstPi.pi.addTupleTool('TupleToolANNPIDTraining') # This is the only difference between the two tuples

sequenceDstK = SelectionSequence(
    'SeqDstK', TopSelection=Dst2D0Pi, PostSelectionAlgs=[dttDstK])
sequenceDstPi = SelectionSequence(
    'SeqDstPi', TopSelection=Dst2D0Pi, PostSelectionAlgs=[dttDstPi])

DaVinci().UserAlgorithms += [sequenceDstK.sequence(), sequenceDstPi.sequence()]


#########################################
# K/pi ntuples for DiF smearing studies #
#########################################

# Loosely select true Kaons satisfying ISMUON
filterKDiF  = FilterDesktop('FilterKDiF',  Code=f'ISLONG & ISMUON & {isKLoose}', Preambulo=mc_match_preambulo)

selectionKDiF = Selection('SelKDiF', Algorithm=filterKDiF, RequiredSelections=[StdAllNoPIDsKaons])

dttKDiF = DecayTreeTuple('TupleKDiF')
dttKDiF.setDescriptorTemplate('${k}[K+]CC')
dttKDiF.Inputs = [selectionKDiF.outputLocation()]
dttKDiF.addTupleTool('TupleToolMCTruth')
dttKDiF.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolPID',
    'MCTupleToolHierarchy'
]
dttKDiF.k.addTupleTool('TupleToolANNPIDTraining')

sequenceK_dif = SelectionSequence(
    'SeqKDiF', TopSelection=selectionKDiF, PostSelectionAlgs=[dttKDiF])

# Loosely select true Pions satisfying ISMUON
filterPiDiF = FilterDesktop('FilterPiDiF', Code=f'ISLONG & ISMUON & {isPiLoose}', Preambulo=mc_match_preambulo)

selectionPiDiF = Selection('SelPiDiF', Algorithm=filterPiDiF, RequiredSelections=[StdAllNoPIDsPions])

dttPiDiF = DecayTreeTuple('TuplePiDiF')
dttPiDiF.setDescriptorTemplate('${pi}[pi+]CC')
dttPiDiF.Inputs = [selectionPiDiF.outputLocation()]
dttPiDiF.addTupleTool('TupleToolMCTruth')
dttPiDiF.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolPID',
    'MCTupleToolHierarchy'
]
dttPiDiF.pi.addTupleTool('TupleToolANNPIDTraining')

sequencePi_dif = SelectionSequence(
    'SeqPiDiF', TopSelection=selectionPiDiF, PostSelectionAlgs=[dttPiDiF])

DaVinci().UserAlgorithms += [sequenceK_dif.sequence(), sequencePi_dif.sequence()]


################
# ghost tracks #
################

# Select true ghost tracks
filterGhost = FilterDesktop('FilterGhost',  Code=f'ISLONG & {isGhost}', Preambulo=mc_match_preambulo)

selectionGhost = Selection('SelGhost', Algorithm=filterGhost, RequiredSelections=[StdAllNoPIDsMuons])

dttGhost = DecayTreeTuple('Ghost')
dttGhost.setDescriptorTemplate('${mu}[mu+]CC')
dttGhost.Inputs = [selectionGhost.outputLocation()]
dttGhost.addTupleTool('TupleToolMCTruth')
dttGhost.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolPID',
    'MCTupleToolHierarchy'
]
dttGhost.mu.addTupleTool('TupleToolANNPIDTraining')

sequence_g = SelectionSequence(
    'SeqGhost', TopSelection=selectionGhost, PostSelectionAlgs=[dttGhost])

DaVinci().UserAlgorithms += [sequence_g.sequence()]

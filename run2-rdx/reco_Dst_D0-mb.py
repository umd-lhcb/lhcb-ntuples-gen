# Author: Lucas Meyer Garcia
# License: BSD 2-clause
#
# Description: Definitions of selection and reconstruction procedures for
#              [D*+ -> D0 pi+]cc samples needed for misid studies in run 2 R(D(*)).
#              Based on run2-rdx/reco_Dst_D0.py.
#


#####################
# Configure DaVinci #
#####################

from Configurables import (DecayTreeTuple, CombineParticles, FilterDesktop,
                           BackgroundCategory, TrackSmearState,
                           TupleToolMCDaughters, DaVinci)
from DecayTreeTuple.Configuration import *
from PhysSelPython.Selections import Selection, SelectionSequence
from StandardParticles import (StdAllNoPIDsKaons, StdAllNoPIDsPions)

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

# Define truth-matching requirements
fromD0     = 'MCSELMATCH( MCINANCESTORS( MCABSID == "D0" ) )'
fromDst    = 'MCSELMATCH( MCINANCESTORS( MCABSID == "D*(2010)+" ) )'
fromPi     = 'MCSELMATCH( MCINANCESTORS( MCABSID == "pi+" ) )'
fromK      = 'MCSELMATCH( MCINANCESTORS( MCABSID == "K+" ) )'
notFromD0  = f'(NINTREE( {fromD0} ) < 1)'
isDst      = 'mcMatch("[D*(2010)+]cc")'
isK        = 'mcMatch("[K+]cc")'
isPi       = 'mcMatch("[pi+]cc")'
isMu       = 'mcMatch("[mu-]cc")'
isKLoose   = f'( {isK}  | ({isMu} & {fromK} ) )'
isPiLoose  = f'( {isPi} | ({isMu} & {fromPi}) )'

# Define trigger list for TupleToolTISTOS
trig_list = [
    'Hlt2PIDD02KPiTagTurboCalibDecision'
]

#################################################################
# D* -> D0(-> K pi) pi ntuples for study K/pi misid corrections #
#################################################################


cutK      = f'ISLONG & (P > 2000) & (PT > 250) & {fromDst} & {fromD0}'
cutPi     = f'ISLONG & (P > 2000) & (PT > 250) & {fromDst} & {fromD0}'
cutPiSoft = f'ISLONG & (P > 1000) & (PT > 100) & {fromDst} & {notFromD0} & {isPiLoose}'

filterK = FilterDesktop(
    'FilterK',
    Code=cutK,
    Preambulo=mc_match_preambulo)
filterPi = FilterDesktop(
    'FilterPi',
    Code=cutPi,
    Preambulo=mc_match_preambulo)
filterPiSoft = FilterDesktop(
    'FilterPiSoft',
    Code=cutPiSoft,
    Preambulo=mc_match_preambulo)

selectionK = Selection('SelK',
                    Algorithm=filterK,
                    RequiredSelections=[StdAllNoPIDsKaons])
selectionPi = Selection('SelPi',
                        Algorithm=filterPi,
                        RequiredSelections=[StdAllNoPIDsPions])
selectionPiSoft = Selection('SelPiSoft',
                            Algorithm=filterPiSoft,
                            RequiredSelections=[StdAllNoPIDsPions])

D02KPiDauCuts = {'K-': 'ALL', 'pi+': 'ALL'}
D02KPiComCuts = 'AHASCHILD( (TRGHOSTPROB < 0.5) & HASMUON & in_range(3000, P, 100000) ) & (AMAXCHILD(PT) > 1000) & (APT > 1500)'
D02KPiMotCuts = 'in_range(1825, M, 1910)'
D02KPiCombination = CombineParticles('CombD02KPi',
                                     DecayDescriptor='[D0 -> K- pi+]cc',
                                     MotherCut=D02KPiMotCuts,
                                     DaughtersCuts=D02KPiDauCuts,
                                     CombinationCut=D02KPiComCuts)
D02KPi = Selection('SelD02KPi',
                   Algorithm=D02KPiCombination,
                   RequiredSelections=[selectionK, selectionPi])

# define D* -> D0 pi decay
Dst2D0PiDauCuts = {'D0': 'ALL', 'pi+': 'ALL'}
Dst2D0PiComCuts = 'AALL'
Dst2D0PiMotCuts = f'{isDst} & in_range(141, M - CHILD(M, 1), 153) & CHILDCUT( (abs(WM("pi+","pi-") - PDGMASS) > 25) & (abs(WM("K+","K-") - PDGMASS) > 25) & (abs(WM("pi+","K-") - PDGMASS) > 25) , 1 )'
Dst2D0PiCombination = CombineParticles(
    'CombDst2D0Pi',
    DecayDescriptor='[D*(2010)+ -> D0 pi+]cc',
    MotherCut=Dst2D0PiMotCuts,
    DaughtersCuts=Dst2D0PiDauCuts,
    CombinationCut=Dst2D0PiComCuts)
Dst2D0Pi = Selection('SelDst2D0Pi',
                     Algorithm=Dst2D0PiCombination,
                     RequiredSelections=[D02KPi, selectionPiSoft])

# Define decay tree tuple with uBDT input for K candidate
dttDstK = DecayTreeTuple('TupleDstANNK')
dttDstK.setDescriptorTemplate(
    '${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+)]CC')
dttDstK.Inputs = [Dst2D0Pi.outputLocation()]
dttDstK.k.addTupleTool('TupleToolPid')
dttDstK.k.TupleToolPid.Verbose = True
dttDstK.addTupleTool('TupleToolTISTOS')
dttDstK.TupleToolTISTOS.Verbose = True
dttDstK.TupleToolTISTOS.TriggerList = trig_list
dttDstK.addTupleTool('TupleToolRecoStats')
dttDstK.addTupleTool('TupleToolTrackInfo')
dttDstK.addTupleTool('TupleToolMCBackgroundInfo')
dttDstK.TupleToolMCBackgroundInfo.addTool(BackgroundCategory)
dttDstK.addTupleTool('TupleToolMCTruth')
dttDstK.TupleToolMCTruth.IP2MCPAssociatorTypes = ['DaVinciSmartAssociator']
dttDstK.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolHierarchyExt'
]
dttDstK.k.addTupleTool('TupleToolANNPIDTraining')

dttDstK.k.addTool(TupleToolMCDaughters, name="TupleToolMCDaughtersK_K")
dttDstK.k.ToolList+=["TupleToolMCDaughters/TupleToolMCDaughtersK_K"]

dttDstK.pi.addTool(TupleToolMCDaughters, name="TupleToolMCDaughtersPi_K")
dttDstK.pi.ToolList+=["TupleToolMCDaughters/TupleToolMCDaughtersPi_K"]

dttDstK.d0.addTool(TupleToolMCDaughters, name="TupleToolMCDaughtersD0_K")
dttDstK.d0.ToolList+=["TupleToolMCDaughters/TupleToolMCDaughtersD0_K"]

dttDstK.dst.addTool(TupleToolMCDaughters, name="TupleToolMCDaughtersDst_K")
dttDstK.dst.ToolList+=["TupleToolMCDaughters/TupleToolMCDaughtersDst_K"]

# Now define decay tree tuple with uBDT input for pi candidate
dttDstPi = DecayTreeTuple('TupleDstANNPi')
dttDstPi.setDescriptorTemplate(
    '${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+)]CC')
dttDstPi.Inputs = [Dst2D0Pi.outputLocation()]
dttDstPi.pi.addTupleTool('TupleToolPid')
dttDstPi.pi.TupleToolPid.Verbose = True
dttDstPi.addTupleTool('TupleToolTISTOS')
dttDstPi.TupleToolTISTOS.Verbose = True
dttDstPi.TupleToolTISTOS.TriggerList = trig_list
dttDstPi.addTupleTool('TupleToolRecoStats')
dttDstPi.addTupleTool('TupleToolTrackInfo')
dttDstPi.addTupleTool('TupleToolMCBackgroundInfo')
dttDstPi.TupleToolMCBackgroundInfo.addTool(BackgroundCategory)
dttDstPi.addTupleTool('TupleToolMCTruth')
# TupleToolMCTruth default behavior is to try DaVinciSmartAssociator and, if not
# succesfull, try again with MCMatchObjP2MCRelator. Since I still don't understand
# MCMatchObjP2MCRelator very well, let's use only DaVinciSmartAssociator.
dttDstPi.TupleToolMCTruth.IP2MCPAssociatorTypes = ['DaVinciSmartAssociator']
dttDstPi.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolHierarchyExt'
]
dttDstPi.pi.addTupleTool('TupleToolANNPIDTraining')

dttDstPi.k.addTool(TupleToolMCDaughters, name="TupleToolMCDaughtersK_Pi")
dttDstPi.k.ToolList+=["TupleToolMCDaughters/TupleToolMCDaughtersK_Pi"]

dttDstPi.pi.addTool(TupleToolMCDaughters, name="TupleToolMCDaughtersPi_Pi")
dttDstPi.pi.ToolList+=["TupleToolMCDaughters/TupleToolMCDaughtersPi_Pi"]

dttDstPi.d0.addTool(TupleToolMCDaughters, name="TupleToolMCDaughtersD0_Pi")
dttDstPi.d0.ToolList+=["TupleToolMCDaughters/TupleToolMCDaughtersD0_Pi"]

dttDstPi.dst.addTool(TupleToolMCDaughters, name="TupleToolMCDaughtersDst_Pi")
dttDstPi.dst.ToolList+=["TupleToolMCDaughters/TupleToolMCDaughtersDst_Pi"]

sequenceDstK = SelectionSequence('SeqDstK',
                                 TopSelection=Dst2D0Pi,
                                 PostSelectionAlgs=[dttDstK])

sequenceDstPi = SelectionSequence('SeqDstPi',
                                  TopSelection=Dst2D0Pi,
                                  PostSelectionAlgs=[dttDstPi])

DaVinci().UserAlgorithms += [sequenceDstK.sequence(), sequenceDstPi.sequence()]

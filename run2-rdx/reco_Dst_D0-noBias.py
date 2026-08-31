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

from Configurables import (DecayTreeTuple, CombineParticles, FilterDesktop, DaVinci, TrackScaleState)
from DecayTreeTuple.Configuration import *
from PhysSelPython.Selections import Selection, SelectionSequence
from StandardParticles import (StdAllNoPIDsKaons, StdAllNoPIDsPions)

DaVinci().InputType = 'DST'
DaVinci().PrintFreq = 10000
DaVinci().SkipEvents = 0
DaVinci().Lumi = not DaVinci().Simulation
DaVinci().EvtMax = -1

ms_scale = TrackScaleState('StateScale')
DaVinci().appendToMainSequence([ms_scale])

# Define trigger list for TupleToolTISTOS
trig_list = [
    'Hlt2PIDD02KPiTagTurboCalibDecision'
]

#################################################################
# D* -> D0(-> K pi) pi ntuples for study K/pi misid corrections #
#################################################################

cutK      = f'ISLONG & (P > 2000.) & (PT > 250.)'
cutPi     = f'ISLONG & (P > 2000.) & (PT > 250.)'
cutPiSoft = f'ISLONG & (P > 1000.) & (PT > 100.)'

filterK = FilterDesktop(
    'FilterK',
    Code=cutK)
filterPi = FilterDesktop(
    'FilterPi',
    Code=cutPi)
filterPiSoft = FilterDesktop(
    'FilterPiSoft',
    Code=cutPiSoft)

selectionK = Selection('SelK',
                    Algorithm=filterK,
                    RequiredSelections=[StdAllNoPIDsKaons])
selectionPi = Selection('SelPi',
                        Algorithm=filterPi,
                        RequiredSelections=[StdAllNoPIDsPions])
selectionPiSoft = Selection('SelPiSoft',
                            Algorithm=filterPiSoft,
                            RequiredSelections=[StdAllNoPIDsPions])

# [D0 -> K+ pi+]cc (WS)
D02KPiDauCuts = {'K+': 'ALL', 'pi+': 'ALL'}
D02KPiComCuts = 'AHASCHILD( (TRGHOSTPROB < 0.5) & HASMUON & in_range(3000, P, 100000) & in_range(1.7, ETA, 5.0) ) & (AMAXCHILD(PT) > 1000) & (APT > 1500) & ACUTDOCA(0.1*mm,\'\')'
D02KPiMotCuts = 'in_range(1735, M, 2000)'

D02KPiCombination = CombineParticles('CombD02KPi',
                                     DecayDescriptor='[D0 -> K+ pi+]cc',
                                     MotherCut=D02KPiMotCuts,
                                     DaughtersCuts=D02KPiDauCuts,
                                     CombinationCut=D02KPiComCuts)
D02KPi = Selection('SelD02KPi',
                   Algorithm=D02KPiCombination,
                   RequiredSelections=[selectionK, selectionPi])

# define D*+ -> D0 pi+ decay
Dst2D0PiDauCuts = {'D0': 'ALL', 'pi+': 'ALL'}
Dst2D0PiComCuts = 'AALL'
Dst2D0PiMotCuts = '(M - CHILD(M, 1)) < 168'
Dst2D0PiMotCuts_WMcut = '((M - CHILD(M, 1)) < 168) & CHILDCUT( (abs(WM("pi+","pi-") - PDGMASS) > 25) & (abs(WM("K+","K-") - PDGMASS) > 25) & (abs(WM("pi+","K-") - PDGMASS) > 25) , 1 )'

Dst2D0PiCombination_SS = CombineParticles(
    'CombDst2D0Pi_SS',
    DecayDescriptor='[D*(2010)+ -> D0 pi+]cc',
    MotherCut=Dst2D0PiMotCuts,
    DaughtersCuts=Dst2D0PiDauCuts,
    CombinationCut=Dst2D0PiComCuts)
Dst2D0Pi_SS = Selection('SelDst2D0Pi_SS',
                     Algorithm=Dst2D0PiCombination_SS,
                     RequiredSelections=[D02KPi, selectionPiSoft])

Dst2D0PiCombination_OS = CombineParticles(
    'CombDst2D0Pi_OS',
    DecayDescriptor='[D*(2010)+ -> D~0 pi+]cc',
    MotherCut=Dst2D0PiMotCuts,
    DaughtersCuts=Dst2D0PiDauCuts,
    CombinationCut=Dst2D0PiComCuts)
Dst2D0Pi_OS = Selection('SelDst2D0Pi_OS',
                     Algorithm=Dst2D0PiCombination_OS,
                     RequiredSelections=[D02KPi, selectionPiSoft])

Dst2D0PiCombination_SS_WMcut = CombineParticles(
    'CombDst2D0Pi_SS_WMcut',
    DecayDescriptor='[D*(2010)+ -> D0 pi+]cc',
    MotherCut=Dst2D0PiMotCuts_WMcut,
    DaughtersCuts=Dst2D0PiDauCuts,
    CombinationCut=Dst2D0PiComCuts)
Dst2D0Pi_SS_WMcut = Selection('SelDst2D0Pi_SS_WMcut',
                     Algorithm=Dst2D0PiCombination_SS_WMcut,
                     RequiredSelections=[D02KPi, selectionPiSoft])

Dst2D0PiCombination_OS_WMcut = CombineParticles(
    'CombDst2D0Pi_OS_WMcut',
    DecayDescriptor='[D*(2010)+ -> D~0 pi+]cc',
    MotherCut=Dst2D0PiMotCuts_WMcut,
    DaughtersCuts=Dst2D0PiDauCuts,
    CombinationCut=Dst2D0PiComCuts)
Dst2D0Pi_OS_WMcut = Selection('SelDst2D0Pi_OS_WMcut',
                     Algorithm=Dst2D0PiCombination_OS_WMcut,
                     RequiredSelections=[D02KPi, selectionPiSoft])

# Define decay tree tuples with uBDT input for K candidate

# SS soft pion
dttDstK_SS = DecayTreeTuple('TupleDstANNK_SS')
dttDstK_SS.setDescriptorTemplate(
    '${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K+ ${pi}pi+) ${spi}pi+)]CC')
dttDstK_SS.Inputs = [Dst2D0Pi_SS.outputLocation()]
dttDstK_SS.k.addTupleTool('TupleToolPid')
dttDstK_SS.k.TupleToolPid.Verbose = True
dttDstK_SS.addTupleTool('TupleToolTISTOS')
dttDstK_SS.TupleToolTISTOS.Verbose = True
dttDstK_SS.TupleToolTISTOS.TriggerList = trig_list
dttDstK_SS.addTupleTool('TupleToolRecoStats')
dttDstK_SS.addTupleTool('TupleToolTrackInfo')
dttDstK_SS.k.addTupleTool('TupleToolANNPIDTraining')

# OS soft pion
dttDstK_OS = DecayTreeTuple('TupleDstANNK_OS')
dttDstK_OS.setDescriptorTemplate(
    '${dst}[(D*(2010)+ -> ${d0}(D~0 -> ${k}K- ${pi}pi-) ${spi}pi+)]CC')
dttDstK_OS.Inputs = [Dst2D0Pi_OS.outputLocation()]
dttDstK_OS.k.addTupleTool('TupleToolPid')
dttDstK_OS.k.TupleToolPid.Verbose = True
dttDstK_OS.addTupleTool('TupleToolTISTOS')
dttDstK_OS.TupleToolTISTOS.Verbose = True
dttDstK_OS.TupleToolTISTOS.TriggerList = trig_list
dttDstK_OS.addTupleTool('TupleToolRecoStats')
dttDstK_OS.addTupleTool('TupleToolTrackInfo')
dttDstK_OS.k.addTupleTool('TupleToolANNPIDTraining')

# SS soft pion with wm cut
dttDstK_SS_WMcut = DecayTreeTuple('TupleDstANNK_SS_WMcut')
dttDstK_SS_WMcut.setDescriptorTemplate(
    '${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K+ ${pi}pi+) ${spi}pi+)]CC')
dttDstK_SS_WMcut.Inputs = [Dst2D0Pi_SS_WMcut.outputLocation()]
dttDstK_SS_WMcut.k.addTupleTool('TupleToolPid')
dttDstK_SS_WMcut.k.TupleToolPid.Verbose = True
dttDstK_SS_WMcut.addTupleTool('TupleToolTISTOS')
dttDstK_SS_WMcut.TupleToolTISTOS.Verbose = True
dttDstK_SS_WMcut.TupleToolTISTOS.TriggerList = trig_list
dttDstK_SS_WMcut.addTupleTool('TupleToolRecoStats')
dttDstK_SS_WMcut.addTupleTool('TupleToolTrackInfo')
dttDstK_SS_WMcut.k.addTupleTool('TupleToolANNPIDTraining')

# OS soft pion with wm cut
dttDstK_OS_WMcut = DecayTreeTuple('TupleDstANNK_OS_WMcut')
dttDstK_OS_WMcut.setDescriptorTemplate(
    '${dst}[(D*(2010)+ -> ${d0}(D~0 -> ${k}K- ${pi}pi-) ${spi}pi+)]CC')
dttDstK_OS_WMcut.Inputs = [Dst2D0Pi_OS_WMcut.outputLocation()]
dttDstK_OS_WMcut.k.addTupleTool('TupleToolPid')
dttDstK_OS_WMcut.k.TupleToolPid.Verbose = True
dttDstK_OS_WMcut.addTupleTool('TupleToolTISTOS')
dttDstK_OS_WMcut.TupleToolTISTOS.Verbose = True
dttDstK_OS_WMcut.TupleToolTISTOS.TriggerList = trig_list
dttDstK_OS_WMcut.addTupleTool('TupleToolRecoStats')
dttDstK_OS_WMcut.addTupleTool('TupleToolTrackInfo')
dttDstK_OS_WMcut.k.addTupleTool('TupleToolANNPIDTraining')

# Now define decay tree tuples with uBDT input for pi candidate

# SS soft pion
dttDstPi_SS = DecayTreeTuple('TupleDstANNPi_SS')
dttDstPi_SS.setDescriptorTemplate(
    '${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K+ ${pi}pi+) ${spi}pi+)]CC')
dttDstPi_SS.Inputs = [Dst2D0Pi_SS.outputLocation()]
dttDstPi_SS.pi.addTupleTool('TupleToolPid')
dttDstPi_SS.pi.TupleToolPid.Verbose = True
dttDstPi_SS.addTupleTool('TupleToolTISTOS')
dttDstPi_SS.TupleToolTISTOS.Verbose = True
dttDstPi_SS.TupleToolTISTOS.TriggerList = trig_list
dttDstPi_SS.addTupleTool('TupleToolRecoStats')
dttDstPi_SS.addTupleTool('TupleToolTrackInfo')
dttDstPi_SS.pi.addTupleTool('TupleToolANNPIDTraining')

# OS soft pion
dttDstPi_OS = DecayTreeTuple('TupleDstANNPi_OS')
dttDstPi_OS.setDescriptorTemplate(
    '${dst}[(D*(2010)+ -> ${d0}(D~0 -> ${k}K- ${pi}pi-) ${spi}pi+)]CC')
dttDstPi_OS.Inputs = [Dst2D0Pi_OS.outputLocation()]
dttDstPi_OS.pi.addTupleTool('TupleToolPid')
dttDstPi_OS.pi.TupleToolPid.Verbose = True
dttDstPi_OS.addTupleTool('TupleToolTISTOS')
dttDstPi_OS.TupleToolTISTOS.Verbose = True
dttDstPi_OS.TupleToolTISTOS.TriggerList = trig_list
dttDstPi_OS.addTupleTool('TupleToolRecoStats')
dttDstPi_OS.addTupleTool('TupleToolTrackInfo')
dttDstPi_OS.pi.addTupleTool('TupleToolANNPIDTraining')

# SS soft pion with wm cut
dttDstPi_SS_WMcut = DecayTreeTuple('TupleDstANNPi_SS_WMcut')
dttDstPi_SS_WMcut.setDescriptorTemplate(
    '${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K+ ${pi}pi+) ${spi}pi+)]CC')
dttDstPi_SS_WMcut.Inputs = [Dst2D0Pi_SS_WMcut.outputLocation()]
dttDstPi_SS_WMcut.pi.addTupleTool('TupleToolPid')
dttDstPi_SS_WMcut.pi.TupleToolPid.Verbose = True
dttDstPi_SS_WMcut.addTupleTool('TupleToolTISTOS')
dttDstPi_SS_WMcut.TupleToolTISTOS.Verbose = True
dttDstPi_SS_WMcut.TupleToolTISTOS.TriggerList = trig_list
dttDstPi_SS_WMcut.addTupleTool('TupleToolRecoStats')
dttDstPi_SS_WMcut.addTupleTool('TupleToolTrackInfo')
dttDstPi_SS_WMcut.pi.addTupleTool('TupleToolANNPIDTraining')

# OS soft pion with wm cut
dttDstPi_OS_WMcut = DecayTreeTuple('TupleDstANNPi_OS_WMcut')
dttDstPi_OS_WMcut.setDescriptorTemplate(
    '${dst}[(D*(2010)+ -> ${d0}(D~0 -> ${k}K- ${pi}pi-) ${spi}pi+)]CC')
dttDstPi_OS_WMcut.Inputs = [Dst2D0Pi_OS_WMcut.outputLocation()]
dttDstPi_OS_WMcut.pi.addTupleTool('TupleToolPid')
dttDstPi_OS_WMcut.pi.TupleToolPid.Verbose = True
dttDstPi_OS_WMcut.addTupleTool('TupleToolTISTOS')
dttDstPi_OS_WMcut.TupleToolTISTOS.Verbose = True
dttDstPi_OS_WMcut.TupleToolTISTOS.TriggerList = trig_list
dttDstPi_OS_WMcut.addTupleTool('TupleToolRecoStats')
dttDstPi_OS_WMcut.addTupleTool('TupleToolTrackInfo')
dttDstPi_OS_WMcut.pi.addTupleTool('TupleToolANNPIDTraining')


sequenceDstK_SS = SelectionSequence('SeqDstK_SS',
                                 TopSelection=Dst2D0Pi_SS,
                                 PostSelectionAlgs=[dttDstK_SS])

sequenceDstK_OS = SelectionSequence('SeqDstK_OS',
                                 TopSelection=Dst2D0Pi_OS,
                                 PostSelectionAlgs=[dttDstK_OS])

sequenceDstK_SS_WMcut = SelectionSequence('SeqDstK_SS_WMcut',
                                 TopSelection=Dst2D0Pi_SS_WMcut,
                                 PostSelectionAlgs=[dttDstK_SS_WMcut])

sequenceDstK_OS_WMcut = SelectionSequence('SeqDstK_OS_WMcut',
                                 TopSelection=Dst2D0Pi_OS_WMcut,
                                 PostSelectionAlgs=[dttDstK_OS_WMcut])

sequenceDstPi_SS = SelectionSequence('SeqDstPi_SS',
                                  TopSelection=Dst2D0Pi_SS,
                                  PostSelectionAlgs=[dttDstPi_SS])

sequenceDstPi_OS = SelectionSequence('SeqDstPi_OS',
                                  TopSelection=Dst2D0Pi_OS,
                                  PostSelectionAlgs=[dttDstPi_OS])

sequenceDstPi_SS_WMcut = SelectionSequence('SeqDstPi_SS_WMcut',
                                  TopSelection=Dst2D0Pi_SS_WMcut,
                                  PostSelectionAlgs=[dttDstPi_SS_WMcut])

sequenceDstPi_OS_WMcut = SelectionSequence('SeqDstPi_OS_WMcut',
                                  TopSelection=Dst2D0Pi_OS_WMcut,
                                  PostSelectionAlgs=[dttDstPi_OS_WMcut])

DaVinci().UserAlgorithms += [sequenceDstK_SS.sequence(), sequenceDstK_OS.sequence(), sequenceDstK_SS_WMcut.sequence(), sequenceDstK_OS_WMcut.sequence(),
                             sequenceDstPi_SS.sequence(), sequenceDstPi_OS.sequence(), sequenceDstPi_SS_WMcut.sequence(), sequenceDstPi_OS_WMcut.sequence()]

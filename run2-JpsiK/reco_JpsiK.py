# Author: Greg Ciezarek, Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Jan 05, 2022 at 10:01 PM +0100
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


#######################
# Particle references #
#######################

line_strip = 'BetaSBu2JpsiKDetachedLine'
tes_stripped = '/Event/Dimuon/Phys/{}/Particles/'.format(line_strip)


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
                        # HLT 1
                        'Hlt1TrackAllL0Decision',
                        'Hlt1TrackMuonDecision',
                        # HLT 2
                        'Hlt2Topo2BodyBBDTDecision',
                        'Hlt2Topo3BodyBBDTDecision',
                        'Hlt2Topo4BodyBBDTDecision',
                        'Hlt2TopoMu2BodyBBDTDecision',
                        'Hlt2TopoMu3BodyBBDTDecision',
                        'Hlt2TopoMu4BodyBBDTDecision',
                        'Hlt2DiMuonDecision',
                        'Hlt2DiMuonJPsiDecision',
                        'Hlt2DiMuonDetachedDecision',
                        'Hlt2DiMuonDetachedJPsiDecision'
                    ]
                    ):
    tp = DecayTreeTuple(name)

    tp_input = sel_seq if isinstance(sel_seq, str) else sel_seq.outputLocation()
    tp.Inputs = [tp_input]

    tp.setDescriptorTemplate(template)
    # tp.NTupleDir=''  # From Greg, might be interesting
    # tp.TupleName='NotDecayTree'

    tp.ToolList += tools

    tt_pid = really_add_tool(tp, 'TupleToolPid')
    tt_pid.Verbose = True

    tt_geo = really_add_tool(tp, 'TupleToolGeometry')
    tt_geo.Verbose = True

    tt_tistos = really_add_tool(tp, 'TupleToolTISTOS')
    tt_tistos.Verbose = True
    tt_tistos.TriggerList = trigger_list

    tt_app_iso = getattr(tp, B_meson).addTupleTool('TupleToolApplyIsolation')
    tt_app_iso.WeightsFile = weights
    # tt_app_iso.OutputSuffix = ''

    return tp


if not DaVinci().Simulation:
    tuple_spec = tuple_spec_data
else:
    tuple_spec = tuple_spec_data


# B- ###########################################################################
tp_Bminus = tuple_spec(
    'TupleBminus',
    tes_stripped,
    '${b}[B+ -> ${j}(J/psi(1S) -> ${amu}mu+ ${mu}mu-) ${k}K+]CC'
)


################################################
# Add selection & tupling sequences to DaVinci #
################################################

DaVinci().UserAlgorithms += [tp_Bminus]
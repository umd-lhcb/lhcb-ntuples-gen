#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 06:34 PM +0800

import uproot
import sys
import yaml

from pyTuplingUtils.io import yaml_gen
from pyTuplingUtils.utils import extract_uid
from pyTuplingUtils.cutflow import CutflowGen, CutflowRule as Rule


ALIASES = {
    'SeqMyB0': 'Total events',
    'StrippedBCands': r'Stripped $D^0 \mu^-$',
    'SelMyD0': r'$D^0 \rightarrow K^- \pi^+$ (tigter $K \pi$)',
    'SelMyDst': r'$D^{*+} \rightarrow D^0 \pi^+$',
    'SelMyB0': r'$\bar{B}^0 \rightarrow D^{*+} \mu^-$',
    'SelMyRefitB02DstMu': r'Refit $\bar{B}^0$ decay tree',
}


CUTFLOWS = [
    Rule('muplus_L0Global_TIS & (Y_L0Global_TIS | Dst_2010_minus_L0HadronDecision_TOS)', 'L0'),
    Rule('Kplus_Hlt1TrackAllL0Decision_TOS | piminus0_Hlt1TrackAllL0Decision_TOS', 'Hlt1'),
    Rule('D0_Hlt2CharmHadD02HH_D02KPiDecision_TOS', 'Hlt2'),
    Rule('muplus_isMuon & muplus_PIDmu > 2', r'$\mu$ PID'),
    Rule('Y_ISOLATION_BDT < 0.15', r'$\text{IsoBDT}_{\Upsilon(\text{4s})} < 0.15$'),
    Rule('Y_M < 5280', r'$m_{\Upsilon(\text{4s})} < 5280$'),
]


if __name__ == '__main__':
    ntp_path, input_yml, output_yml = sys.argv[1:]
    tree = 'TupleB0/DecayTree'

    _, _, total_size, uniq_size, _ = extract_uid(uproot.open(ntp_path), tree)

    with open(input_yml) as f:
        result = yaml.safe_load(f)

    for cut, val in result.items():
        if cut in ALIASES:
            val['name'] = ALIASES[cut]
        if val['output'] is None:
            val['output'] = uniq_size

    result_addon = CutflowGen(ntp_path, tree, CUTFLOWS, total_size).do()
    result.update(result_addon)

    with open(output_yml, 'w') as f:
        f.write(yaml_gen(result))

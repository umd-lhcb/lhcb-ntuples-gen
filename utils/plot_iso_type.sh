#!/bin/bash

OUTPUT_DIR="../gen/"
NTP_DV36="../2012-b2D0MuXB2DMuNuForTauMuLine/sample/BCands_Dst-data-2012-mag_down-davinci_v36r1p2-subset.root"

root -q -l 'make_histo_float.cxx(
    "'"${NTP_DV36}"'", "'"${OUTPUT_DIR}"'",
    "_dv36r1",
    "TupleY/DecayTree", "Y_ISOLATION_Type", 40, 0, 5)'

#!/bin/bash

FILE1="../2012-b2D0MuXB2DMuNuForTauMuLine/sample/BCands_Dst-data-2012-mag_down-davinci_v42r8p1-subset.root"
FILE2="../2012-b2D0MuXB2DMuNuForTauMuLine/sample/BCands_Dst-data-2012-mag_down.root"

root -q -l 'extract_uid.cxx("'"${FILE1}"'", "'"${FILE2}"'",
    "uid.root", "TupleY/DecayTree", "YCands/DecayTree")'

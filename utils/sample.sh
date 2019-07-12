#!/bin/bash

root -q -l 'extract_uid.C(
    "../2012-b2D0MuXB2DMuNuForTauMuLine/data/sample/BCands_Dst-data-2012-mag_down-davinci_v42r8p1-subset.root",
    "../2012-b2D0MuXB2DMuNuForTauMuLine/data/sample/BCands_Dst-data-2012-mag_down.root",
    "uid.root", "TupleY/DecayTree", "YCands/DecayTree")'

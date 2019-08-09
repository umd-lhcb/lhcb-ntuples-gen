#!/bin/bash

root -q -l 'ntuple_validate.cxx(
	"../2012-b2D0MuXB2DMuNuForTauMuLine/data/sample/BCands_Dst-data-2012-mag_down-davinci_v42r8p1-subset.root",
	"../2012-b2D0MuXB2DMuNuForTauMuLine/data/sample/BCands_Dst-data-2012-mag_down-davinci_v36r1p2-subset.root",
	"TupleY/DecayTree", "TupleY/DecayTree", "D0_P", "D0_P",
	"davinci_compare")'

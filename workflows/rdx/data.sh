#!/usr/bin/env bash
# Author: Yipeng Sun
# Last Change: Sat Jun 26, 2021 at 05:22 PM +0200

INPUT_NTP=$1
INPUT_YML=$2
OUTPUT_SUFFIX=$3

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
CPP_TMPL=$DIR/../../postprocess/cpp_templates/rdx.cpp
MU_BDT_WEIGHT=$DIR/../../run2-rdx/weights_run2_no_cut_ubdt.xml

HEADER_DIR=$DIR/../../include
COMPILER=$(root-config --cxx)
CXX_FLAGS=$(root-config --cflags)
LINK_FLAGS=$(root-config --libs)
ADDF_FLAGS="-I${HEADER_DIR}"

cpp_gen() {
    babymaker -i ${INPUT_YML} -o baby.cpp -n ${INPUT_NTP} -t ${CPP_TMPL} -f $@
}

cpp_compile() {
    ${COMPILER} ${CXX_FLAGS} ${ADDF_FLAGS} -o baby baby.cpp ${LINK_FLAGS}
}

add_mu_bdt() {
    addUBDTBranch ${INPUT_NTP} "mu_isMuonTight" ${MU_BDT_WEIGHT} mu_bdt.root $@
    rm -rf ./weights  # This folder is generated by UBDT adder for unknown reason
}

add_mu_bdt "TupleB0/DecayTree" "TupleBminus/DecayTree"
cpp_gen mu_bdt.root
cpp_compile
./baby "--${OUTPUT_SUFFIX}"
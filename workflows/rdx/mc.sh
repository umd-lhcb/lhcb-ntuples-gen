#!/usr/bin/env bash
# Author: Yipeng Sun
# Last Change: Mon Sep 13, 2021 at 10:52 PM +0200

INPUT_NTP=$1
INPUT_YML=$2
OUTPUT_SUFFIX=$3

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
CPP_TMPL=$DIR/../../postprocess/cpp_templates/rdx.cpp

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

aux_name() {
    DIRNAME=$(dirname ${INPUT_NTP})
    FILENAME=$(basename ${INPUT_NTP} .root)
    echo "${DIRNAME}/${FILENAME}__aux_mu_bdt.root"
}

hammer_reweight() {
    ReweightRDX ${INPUT_NTP} ham_wt.root TupleBminus/DecayTree run2
    ReweightRDX ${INPUT_NTP} ham_wt.root TupleB0/DecayTree run2
}

hammer_reweight
cpp_gen ham_wt.root
cpp_compile
./baby "--${OUTPUT_SUFFIX}"

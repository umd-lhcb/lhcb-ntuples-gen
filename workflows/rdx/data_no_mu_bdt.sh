#!/usr/bin/env bash
# Author: Yipeng Sun
# Last Change: Sun Jun 27, 2021 at 12:53 AM +0200

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
    babymaker -i ${INPUT_YML} -o baby.cpp -n ${INPUT_NTP} -t ${CPP_TMPL}
}

cpp_compile() {
    ${COMPILER} ${CXX_FLAGS} ${ADDF_FLAGS} -o baby baby.cpp ${LINK_FLAGS}
}

cpp_gen
cpp_compile
./baby "--${OUTPUT_SUFFIX}"

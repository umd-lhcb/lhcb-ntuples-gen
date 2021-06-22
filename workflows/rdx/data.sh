#!/usr/bin/env bash
# Author: Yipeng Sun
# Last Change: Tue Jun 22, 2021 at 02:59 AM +0200

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
CPP_TMPL=$DIR/../../postprocess/cpp_templates/rdx.cpp

HEADER_DIR=$DIR/../../include
COMPILER=$(root-config --cxx)
CXX_FLAGS=$(root-config --cflags)
LINK_FLAGS=$(root-config --libs)
ADDF_FLAGS="-I${HEADER_DIR}"

INPUT_NTP=$1
INPUT_YML=$2

cpp_gen() {
    babymaker -i ${INPUT_YML} -o baby.cpp -n ${INPUT_NTP} -t ${CPP_TMPL}
}

cpp_compile() {
    ${COMPILER} ${CXX_FLAGS} ${ADDF_FLAGS} -o $2 $1 ${LINK_FLAGS}
}

cpp_gen
cpp_compile baby.cpp baby

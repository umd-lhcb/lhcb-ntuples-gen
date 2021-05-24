#!/usr/bin/env bash
# Author: Yipeng Sun
# Last Change: Mon May 24, 2021 at 05:47 PM +0200

NTPS=$1
INPUT_YML=$2
MODE=$3

# Generate the cutflow YML
cutflow_output_yml_gen.py ${NTPS} \
    -i ${INPUT_YML} -o cutflow.yml \
    -m ${MODE}

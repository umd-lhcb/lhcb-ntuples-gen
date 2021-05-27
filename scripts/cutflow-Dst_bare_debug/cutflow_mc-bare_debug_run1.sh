#!/usr/bin/env bash
# NOTE: This is just an example! To generate all bare component cutflows, go to
#       project root, then 'make rdx-cutflow'

RUN1_NTP=../../run1-rdx/cutflow_mc-bare.root
RUN1_LOG=../../run1-rdx/logs/Dst_D0-21_05_26-cutflow_mc-bare.log

# Log
../../tools/davinci_log_parser.py ./run1_debug_raw.yml $RUN1_LOG
head -n 90 ./run1_debug_raw.yml > ./run1_debug.yml

# Cutflow yml
../cutflow_output_yml_gen.py ${RUN1_NTP} \
    -i ./run1_debug.yml -o ./cutflow_run1_debug.yml \
    -m run1-Dst-bare

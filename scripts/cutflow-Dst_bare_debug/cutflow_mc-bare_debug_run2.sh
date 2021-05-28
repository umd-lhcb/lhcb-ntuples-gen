#!/usr/bin/env bash
# NOTE: This is just an example! To generate all bare component cutflows, go to
#       project root, then 'make rdx-cutflow'

RUN2_NTP=../../run2-rdx/samples/Dst_D0--21_05_28--cutflow_mc--cocktail--2016--md--dv45-subset-bare.root
RUN2_LOG=../../run2-rdx/logs/Dst_D0-21_05_28-cutflow_mc-bare.log

# Log
../../tools/davinci_log_parser.py ./run2_debug.yml $RUN2_LOG

# Cutflow yml
../cutflow_output_yml_gen.py ${RUN2_NTP} \
    -i ./run2_debug.yml -o ./cutflow_run2_debug.yml \
    -m run2-Dst-bare

#!/usr/bin/env bash
# NOTE: This is just an example! To generate all bare component cutflows, go to
#       project root, then 'make rdx-cutflow'

RUN1_NTP=../../run1-rdx/samples/Dst_D0--21_05_26--cutflow_mc--cocktail--2011--md--dv45-subset-bare.root
RUN1_LOG=../../run1-rdx/logs/Dst_D0-21_05_26-cutflow_mc-bare.log

RUN2_NTP=../../run2-rdx/samples/Dst_D0--21_05_28--cutflow_mc--cocktail--2016--md--dv45-subset-bare.root
RUN2_LOG=../../run2-rdx/logs/Dst_D0-21_05_28-cutflow_mc-bare.log

# Log
../../tools/davinci_log_parser.py ./run1_debug.yml $RUN1_LOG
../../tools/davinci_log_parser.py ./run2_debug.yml $RUN2_LOG

# Cutflow yml
../cutflow_output_yml_gen.py ${RUN1_NTP} \
    -i ./run1_debug.yml -o ./cutflow_run1_debug.yml \
    -m run1-Dst-bare
../cutflow_output_yml_gen.py ${RUN2_NTP} \
    -i ./run2_debug.yml -o ./cutflow_run2_debug.yml \
    -m run2-Dst-bare

# Table
../cutflow_gen.py -o ./cutflow_run1_debug.yml -t ./cutflow_run2_debug.yml \
    -n > ./cutflow_debug.csv
cat ./cutflow_debug.csv | tabgen.py -f github > ./cutflow_debug.md

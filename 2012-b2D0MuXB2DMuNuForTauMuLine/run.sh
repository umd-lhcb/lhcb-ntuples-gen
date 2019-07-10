#!/bin/bash

case $1 in
    'data')
        run gaudirun.py ./ntuple_options_base.py
        ;;
    'mc')
        run gaudirun.py ./ntuple_options_mc_conf.py ./ntuple_options_base.py
        ;;
    *)
        echo "Unknown argument: ${1}"
        ;;
esac

#!/bin/bash

case $1 in
    'Dst')
        run gaudirun.py ./reco_$1_conf-$2.py ./reco_$1.py
        ;;
    *)
        echo "Unknown argument: ${1}"
        ;;
esac

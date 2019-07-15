#!/bin/bash

case $1 in
    'Dst')
        run gaudirun.py ./conds/cond_$1-$2.py ./reco_$1.py
        ;;
    *)
        echo "Unknown argument: ${1}"
        ;;
esac

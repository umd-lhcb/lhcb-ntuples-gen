#!/bin/bash

export CMTCONFIG=x86_64-slc6-gcc48-opt

case $3 in
    debug)
        lb-run DaVinci/v36r1p2 gaudirun.py $2 $1 \
            --option="from Configurables import DaVinci; DaVinci().EvtMax = 5000"
        ;;

    *)
        lb-run DaVinci/v36r1p2 gaudirun.py $2 $1
        ;;
esac

#!/bin/bash

case $3 in
    debug)
        run gaudirun.py $1 ./reco_Dst_D0.py \
            --option="from Configurables import DaVinci; DaVinci().EvtMax = 5000"
        ;;

    *)
        run gaudirun.py $1 ./reco_Dst_D0.py
        ;;
esac

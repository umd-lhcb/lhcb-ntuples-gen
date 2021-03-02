#!/bin/bash

case $2 in
    debug)
        ../DaVinciDev_v45r6/run gaudirun.py $1 ./reco_Dst_D0.py \
            --option="from Configurables import DaVinci; DaVinci().EvtMax = 5000"
        ;;

    *)
        run gaudirun.py $1 ./reco_Dst_D0.py
        ;;
esac

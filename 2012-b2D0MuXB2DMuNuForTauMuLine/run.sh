#!/bin/bash

case $3 in
    debug)
        run gaudirun.py ./conds/cond-$2.py ./reco_$1.py \
            --option="from Configurables import DaVinci; DaVinci().EvtMax = 10"
        ;;

    *)
        run gaudirun.py ./conds/cond-$2.py ./reco_$1.py
        ;;
esac

#!/bin/bash

case $3 in
    debug)
        run gaudirun.py $2 $1 \
            --option="from Configurables import DaVinci; DaVinci().EvtMax = 5000"
        ;;

    *)
        run gaudirun.py $2 $1
        ;;
esac

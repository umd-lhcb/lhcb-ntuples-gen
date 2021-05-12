#!/bin/sh
# NOTE: Don't forget to run lhcb-proxy-init

# 2011 MD
lb-dirac dirac-bookkeeping-get-stats --BK "/LHCb/Collision11/Beam3500GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping21r1/90000000/SEMILEPTONIC.DST"

# 2016 MD
lb-dirac dirac-bookkeeping-get-stats --BK "/LHCb/Collision16/Beam6500GeV-VeloClosed-MagDown/Real Data/Reco16/Stripping28r1/90000000/SEMILEPTONIC.DST"

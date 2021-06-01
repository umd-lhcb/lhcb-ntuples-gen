#!/usr/bin/env bash
# NOTE: Don't forget to run lhcb-proxy-init

# Run 1
# 2011
lb-dirac dirac-bookkeeping-get-stats --BK '/LHCb/Collision11/Beam3500GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping21r1/90000000/SEMILEPTONIC.DST'
lb-dirac dirac-bookkeeping-get-stats --BK '/LHCb/Collision11/Beam3500GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping21r1/90000000/SEMILEPTONIC.DST'

# 2012
lb-dirac dirac-bookkeeping-get-stats --BK LHCb/Collision12/Beam4000GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping21/90000000/SEMILEPTONIC.DST'
lb-dirac dirac-bookkeeping-get-stats --BK LHCb/Collision12/Beam4000GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping21/90000000/SEMILEPTONIC.DST'

# Run 2
# 2015
lb-dirac dirac-bookkeeping-get-stats --BK 'LHCb/Collision15/Beam6500GeV-VeloClosed-MagDown/Real Data/Reco15a/Stripping24r2/90000000/SEMILEPTONIC.DST'
lb-dirac dirac-bookkeeping-get-stats --BK 'LHCb/Collision15/Beam6500GeV-VeloClosed-MagUp/Real Data/Reco15a/Stripping24r2/90000000/SEMILEPTONIC.DST'

# 2016
lb-dirac dirac-bookkeeping-get-stats --BK "/LHCb/Collision16/Beam6500GeV-VeloClosed-MagDown/Real Data/Reco16/Stripping28r2/90000000/SEMILEPTONIC.DST"
lb-dirac dirac-bookkeeping-get-stats --BK "/LHCb/Collision16/Beam6500GeV-VeloClosed-MagUp/Real Data/Reco16/Stripping28r2/90000000/SEMILEPTONIC.DST"

# 2017
lb-dirac dirac-bookkeeping-get-stats --BK 'LHCb/Collision17/Beam6500GeV-VeloClosed-MagUp/Real Data/Reco17/Stripping29r2/90000000/SEMILEPTONIC.DST'
lb-dirac dirac-bookkeeping-get-stats --BK 'LHCb/Collision17/Beam6500GeV-VeloClosed-MagDown/Real Data/Reco17/Stripping29r2/90000000/SEMILEPTONIC.DST'

# 2018
lb-dirac dirac-bookkeeping-get-stats --BK 'LHCb/Collision18/Beam6500GeV-VeloClosed-MagUp/Real Data/Reco18/Stripping34/90000000/SEMILEPTONIC.DST'
lb-dirac dirac-bookkeeping-get-stats --BK 'LHCb/Collision18/Beam6500GeV-VeloClosed-Magdown/Real Data/Reco18/Stripping34/90000000/SEMILEPTONIC.DST'

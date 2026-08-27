# Producing PID weights for $J/\psi K$ MC

1. On lxplus, execute `run2-JpsiK_withIsMuon.sh` to produce the full $K$ and $\mu$ PID efficiencies with the binning scheme set in `binning.json`.
For the $\mu$, this includes both the isMuon and DLLmu cuts.
The root histograms with the raw PIDCalib results will be located in `root-run2-JpsiK_withIsMuon-tmp`, while the shifted efficiencies will be located in `root-run2-JpsiK_withIsMuon-tmp-shifted`.
You should then move these efficiencies into `root-run2-JpsiK_withIsMuon` and `root-run2-JpsiK_withIsMuon-shifted`, respectively.

2. Still on lxplus, execute `run2-JpsiK_DLLmu_conditional_on_isMuon.sh` to produce the conditional $\mu$ PID efficiencies (DLLmu assuming isMuon is true) with the binning scheme set in `binning.json`.
The root histograms with the raw PIDCalib results will be located in `root-run2-JpsiK_DLLmu_conditional_on_isMuon-tmp`, while the shifted efficiencies will be located in `root-run2-JpsiK_DLLmu_conditional_on_isMuon-tmp-shifted`.
You should then move these efficiencies into `root-run2-JpsiK_DLLmu_conditional_on_isMuon` and `root-run2-JpsiK_DLLmu_conditional_on_isMuon-shifted`, respectively.

**Note: Currently, we apply isMuon as a cut in the $J/\psi K$ MC and rely on the conditional $\mu$ PID efficiencies from 2 instead of those from 1.**

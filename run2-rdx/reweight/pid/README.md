# Producing PID weights for RDx MC

1. On lxplus, execute `run2-rdx_oldcut.sh` to produce the $K$ and $\pi$ PID efficiencies with the binning scheme set in `binning.json`, corresponding to the PID cuts applied on the $D^0$ daughters.
The root histograms with the raw PIDCalib results will be located in `root-run2-rdx_oldcut-tmp`, while the shifted efficiencies will be located in `root-run2-rdx_oldcut-tmp-shifted`.
You should then move these efficiencies into `KPiPID-<year>` and `KPiPID-<year>-shifted`, respectively.

2. Still on lxplus, execute `run2-rdx_iso.sh` to produce the PID efficiencies corresponding to the PID cuts applied on the additional tracks with the binning scheme set in `binning_iso.json`.
The root histograms with the raw PIDCalib results will be located in `root-run2-rdx_iso-tmp`, while the shifted efficiencies will be located in `root-run2-rdx_iso-tmp-shifted`.
You should then move these efficiencies into `KPiPMuE_IsoTrackSkimPID-<year>` and `KPiPMuE_IsoTrackSkimPID-<year>-shifted`, respectively.

3. On **glacier**, use [this script](https://github.com/umd-lhcb/pidcalib2/blob/master/efficiency_gen/rdx-run2-ubdt.sh) (located in our pidcalib2 fork) to produce the $\mu$ PID efficiencies corresponding to the PID cuts applied on the $\mu$ candidate with the binning scheme set in `binning.json`.
The root histograms with the raw PIDCalib results will be located in `root-run2-rdx_mu_ubdt-tmp`.

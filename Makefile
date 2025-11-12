# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Mar 15, 2024 at 12:24 PM -0400

VPATH := postprocess:test:scripts:ntuples
VPATH := run1-rdx/cutflow:run2-rdx/cutflow:$(VPATH)

# System env
OS  := $(shell uname)
PWD := $(shell pwd)
# In-house Python libraries
LIB_PY := $(wildcard lib/python/*)
DAVINCI_VERSION = DaVinci-v45r6-SL

TIMESTAMP := $(shell date +"%y_%m_%d_%H_%M")

.PHONY: all clean history tagdate install-dep

clean:
	@rm -rf ./gen/*

history:
	@git tag -l -n99

tagdate:
	@git log --date-order --tags --simplify-by-decoration --pretty='format:%C(green)%ad %C(red)%h %C(reset)%D' --date=short

# This is unused. Kept for archival purposes
install-dep-pip:
	@echo "Installing third-party Python libraries..."
	@pip install --no-deps -r ./run2-JpsiK/requirements.txt

install-dep:
	@echo "Installing in-house Python libraries..."
	@for p in $(LIB_PY); do \
			cd $(PWD)/$$p; \
			pip install .; \
		done;


#####################
# Run docker images #
#####################

.PHONY: docker-dv

ifeq ($(OS),Darwin)
DV_CMD = "docker run --rm -it -v $(PWD):/data -e UID=$$(id -u) -e GID=$$(id -g) --net=host umdlhcb/lhcb-stack-cc7:${DAVINCI_VERSION}"
else
DV_CMD = "docker run --rm -it -v $(PWD):/data -v $$HOME/.Xauthority:/home/physicist/.Xauthority -e DISPLAY -e UID=$$(id -u) -e GID=$$(id -g) --net=host umdlhcb/lhcb-stack-cc7:${DAVINCI_VERSION}"
endif

docker-dv:
	@eval $(DV_CMD)


#########
# Tests #
#########

.PHONY: test-naming-conv

# Test if specific files follow naming conventions (actually... we changed this, and it isn't assumed anywhere to my knowledge, so I'm going to override)
test-naming-conv:
	workflows/validate_filename.py override


#################################
# RJpsi run 2 ntuple generation #
#################################

RJpsi-ntuple-run2-mc_ghost:
	workflows/rdx.py $@


###############################
# RDX run 2 ntuple generation #
###############################

rdx-ntuple-run2-all:  Dst_D0-mc-fullsim-Lb Dst_D0-std Dst_D0-mu_misid rdx-ntuple-run2-mc-to-all

Dst_D0-std:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-ntuple_data.log

rdx-ntuple-run2-data-cut_opt:
	workflows/rdx.py $@

Dst_D0-mu_misid:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-ntuple_mu_misid.log

# this is FullSim
rdx-ntuple-run2-mc:
	workflows/rdx.py $@

Dst_D0-mc-fullsim-Lb:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-ntuple_mc-fullsim-lb.log

rdx-ntuple-run2-mc-cut_opt:
	workflows/rdx.py $@

rdx-ntuple-run2-misid_study:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-ntuple_misid_study.log


# this is for MC ghost study
rdx-ntuple-run2-mc_ghost:
	workflows/rdx.py $@

# this is tracker-only
rdx-ntuple-run2-mc-to-all: \
	Dst_D0-mc-tracker_only-sig_norm  \
	Dst_D0-mc-tracker_only-DDX  \
	Dst_D0-mc-tracker_only-Dstst \
	Dst_D0-mc-tracker_only-Dstst_heavy \
	Dst_D0-mc-tracker_only-D_s

Dst_D0-mc-tracker_only-sig_norm :
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-ntuple_mc-to-sig-norm.log

Dst_D0-mc-tracker_only-DDX :
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-ntuple_mc-to-ddx.log

# rdx-ntuple-run2-mc-to-missing-ddx:
# 	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-missing-ddx-DstDspi:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-ddx-test:
	workflows/rdx.py $@

Dst_D0-mc-tracker_only-Dstst:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-ntuple_mc-to-dstst.log

Dst_D0-mc-tracker_only-Dstst_heavy:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-ntuple_mc-to-dstst-heavy.log

Dst_D0-mc-tracker_only-D_s:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-ntuple_mc-to-d_s.log

# b-inclusive D* ntuplesfor misid studies
incl_b_dst_mc-misid_corrections-k:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-incl_b_dst_mc-misid-k.log

incl_b_dst_mc-misid_corrections-pi:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-incl_b_dst_mc-misid-pi.log

incl_b_dst_mc-misid_smearing-k:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-incl_b_dst_mc-smr-k.log

incl_b_dst_mc-misid_smearing-pi:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-incl_b_dst_mc-smr-pi.log

incl_b_dst_mc-eghost-unfolding:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-incl_b_dst_mc-eghost.log

# Additional inclusive D* ntuples for misid studies
bd_dstx_mc-misid_corrections-k:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-bd_dstx_mc-misid-k.log

bd_dstx_mc-misid_corrections-pi:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-bd_dstx_mc-misid-pi.log

# inclusive D* samples with mis-reconstructed D0 decays
d0_bkg_all: d0_bkg_k d0_bkg_pi

d0_bkg_k: \
	d0_bkg_pipipi0_phsp-misid_corrections-k \
	d0_bkg_pipipi0_dalitz-misid_corrections-k \
	d0_bkg_pimunu-misid_corrections-k \
	d0_bkg_kmunu-misid_corrections-k \
	d0_bkg_pipi-misid_corrections-k \
	d0_bkg_kspipi-misid_corrections-k \
	d0_bkg_pienu-misid_corrections-k \
	d0_bkg_kenu-misid_corrections-k

d0_bkg_pi: \
	d0_bkg_pipipi0_phsp-misid_corrections-pi \
	d0_bkg_pipipi0_dalitz-misid_corrections-pi \
	d0_bkg_pimunu-misid_corrections-pi \
	d0_bkg_kmunu-misid_corrections-pi \
	d0_bkg_pipi-misid_corrections-pi \
	d0_bkg_kspipi-misid_corrections-pi \
	d0_bkg_pienu-misid_corrections-pi \
	d0_bkg_kenu-misid_corrections-pi


d0_bkg_pipipi0_phsp-misid_corrections-k:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_pipipi0_phsp_mc-misid-k.log

d0_bkg_pipipi0_dalitz-misid_corrections-k:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_pipipi0_dalitz_mc-misid-k.log

d0_bkg_pimunu-misid_corrections-k:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_pimunu_mc-misid-k.log

d0_bkg_kmunu-misid_corrections-k:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_kmunu_mc-misid-k.log

d0_bkg_pipi-misid_corrections-k:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_pipi_mc-misid-k.log

d0_bkg_kspipi-misid_corrections-k:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_kspipi_mc-misid-k.log

d0_bkg_pienu-misid_corrections-k:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_pienu_mc-misid-k.log

d0_bkg_kenu-misid_corrections-k:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_kenu_mc-misid-k.log

d0_bkg_pipipi0_phsp-misid_corrections-pi:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_pipipi0_phsp_mc-misid-pi.log

d0_bkg_pipipi0_dalitz-misid_corrections-pi:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_pipipi0_dalitz_mc-misid-pi.log

d0_bkg_pimunu-misid_corrections-pi:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_pimunu-misid-pi.log

d0_bkg_kmunu-misid_corrections-pi:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_kmunu_mc-misid-pi.log

d0_bkg_pipi-misid_corrections-pi:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_pipi_mc-misid-pi.log

d0_bkg_kspipi-misid_corrections-pi:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_kspipi_mc-misid-pi.log

d0_bkg_pienu-misid_corrections-pi:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_pienu_mc-misid-pi.log

d0_bkg_kenu-misid_corrections-pi:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_pipi_mc-misid-pi.log

# b-inclusive minimum bias samples with [D*+ -> (D0 -> X) pi+]cc candidates
d0_bkg_mb: \
    d0_bkg-mb-misid_corrections-k \
    d0_bkg-mb-misid_corrections-pi

d0_bkg-mb-misid_corrections-k:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_mb_mc-misid-k.log

d0_bkg-mb-misid_corrections-pi:
	workflows/rdx.py $@ 2>&1 | tee ${TIMESTAMP}-step2-d0_bkg_mb_mc-misid-pi.log

# Debug
rdx-ntuple-run2-mc-demo:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-demo-ddx:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-demo:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-dss:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-sub:
	workflows/rdx.py $@

rdx-ntuple-run2-data-demo:
	workflows/rdx.py $@

rdx-ntuple-run2-data-no-Dst-veto:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-sig-norm-no-Dst-veto:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-dst0norm-for-vertexsmear:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-dst0normsubsamp-for-vertexsmear:
	workflows/rdx.py $@

rdx-ntuple-run2-data-debug:
	workflows/rdx.py $@

rdx-ntuple-run2-misid_study-demo:
	workflows/rdx.py $@

rdx-ntuple-run2-mu_misid-demo:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-sig-norm-demo:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-dstst-debug:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-sig-norm-dst-ff-debug-10sig:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-sig-norm-dst-ff-debug:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-sig-norm-dst-ff-debug-nocorr:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-sig-norm-dst-ff-debug-10sig-nocorr:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-sig-norm-dst-ff-debug-phoebe:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-sig-norm-dst-ff-debug-no-rescale:
	workflows/rdx.py $@


###############################
# RDX run 1 ntuple generation #
###############################

rdx-ntuple-run1-all: rdx-ntuple-run1-data rdx-ntuple-run1-data-D0-comp

rdx-ntuple-run1-data:
	workflows/rdx.py $@

# Debug
rdx-ntuple-run1-data-D0-comp:
	workflows/rdx.py $@

rdx-ntuple-run1-data-Dst-comp:
	workflows/rdx.py $@


#########################################
# Reference RDX run 1 ntuple generation #
#########################################

ref-rdx-ntuple-run1-all: \
	ref-rdx-ntuple-run1-data-Dst ref-rdx-ntuple-run1-data-D0 \
	ref-rdx-ntuple-run1-data-Dst-comp ref-rdx-ntuple-run1-data-D0-comp

ref-rdx-ntuple-run1-data-Dst:
	workflows/rdx.py $@

ref-rdx-ntuple-run1-data-Dst-comp: rdx-ntuple-run1-data-Dst-comp
	workflows/rdx.py $@

ref-rdx-ntuple-run1-data-D0:
	workflows/rdx.py $@

ref-rdx-ntuple-run1-data-D0-comp: rdx-ntuple-run1-data-D0-comp
	workflows/rdx.py $@


###################################
# J/psi K run 2 ntuple generation #
###################################

JpsiK-ntuple-run2-data:
	workflows/JpsiK.py $@

JpsiK-ntuple-run2-mc:
	workflows/JpsiK.py $@

# debug
JpsiK-ntuple-run2-data-demo:
	workflows/JpsiK.py $@

JpsiK-ntuple-run2-mc-demo:
	workflows/JpsiK.py $@

JpsiK-ntuple-run2-mc-sub:
	workflows/JpsiK.py $@


###############
# RDX cutflow #
###############

rdx-cutflows:
	workflows/rdx_cutflows.py all

rdx-cutflow-data-pid-last:
	workflows/rdx_cutflows.py $@

rdx-cutflow-data:
	workflows/rdx_cutflows.py $@

rdx-cutflow-bare:
	workflows/rdx_cutflows.py $@

rdx-cutflow-dsttau:
	workflows/rdx_cutflows.py $@

rdx-cutflow-bare-comp:
	workflows/rdx_cutflows.py rdx-cutflow-bare-sig
	workflows/rdx_cutflows.py rdx-cutflow-bare-nor
	workflows/rdx_cutflows.py rdx-cutflow-bare-dss

rdx-cutflow-vali-Dst:
	workflows/rdx_cutflows.py rdx-cutflow-vali-dst-2011-md-rs
	workflows/rdx_cutflows.py rdx-cutflow-vali-dst-2011-md-ws-mu
	workflows/rdx_cutflows.py rdx-cutflow-vali-dst-2011-md-ws-pi

rdx-cutflow-vali-Dst-reduced:
	workflows/rdx_cutflows.py rdx-cutflow-vali-dst-2011-md-rs-reduced
	workflows/rdx_cutflows.py rdx-cutflow-vali-dst-2011-md-ws-mu-reduced
	workflows/rdx_cutflows.py rdx-cutflow-vali-dst-2011-md-ws-pi-reduced


####################
# Generic patterns #
####################

%.root:
	@echo -e "No such file present: " $@
	@exit 1

# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Oct 17, 2022 at 10:02 AM -0400

VPATH := postprocess:test:scripts:ntuples
VPATH := run1-rdx/cutflow:run2-rdx/cutflow:$(VPATH)

# System env
OS := $(shell uname)
PWD := $(shell pwd)
# In-house Python libraries
LIB_PY := $(wildcard lib/python/*)
DAVINCI_VERSION=DaVinci-v45r6-SL


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
	@pip install -r ./requirements.txt

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

# Test if specific files follow naming conventions.
test-naming-conv:
	workflows/validate_filename.py


#################################
# RJpsi run 2 ntuple generation #
#################################

RJpsi-ntuple-run2-mc_ghost:
	workflows/rdx.py $@


###############################
# RDX run 2 ntuple generation #
###############################

rdx-ntuple-run2-all: rdx-ntuple-run2-data rdx-ntuple-run2-mu_misid rdx-ntuple-run2-mc

rdx-ntuple-run2-data:
	workflows/rdx.py $@

rdx-ntuple-run2-data-cut_opt:
	workflows/rdx.py $@

rdx-ntuple-run2-mu_misid:
	workflows/rdx.py $@

# this is FullSim
rdx-ntuple-run2-mc:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-cut_opt:
	workflows/rdx.py $@

rdx-ntuple-run2-misid_study:
	workflows/rdx.py $@

# this is for MC ghost study
rdx-ntuple-run2-mc_ghost:
	workflows/rdx.py $@

# this is tracker-only
rdx-ntuple-run2-mc-to-all: \
    rdx-ntuple-run2-mc-to-sig-norm \
    rdx-ntuple-run2-mc-to-ddx \
    rdx-ntuple-run2-mc-to-dstst \
    rdx-ntuple-run2-mc-to-dstst-heavy \
    rdx-ntuple-run2-mc-to-d_s

rdx-ntuple-run2-mc-to-sig-norm:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-ddx:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-dstst:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-dstst-heavy:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-to-d_s:
	workflows/rdx.py $@

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

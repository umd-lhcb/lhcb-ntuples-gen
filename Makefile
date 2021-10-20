# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Oct 20, 2021 at 02:11 AM +0200

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

install-dep:
	@echo "Installing third-party Python libraries..."
	@pip install -r ./requirements.txt -U
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
	test/test_filename_convention.py


###############################
# RDX run 2 ntuple generation #
###############################

rdx-ntuple-run2-all: rdx-ntuple-run2-data-oldcut rdx-ntuple-run2-mc-demo

rdx-ntuple-run2-data-oldcut:
	workflows/rdx.py $@

rdx-ntuple-run2-data-oldcut-no-Dst-veto:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-demo:
	workflows/rdx.py $@


###############################
# RDX run 1 ntuple generation #
###############################

rdx-ntuple-run1-all: rdx-ntuple-run1-data

rdx-ntuple-run1-data:
	workflows/rdx.py $@


#########################################
# Reference RDX run 1 ntuple generation #
#########################################

ref-rdx-ntuple-run1-all: ref-rdx-ntuple-run1-data-Dst ref-rdx-ntuple-run1-data-D0

ref-rdx-ntuple-run1-data-Dst:
	workflows/rdx.py $@

ref-rdx-ntuple-run1-data-D0:
	workflows/rdx.py $@


###############
# RDX cutflow #
###############

rdx-cutflows:
	workflows/rdx_cutflows.py all


####################
# Generic patterns #
####################

%.root:
	@echo -e "No such file present: " $@
	@exit 1

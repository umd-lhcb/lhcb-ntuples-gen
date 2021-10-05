# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Oct 05, 2021 at 02:35 AM +0200

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

rdx-ntuple-run2-oldcut:
	workflows/rdx.py $@

rdx-ntuple-run2-mc-demo: \
	./run2-rdx/samples/Dst_D0--21_07_22--mc--Bd2DstMuNu--2016--md--py8-sim09j-dv45-subset.root \
	rdx-run2/rdx-run2_with_run1_cuts.yml
	workflows/rdx.py $@ $< --debug \
		--mode mc_ref -A input_yml:$(abspath $(word 2, $^))


###############################
# RDX run 1 ntuple generation #
###############################

rdx-ntuple-run1:
	workflows/rdx.py $@

ref-rdx-ntuple-run1:
	workflows/rdx.py $@


###############
# RDX cutflow #
###############

.PHONY: rdx-cutflows

rdx-cutflows:
	workflows/rdx_cutflows.py


####################
# Generic patterns #
####################

%.root:
	@echo -e "No such file present: " $@
	@exit 1

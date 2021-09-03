# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Sep 03, 2021 at 04:16 PM +0200

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


#########################
# RDX ntuple generation #
#########################

.PHONY: rdx-ntuple-run2-oldcut

rdx-ntuple-run2-oldcut: \
	0.9.4-trigger_emulation/Dst_D0-std \
	rdx-run2/rdx-run2_with_run1_cuts.yml
	workflows/rdx.py $@ $< --debug \
		--mode data -A input_yml:$(abspath $(word 2, $^))

rdx-ntuple-run2-oldcut-no-ubdt: \
	0.9.4-trigger_emulation/Dst_D0-std \
	rdx-run2/rdx-run2_with_run1_cuts.yml
	workflows/rdx.py $@ $< --debug \
		--mode data_no_mu_bdt -A input_yml:$(abspath $(word 2, $^))

rdx-ntuple-run1: \
	0.9.2-2011_production/Dst_D0-std \
	rdx-run1/rdx-run1.yml
	workflows/rdx.py $@ $< --debug \
		--mode data_no_mu_bdt -A input_yml:$(abspath $(word 2, $^))

rdx-ntuple-run1-no-Dst-veto: \
	run1-rdx/samples/Dst_D0--21_08_25--std--data--2012--md--dv45-subset.root \
	rdx-run1/rdx-run1_no_Dst_veto.yml
	workflows/rdx.py $@ $< --debug \
		--mode data_ref -A input_yml:$(abspath $(word 2, $^))

ref-rdx-ntuple-run1: \
	ref-rdx-run1/Dst-mix \
	ref-rdx-run1/rdst-2011-mix.yml
	workflows/rdx.py $@ $< --debug \
		--mode data_ref -A input_yml:$(abspath $(word 2, $^))


#########################
# RDX Trigger emulation #
#########################

.PHONY: rdx-trigger-emu-nor rdx-trigger-emu-nor-fs-vs-to

rdx-trigger-emu-nor: \
	0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root
	workflows/rdx.py $@ $< --mode trigger_emulation

rdx-trigger-emu-nor-fs-vs-to: \
	0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root \
	0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09j_Reco16_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root
	workflows/rdx.py $@ $^ --mode trigger_emulation_fs_vs_to


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

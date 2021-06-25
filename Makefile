# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sat Jun 26, 2021 at 12:07 AM +0200

export PATH := workflows:test:scripts:tools:$(PATH)

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
	@pip install -r ./requirements.txt
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


#############################
# Generic ntuple generation #
#############################

.PHONY: rdx-ntuple-run2-oldcut

rdx-ntuple-run2-oldcut: \
	0.9.4-trigger_emulation/Dst_D0-std \
	rdx-run2/rdx-run2_with_run1_cuts.yml
	@rdx.py $@ $< --debug \
		--mode data -A input_yml:$(abspath $(word 2, $^))


#########
# Tests #
#########

.PHONY: test-naming-conv

# Test if specific files follow naming conventions.
test-naming-conv:
	@test_filename_convention.py


#########################
# RDX Trigger emulation #
#########################

.PHONY: rdx-trigger-emu-nor rdx-trigger-emu-nor-fs-vs-to

rdx-trigger-emu-nor: \
	0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root
	@rdx.py $@ $< --mode trigger_emulation

rdx-trigger-emu-nor-fs-vs-to: \
	0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root \
	0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09j_Reco16_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root
	@rdx.py $@ $^ --mode trigger_emulation_fs_vs_to


###############
# RDX cutflow #
###############

.PHONY: rdx-cutflow
.SECONDARY:  # Don't delete intermediate files!

rdx-cutflow: \
	gen/rdx-cutflow-Dst-bare \
	gen/rdx-cutflow-Dst-bare-sig \
	gen/rdx-cutflow-Dst-bare-nor \
	gen/rdx-cutflow-Dst-bare-dss

# Generic cutflow table generation
gen/rdx-cutflow-Dst-%: \
	gen/rdx-cutflow-run1-Dst-%/cutflow.yml \
	gen/rdx-cutflow-run2-Dst-%/cutflow.yml
	@mkdir -p $@
	@cutflow_gen.py -o $< -t $(word 2, $^) -n > $@/cutflow.csv
	@cat $@/cutflow.csv | tabgen.py -f latex_booktabs_raw > $@/cutflow.tex
	@cat $@/cutflow.csv | tabgen.py -f github > $@/cutflow.md

# Generic cutflow YAML generation
gen/rdx-cutflow-run1-Dst-%/cutflow.yml: \
	0.9.4-trigger_emulation/Dst_D0-cutflow_mc \
	21_05_31-run1_bare.yml
	$(eval JOBNAME	:=	$(notdir $(patsubst %/,%,$(dir $@))))
	$(eval MODE	:=	$(subst rdx-cutflow-,,${JOBNAME}))
	@rdx.py ${JOBNAME} $< --mode cutflow \
		-A keep:2011,bare mode:${MODE} input_yml:$(abspath $(word 2, $^))

gen/rdx-cutflow-run2-Dst-%/cutflow.yml: \
	0.9.4-trigger_emulation/Dst_D0-cutflow_mc \
	21_05_31-run2_bare.yml
	$(eval JOBNAME	:=	$(notdir $(patsubst %/,%,$(dir $@))))
	$(eval MODE	:=	$(subst rdx-cutflow-,,${JOBNAME}))
	@rdx.py ${JOBNAME} $< --mode cutflow \
		-A keep:2016,bare mode:${MODE} input_yml:$(abspath $(word 2, $^))


####################
# Generic patterns #
####################

%.root:
	@echo -e "No such file present:" $@

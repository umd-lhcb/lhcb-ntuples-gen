# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Mar 15, 2021 at 12:53 AM +0100

BINPATH	:=	bin

export PATH := test:scripts:$(BINPATH):$(PATH)

VPATH := postprocess:test:scripts:$(BINPATH)

# Sub-makefiles for different analyses
include ./workflows/rdx.mk  # R(D(*))

# System env
OS := $(shell uname)
PWD := $(shell pwd)

# In-house Python libraries
LIB_PY := $(wildcard lib/python/*)

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDFLAGS	:=	-Iinclude

DAVINCI_VERSION=DaVinci-v45r6-SL


.PHONY: all clean history tagdate install-dep

clean:
	@rm -rf $(BINPATH)/*
	@find ./gen -name '*.root' -delete
	@find ./gen -name '*.cpp' -delete
	@find ./gen -name '*.yml' -delete

history:
	@git tag -l -n99

tagdate:
	@git log --date-order --tags --simplify-by-decoration --pretty='format:%C(green)%ad %C(red)%h %C(reset)%D' --date=short

install-dep:
	@echo "Installing third-party Python libraries..."
	@pip install -U -r ./requirements.txt
	@echo "Installing in-house Python libraries..."
	@for p in $(LIB_PY); do \
			cd $(PWD)/$$p; \
			pip install --force-reinstall .; \
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

.PHONY: ntuple-rdx-run1 ntuple-rdx-run2

ntuple-rdx-run1: \
	gen/run1-Dst_D0-step2/Dst_D0--20_10_14--mc--Bd2DstTauNu--2012--md--py6-sim08a-dv45-subset-step1.1.root \
	gen/run1-Dst_D0-step2/Dst_D0--20_10_12--std--data--2011--md--step2.root \
	gen/run1-Dst-step2/Dst--20_07_02--mix--data--2011--md--phoebe-step2.root \
	gen/run1-Dst-step2/Dst--20_09_16--std--data--2011--md--phoebe-step2.root

ntuple-rdx-run2: \
	gen/run2-Dst-step2/Dst--19_09_09--std--data--2016--md--step2.root


#########
# Tests #
#########

.PHONY: test-all test-naming-conv

test-all: \
	test-naming-conv \
	test-cutflow-rdst-run1 \
	test-cutflow-rdst-run2 \
	test-cutflow-consistency-rdst

# Test if specific files follow naming conventions.
test-naming-conv:
	@test_filename_convention.py


####################
# Generic patterns #
####################

%.pp: gen/%.cpp \
	include/functor/*.h \
	include/*.h
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS)

%.root:
	@echo -e "No such file present:" $@

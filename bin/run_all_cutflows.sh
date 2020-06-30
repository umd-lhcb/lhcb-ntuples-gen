#! /bin/bash

################################################################################
#### RUN1: Finding Signal, Normalization, and D** yields from BARE Run2 ntuples
run1_ntuple=ntuples/0.9.0-cutflow/Dst-cutflow_mc/Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root

./utils/cutflow-components.py $run1_ntuple gen/cutflow/output-run1-sig.yml run1-sig -t 'TupleB0/DecayTree'
./utils/cutflow-components.py $run1_ntuple gen/cutflow/output-run1-nor.yml run1-nor -t 'TupleB0/DecayTree'
./utils/cutflow-components.py $run1_ntuple gen/cutflow/output-run1-dss.yml run1-dss -t 'TupleB0/DecayTree'

## Producing cutflow tables in LaTeX format
./utils/table-cutflow-components.py -s gen/cutflow/output-run1-sig.yml -n gen/cutflow/output-run1-nor.yml -d gen/cutflow/output-run1-dss.yml | tabgen.py -f latex_raw



################################################################################
#### RUN2: Finding Signal, Normalization, and D** yields from BARE ntuples
run2_ntuple=ntuples/0.9.0-cutflow/Dst-cutflow_mc/Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root

./utils/cutflow-components.py $run2_ntuple gen/cutflow/output-run2-sig.yml run2-sig -t 'TupleB0/DecayTree'
./utils/cutflow-components.py $run2_ntuple gen/cutflow/output-run2-nor.yml run2-nor -t 'TupleB0/DecayTree'
./utils/cutflow-components.py $run2_ntuple gen/cutflow/output-run2-dss.yml run2-dss -t 'TupleB0/DecayTree'

## Producing cutflow tables in LaTeX format
./utils/table-cutflow-components.py -s gen/cutflow/output-run2-sig.yml -n gen/cutflow/output-run2-nor.yml -d gen/cutflow/output-run2-dss.yml | tabgen.py -f latex_raw


###############################################################################
##### Standard cutflow double ratio
./utils/cutflow_output_yml_gen_pre_0.9.0.py ntuples/pre-0.9.0/Dst-cutflow_mc/Dst--20_03_18--cutflow_mc--cocktail--2011--md.root run1-b2D0MuXB2DMuNuForTauMuLine/cutflow/input-run1.yml gen/cutflow/output-run1.yml run1 -t 'TupleB0/DecayTree'
./utils/cutflow_output_yml_gen_pre_0.9.0.py ntuples/pre-0.9.0/Dst-cutflow_mc/Dst--20_03_18--cutflow_mc--cocktail--2016--md.root run2-b2D0MuXB2DMuForTauMuLine/cutflow/input-run2.yml gen/cutflow/output-run2.yml run2 -t 'TupleB0/DecayTree'
utils/cutflow_gen.py -o gen/cutflow/output-run1.yml -t gen/cutflow/output-run2.yml -n | tabgen.py -f latex_raw

################################################################################
#### BARE cutflow double ratio
run1_ntuple=ntuples/0.9.0-cutflow/Dst-cutflow_mc/Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root
run1_log=run1-b2D0MuXB2DMuNuForTauMuLine/cutflow/input-run1-bare.yml
run2_ntuple=ntuples/0.9.0-cutflow/Dst-cutflow_mc/Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root
run2_log=run2-b2D0MuXB2DMuForTauMuLine/cutflow/input-run2-bare.yml

run1_out=gen/cutflow/output-run1-bare.yml
run2_out=gen/cutflow/output-run2-bare.yml

./utils/cutflow_output_yml_gen.py $run1_ntuple $run1_log $run1_out run1-bare -t 'TupleB0/DecayTree'
./utils/cutflow_output_yml_gen.py $run2_ntuple $run2_log $run2_out run2-bare -t 'TupleB0/DecayTree'
./utils/cutflow_gen.py -o $run1_out -t $run2_out -n | tabgen.py -f latex_raw

###############################################################################
##### DATA standard cutflow double ratio
utils/cutflow_output_yml_gen-pre-0.9.0.py ntuples/pre-0.9.0/Dst-cutflow_data/Dst--20_04_03--cutflow_data--data--2012--md.root run1-b2D0MuXB2DMuNuForTauMuLine/cutflow/input-run1-data.yml gen/cutflow/output-run1-data.yml run1 -t 'TupleB0/DecayTree'
utils/cutflow_output_yml_gen-pre-0.9.0.py ntuples/pre-0.9.0/Dst-cutflow_data/Dst--20_04_03--cutflow_data--data--2016--md.root run2-b2D0MuXB2DMuForTauMuLine/cutflow/input-run2-data.yml gen/cutflow/output-run2-data.yml run2-data -t 'TupleB0/DecayTree'
utils/cutflow_gen.py -o gen/cutflow/output-run1-data.yml -t gen/cutflow/output-run2-data.yml -n | tabgen.py -f latex_raw


#!/usr/bin/env bash
# NOTE: This is just an example! To generate all bare component cutflows, go to
#       project root, then 'make rdx-cutflow'

RUN1_NTP_MD=../../../ntuples/0.9.0-cutflow/Dst-cutflow_mc/Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root
RUN1_INPUT_YML=input-run1-bare.yml

RUN2_NTP_MD=../../../ntuples/0.9.0-cutflow/Dst-cutflow_mc/Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root
RUN2_INPUT_YML=input-run2-bare.yml

# D* tau nu
./cutflow_output_yml_gen.py ${RUN1_NTP_MD} -i ${RUN1_INPUT_YML} -o ./cutflow_run1-sig.yml -m run1-Dst-bare-sig
./cutflow_output_yml_gen.py ${RUN2_NTP_MD} -i ${RUN2_INPUT_YML} -o ./cutflow_run2-sig.yml -m run2-Dst-bare-sig
./cutflow_gen.py -o ./cutflow_run1-sig.yml -t ./cutflow_run2-sig.yml -n > ./cutflow-sig.csv
cat ./cutflow-sig.csv | tabgen.py -f latex_booktabs_raw > ./cutflow-sig.tex
cat ./cutflow-sig.csv | tabgen.py -f github > ./cutflow-sig.md

# D* mu nu
./cutflow_output_yml_gen.py ${RUN1_NTP_MD} -i ${RUN1_INPUT_YML} -o ./cutflow_run1-nor.yml -m run1-Dst-bare-nor
./cutflow_output_yml_gen.py ${RUN2_NTP_MD} -i ${RUN2_INPUT_YML} -o ./cutflow_run2-nor.yml -m run2-Dst-bare-nor
./cutflow_gen.py -o ./cutflow_run1-nor.yml -t ./cutflow_run2-nor.yml -n > ./cutflow-nor.csv
cat ./cutflow-nor.csv | tabgen.py -f latex_booktabs_raw > ./cutflow-nor.tex
cat ./cutflow-nor.csv | tabgen.py -f github > ./cutflow-nor.md

# D** mu nu
./cutflow_output_yml_gen.py ${RUN1_NTP_MD} -i ${RUN1_INPUT_YML} -o ./cutflow_run1-dss.yml -m run1-Dst-bare-dss
./cutflow_output_yml_gen.py ${RUN2_NTP_MD} -i ${RUN2_INPUT_YML} -o ./cutflow_run2-dss.yml -m run2-Dst-bare-dss
./cutflow_gen.py -o ./cutflow_run1-dss.yml -t ./cutflow_run2-dss.yml -n > ./cutflow-dss.csv
cat ./cutflow-dss.csv | tabgen.py -f latex_booktabs_raw > ./cutflow-dss.tex
cat ./cutflow-dss.csv | tabgen.py -f github > ./cutflow-dss.md

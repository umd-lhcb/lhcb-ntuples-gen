# Last Change: Wed Feb 16, 2022 at 09:38 AM -0500

.PHONY: fit

fit:
	./fit/fit_and_sweight.py -i \
		"../ntuples/0.9.6-2016_production/JpsiK-std/JpsiK--22_02_14--std--data--2016--md/*.root:tree" \
        -p ./fit_params/nominal.yml \
		-o fit_results/$(shell date +"%y_%m_%d_%H_%M")-fit-JpsiK

plot-init:
	./fit/fit_and_sweight.py -i \
		"../ntuples/0.9.6-2016_production/JpsiK-std/JpsiK--22_02_14--std--data--2016--md/*.root:tree" \
        -p ./fit_params/nominal.yml \
		-I plots/$(shell date +"%y_%m_%d_%H_%M")-fit-JpsiK-init.png --noFit

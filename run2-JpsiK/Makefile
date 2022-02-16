.PHONY: fit

fit:
	./fit/fit_and_sweight.py -i \
		"../ntuples/0.9.6-2016_production/JpsiK-std/JpsiK--22_02_14--std--data--2016--md/*.root:tree" \
		-o fit_results/$(shell date +"%y_%m_%d_%H_%M")-fit-JpsiK

plot-init:
	./fit/fit_and_sweight.py -i \
		"../ntuples/0.9.6-2016_production/JpsiK-std/JpsiK--22_02_14--std--data--2016--md/*.root:tree" \
		-I plots/$(shell date +"%y_%m_%d_%H_%M")-fit-JpsiK-init.png --noFit \
        -p ./fit_params/nominal.yml

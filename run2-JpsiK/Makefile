# Last Change: Thu Feb 17, 2022 at 12:53 AM -0500

.PHONY: fit

fit:
	$(eval TIME_STAMP	:=	$(shell date +"%y_%m_%d_%H_%M"))
	$(eval OUT_DIR	:=	fit_results/$(TIME_STAMP)-fit-JpsiK)
	@mkdir -p $(OUT_DIR)
	./fit/fit_and_sweight.py -i \
		"../ntuples/0.9.6-2016_production/JpsiK-std/JpsiK--22_02_14--std--data--2016--md/*.root:tree" \
		"../ntuples/0.9.6-2016_production/JpsiK-std/JpsiK--22_02_14--std--data--2016--mu/*.root:tree" \
		-p ./fit_params/nominal.yml \
		-o $(OUT_DIR) | tee $(OUT_DIR)/fit.log

plot-init:
	./fit/fit_and_sweight.py -i \
		"../ntuples/0.9.6-2016_production/JpsiK-std/JpsiK--22_02_14--std--data--2016--md/*.root:tree" \
		"../ntuples/0.9.6-2016_production/JpsiK-std/JpsiK--22_02_14--std--data--2016--mu/*.root:tree" \
		-p ./fit_params/nominal.yml \
		-I plots/$(shell date +"%y_%m_%d_%H_%M")-fit-JpsiK-init.png --noFit

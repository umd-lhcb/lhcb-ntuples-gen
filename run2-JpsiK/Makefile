# Last Change: Fri Feb 18, 2022 at 04:22 PM -0500

.PHONY: fit

fit:
	$(eval TIME_STAMP	:=	$(shell date +"%y_%m_%d_%H_%M"))
	$(eval OUT_DIR	:=	gen/JpsiK-$(TIME_STAMP)-std-fit)
	@mkdir -p $(OUT_DIR)
	./fit/fit_and_sweight.py -i \
		"../ntuples/0.9.6-2016_production/JpsiK-std/JpsiK--22_02_14--std--data--2016--md/*.root:tree" \
		"../ntuples/0.9.6-2016_production/JpsiK-std/JpsiK--22_02_14--std--data--2016--mu/*.root:tree" \
		-p ./fit/fit_params/init.yml \
        -O $(OUT_DIR)/JpsiK-$(TIME_STAMP)-fit_sweights.root \
		-o $(OUT_DIR) | tee $(OUT_DIR)/fit.log

plot-init:
	./fit/fit_and_sweight.py -i \
		"../ntuples/0.9.6-2016_production/JpsiK-std/JpsiK--22_02_14--std--data--2016--md/*.root:tree" \
		"../ntuples/0.9.6-2016_production/JpsiK-std/JpsiK--22_02_14--std--data--2016--mu/*.root:tree" \
		-p ./fit/fit_params/init.yml \
		-I gen/JpsiK-$(shell date +"%y_%m_%d_%H_%M")-std-fit_init.png --noFit

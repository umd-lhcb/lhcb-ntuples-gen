# Last Change: Thu Feb 24, 2022 at 12:51 AM -0500

.PHONY: fit

fit:
	$(eval TIME_STAMP	:=	$(shell date +"%y_%m_%d_%H_%M"))
	$(eval OUT_DIR	:=	gen/JpsiK-$(TIME_STAMP)-std-fit)
	@mkdir -p $(OUT_DIR)
	./fit/fit_and_sweight.py -i \
		"../ntuples/0.9.6-2016_production/JpsiK-std-step2/JpsiK--22_02_22--std--data--2016--md/*.root:tree" \
		"../ntuples/0.9.6-2016_production/JpsiK-std-step2/JpsiK--22_02_22--std--data--2016--mu/*.root:tree" \
		-p ./fit/fit_params/init.yml \
		-o $(OUT_DIR) | tee $(OUT_DIR)/fit.log
	./fit/splot.py -i $(OUT_DIR)/fit.root -p $(OUT_DIR)/params.yml \
		-o $(OUT_DIR)/splot_sig.pdf -m sig --modelLabel "sig."
	./fit/splot.py -i $(OUT_DIR)/fit.root -p $(OUT_DIR)/params.yml \
		-o $(OUT_DIR)/splot_bkg.pdf -m bkg --modelLabel "bkg."

plot-init:
	./fit/fit_and_sweight.py -i \
		"../ntuples/0.9.6-2016_production/JpsiK-std-step2/JpsiK--22_02_22--std--data--2016--md/*.root:tree" \
		"../ntuples/0.9.6-2016_production/JpsiK-std-step2/JpsiK--22_02_22--std--data--2016--mu/*.root:tree" \
		-p ./fit/fit_params/init.yml \
		-I gen/JpsiK-$(shell date +"%y_%m_%d_%H_%M")-std-fit_init.png --noFit

gen-weights:
	./fit/gen_weights.py \
		-d ./fit/fit_results/JpsiK-22_02_23_21_42-std-fit/fit.root \
		-m \
			"../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_02_23--mc--12143001--2016--md/*.root" \
			"../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_02_23--mc--12143001--2016--mu/*.root" \
		-o ./gen/run2-JpsiK-2016-md-Any-ndof_ntracks__pt_eta.root
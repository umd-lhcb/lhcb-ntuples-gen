# Last Change: Tue Sep 20, 2022 at 12:40 AM -0400

export LD_LIBRARY_PATH	:=	${STUB_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH}


.PHONY: fit-2016 plot-init-2016 gen-weights-2016

fit-2016:
	$(eval TIME_STAMP	:=	$(shell date +"%y_%m_%d_%H_%M"))
	$(eval OUT_DIR	:=	gen/JpsiK-$(TIME_STAMP)-std-fit-2016)
	@mkdir -p $(OUT_DIR)
	./fit/fit_and_sweight.py -i \
		"../ntuples/0.9.8-JpsiK_L0/JpsiK-std-step2/JpsiK--24_03_22--std--data--2016--md.root:tree" \
		"../ntuples/0.9.8-JpsiK_L0/JpsiK-std-step2/JpsiK--24_03_22--std--data--2016--mu.root:tree" \
		-p ./fit/fit_params/init.yml \
		-o $(OUT_DIR) | tee $(OUT_DIR)/fit.log
	./fit/splot.py -i $(OUT_DIR)/fit.root -p $(OUT_DIR)/params.yml \
		-o $(OUT_DIR)/splot_sig.pdf -m sig --modelLabel "sig."
	./fit/splot.py -i $(OUT_DIR)/fit.root -p $(OUT_DIR)/params.yml \
		-o $(OUT_DIR)/splot_bkg.pdf -m bkg --modelLabel "bkg."


plot-init-2016:
	./fit/fit_and_sweight.py -i \
		"../ntuples/0.9.8-JpsiK_L0/JpsiK-std-step2/JpsiK--24_03_22--std--data--2016--md.root:tree" \
		"../ntuples/0.9.8-JpsiK_L0/JpsiK-std-step2/JpsiK--24_03_22--std--data--2016--mu.root:tree" \
		-p ./fit/fit_params/init.yml \
		-I gen/JpsiK-$(shell date +"%y_%m_%d_%H_%M")-std-fit_init-2016.pdf --noFit


gen-weights-2016:
	./fit/gen_weights.py \
		-d fit/fit_results/JpsiK-24_03_23_10_26-std-fit-2016/fit.root \
		-m \
			"../ntuples/0.9.9-JpsiK_noPID/JpsiK-mc-step2/JpsiK--24_04_03--mc--12143001--2016--md.root" \
			"../ntuples/0.9.9-JpsiK_noPID/JpsiK-mc-step2/JpsiK--24_04_03--mc--12143001--2016--mu.root" \
		-o ./gen/run2-JpsiK-2016-md-B-ndof_ntracks__pt_eta.root

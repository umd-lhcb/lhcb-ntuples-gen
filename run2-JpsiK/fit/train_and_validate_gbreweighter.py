#!/usr/bin/env python3

# Author: Alex Fernez (largely GPT-generated)
# uses fit_results output from fit_and_sweight.py (ie. sw_sig), and then trains GBReweighter (from hep_ml) on half of the JpsiK MC (original) + sweighted data (target) and validates the BDTs on the other half of the samples, including plotting the agreement for the test sample between the reweighted (either with GBReweighter or GradientBoostingClassifier weights) JpsiK MC and sweighted data and also 
# option: maybe also try k-fold reweighting?

import uproot
import pandas as pd
import numpy as np

from hep_ml.reweight import GBReweighter

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score

import matplotlib.pyplot as plt


variables = ["b_pt", "b_eta", "ntracks", "b_ownpv_ndof"]

target_weight = "sw_sig"
original_weight = "wtrk * pid_mc_ok * wpid" # pid_mc_ok == mu_ismu && amu_ismu, wpid == wpid_k*wpid_mu*wpid_amu (which are each probabilities to pass PIDK>4, PIDmu>2, PIDamu>2 cuts)
original_weights = original_weight.split(' * ') # make sure the formatting is consistent above!

target_df = uproot.concatenate(
    ["/home/alex/misc/lhcb-ntuples-gen/run2-JpsiK/fit/fit_results/JpsiK-25_05_11_17_29-std-fit-2016/fit.root:tree"],
    variables + [target_weight],
    library="pd"
)

original_df = uproot.concatenate(
    ["/home/alex/misc/lhcb-ntuples-gen/ntuples/glacier_links/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/JpsiK-mc/step2/JpsiK--25_05_11--mc--12143001--2016--md.root:tree", "/home/alex/misc/lhcb-ntuples-gen/ntuples/glacier_links/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/JpsiK-mc/step2/JpsiK--25_05_11--mc--12143001--2016--mu.root:tree"],
    variables + original_weights,
    library="pd"
)


### Train and test (and TODO save GBReweighter)

target_train_df, target_test_df = train_test_split(
    target_df,
    test_size=0.5,
    random_state=42
)

original_train_df, original_test_df = train_test_split(
    original_df,
    test_size=0.5,
    random_state=42
)

X_target_train = target_train_df[variables].to_numpy()
X_original_train = original_train_df[variables].to_numpy()
target_train_weights = target_train_df[target_weight].to_numpy()
original_train_weights = np.ones(len(original_train_df[original_weights[0]].to_numpy()))
for w in original_weights:
    original_train_weights = original_train_weights * original_train_df[w].to_numpy()

gbrwt = GBReweighter(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=3,
    min_samples_leaf=1000,
    gb_args={
        "subsample": 0.5
    }
)

gbrwt.fit(
    original=X_original_train,
    target=X_target_train,
    original_weight=original_train_weights,
    target_weight=target_train_weights
)
# TODO save gbrwt

X_original_test = original_test_df[variables].to_numpy()

gb_weights_test = gbrwt.predict_weights(X_original_test)

# optional clipping
# gb_weights_test = np.clip(
#     gb_weights_test,
#     0,
#     20
# )

# training on full sample instead of splitting in half for train/validation-- probably should just use the training on half sample, though
# original_df["gb_weight"] = gbrwt.predict_weights(
#     original_df[variables].to_numpy()
# )


### Validation ... continue here ...

# plotting (test sample)
def compare_distribution(tar_values, orig_values, tar_weights, orig_weights, reweights, xlabel, bins=50, tag=''):
    low = np.min(orig_values)
    high = np.max(orig_values)
    leg_label = "JpsiK"
    black_label = "Data (sweighted)"
    if 'rdx' in tag:
        leg_label = "DstMuNu"
        black_label = "MC (old rwgt)"

    plt.figure(figsize=(8, 6))
    if len (tar_values>0): 
        plt.hist(
            tar_values,
            bins=bins,
            range=(low, high),
            weights=tar_weights,
            density=True,
            histtype="step",
            linewidth=2,
            label=f"{leg_label} {black_label}",
            color='k'
        )
    plt.hist(
        orig_values,
        bins=bins,
        range=(low, high),
        weights=orig_weights,
        density=True,
        histtype="step",
        linewidth=2,
        label=f"{leg_label} MC (before)",
        color='r'
    )
    plt.hist(
        orig_values,
        bins=bins,
        range=(low, high),
        weights=orig_weights*reweights,
        density=True,
        histtype="step",
        linewidth=2,
        label=f"{leg_label} MC (GBReweight)",
        color='b'
    )

    plt.xlabel(xlabel)
    plt.ylabel("Normalized density")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'gbreweighter_results/{tag}{xlabel}.png')

orig_test_weights = np.ones(len(original_test_df[original_weights[0]].to_numpy()))
for w in original_weights:
    orig_test_weights = orig_test_weights * original_test_df[w].to_numpy()
for var in variables:
    compare_distribution(target_test_df[var].to_numpy(), original_test_df[var].to_numpy(), target_test_df["sw_sig"].to_numpy(), orig_test_weights, gb_weights_test, xlabel=var)


# check that it looks reasonable when applying to rdx (in particular, no ridiculous second peak in ntracks distribution)
rdx_variables_form = {"b_pt": "1000*b_pt", "b_eta": "b_eta", "ntracks": "nTracks", "b_ownpv_ndof": "b_ndof"} # not sure why this doesn't work below
rdx_variables = list(rdx_variables_form.keys())
rdx_wts_form = {"wff": "min(wff,50.0)", "w_w_ubdt": "min(w_w_ubdt/wjk,10.0)"} # not sure why this doesn't work below
rdx_wts_dummy = {"wff": "wff", "w_w_ubdt": "w_w_ubdt", "wjk": "wjk"}
# forms = {}
# forms.update(rdx_variables_form)
# forms.update(rdx_wts_form)
rdx_wts = list(rdx_wts_dummy.keys())
rdx_dstmunu = uproot.concatenate(
    ["/home/alex/misc/rdx-run2-analysis-v2/ntuples/glacier_links/0.9.17-all_years/2016/norm_DstMu/DstMu-11574021-MagDown/Dst--25_08_20--mc--11574021--2016--md--tracker_only.root:tree", "/home/alex/misc/rdx-run2-analysis-v2/ntuples/glacier_links/0.9.17-all_years/2016/norm_DstMu/DstMu-11574021-MagUp/Dst--25_08_20--mc--11574021--2016--mu--tracker_only.root:tree"],
    expressions = rdx_variables+rdx_wts,
    # aliases = forms,
    aliases = {"b_pt": "b_pt", "b_eta": "b_eta", "ntracks": "nTracks", "b_ownpv_ndof": "b_ndof", "wff": "wff", "w_w_ubdt": "w_w_ubdt", "wjk": "wjk"},
    cut = "skim_global_ok & ham_ok & mu_ubdt_ok & (k_p < 200) & (pi_p < 200) & (mu_p < 100) & (iso_p1 < 200) & (iso_p2 < 200) & (iso_p3 < 200) & tracks_chi2ndof_ok",
    library="pd"
)
rdx_dstmunu['b_pt'] = 1000.0*rdx_dstmunu['b_pt'] # GeV in rdx tuples, MeV in JpsiK (GBReweight expects it in MeV)
rdx_dstmunu_gbwts = gbrwt.predict_weights(rdx_dstmunu[rdx_variables].to_numpy())
# print(rdx_dstmunu_gbwts)
# rdx_dstmunu_wts = np.ones(len(rdx_dstmunu[rdx_wts[0]].to_numpy()))
# for w in rdx_wts:
#     print(rdx_dstmunu_wts)
#     wts = rdx_dstmunu[w].to_numpy()
#     print(f'{w}: {wts}')
#     rdx_dstmunu_wts = rdx_dstmunu_wts * wts
# print(np.minimum(rdx_dstmunu['wff'].to_numpy(), 50.0))
# print(np.minimum(np.nan_to_num(rdx_dstmunu['w_w_ubdt'].to_numpy()/rdx_dstmunu['wjk'].to_numpy(), nan=0.0, posinf=10.0, neginf=0.0), 10.0))
rdx_dstmunu_wts = np.minimum(rdx_dstmunu['wff'].to_numpy(), 50.0) * np.minimum(np.nan_to_num(rdx_dstmunu['w_w_ubdt'].to_numpy()/rdx_dstmunu['wjk'].to_numpy(), nan=0.0, posinf=10.0, neginf=0.0), 10.0)
rdx_dstmunu_old_wts = np.minimum(rdx_dstmunu['wff'].to_numpy(), 50.0) * np.minimum(rdx_dstmunu['w_w_ubdt'].to_numpy(), 10.0)
for var in variables:
    compare_distribution(rdx_dstmunu[var].to_numpy(), rdx_dstmunu[var].to_numpy(), rdx_dstmunu_old_wts, rdx_dstmunu_wts, rdx_dstmunu_gbwts, xlabel=var, tag='rdx_dstmunu-')

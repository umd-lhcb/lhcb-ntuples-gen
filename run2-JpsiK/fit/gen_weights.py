#!/usr/bin/env python3
#
# hep_ml version of gen_weights.py, written to mimic the original sequential
# 2D reweighting workflow as closely as possible.
#
# Main points preserved from the original code:
#   - same REWEIGHT_PROCEDURE, DATA_WTS, MC_WTS, MC_CUTS
#   - sequential weights: h_kinematic is trained/applied on top of h_occupancy
#   - previous-step lookup uses zero-padded underflow/overflow, so outside-range
#     events get previous weight 0, not nearest-edge clipping
#   - data sWeights are kept event-by-event, including negative sWeights
#   - binned negative data yields are clipped to zero in *_data_raw, like original
#   - output keeps *_data_raw, *_mc_raw, *_mc_no_wt, *_nan_kept, and final hist name
#
# Difference from the original:
#   - the final correction histogram is produced by hep_ml.BinsReweighter or
#     hep_ml.GBReweighter, evaluated at the centers of the original output bins,
#     rather than by the raw fixed-bin ratio.
#   - GBReweighter is less identical to the original binned ratio logic than
#     BinsReweighter; use it mainly as an alternative/smoothing cross-check.

import numpy as np

from argparse import ArgumentParser
from dataclasses import dataclass
from uproot import concatenate, recreate
from hep_ml import reweight

from typing import List, Union
from copy import deepcopy
from numpy.typing import ArrayLike


#################
# Configuration #
#################

@dataclass
class RwtRule:
    vars: List[str]
    bins: Union[ArrayLike, List[int], int]
    range: List[List[float]]


REWEIGHT_PROCEDURE = {
    'h_occupancy': RwtRule(['b_ownpv_ndof', 'ntracks'], [20, 20], [[1, 250], [0, 450]]),
    'h_kinematic': RwtRule(['b_pt', 'b_eta'], [20, 9], [[0, 30e3], [2, 6]]),
}

DATA_WTS = ['sw_sig']
MC_WTS = ['wtrk', 'wpid_k', 'wpid_mu', 'wpid_amu']
MC_CUTS = {'mu_ismu': 0, 'amu_ismu': 0}


#######################
# Command line parser #
#######################

def parse_input():
    parser = ArgumentParser(
        description='generate weights for sequential 2D reweighting using hep_ml, mimicking original gen_weights.py.'
    )

    parser.add_argument('-d', '--dataNtp', required=True, nargs='+',
                        help='specify data input ntuples, which must contain sWeight branches.')

    parser.add_argument('-m', '--mcNtp', required=True, nargs='+',
                        help='specify MC input ntuples.')

    parser.add_argument('-o', '--output', required=True,
                        help='specify output ntuple, which contains histograms.')

    parser.add_argument('-t', '--tree', default='tree',
                        help='specify the tree name in the input ntuple.')

    parser.add_argument('--n-bins', type=int, default=100,
                        help='hep_ml BinsReweighter n_bins per dimension. Default: 100')

    parser.add_argument('--n-neighs', type=float, default=5.0,
                        help='hep_ml BinsReweighter Gaussian smoothing size in bins. Default: 5.0')

    parser.add_argument('--bins-min-in-bin', type=float, default=0.1,
                        help=('BinsReweighter minimum internal bin content used when forming the '
                              'smoothed density ratio. Lower values are more aggressive; larger '
                              'values are smoother. Default: 0.1'))

    parser.add_argument('--method', choices=['bins', 'gb'], default='bins',
                        help='hep_ml reweighter to use: bins = BinsReweighter, gb = GBReweighter. Default: bins')

    parser.add_argument('--gb-n-estimators', type=int, default=40,
                        help='GBReweighter number of boosting stages. Default: 40')

    parser.add_argument('--gb-learning-rate', type=float, default=0.2,
                        help='GBReweighter learning rate. Default: 0.2')

    parser.add_argument('--gb-max-depth', type=int, default=3,
                        help='GBReweighter maximum tree depth. Default: 3')

    parser.add_argument('--gb-min-samples-leaf', type=int, default=200,
                        help='GBReweighter minimum events per terminal tree leaf. Default: 200')

    parser.add_argument('--gb-loss-regularization', type=float, default=5.0,
                        help='GBReweighter loss regularization. Larger is smoother. Default: 5.0')

    parser.add_argument('--gb-subsample', type=float, default=0.5,
                        help='GBReweighter stochastic subsample fraction. Default: 0.5')

    parser.add_argument('--gb-sweight-mode', choices=['signed', 'clip-zero'], default='signed',
                        help=('How to pass data sWeights to GBReweighter. signed keeps negative event sWeights '
                              'and best mimics the original event-level treatment; clip-zero sets negative '
                              'event sWeights to zero if the GB training backend cannot handle signed weights. '
                              'Default: signed'))

    parser.add_argument('--clip-min', type=float, default=None,
                        help='optional minimum for exported hep_ml correction histogram. Default: no clipping')

    parser.add_argument('--clip-max', type=float, default=None,
                        help='optional maximum for exported hep_ml correction histogram. Default: no clipping')

    return parser.parse_args()


###########
# Helpers #
###########

def unique_preserve_order(items):
    return list(dict.fromkeys(items))


def load_brs(ntp, tree, add_brs=None, extra_brs=None):
    br_names = [] if not add_brs else deepcopy(add_brs)
    for r in REWEIGHT_PROCEDURE.values():
        br_names += r.vars
    if extra_brs:
        for var in extra_brs:
            br_names += [var]

    br_names = unique_preserve_order(br_names)
    return concatenate([f'{i}:{tree}' for i in ntp], br_names, library='np')


def gen_cut_original_upper_only(brs, rule, extraCuts=None):
    """
    Original gen_weights.py behavior: cut only the upper edge of each
    reweighting variable, plus extraCuts. This is used for previous-step
    lookup compatibility.
    """
    cuts = []
    for idx, _ in enumerate(rule.vars):
        var = rule.vars[idx]
        cuts.append(np.asarray(brs[var]) < rule.range[idx][1])
        cuts.append(np.isfinite(np.asarray(brs[var], dtype=np.float64)))

    if extraCuts:
        for var, val in extraCuts.items():
            cuts.append(np.asarray(brs[var]) > val)
            cuts.append(np.isfinite(np.asarray(brs[var], dtype=np.float64)))

    return np.logical_and.reduce(cuts)


def gen_cut_in_hist_range(brs, rule, extraCuts=None):
    """
    Explicit in-range cut for hep_ml training. The original code only cut the
    upper edge, but np.histogram2d ignored values below the lower edge anyway.
    For hep_ml we must remove below-range events explicitly, otherwise they
    would enter the training.
    """
    cuts = []
    for idx, var in enumerate(rule.vars):
        lo, hi = rule.range[idx]
        vals = np.asarray(brs[var], dtype=np.float64)
        cuts.append(np.isfinite(vals))
        cuts.append(vals >= lo)
        cuts.append(vals < hi)  # ROOT-compatible right edge

    if extraCuts:
        for var, val in extraCuts.items():
            vals = np.asarray(brs[var], dtype=np.float64)
            cuts.append(np.isfinite(vals))
            cuts.append(vals > val)

    return np.logical_and.reduce(cuts)


def apply_mask(brs, mask):
    return {k: np.asarray(v)[mask] for k, v in brs.items()}


def make_edges(rule):
    return [np.linspace(rr[0], rr[1], int(nb) + 1) for nb, rr in zip(rule.bins, rule.range)]


def stack_vars(brs, vars_):
    return np.vstack([np.asarray(brs[v], dtype=np.float64) for v in vars_]).T


def product_weights(brs, names):
    if not names:
        raise RuntimeError('No MC weight branches were provided')

    weights = np.ones(len(brs[names[0]]), dtype=np.float64)
    for name in names:
        weights *= np.asarray(brs[name], dtype=np.float64)
    return weights


def get_weights(brs_dict, histo_raw, rule_prev):
    """
    Same previous-step lookup convention as the original gen_weights.py:
      - pad the histogram with zeros
      - np.digitize underflow/overflow goes to the zero-padded bins
      - multiply by original upper-edge cut
    """
    histo, *bin_specs = histo_raw
    brs = [np.asarray(brs_dict[i], dtype=np.float64) for i in rule_prev.vars]
    histo_padded = np.pad(histo, tuple((1, 1) for _ in range(histo.ndim)))
    bin_idx = tuple(np.digitize(br, spec) for br, spec in zip(brs, bin_specs))

    cut_prev = gen_cut_original_upper_only(brs_dict, rule_prev)
    return histo_padded[bin_idx] * cut_prev


def histogram_raw(brs, rule, weights=None):
    vals = [np.asarray(brs[v], dtype=np.float64) for v in rule.vars]
    X = np.vstack(vals).T
    return np.histogramdd(X, bins=make_edges(rule), weights=weights)


def make_raw_ratio_like_original(h_data_raw, h_mc_raw):
    """Compute the original direct ratio diagnostic, including nan/inf handling."""
    with np.errstate(divide='ignore', invalid='ignore'):
        h_tmp = (h_data_raw[0] / h_mc_raw[0]) * (
            np.sum(h_mc_raw[0]) / np.sum(h_data_raw[0])
        )
    h_tmp_histo = (h_tmp, *h_data_raw[1:])
    h_ratio_histo = np.nan_to_num(h_tmp, nan=0.0, posinf=1.0, neginf=1.0)
    h_ratio = (h_ratio_histo, *h_data_raw[1:])
    return h_tmp_histo, h_ratio


def normalize_sum_to_one(w, label):
    w = np.asarray(w, dtype=np.float64)
    s = np.sum(w)
    if not np.isfinite(s) or s <= 0:
        raise RuntimeError(f'{label}: non-positive/non-finite sum of weights: {s}')
    return w / s


def clean_for_hepml_training(X, w, label, allow_negative=True):
    """
    Keep negative sWeights, matching the original event-level treatment.
    For MC, this function also keeps zero weights, because the original code
    did not remove them; zero-weight events simply contribute no density.
    """
    X = np.asarray(X, dtype=np.float64)
    w = np.asarray(w, dtype=np.float64)

    mask = np.all(np.isfinite(X), axis=1) & np.isfinite(w)
    if not allow_negative:
        mask &= (w >= 0)

    print(f'{label}: before training clean = {len(w)}, after = {np.sum(mask)}')
    if np.sum(mask) == 0:
        raise RuntimeError(f'{label}: no events left after cleaning')

    return X[mask], w[mask], mask


def make_reweighter(args):
    if args.method == 'bins':
        model = reweight.BinsReweighter(
            n_bins=args.n_bins,
            n_neighs=args.n_neighs,
        )
        model.min_in_the_bin = args.bins_min_in_bin
        print(
            f'Using BinsReweighter: '
            f'n_bins={args.n_bins}, '
            f'n_neighs={args.n_neighs}, '
            f'min_in_the_bin={args.bins_min_in_bin}'
        )
        return model

    if args.method == 'gb':
        return reweight.GBReweighter(
            n_estimators=args.gb_n_estimators,
            learning_rate=args.gb_learning_rate,
            max_depth=args.gb_max_depth,
            min_samples_leaf=args.gb_min_samples_leaf,
            loss_regularization=args.gb_loss_regularization,
            gb_args={'subsample': args.gb_subsample},
        )

    raise RuntimeError(f'Unknown method: {args.method}')


def evaluate_model_on_original_grid(model, rule, clip_min=None, clip_max=None):
    """
    Export the hep_ml model onto the original output histogram grid.
    """
    edges = make_edges(rule)
    centers = [0.5 * (e[:-1] + e[1:]) for e in edges]

    mesh = np.meshgrid(*centers, indexing='ij')
    points = np.vstack([m.reshape(-1) for m in mesh]).T.astype(np.float64)

    vals = np.asarray(model.predict_weights(points), dtype=np.float64)

    # Non-finite values are treated like the original ratio protection.
    vals = np.nan_to_num(vals, nan=0.0, posinf=1.0, neginf=1.0)

    if clip_min is not None or clip_max is not None:
        lo = -np.inf if clip_min is None else clip_min
        hi = np.inf if clip_max is None else clip_max
        vals = np.clip(vals, lo, hi)

    histo = vals.reshape([len(c) for c in centers])
    return histo, *edges


def print_weight_summary(name, w):
    w = np.asarray(w, dtype=np.float64)
    finite = w[np.isfinite(w)]

    print(f'\n{name}')
    print('-' * len(name))
    print(f'entries: {len(w)}')
    print(f'finite:  {len(finite)}')
    if len(finite) == 0:
        return
    print(f'min:     {np.min(finite):.6g}')
    print(f'p01:     {np.percentile(finite, 1):.6g}')
    print(f'median:  {np.median(finite):.6g}')
    print(f'p99:     {np.percentile(finite, 99):.6g}')
    print(f'max:     {np.max(finite):.6g}')
    print(f'sum:     {np.sum(finite):.6g}')
    print(f'n < 0:   {np.sum(finite < 0)}')
    print(f'n == 0:  {np.sum(finite == 0)}')


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()
    ntp = recreate(args.output)
    rules = dict()
    histos = dict()

    print('Loading branches ...')
    brs_data_raw = load_brs(args.dataNtp, args.tree, add_brs=DATA_WTS)
    brs_mc_raw = load_brs(args.mcNtp, args.tree, add_brs=MC_WTS, extra_brs=MC_CUTS)

    for idx, (name, r) in enumerate(REWEIGHT_PROCEDURE.items()):
        print(f'\nProcessing {name} with hep_ml method = {args.method}')
        print(f'  variables: {r.vars}')
        rules[idx] = r

        # For hep_ml, explicitly use the histogram range. This mimics what the
        # old np.histogram2d effectively did: values below/above the range did
        # not contribute to the fixed-bin ratio.
        cut_data = gen_cut_in_hist_range(brs_data_raw, r)
        cut_mc = gen_cut_in_hist_range(brs_mc_raw, r, MC_CUTS)

        brs_data = apply_mask(brs_data_raw, cut_data)
        brs_mc = apply_mask(brs_mc_raw, cut_mc)

        X_data = stack_vars(brs_data, r.vars)
        X_mc = stack_vars(brs_mc, r.vars)

        # Data sWeights: keep negative event weights, like original.
        w_data = np.asarray(brs_data[DATA_WTS[0]], dtype=np.float64)

        # MC base weights exactly as original.
        w_mc_base = product_weights(brs_mc, MC_WTS)

        # Sequential previous-step correction, same convention as original.
        if idx == 0:
            w_mc_final = w_mc_base
        else:
            w_prev = get_weights(brs_mc, histos[idx - 1], rules[idx - 1])
            w_mc_final = w_mc_base * w_prev

        print_weight_summary(f'{name} data weights before hep_ml', w_data)
        print_weight_summary(f'{name} MC weights before hep_ml', w_mc_final)

        # Clean only non-finite values. Keep negative sWeights for data.
        # For MC, keep zero weights to mimic original; reject negative MC weights
        # because hep_ml density denominators are not meaningful if negative.
        X_data_fit, w_data_fit_raw, mask_data_fit = clean_for_hepml_training(
            X_data, w_data, f'{name} data', allow_negative=True
        )
        X_mc_fit, w_mc_fit_raw, mask_mc_fit = clean_for_hepml_training(
            X_mc, w_mc_final, f'{name} MC', allow_negative=False
        )

        # Match original shape-only normalization: the raw ratio was normalized
        # by total MC / total data. Here both samples are normalized to unit sum
        # before estimating the density ratio.
        #
        # For maximum fidelity to the original, keep signed data sWeights.
        # Some GB backends can be less tolerant of negative sample weights. If
        # needed, use --gb-sweight-mode clip-zero as an explicit cross-check;
        # this is less faithful to the original than the default signed mode.
        if args.method == 'gb' and args.gb_sweight_mode == 'clip-zero':
            print(f'{name}: clipping negative data event weights to zero for GB training')
            w_data_for_model = np.maximum(w_data_fit_raw, 0.0)
        else:
            w_data_for_model = w_data_fit_raw

        w_data_fit = normalize_sum_to_one(w_data_for_model, f'{name} data')
        w_mc_fit = normalize_sum_to_one(w_mc_fit_raw, f'{name} MC')

        model = make_reweighter(args)
        model.fit(
            original=X_mc_fit,
            original_weight=w_mc_fit,
            target=X_data_fit,
            target_weight=w_data_fit,
        )

        # Export hep_ml correction on the original output grid.
        h_ratio_hepml = evaluate_model_on_original_grid(
            model, r, clip_min=args.clip_min, clip_max=args.clip_max
        )
        histos[idx] = h_ratio_hepml

        # Save raw diagnostic histograms. Data bin-level negative yields are
        # clipped to zero, exactly as in the original code.
        h_data_raw = histogram_raw(brs_data, r, weights=w_data)
        h_data_raw[0][h_data_raw[0] < 0] = 0

        h_mc_no_wt = histogram_raw(brs_mc, r, weights=None)
        h_mc_raw = histogram_raw(brs_mc, r, weights=w_mc_final)

        h_tmp_histo, h_ratio_raw = make_raw_ratio_like_original(h_data_raw, h_mc_raw)

        print_weight_summary(f'{name} hep_ml output ratio values', h_ratio_hepml[0].ravel())
        print_weight_summary(f'{name} old-style raw ratio values', h_ratio_raw[0].ravel())

        # Save histograms. The final name is the hep_ml correction. Diagnostics
        # preserve the original output names.
        ntp[f'{name}_data_raw'] = h_data_raw
        ntp[f'{name}_mc_raw'] = h_mc_raw
        ntp[f'{name}_mc_no_wt'] = h_mc_no_wt
        ntp[f'{name}_nan_kept'] = h_tmp_histo
        ntp[f'{name}_raw_ratio'] = h_ratio_raw
        ntp[name] = h_ratio_hepml

    print(f'\nWrote {args.output}')

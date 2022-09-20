#!/usr/bin/env python
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Sep 20, 2022 at 12:51 PM -0400
#
# Description: plot fit variables w/ w/o decay-in-flight smearing

import mplhep
import numpy as np

from argparse import ArgumentParser

from pyTuplingUtils.utils import gen_histo_stacked_baseline, gen_histo
from pyTuplingUtils.plot import (
    plot_prepare,
    plot_histo,
    ax_add_args_histo,
    plot_step,
    ax_add_args_step,
)
from pyTuplingUtils.boolean.eval import BooleanEvaluator


################
# Configurable #
################

DEFAULT_COLORS = ["#00429d", "#5585b7", "#8bd189", "#d15d5f", "#93003a"]
DEFAULT_OVERALL_COLORS = ["black", "red"]
LEGEND_LOC = {"q2": "upper left", "mm2": "upper left", "el": "upper right"}

MISID_TAGS = {
    "is_misid_pi": r"$\pi$ tag",
    "is_misid_k": r"$K$ tag",
    "is_misid_p": r"$p$ tag",
    "is_misid_e": r"$e$ tag",
    "is_misid_g": r"ghost tag",
}
PLOT_VARS = {
    "mm2": r"$m_{miss}^2$ [GeV$^2$]",
    "q2": r"$q^2$ [GeV$^2$]",
    "el": r"$E_l$ [GeV]",
}
PLOT_VARS_SMR_SUF = ['_smr_pi', '_smr_k', '_no_smr']

PLOT_RANGE = {"q2": [-0.4, 12.6], "mm2": [-2.0, 10.9], "el": [0.1, 2.65]}
SMR_WTS = [["", "_smr_pi", "_smr_k"], ["_no_smr", "_smr_pi", "_smr_k"]]

MISID_WTS = {
    'q2': 'wmis*skim_global_ok',
    'q2_smr_pi': 'wmis_smr_pi*skim_global_ok_smr_pi',
    'q2_smr_k': 'wmis_smr_k*skim_global_ok_smr_k',
    'q2_no_smr': 'wmis_no_smr*skim_global_ok_no_smr'
}

for br in ['mm2', 'el']:
    for s in [''] + PLOT_VARS_SMR_SUF:
        name = f'{br}{s}' if s != '' else br
        name_ref = f'q2{s}' if s != '' else 'q2'
        MISID_WTS[name] = MISID_WTS[name_ref]


#######################
# Command line helper #
#######################


def parse_input():
    parser = ArgumentParser(
        description="plot fit variables w/ w/o decay-in-flight smearing."
    )

    parser.add_argument("-i", "--input", nargs="+", help="specify main input ntuple.")
    parser.add_argument("-o", "--output", help="specify output folder.")
    parser.add_argument("-t", "--tree", help="specify tree name.", default="tree")

    parser.add_argument("--bins", help="specify number of bins.", type=int, default=120)

    parser.add_argument(
        "-p", "--prefix", help="specify plot filename prefix.", default="D0"
    )

    parser.add_argument(
        "--title", help="specify plot title.", default=r"2016 misID, $D^0$"
    )

    parser.add_argument(
        "--ylabel", help="specify plot y label.", default="Number of events"
    )

    parser.add_argument(
        "--show-title",
        nargs="+",
        type=int,
        default=[1, 0, 0],
        help="control display of title for each individual plot.",
    )

    parser.add_argument(
        "--show-legend",
        nargs="+",
        type=int,
        default=[1, 0, 0],
        help="control display of legend for each individual plot.",
    )

    return parser.parse_args()


###########
# Helpers #
###########


def plot_comp(
    histos,
    legends,
    title,
    xlabel,
    ylabel,
    output_dir,
    output_filename,
    legend_loc="upper left",
    show_title=True,
    show_legend=True,
    suffix="pdf",
    colors=DEFAULT_COLORS,
):
    data = [h[0] for h in histos]
    binspecs = [h[1] for h in histos]
    baselines = gen_histo_stacked_baseline(data)

    plotters = []
    for lbl, hist, bins, bot, clr in zip(legends, data, binspecs, baselines, colors):
        add_args = ax_add_args_histo(lbl, clr, baseline=bot)
        plotters.append(
            lambda fig, ax, b=bins, h=hist + bot, add=add_args: plot_histo(
                b, h, add, figure=fig, axis=ax, show_legend=False
            )
        )

    title = title if show_title else "    "
    fig, ax, _ = plot_prepare(
        xlabel=xlabel, ylabel=ylabel, title=title, show_legend=False
    )
    for p in plotters:
        p(fig, ax)

    if show_legend:
        handles, leg_lbls = ax.get_legend_handles_labels()
        ax.legend(
            handles[::-1], leg_lbls[::-1], numpoints=1, loc=legend_loc, frameon="true"
        )

    fig.savefig(f"{output_dir}/{output_filename}.{suffix}")


def plot_overall(
    histos,
    legends,
    title,
    xlabel,
    ylabel,
    output_dir,
    output_filename,
    legend_loc="upper left",
    show_title=True,
    show_legend=True,
    suffix="pdf",
    colors=DEFAULT_OVERALL_COLORS,
):
    data = [h[0] for h in histos]
    binspecs = [h[1] for h in histos]

    plotters = []
    for lbl, hist, bins, clr in zip(legends, data, binspecs, colors):
        add_args = ax_add_args_step(lbl, clr)
        plotters.append(
            lambda fig, ax, b=bins, h=hist, add=add_args: plot_step(
                b, h, add, figure=fig, axis=ax, show_legend=False
            )
        )

    title = title if show_title else "    "
    fig, ax, _ = plot_prepare(
        xlabel=xlabel, ylabel=ylabel, title=title, show_legend=False
    )
    for p in plotters:
        p(fig, ax)

    if show_legend:
        handles, leg_lbls = ax.get_legend_handles_labels()
        ax.legend(
            handles[::-1], leg_lbls[::-1], numpoints=1, loc=legend_loc, frameon="true"
        )

    fig.savefig(f"{output_dir}/{output_filename}.{suffix}")


########
# Main #
########

if __name__ == "__main__":
    mplhep.style.use("LHCb2")
    args = parse_input()
    reader = BooleanEvaluator(args.input, args.tree)


    for br_name, show_title, show_legend in zip(
        PLOT_VARS, args.show_title, args.show_legend
    ):
        histos_misid = []
        histos_smr = []
        data_range = PLOT_RANGE[br_name]

        for cut_tag in MISID_TAGS:
            # unsmeared:
            expr_wt_unsmr = f'{cut_tag}*{MISID_WTS[br_name]}'
            br = reader.eval(br_name)
            wt_unsmr = reader.eval(expr_wt_unsmr)

            histos_misid.append(
                gen_histo(
                    br,
                    args.bins,
                    data_range=data_range,
                    weights=wt_unsmr,
                )
            )

            # smeared
            tmp_histos = []
            for br_name_suf in PLOT_VARS_SMR_SUF:
                br_name_smr = f'{br_name}{br_name_suf}'
                if 'no_smr' in br_name_smr:
                    br_name_smr = br_name
                expr_wt_smr = f'{cut_tag}*{MISID_WTS[br_name_smr]}'

                br_smr = reader.eval(br_name_smr)
                wt_smr = reader.eval(expr_wt_smr)
                tmp_histos.append(
                    gen_histo(
                        br_smr,
                        args.bins,
                        data_range=data_range,
                        weights=wt_smr,
                    )
                )
            merged_tmp_histo = np.add.reduce([h[0] for h in tmp_histos])
            histos_smr.append((merged_tmp_histo, tmp_histos[0][1]))

        xlabel = PLOT_VARS[br_name]

        # unsmeared, w/ misID weights
        plot_comp(
            histos_misid,
            MISID_TAGS.values(),
            f"{args.title} (misID weighted)",
            xlabel,
            args.ylabel,
            args.output,
            f"{args.prefix}_{br_name}",
            legend_loc=LEGEND_LOC[br_name],
            show_title=show_title,
            show_legend=show_legend,
        )

        # smeared, w/ misID weights
        plot_comp(
            histos_smr,
            MISID_TAGS.values(),
            f"{args.title} (misID weighted smeared)",
            xlabel,
            args.ylabel,
            args.output,
            f"{args.prefix}_{br_name}_smr",
            legend_loc=LEGEND_LOC[br_name],
            show_title=show_title,
            show_legend=show_legend,
        )

        # shape comparison
        # NOTE: The overall number of event is NOT guaranteed to conserve,
        #       as after smearing, some of the events might fall out of the
        #       fit variable acceptance cut
        merged_histo_misid = (
            np.add.reduce([h[0] for h in histos_misid]),
            histos_misid[0][1],
        )
        merged_histo_smr = (
            np.add.reduce([h[0] for h in histos_smr]),
            histos_smr[0][1],
        )
        plot_overall(
            [merged_histo_misid, merged_histo_smr],
            ["unsmeared", "smeared"],
            f"{args.title} (misID unsmeared/smeared comparison)",
            xlabel,
            args.ylabel,
            args.output,
            f"{args.prefix}_{br_name}_comp",
            legend_loc=LEGEND_LOC[br_name],
            show_title=show_title,
            show_legend=show_legend,
        )

#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Shift negative efficiencies to a value between [0, 1]

import numpy as np
import os.path as op
import shutil as sh

from argparse import ArgumentParser
from itertools import product
from glob import glob
from os import makedirs, remove

from scipy.special import erf, erfinv

import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True  # Don't hijack argparse!
ROOT.PyConfig.DisableRootLogon = True  # Don't read .rootlogon.py

from ROOT import TFile


#################################
# Command line arguments parser #
#################################


def parseInputs():
    parser = ArgumentParser(
        description="Shift negative efficiencies to a value between [0, 1]."
    )

    parser.add_argument("input", help="specify input folder containing eff ntuples.")
    parser.add_argument("output", help="specify output folder.")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase verbosity."
    )

    return parser.parse_args()


###########
# Helpers #
###########


def getHistoBinIdxFlattened(histo):
    if "TH1" in str(type(histo)):
        nbinsX = histo.GetNbinsX()
        return [(i,) for i in range(1, nbinsX + 1)]

    if "TH2" in str(type(histo)):
        nbinsX = histo.GetNbinsX()
        nbinsY = histo.GetNbinsY()
        return list(product(range(1, nbinsX + 1), range(1, nbinsY + 1)))

    if "TH3" in str(type(histo)):
        nbinsX = histo.GetNbinsX()
        nbinsY = histo.GetNbinsY()
        nbinsZ = histo.GetNbinsZ()
        return list(
            product(range(1, nbinsX + 1), range(1, nbinsY + 1), range(1, nbinsZ + 1))
        )

    return []


def shiftEff(idx, mean, std, badErrThresh=0.2, verbose=False):
    zero = 1e-12

    if std <= zero:
        shifted = mean
    else:
        half = 0.5 * (
            erf((1 - mean) / (std * np.sqrt(2))) + erf((0 - mean) / (std * np.sqrt(2)))
        )
        shifted = erfinv(half) * std * np.sqrt(2) + mean

    bad = False
    if shifted <= zero:
        bad = True
        print(f"    URGENT: Shifted mean ({shifted}) < 0 for {idx}!")
        shifted = zero

    if abs(std) > badErrThresh:
        bad = True
        print(f"    WARNING: Very large std: {std} in {idx}!")

    if mean <= zero or mean > 1:
        bad = True
        print(f"    WARNING: Raw mean ({mean}) not in [0, 1] for {idx}!")
        if abs(mean) <= zero:
            mean = zero

    if max(abs(shifted / mean), abs(mean / shifted)) > 5:
        bad = True
        print(
            f"    WARNING: Raw ({mean}) and shifted ({shifted}) are very different for {idx}!"
        )

    if bad or verbose:
        print(f"      {idx}: Raw: {mean:.7f} ± {std:.7f}. Shifted: {shifted:.7f}")

    return shifted


########
# Main #
########

if __name__ == "__main__":
    args = parseInputs()
    ntps = glob(f"{args.input}/*.root")

    if args.input == args.output:
        print("Can't reuse input folder as output folder!")
        exit(1)

    if op.isdir(args.output):
        print(f"{args.output} already exist! Removing it...")
        sh.rmtree(args.output, ignore_errors=True)
    makedirs(args.output)

    for n in ntps:
        print(f"Working on {n}...")
        inputNtp = TFile.Open(n, "read")
        outputPath = f"{args.output}/{op.basename(n)}"

        empty = True
        for h in inputNtp.GetListOfKeys():
            name = h.GetName()
            if name != "eff":
                print(f"  WARNING: Skipping {name}")
                continue

            histo = inputNtp.Get(name)
            binIdxes = getHistoBinIdxFlattened(histo)
            if not binIdxes:
                continue

            print(f"  Handling {name}")
            outputNtp = TFile.Open(outputPath, "update")
            for i in binIdxes:
                idx = histo.GetBin(*i)

                mean = histo.GetBinContent(idx)
                std = histo.GetBinError(idx)

                meanShifted = shiftEff(idx, mean, std, verbose=args.verbose)
                histo.SetBinContent(idx, meanShifted)
            histo.Write()
            empty = False
            outputNtp.Close()

        if empty:
            try:
                remove(outputPath)
            except FileNotFoundError:
                pass

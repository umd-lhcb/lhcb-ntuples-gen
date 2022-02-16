#!/usr/bin/env python
#
# Description: Plot the following form-factor related figures
#              - q2, normalized
#              - FF weights
#              - line shapes of various D**, normalized

import os
import sys
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt

from os.path import isdir, basename
from glob import glob
from numpy import logical_and as AND
from numpy import arange

from pyTuplingUtils.io import read_branches, read_branch
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.plot import (
    plot_step, plot_fill, plot_top,
    ax_add_args_step, ax_add_args_fill
)


###########
# Helpers #
###########

def runCmd(cmd):
    print('  \033[92m'+cmd+'\033[0m')
    os.system(cmd)


ntpInFolder = '../../gen/rdx-ntuple-run2-mc-dss'

if not isdir(ntpInFolder):
    print(f'The ntuple folder {ntpInFolder} does not exist!')
    print('Run "make rdx-ntuple-run2-mc-dss" in project root to generate the ntuples first!')
    sys.exit(1)

ntpsIn = glob(f'{ntpInFolder}/ntuple/D0*.root')


def findMcInfo(name):
    particle, _, _, decayMode, _, polarity = \
        basename(name).replace('.root', '').split('--')
    return particle, decayMode, polarity


def findLep(truthmatch):
    if truthmatch % 10 == 1:
        return r'\tau \nu'
    return r'\mu \nu'


def findDss(truthmatch):
    mapDst = {
        11: r'D^{*0}_0',
        12: r'D^{0}_1',
        13: r"D^{'0}_1",
        14: r'D^{*0}_2',
        21: r'D^{*+}_0',
        22: r'D^{+}_1',
        23: r"D^{'+}_1",
        24: r'D^{*+}_2',
    }

    if (truthmatch // 10) not in mapDst:
        return 'D_{unknown}'

    return mapDst[truthmatch // 10]


def findDssInNtp(ntp, thresh=50000):
    truthMatch = read_branch(ntp, 'tree', 'truthmatch')
    particlesDss = np.unique(truthMatch)
    return particlesDss[particlesDss < thresh]


#########
# Plots #
#########

defaultBinning = 25


def plotBaseName(ntpName):
    return '_'.join(findMcInfo(ntpName))


def plotNoComp(ntpIn, br, output, label, xlabel, cut,
               normalize=False, title=None):
    cmd = f'plotbr -n {ntpIn}/tree -b {br} -o {output} --labels "{label}" -XL "{xlabel}" --cuts "{cut}"'

    if normalize:
        cmd += ' --normalize -YL "Normalized"'

    if title:
        cmd += f' --title "{title}"'

    runCmd(cmd)


def plotComp(ntpIn, br, output, title, xlabel, cut,
             normalize=True, wtBr='wff', xRange=None,
             labels=['ISGW2', 'BLR'], yscale='linear'):
    labels = ' '.join([f'"{i}"' for i in labels])
    weights = ' '.join(['None', wtBr])
    cmd = fr'''
        plotbr -n {ntpIn}/tree -b {br} {br} -o {output} --labels {labels} -XL "{xlabel}" \
        --cuts "{cut}" "{cut}" --weights {weights} \
        --title "{title}" --yscale {yscale}'''

    if normalize:
        cmd += ' --normalize -YL "Normalized"'

    if xRange:
        xRange = ' '.join([str(i) for i in xRange])
        cmd += f' -XD {xRange}'

    runCmd(cmd)


def findNormFac(br, wt=None, bins=defaultBinning, xRange=None):
    wt = np.ones(br.size) if wt is None else wt
    histo, _ = gen_histo(br, bins=bins, data_range=xRange, weights=wt)
    histoNorm, _ = gen_histo(br, bins=bins, data_range=xRange, weights=wt,
                             density=True)
    return np.sum(histo) / np.sum(histoNorm)


def findErr(br, binBdy, wt=None, xRange=None, normalize=True):
    binIdx = np.digitize(br, binBdy)
    wt = np.ones(br.size) if wt is None else wt

    normFac = findNormFac(br, wt, len(binBdy)-1, xRange) if normalize else 1
    err = []
    for i in range(1, len(binBdy)):
        binErr = np.sqrt(np.sum(np.power(wt[binIdx == i], 2))) / normFac
        err.append(binErr)
    return np.array(err)


def plotRaw(br, wt, output, title, xlabel,
            normalize=True, xRange=None, xLim=None, yLim=None,
            labels=['ISGW2', 'BLR'], yscale='log',
            colors=['black', 'crimson'], binning=defaultBinning):
    # Generated the unweighted histo
    histoOrig, bins = gen_histo(br, bins=binning, data_range=xRange,
                                density=normalize)
    errOrig = findErr(br, bins, None, xRange, normalize)
    intvOrig = (histoOrig - errOrig, histoOrig + errOrig)

    # Compute the weighted Poisson variance
    histoWt, _ = gen_histo(br, bins=binning, data_range=xRange, weights=wt,
                           density=normalize)
    errWt = findErr(br, bins, wt, xRange, normalize)
    intvWt = (histoWt - errWt, histoWt + errWt)

    # Prepare for plot
    top_plotters = []

    stepArgsOrig = ax_add_args_step(labels[0], colors[0])
    top_plotters.append(
        lambda fig, ax, b=bins, h=histoOrig, add=stepArgsOrig:
        plot_step(b, h, add, figure=fig, axis=ax, show_legend=False))

    errArgsOrig = ax_add_args_fill(colors[0], alpha=0.4)
    top_plotters.append(
        lambda fig, ax, b=bins, y=intvOrig, add=errArgsOrig:
        plot_fill(b, y, add, figure=fig, axis=ax, show_legend=False))

    stepArgsWt = ax_add_args_step(labels[1], colors[1])
    top_plotters.append(
        lambda fig, ax, b=bins, h=histoWt, add=stepArgsWt:
        plot_step(b, h, add, figure=fig, axis=ax, show_legend=False))

    errArgsWt = ax_add_args_fill(colors[1], alpha=0.4)
    top_plotters.append(
        lambda fig, ax, b=bins, y=intvWt, add=errArgsWt:
        plot_fill(b, y, add, figure=fig, axis=ax, show_legend=False))

    # Plot
    ylabel = 'Normalized' if normalize else 'Number of events'

    fig, *_ = plot_top(top_plotters, title=title, xlabel=xlabel, ylabel=ylabel,
                       yscale=yscale, xlim=xLim, ylim=yLim)
    fig.savefig(output)


# q2Min = arange(0.05, 8, 0.1)
q2Min = arange(0, 8, 0.1)
q2Max = q2Min + 0.1
plotBinning = 75

dataRange = {
    # 230: (2150, 3150),
    230: (2150, 5150),
    # 230: (2150, 3450),
}
# plotXRange = None
# plotYRange = None
# plotXRange = (2050, 3500)
# plotYRange = (5e-6, 5e-3)
plotXRange = (2000, 5400)
plotYRange = (1e-6, 5e-3)

particles = [
    # 210,
    # 220,
    230,
    # 240,
]


debugMode = len(sys.argv) == 1
print(f'Running in debug mode or not: {debugMode}')


for ntp in ntpsIn:
    hep.style.use('LHCb2')

    plotCommonName = plotBaseName(ntp)

    # particles = findDssInNtp(ntp)

    weight, tm, q2True, mass = read_branches(
        ntp, 'tree', ['wff', 'truthmatch', 'q2_true', 'ff_d_mass'])
    # massB = read_branch(ntp, 'tree', 'ff_b_mass')
    # rFac = mass / massB

    for p in particles:
        subplotCommonName = plotCommonName + f'_{p}'

        pNum = weight[tm == p].size
        pWeight = weight[tm == p].sum()
        pMass = mass[tm == p]
        xMin, xMax = pMass.min(), pMass.max()
        labels = [
            f'ISGW2 ({pNum})',
            f'BLR ({pWeight:.1f})'
        ]

        label = fr'\$B \\rightarrow {findDss(p)} {findLep(p)}$'
        plotNoComp(ntp, 'wff', subplotCommonName+'_wff.png',
                   label, 'FF weight', f'truthmatch == {p}',
                   title=f'ISGW2/BLR = {pNum}/{pWeight:.1f} = {pNum/pWeight:.2f}'
                   )
        plotComp(ntp, 'q2', subplotCommonName+'_q2.png', label,
                 r'\$q^2$ [GeV\$^2$]', f'truthmatch == {p}', labels=labels)
        plotComp(ntp, 'q2_true', subplotCommonName+'_q2_true.png', label,
                 r'True \$q^2$ [GeV\$^2$]', f'truthmatch == {p}', labels=labels)
        plotComp(ntp, 'ff_d_mass', subplotCommonName+'_ff_d_mass.png',
                 label, fr'\${findDss(p)}$ true mass [MeV\$^2$]',
                 f'truthmatch == {p}', labels=labels, xRange=[xMin, xMax])

        for qLow, qHigh in zip(q2Min, q2Max):
            labelTmp = fr'$B \rightarrow {findDss(p)} {findLep(p)}$, ${qLow:.2f} < q^2_{{true}} < {qHigh:.2f}$ GeV$^2$'

            if p in dataRange:
                xMin, xMax = dataRange[p]

            sel = AND(AND(tm == p, q2True > qLow), q2True < qHigh)
            pNum = weight[sel].size
            pWeight = weight[sel].sum()
            labels = [
                f'ISGW2 ({pNum})',
                f'BLR ({pWeight:.1f})'
            ]

            if pNum == 0:
                continue

            filename = \
                subplotCommonName+f'_ff_d_mass_{qLow:.2f}_{qHigh:.2f}.png'
            print(f'Generating {filename}...')
            plotRaw(mass[sel], weight[sel], filename,
                    labelTmp, fr'${findDss(p)}$ true mass [MeV$^2$]',
                    xRange=[xMin, xMax], xLim=plotXRange, yLim=plotYRange,
                    labels=labels, binning=plotBinning)

            # Add an additional R factor as suggested by Phoebe
            # filenameR = \
            #     subplotCommonName+f'_ff_d_mass_{qLow:.1f}_{qHigh:.1f}_rfac.png'
            # print(f'Generating {filenameR}...')
            # rWt = weight[sel] * rFac[sel]
            # plotRaw(mass[sel], rWt, filenameR,
            #         labelTmp+' add. $R$ factor',
            #         fr'${findDss(p)}$ true mass [MeV$^2$]',
            #         xRange=[xMin, xMax], labels=labels)

            if debugMode:
                sys.exit(1)

        # Clear plot in memory
        plt.close('all')

#!/usr/bin/env python
#
# Description: Plot the following form-factor related figures
#              - q2, normalized
#              - FF weights
#              - line shapes of various D**, normalized

import os
import sys
import uproot
import numpy as np
import mplhep as hep

from os.path import isdir, basename
from glob import glob
from numpy import logical_and as AND
from numpy import arange

from pyTuplingUtils.io import read_branch
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

ntpsIn = glob(f'{ntpInFolder}/ntuple/*.root')


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


def plotRaw(br, wt, output, title, xlabel,
            normalize=True, xRange=None,
            labels=['ISGW2', 'BLR'], yscale='log',
            colors=['black', 'crimson']):
    # Generated the unweighted histo
    histoOrig, bins = gen_histo(br, bins=25, data_range=xRange)
    errOrig = np.sqrt(histoOrig)
    intvOrig = (histoOrig - errOrig, histoOrig + errOrig)

    # Compute the weighted Poisson variance
    binIdx = np.digitize(wt, bins)
    histoWt, _ = gen_histo(br, bins=25, data_range=xRange, weights=wt)
    errWt = []
    for i in range(1, len(bins)):
        binErr = np.sqrt(np.sum(np.power(wt[binIdx == i], 2)))
        errWt.append(binErr)
    errWt = np.array(errWt)
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
                       yscale=yscale)
    fig.savefig(output)


q2Min = arange(0, 8, 0.1)
q2Max = q2Min + 0.1

plotRange = {
    230: (2150, 3150)
}


debugMode = len(sys.argv) == 1
print(f'Running in debug mode or not: {debugMode}')


for ntpName in ntpsIn:
    hep.style.use('LHCb2')

    plotCommonName = plotBaseName(ntpName)

    ntp = uproot.open(ntpName)
    particles = findDssInNtp(ntp)
    weight = read_branch(ntp, 'tree', 'wff')
    mass = read_branch(ntp, 'tree', 'ff_d_mass')
    tm = read_branch(ntp, 'tree', 'truthmatch')
    q2_true = read_branch(ntp, 'tree', 'q2_true')

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
        plotNoComp(ntpName, 'wff', subplotCommonName+'_wff.png',
                   label, 'FF weight', f'truthmatch == {p}',
                   title=f'ISGW2/BLR = {pNum}/{pWeight:.1f} = {pNum/pWeight:.2f}'
                   )
        plotComp(ntpName, 'q2', subplotCommonName+'_q2.png', label,
                 r'\$q^2$ [GeV\$^2$]', f'truthmatch == {p}', labels=labels)
        plotComp(ntpName, 'q2_true', subplotCommonName+'_q2_true.png', label,
                 r'True \$q^2$ [GeV\$^2$]', f'truthmatch == {p}', labels=labels)
        plotComp(ntpName, 'ff_d_mass', subplotCommonName+'_ff_d_mass.png',
                 label, fr'\${findDss(p)}$ true mass [MeV\$^2$]',
                 f'truthmatch == {p}', labels=labels, xRange=[xMin, xMax])

        for qLow, qHigh in zip(q2Min, q2Max):
            labelTmp = fr'$B \rightarrow {findDss(p)} {findLep(p)}$, ${qLow:.1f} < q^2_{{true}} < {qHigh:.1f}$ GeV$^2$'

            if p in plotRange:
                xMin, xMax = plotRange[p]

            sel = AND(AND(tm == p, q2_true > qLow), q2_true < qHigh)
            pNum = weight[sel].size
            pWeight = weight[sel].sum()
            labels = [
                f'ISGW2 ({pNum})',
                f'BLR ({pWeight:.1f})'
            ]

            if pNum == 0:
                continue

            filename = \
                subplotCommonName+f'_ff_d_mass_{qLow:.1f}_{qHigh:.1f}.png'
            print(f'Generating {filename}...')
            plotRaw(mass[sel], weight[sel], filename,
                    labelTmp, fr'${findDss(p)}$ true mass [MeV$^2$]',
                    xRange=[xMin, xMax], labels=labels)

            if debugMode:
                sys.exit(1)

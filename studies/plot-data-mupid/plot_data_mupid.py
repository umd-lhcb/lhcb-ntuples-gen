#import os
#imort copy
import numpy as np
import matplotlib.pyplot as plt
#import mplhep as hep
import uproot
#import math

from pyTuplingUtils.utils import gen_histo
from uproot.behaviors.TBranch import concatenate

### Helpers

# extract trees
tree = '../../gen/rdx-ntuple-run2-data/ntuple_merged/Dst--22_07_21--std--data--2016--md.root:tree'

# vars to be plotted
vars = ['mu_pid_mu']
ranges = [[-15, 20]]
bins = [70]
x_axes = ['$\mu$ PID$\mu$']
x_labels = [x_axes[0]+'      ']
y_labels = [f'Candidates / {(ranges[0][1]-ranges[0][0])/bins[0]:.2f} {x_labels[-4:-1]}']

# weights
# weights = ['w']

# extract relevants branches from trees
# brs = uproot.concatenate(tree, vars+weights, library='np')
brs = uproot.concatenate(tree, vars, library='np')

# make histograms
h, b = gen_histo(brs[vars[0]], bins[0], data_range=ranges[0])#, weights=brs['w'])
entries = [np.sum(h), 1]

# make the plots
title = f'Run 2 2016 MD Data {x_axes[0]}, $D^*$ Sample, All (Other) Cuts, All Skims'
fig = plt.figure()
ax = fig.add_subplot()
ax.set_title(title, fontsize=10)
ax.set_xlabel(x_labels[0])
ax.set_ylabel(y_labels[0])
ax.set_xlim(ranges[0])
ax.stairs(h, b, label=x_axes[0]+f': {entries[0]}')
ax.legend()
plt.axvline(2, color='r', linestyle='dashed')
fig.set_tight_layout({'pad': 0.0})
fig.savefig('test.pdf')
plt.close(fig)







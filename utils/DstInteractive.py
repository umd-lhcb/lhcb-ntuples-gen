#!/usr/bin/env python
#
# Author: Yipeng Sun <syp at umd dot edu>
# Last Change: Mon Dec 17, 2018 at 11:55 PM -0500

import sys

import GaudiPython as GP
from GaudiConf import IOHelper
from Configurables import DaVinci

DaVinci().DataType = '2012'
DaVinci().Simulation = False

# Pass file to open as first command line argument
inputFiles = [sys.argv[-1]]
IOHelper('ROOT').inputFiles(inputFiles)

appMgr = GP.AppMgr()
evt = appMgr.evtsvc()

appMgr.run(1)
evt.dump()


def nodes(evt, node=None):
    """List all nodes in `evt`"""
    nodenames = []

    if node is None:
        root = evt.retrieveObject('')
        node = root.registry()

    if node.object():
        nodenames.append(node.identifier())
        for l in evt.leaves(node):
            # skip a location that takes forever to load
            # XXX How to detect these automatically??
            if 'Swum' in l.identifier():
                continue

            nodenames += nodes(evt, l)

    else:
        nodenames.append(node.identifier())

    return nodenames


def advance(decision, prefix='Stripping', suffix='Decision'):
    """Advance until stripping decision is true, returns
    number of events by which we advanced"""
    n = 0
    while True:
        appMgr.run(1)

        if not evt['/Event/Rec/Header']:
            print('Reached end of input files')
            break

        n += 1
        dec = evt['/Event/Strip/Phys/DecReports']
        if dec.hasDecisionName('{0}{1}{2}'.format(prefix, decision, suffix)):
            break

    return n

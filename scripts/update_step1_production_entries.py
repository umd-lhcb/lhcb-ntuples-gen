#!/usr/bin/env python3
#
# Author: Alex Fernez
# Take a production folder as input, and update production_summary.yml with the number of entries
# for all tuples (and create this file if it doesn't already exist)
# If files aren't downloaded and not working on glacier, they won't be updated in the yml
# If the user doesn't supply the command line arg (ntuple folder location) correctly, just exit

import os
import os.path as op
from glob import glob
import yaml as yml
import socket
import ROOT
import sys
from tabulate import tabulate
sys.path.insert(1, '../workflows')
from utils import check_ntp_name, download_file
from step1_slim import trees

ROOT.gErrorIgnoreLevel = ROOT.kFatal ## Suppressing output

recount = False # if this is True, recount all jobs; else, if something's already in production summary, skip counting
try_linking = True # if working on glacier, if files are annexed (and not downloaded) in user's directory, try finding them on glacier
print_table = True # print a summary table to stdout

### checks

if len(sys.argv) != 2:
    assert False, 'run script as: update_step1_production_entries.py path_to_step1_production'
root_files = [y for x in os.walk(sys.argv[1]) for y in glob(os.path.join(x[0], '*.root'))]
if len(root_files)==0:
    assert False, 'path to step1 production invalid, no root files found... make sure this is a folder inside ntuples/'
filenames = [rfpath.split('/')[-1] for rfpath in root_files]
for rf in filenames:
    if not len(check_ntp_name(rf)[1])==0: # means no unexpected filename formatting
        assert False, f'{rf} name formatting is unexpected... exiting'

### main code

# at this point, everything should be safe, so go ahead and update/create production_summary.yml
log = f'{sys.argv[1]}/production_summary.yml'
if op.isfile(log):
    with open(log) as f:
        summary = yml.safe_load(f)
else:
    summary = {}

print(f'Updating stats for {sys.argv[1]}...\n')
# use identifiers to partition ntuples
years = ['_2016_', '_2017_', '_2018_', '_Collision16_', '_Collision17_', '_Collision18_']
pols = ['-MagDown', '-MagUp']
modes = ['--std--', '--mu_misid--', '_12573012_', '_11574021_', '_12773410_', '_12573001_', '_11574011_', '_12773400_',
         '_11874430_', '_11874440_', '_12873450_', '_12873460_', '_12675011_', '_11674401_', '_12675402_', '_11676012_', '_12875440_',
         '_13874020_', '_13674000_', '_11894600_', '_11895400_', '_11894200_', '_12893600_', '_12893610_',
         '_11894610_', '_11894210_', '_12895400_', '_12895000_', '_11894400_', '_12895410_']
missing = []
for year in years:
    yr_subset = [rf for rf in root_files if year in rf]
    # need to get rid of aux ntuples and non RD(*)
    yr_subset = [rf for rf in yr_subset if not 'aux' in rf]
    yr_subset = [rf for rf in yr_subset if 'Dst_D0--' in rf]
    if len(yr_subset)==0:
        missing_yr = year.split('_')[1]
        missing.append(missing_yr) # print(f'{missing_yr} not present in {sys.argv[1]}\n')
        continue
    for pol in pols:
        pol_subset = [rf for rf in yr_subset if pol in rf]
        if len(pol_subset)==0:
            missing_pol = pol.split('-')[1]
            missing.append(f"{year.split('_')[1]} {missing_pol}") # print(f"{year.split('_')[1]} {missing_pol} not present in {sys.argv[1]}\n")
            continue
        for mode in modes:
            if '--' in mode: # data should also have Collision for year
                if not '_Collision' in year: continue
            else:
                if '_Collision' in year: continue
            subset = [rf for rf in pol_subset if mode in rf]
            if len(subset) == 0:
                missing_mode = 'NA'
                if '--' in mode: missing_mode = mode.split('--')[1]
                else: missing_mode = mode.split('_')[1]
                missing.append(f"{year.split('_')[1]} {pol.split('-')[1]} {missing_mode}") # print(f"{year.split('_')[1]} {pol.split('-')[1]} {missing_mode} not present in {sys.argv[1]}\n")
                continue
            # now, use more sensible identifiers for log entry
            y, p, m = year, pol, mode
            p = p.split('-')[1]
            if '16' in y: y = '2016'
            elif '17' in y: y = '2017'
            elif '18' in y: y = '2018'
            else: y = 'year_unknown'
            if '--' in m:
                if 'std' in m: m = 'Data'
                elif 'mu_misid' in m: m = 'Fake Mu Data'
                else: m = 'Unknown Data Mode'
            else: m = m.split('_')[1]
            # and create keys if necessary
            if not m in summary: summary[m] = {}
            if not f'{y}-{p}' in summary[m]: summary[m][f'{y}-{p}'] = {}
            job_summary = summary[m][f'{y}-{p}']
            for tree in trees:
                if ('WS' in tree) and (not 'Data' in m): continue # no comb for MC
                entry = f'{trees[tree]}-entries'
                if (entry in job_summary) and (not recount): continue # if already counted don't count again
                print(f'...updating {m} {y} {p} {tree}...')
                chain = ROOT.TChain(tree, 'dummy_name')
                for rf in subset:
                    if not op.isfile(rf): # either doesn't exist, or soft link pointing to empty file (not downloaded annexed file)
                        if socket.gethostbyname(socket.gethostname()) == '10.229.60.85':
                            rf = download_file(rf, suppress_printout=True)
                            if not op.isfile(rf): continue
                    chain.Add(rf) # if at this point, isfile(rf) is True
                entries = chain.GetEntries()
                if entries>0: job_summary[entry] = entries

with open(log, 'w') as f:
    yml.dump(summary,f)


# some MC is reco'd in either D0/D* but not used for those modes: don't list these in the table, for clarity
unused = {'12573012': 'Dst', '12773410': 'Dst', '12573001': 'Dst', '12773400': 'Dst',
          '12675011': 'Dst', '11674401': 'Dst', '12875440': 'Dst', '13874020': 'Dst', '13674000': 'D0',
          '11894600': 'Dst', '11895400': 'Dst', '12893600': 'Dst', '11894200': 'Dst', '12893610': 'Dst',
          '11894610': 'D0', '12895400': 'D0', '11894400': 'D0', '12895410': 'D0', '11894210': 'D0', '12895000': 'D0'}
# useful to order the MC similar to the production request table (I did this on purpose when defining modes)
mode_order = ['Data', 'Fake Mu Data'] + [mode.split('_')[1] for mode in modes[2:]]
def reorganize_summary_for_table(s):
    mc_headers = [f'{yr} {pol} {reco_mode}' for yr in ['2016', '2017', '2018'] for reco_mode in ['D0', 'Dst'] for pol in ['MagDown', 'MagUp'] if (not yr in missing) and (not f'{yr} {pol}' in missing)]
    data_headers = [f'20{yr[-2:]} {pol} {reco_mode}' for yr in ['Collision16', 'Collision17', 'Collision18'] for reco_mode in ['D0', 'D0_BComb', 'Dst', 'Dst_BComb', 'Dst_DstComb'] for pol in ['MagDown', 'MagUp'] if (not yr in missing) and (not f'{yr} {pol}' in missing)]
    mc_rows, data_rows = [], []
    for mode in mode_order:
        if mode not in summary: continue # don't have stats for this mode
        rows = mc_rows
        headers = mc_headers
        if 'Data' in mode:
            rows = data_rows
            headers = data_headers
        rows.append([mode])
        for col in headers:
            fields = col.split()
            yr, pol, reco_mode = fields[0], fields[1], fields[2]
            if 'Data' in mode:
                check_if_missing = f"{yr.replace('20', 'Collision')} {pol} {mode.replace('Fake Mu Data', 'mu_misid').replace('Data', 'std')}"
            else:
                check_if_missing = f'{yr} {pol} {mode}'
            is_missing = False
            for miss in missing:
                if miss in check_if_missing: is_missing = True
            if is_missing: rows[-1].append('NA')
            elif mode in unused and unused[mode] in reco_mode: rows[-1].append('-')
            else: rows[-1].append(summary[mode][f'{yr}-{pol}'][f'{reco_mode}-entries'])

    return (mc_rows, mc_headers), (data_rows, data_headers)

if print_table:
    mc_table, data_table = reorganize_summary_for_table(summary)
    print('\nMC summary:\n')
    print(tabulate(mc_table[0], headers=mc_table[1], tablefmt='github'))
    print('\nData summary:\n')
    print(tabulate(data_table[0], headers=data_table[1], tablefmt='github'))


print(f'\n\nMissing from {sys.argv[1]}:')
for miss in missing: print(miss)
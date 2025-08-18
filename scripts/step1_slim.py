#!/usr/bin/env python3
#
# Author: Alex Fernez
# Take info from user-generated batch_skim.py (which contains association between job ID and job info)
# and call the slimming script here instead (also doing checks on the subjobs: make sure that all
# subjobs have an output, and if not warn the user + keep track of subjobs without output; 
# also make sure that all output is nonempty, and if not warn the user + keep track of these subjobs too)
#
# usage: step1_slim.py <job folder location> <output ntuple dir> <batch_skim.sh with job IDs> <slimming yml>
#                      (-s <spec file for ID to template map> --annex)
# eg. if you want to slim the jobs 100, 101 outputs stored in ../../ntuples_to_merge/ and put the
# output in ../ntuples/0.9.12-all_years, and the corresponding batch_skim.sh produced for these jobs
# is in ../, and you want to use the yml ../postprocess/skims/rdx_mc.yml to define what to be dropped, then run:
# step1_slim.py ../../ntuples_to_merge ../ntuples/0.9.12-all_years ../batch_skim.sh ../postprocess/skims/rdx_mc.yml
#
# beyond putting the slimmed tuples in the correct locations (defined in move_step1_ntuples.py),
# this script will also annex the files (copying them to our server glacier) if requested, keep track
# of the problematic subjobs, and count the number of events in the output (this additional info 
# will be stored in the log, defined below, to be placed in the output ntuples/<tag>/ folder)

from argparse import ArgumentParser
import os
import os.path as op
from os.path import basename, abspath, isdir
from glob import glob
import yaml as yml
import socket
import ROOT
from move_step1_ntuples import pdfFromMCID, cTerm

ROOT.gErrorIgnoreLevel = ROOT.kFatal ## Suppressing output

BASE_PATH = op.abspath(op.dirname(op.abspath(__file__)) + '/..')
SPEC_YML = BASE_PATH + '/../rdx-run2-analysis/fit/spec/histos.yml' # this is an assumption... hopefully a safe one

trees = {'TupleBminus/DecayTree': 'D0', 'TupleBminusWS/DecayTree': 'D0_BComb',
         'TupleB0WSMu/DecayTree': 'Dst_BComb', 'TupleB0/DecayTree': 'Dst', 'TupleB0WSPi/DecayTree': 'Dst_DstComb'}

def parseInput():
    parser = ArgumentParser(description='slim/merge (and keep log of) DaVinci output, and annex to glacier')
    parser.add_argument('jobFolder', help='specify folder with DaVinci job output')
    parser.add_argument('outFolder', help='specify folder where slimmed ntuples should go')
    parser.add_argument('batch_skim', help='specify location of script produced in ganga that contains job info')
    parser.add_argument('slim_config', help='specify slimming yml (defines what can be dropped)')
    parser.add_argument('-s', '--histoSpec', default=SPEC_YML, help='histo spec YAML.')
    parser.add_argument('--annex', default=False, action='store_true', help='specify if you want to automatically annex slimmed tuples')
    return parser.parse_args()

### Helpers

def find_good_and_bad_subjobs(job_folder):
    sjs = [i for i in glob(f'{job_folder}/*') if basename(i).isnumeric()]
    good = {}
    bad = {}
    folders = [i+'/output' for i in sjs]
    for folder in folders:
        sj = folder.split('/')[-2]
        rootfiles = glob(f'{folder}/*.root')
        if len(rootfiles) == 0: bad[sj] = 'Empty'
        elif len(rootfiles) > 1: bad[sj] = 'Too many' # this will actually cause an error later...
        else:
            rootfile = rootfiles[0]
            if os.stat(rootfile).st_size < 500 * 1024: # < 500KB file is suspicious (will cause an error later...)
                bad[sj] = 'Too small'
            else:
                good[sj] = rootfile
    return good, bad

### Main

if __name__ == '__main__':
    args = parseInput()
    if args.annex: 
        print('NOTE THAT THIS SCRIPT WILL COMMIT AND PUSH ANY CHANGES STAGED FOR COMMIT (not immediately, but after one job is done slimming)\nIt will pull first, too\n')
        os.system('git pull')
    with open(args.histoSpec) as f:
        spec = yml.safe_load(f)
    log = f'{args.outFolder}/production_summary.yml'
    if op.isfile(log):
        with open(log) as f:
            summary = yml.safe_load(f)
    else:
        summary = {}

    # get properties of jobs to be slimmed, and then do the slimming and get job stats
    jobs_to_slim = {}
    props = {'job_id': None, 'expected_subjobs': None, 'outroot_name': None, 'year': None, 'mc_id': None, 'pol': None, 'pdf': None, 'group': None}
    with open(args.batch_skim) as f:
        for line in f.readlines():
            if len(line)==0: continue
            if line[0] == '#': continue # skip comments
            if 'concat_job' in line and (not 'function' in line):
                props['job_id'] = line.split()[1]
                props['expected_subjobs'] = line.split()[2]
                props['outroot_name'] = line.split()[3]
                props['year'] = '2016'
                if ('2017' in props['outroot_name']) or ('Collision17' in props['outroot_name']): props['year'] = '2017'
                if ('2018' in props['outroot_name']) or ('Collision18' in props['outroot_name']): props['year'] = '2018'
                props['pol'] = 'MagDown'
                if 'MagUp' in props['outroot_name']: props['pol'] = 'MagUp'
                props['mc_id'] = props['outroot_name'].split('_')[-2]
                if '--std--' in props['outroot_name']:
                    props['mc_id'] = 'std'
                    pdf, group = 'data', 'data'
                elif '--mu_misid--' in props['outroot_name']:
                    props['mc_id'] = 'fake_mu'
                    pdf, group = 'data', 'data'
                else:
                    pdf, group = pdfFromMCID(props['mc_id'], spec)
                props['pdf'] = pdf
                props['group'] = group
                # make the destination dir
                outdir = f"{args.outFolder}/{props['year']}/{props['group']}/{props['pdf']}-{props['mc_id']}-{props['pol']}"
                os.system(f'mkdir -p {outdir}')
                existing_files = os.listdir(outdir)
                # run the slimming for this job
                os.system(f"../ganga/ganga_skim_job_output.py {outdir} {args.jobFolder}/{props['job_id']} {args.slim_config}")
                # rename contents of this folder to follow Yipeng's naming scheme (slimming script names files using name of folder that holds them, which we've changed)
                added_files = [f for f in os.listdir(outdir) if f not in existing_files]
                for sjf in added_files:
                    suffix = sjf.split('--')[-1]
                    new_name = f"{props['outroot_name'][:-5]}--{suffix}"
                    sub_count = 1
                    while new_name in existing_files: # happens sometimes when re-submitted a job and re-started subjob counter
                        sub_count += 1
                        if not 'j' in suffix: suffix = suffix.replace('-dv', f'j{sub_count}-dv')
                        else: suffix = suffix.replace(f'j{sub_count-1}-dv', f'j{sub_count}-dv')
                        new_name = f"{props['outroot_name'][:-5]}--{suffix}"
                    os.system(f"mv {outdir}/{sjf} {outdir}/{new_name}")
                # get stats and record them
                mode = props['mc_id']
                if mode=='std': mode = 'Data'
                if mode=='fake_mu': mode = 'Fake Mu Data'
                if not mode in summary: summary[mode] = {}
                mode_summary = summary[mode]
                entry = f"{props['year']}-{props['pol']}"
                if not entry in mode_summary: mode_summary[entry] = {}
                job_summary = mode_summary[entry]
                for tree in trees:
                    prod_chain = ROOT.TChain(tree,tree.split('/')[0]+'chain')
                    prod_chain.Add(f'{outdir}/*dv.root') # will just not add anything if tree doesnt exist
                    entries = prod_chain.GetEntries()
                    if entries>0: job_summary[f'{trees[tree]}-entries'] = entries
                good_sjs, bad_sjs = find_good_and_bad_subjobs(f"{args.jobFolder}/{props['job_id']}")
                for badsj in bad_sjs:
                    sjnum = f"{props['job_id']}.{badsj}"
                    if not 'Bad Subjobs (no output)' in job_summary: job_summary['Bad Subjobs (no output)'] = [sjnum]
                    else: job_summary['Bad Subjobs (no output)'].append(sjnum)
                # annex files
                if args.annex:
                    os.system(f"git annex add {outdir}")
                    os.system(f'git commit -m \"Adding step1 slimmed tuples for {props["year"]} {props["pol"]} {props["pdf"]} ({props["mc_id"]})\"')
                    os.system(f'git push')
                    os.system(f'git annex copy --to glacier {outdir}')
                    if socket.gethostbyname(socket.gethostname()) == '10.229.60.85':
                        os.system(f'git annex drop {outdir}') # you can drop these files once copied (if you're working on glacier)!
    # save the summary to the log file
    with open(log, 'w') as f:
        yml.dump(summary,f)

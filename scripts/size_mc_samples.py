#!/usr/bin/env python3
#
# Author: Manuel Franco Sevilla, Yipeng Sun

from re import search
from argparse import ArgumentParser
from subprocess import check_output
from collections import defaultdict


class Colors:
    BOLD = '\033[1m'
    ENDC = '\033[0m'


def parse_input():
    parser = ArgumentParser(
        description='script to count sizes of given MC samples')

    parser.add_argument('-i', '--input',
                        nargs='+',
                        default=['14543010'],
                        help='MC IDs of sample.')

    parser.add_argument('-m', '--mode',
                        default='run',
                        choices=['run', 'year', 'detail'],
                        help='group output')

    parser.add_argument('-o', '--output',
                        default=None,
                        help='specify output csv file.')

    parser.add_argument('-b', '--blocked-kw',
                        nargs='+',
                        default=[],
                        help='specify blocked keywords in LFN.')

    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='enable debug mode.')

    return parser.parse_args()


def decode_dirac_output(output, blocked_kw, debug=False):
    lines = [i for i in output.decode().split('\n') if i]
    result = dict()

    for line in lines:
        if 'DB tags are not set' in line: continue # command seems to print this out now too; ignore it
        lfn, dddb_tag, sim_cond, num_of_files, num_of_evts, unknown = \
            line.split()

        proceed = True
        for kw in blocked_kw:
            if kw in lfn:
                if debug:
                    print('Skip LFN: {} evts in {}'.format(num_of_evts, lfn))
                proceed = False
                break

        if not proceed:
            continue

        if debug:
            print('Use LFN:  {} evts in {}'.format(num_of_evts, lfn))
        result[lfn] = {'dddb_tag': dddb_tag, 'sim_cond': sim_cond,
                       'num_of_files': int(num_of_files),
                       'num_of_evts': int(num_of_evts),
                       'unknown': int(unknown)}

    return result


def sort_dict(dct):
    return {k: dct[k] for k in sorted(dct)}


def search_addon(lfn):
    # Here we see if additional flags like 'TrackerOnly' or 'NoRICHesSim' is
    # present
    addon = lfn.split('/')[3].split('-')[3]
    if not bool(search(r'^Nu\d(\.\d)?$', addon)):
        return addon
    return None


def group_by_year(decoded):
    result = defaultdict(lambda: 0)

    for lfn, attr in decoded.items():
        year = lfn.split('/')[2]
        result[year] += int(attr['num_of_evts'])

    return sort_dict(result)


def group_by_run(decoded):
    result = defaultdict(lambda: 0)

    for lfn, attr in decoded.items():
        year = int(lfn.split('/')[2])

        if year in (2011, 2012):
            result['run 1'] += attr['num_of_evts']
        elif year in (2015, 2016, 2017, 2018):
            result['run 2'] += attr['num_of_evts']

    return sort_dict(result)


def groub_by_detail(decoded):
    result = defaultdict(lambda: 0)

    for lfn, attr in decoded.items():
        year = lfn.split('/')[2]
        pythia = search(r'Pythia\d', lfn).group(0)
        simcond = search(r'Sim\d\d[a-z]', lfn).group(0)
        addon = search_addon(lfn)

        key = '{}-{}-{}'.format(year, pythia, simcond)
        if addon:
            key += '-{}'.format(addon)

        result[key] += attr['num_of_evts']

    return sort_dict(result)


def csv_gen(modes):
    header = ['mode'] + list(list(modes.values())[0].keys())
    rows = [header]

    for mode, attr in modes.items():
        row = [mode]
        row += [str(i) for i in attr.values()]
        rows.append(row)

    return rows


GROUP_OUTPUT_BY = {
    'run': group_by_run,
    'year': group_by_year,
    'detail': groub_by_detail,
}


if __name__ == '__main__':
    args = parse_input()
    print("Before proceed, don't forget to run lhcb-proxy-init!!")

    all_modes = dict()
    for i in args.input:
        dirac_output = check_output(
            ['lb-dirac', 'dirac-bookkeeping-decays-path', i])
        decoded = decode_dirac_output(dirac_output, args.blocked_kw, args.debug)
        grouped = GROUP_OUTPUT_BY[args.mode](decoded)
        all_modes[i] = grouped

        print('For MC ID {}'.format(Colors.BOLD+i+Colors.ENDC))
        for group, num in grouped.items():
            print('  {}: {}'.format(group, Colors.BOLD+f'{int(num):,}'+Colors.ENDC))

    # Optionally generate a CSV output
    if args.output:
        with open(args.output, 'w') as f:
            for row in csv_gen(all_modes):
                f.write(','.join(row)+'\n')

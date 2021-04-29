#!/usr/bin/env python3
#
# Author: Manuel Franco Sevilla, Yipeng Sun

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
                        choices=['run', 'year'],
                        help='group output')

    parser.add_argument('-o', '--output',
                        default=None,
                        help='specify output csv file.')

    return parser.parse_args()


def decode_dirac_output(output):
    lines = [l for l in output.decode().split('\n') if l]
    result = dict()

    for line in lines:
        lfn, dddb_tag, sim_cond, num_of_files, num_of_evts, unknown = \
            line.split()
        result[lfn] = {'dddb_tag': dddb_tag, 'sim_cond': sim_cond,
                       'num_of_files': int(num_of_files),
                       'num_of_evts': int(num_of_evts),
                       'unknown': int(unknown)}

    return result


def sort_dict(dct):
    return {k: dct[k] for k in sorted(dct)}


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


def csv_gen(modes):
    header = ['mode'] + list(list(modes.values())[0].keys())
    rows = [header]

    for mode, attr in modes.items():
        row = [mode]
        row += list(attr.values())
        rows.append(row)

    return rows


GROUP_OUTPUT_BY = {
    'run': group_by_run,
    'year': group_by_year
}


if __name__ == '__main__':
    args = parse_input()
    print("Before proceed, don't forget to run lb-proxy-init!!")

    all_modes = dict()

    for i in args.input:
        dirac_output = check_output(
            ['lb-dirac', 'dirac-bookkeeping-decays-path', i])
        decoded = decode_dirac_output(dirac_output)
        grouped = GROUP_OUTPUT_BY[args.mode](decoded)
        all_modes[i] = grouped

        print('For MC ID {}'.format(Colors.BOLD+i+Colors.ENDC))
        for group, num in grouped.items():
            print('  {}: {}'.format(group, Colors.BOLD+str(num)+Colors.ENDC))

    # Optionally generate a CSV output
    if args.output:
        with open(args.output, 'w') as f:
            for row in csv_gen(all_modes):
                f.write(','.join(row)+'\n')

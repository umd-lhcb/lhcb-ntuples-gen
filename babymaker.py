#!/usr/bin/env python
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jul 01, 2019 at 03:22 PM -0400

import abc
import yaml
import re

from argparse import ArgumentParser
from datetime import datetime


################################
# Comand line arguments parser #
################################

def parse_input():
    parser = ArgumentParser(description='''
generate compilable C++ source file for ntuple processing.''')

    parser.add_argument('-g', '--generator',
                        nargs='?',
                        choices=['PostProcess', 'Compare'],
                        required=True,
                        help='''
choose a C++ code generator.''')

    parser.add_argument('-i', '--input',
                        nargs='?',
                        help='''
path to input YAML file.''')

    parser.add_argument('-o', '--output',
                        nargs='?',
                        required=True,
                        help='''
path to output C++ file.''')

    parser.add_argument('-d', '--datatype',
                        nargs='?',
                        help='''
path to ntuple datatype YAML file.''')

    parser.add_argument('-H', '--headers',
                        nargs='+',
                        default=[],
                        help='''
additional headers to be included in generated C++.''')

    return parser.parse_args()


##########################
# C++ generator template #
##########################

class CppGenerator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse_conf(self, yaml_conf):
        '''
        Parse configuration file for the writer.
        '''

    @abc.abstractmethod
    def write(self, cpp_file):
        '''
        Write generated C++ file to 'cpp_file'.
        '''

    @staticmethod
    def read_yaml(yaml_file):
        '''
        Read ntuple data structure.
        '''
        with open(yaml_file) as f:
            return yaml.safe_load(f)

    @staticmethod
    def match(patterns, string, return_value=True):
        for p in patterns:
            if bool(re.search(p, string)):
                return return_value
        return not return_value

    @staticmethod
    def cpp_gen_date(time_format='%Y-%m-%d %H:%M:%S.%f'):
        return '// Generated on: {}\n'.format(
            datetime.now().strftime(time_format))

    @staticmethod
    def cpp_header(header):
        return '#include <{}>'.format(header)

    @staticmethod
    def cpp_main(definitions, main):
        return '''
{0}

int main(int, char** argv) {{
  {1}
  return 0;
}}
'''.format(definitions, main)


#################################
# C++ generator implementations #
#################################

class PostProcess(CppGenerator):
    input_file = 'input_file'
    output_file = 'output_file'
    headers = ['TFile.h', 'TTree.h', 'TTreeReader.h', 'TBranch.h']

    def __init__(self, yaml_datatype, headers):
        self.raw_datatype = self.read_yaml(yaml_datatype)
        self.headers += headers
        self.output_directive = {}

    def parse_conf(self, yaml_conf):
        conf = self.read_yaml(yaml_conf)

        for output_tree, opts in conf.items():
            self.output_directive[output_tree] = {}
            try:
                self.headers += opts['headers']
            except KeyError:
                pass

            for input_tree in opts['input']:
                if input_tree in self.raw_datatype.keys():
                    self.output_directive[output_tree][input_tree] = []
                    for input_branch, datatype \
                            in self.raw_datatype[input_tree].items():
                        if 'drop' in opts.keys() and self.match(
                                opts['drop'], input_branch):
                            print('Dropping branch: {}'.format(input_branch))

                        elif self.match(opts['keep'], input_branch):
                            directive = {'input_branch': input_branch,
                                         'datatype': datatype}
                            try:
                                directive['output_branch'] = \
                                    opts['rename'][input_branch]
                            except KeyError:
                                directive['output_branch'] = input_branch
                            try:
                                directive['selection'] = \
                                    opts['selection'][input_branch]
                            except KeyError:
                                directive['selection'] = None

                            self.output_directive[output_tree][input_tree].append(directive)

                else:
                    print('Warning: tree {} not found in input file.'.format(
                        input_tree
                    ))

    def write(self, cpp_file):
        filecontent = self.cpp_gen_date()
        filecontent += ('\n').join([self.cpp_header(h)
                                    for h in set(self.headers)]) + '\n'

        definitions = self.cpp_tuple_generators()
        main = self.cpp_main_addon(self.cpp_calls())
        filecontent += self.cpp_main(definitions, main)

        with open(cpp_file, 'w') as f:
            f.write(filecontent)

    def cpp_main_addon(self, calls):
        return '''
TFile *{0} = new TFile(argv[1], "read");
TFile *{1} = new TFile(argv[2], "recreate");

{2}

{1}->Close();

delete {0};
delete {1};
'''.format(self.input_file, self.output_file, calls)

    def cpp_calls(self):
        calls = ''

        for output_tree, input_trees in self.output_directive.items():
            for input_tree in input_trees:
                calls += '{0}_{1}({2}, {3});\n'.format(
                    self.cpp_make_variable(output_tree, prefix='generator_'),
                    self.cpp_make_variable(input_tree),
                    self.input_file,
                    self.output_file
                )

        return calls

    def cpp_tuple_generators(self):
        tuple_generators = ''

        for output_tree, input_trees in self.output_directive.items():
            for input_tree in input_trees:
                tuple_generators += \
                    'void {0}_{1}(TFile *{2}, TFile *{3}) {{\n'.format(
                        self.cpp_make_variable(output_tree,
                                               prefix='generator_'),
                        self.cpp_make_variable(input_tree),
                        self.input_file,
                        self.output_file
                    )
                tuple_generators += self.cpp_variables(output_tree, input_tree)
                tuple_generators += self.cpp_loops(output_tree, input_tree)
                tuple_generators += '{}->Write();'.format(self.output_file)
                tuple_generators += '}\n\n'

        return tuple_generators

    def cpp_variables(self, output_tree, input_tree):
        variables = ''

        variables += 'TTree {0}("{1}", "{1}");\n'.format(
            self.cpp_make_variable(output_tree), output_tree)
        variables += 'TTreeReader {0}("{1}", {2});\n'.format(
            self.cpp_make_variable(input_tree),
            input_tree,
            self.input_file
        ) + '\n'

        for s in self.output_directive[output_tree][input_tree]:
            variables += '{0} {1};\n'.format(
                s['datatype'], self.cpp_make_variable(s['output_branch']))

            variables += '{0}.Branch("{1}", &{2});\n'.format(
                self.cpp_make_variable(output_tree),
                s['output_branch'],
                self.cpp_make_variable(s['output_branch'])
            )

            variables += 'TTreeReaderValue<{0}> {1}({2}, "{3}");\n'.format(
                s['datatype'],
                self.cpp_make_variable(s['input_branch'], suffix='_src'),
                self.cpp_make_variable(input_tree),
                s['input_branch']
            )
            variables += '\n'

        return variables

    def cpp_loops(self, output_tree, input_tree):
        loops = 'while ({0}.Next()) {{\n'.format(
            self.cpp_make_variable(input_tree),
            input_tree,
            self.input_file
        )
        loops += 'if ({}) {{\n'.format(self.cpp_selections(output_tree,
                                                           input_tree))

        for s in self.output_directive[output_tree][input_tree]:
            loops += '{0} = *{1};\n'.format(
                self.cpp_make_variable(s['output_branch']),
                self.cpp_make_variable(s['input_branch'], suffix='_src')
            )

        loops += '{}.Fill();'.format(self.cpp_make_variable(output_tree))
        loops += '}\n}\n'

        return loops

    def cpp_selections(self, output_tree, input_tree):
        selections = ''

        for s in self.output_directive[output_tree][input_tree]:
            if s['selection']:
                selections += '*{0} {1} &&'.format(
                    self.cpp_make_variable(s['input_branch'], suffix='_src'),
                    s['selection']
                )

        return 'true' if selections == '' else selections[:-3]

    @staticmethod
    def cpp_make_variable(string, prefix='', suffix=''):
        return prefix + re.sub('/', '_', string) + suffix


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    if args.generator == 'PostProcess':
        generator = PostProcess(args.datatype, args.headers)

    generator.parse_conf(args.input)
    generator.write(args.output)

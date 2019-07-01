#!/usr/bin/env python
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jul 01, 2019 at 01:23 PM -0400

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
                        required=True,
                        help='''
path to input YAML file.''')

    parser.add_argument('-o', '--output',
                        nargs='?',
                        required=True,
                        help='''
path to output C++ file.''')

    parser.add_argument('-d', '--datatype',
                        nargs='?',
                        required=True,
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
    headers = ['TFile.h', 'TTree.h', 'TTreeReader.h', 'TBranch.h', 'cmath']

    def __init__(self, yaml_datatype, headers):
        self.raw_datatype = self.read_yaml(yaml_datatype)
        self.headers += headers
        self.output_directive = {}

    def parse_conf(self, yaml_conf):
        conf = self.read_yaml(yaml_conf)

        for tree, tree_settings in conf.items():
            self.output_directive[tree] = []
            for input_tree, branche_settings in tree_settings.items():
                if input_tree in self.raw_datatype.keys():
                    for input_branch, datatype \
                            in self.raw_datatype[input_tree].items():
                        if 'drop' in branche_settings.keys() and self.match(
                                branche_settings['drop'], input_branch):
                            print('Dropping branch: {}'.format(input_branch))

                        elif self.match(branche_settings['keep'], input_branch):
                            directive = {
                                'input_tree': input_tree, 'output_tree': tree,
                                'input_branch': input_branch,
                                'datatype': datatype
                            }
                            try:
                                directive['output_branch'] = \
                                    branche_settings['rename'][input_branch]
                            except KeyError:
                                directive['output_branch'] = input_branch
                            try:
                                directive['selection'] = \
                                    branche_settings['selection'][input_branch]
                            except KeyError:
                                directive['selection'] = None

                            self.output_directive[tree].append(directive)

                else:
                    print('Warning: tree {} not found in input file.'.format(
                        input_tree
                    ))

    def write(self, cpp_file):
        filecontent = self.cpp_gen_date()
        filecontent += ('\n').join([self.cpp_header(h) for h in self.headers])
        filecontent += '\n'

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
        return '\n'.join(['{0}({1}, {2});'.format(
            self.cpp_make_variable(t, prefix='generator'),
            self.input_file,
            self.output_file
        ) for t in self.output_directive.keys()])

    def cpp_tuple_generators(self):
        tuple_generators = ''

        for tree in self.output_directive.keys():
            tuple_generators += 'void {0}(TFile *{1}, TFile *{2}) {{\n'.format(
                self.cpp_make_variable(tree, prefix='generator'),
                self.input_file,
                self.output_file
            )
            tuple_generators += self.cpp_variables(tree)
            tuple_generators += self.cpp_loops(tree)
            tuple_generators += '{}->Write();'.format(self.output_file)
            tuple_generators += '}\n\n'

        return tuple_generators

    def cpp_variables(self, tree):
        variables = ''
        tree_readers = []

        input_settings = self.output_directive[tree]
        variables += 'TTree {0}("{1}", "{1}");\n'.format(
            self.cpp_make_variable(tree), tree)

        for s in input_settings:
            if s['input_tree'] not in tree_readers:
                tree_readers.append(s['input_tree'])
                variables += 'TTreeReader {0}("{1}", {2});\n'.format(
                    self.cpp_make_variable(s['input_tree']),
                    s['input_tree'],
                    self.input_file
                )
                variables += '\n'

            variables += '{0} {1};\n'.format(
                s['datatype'], self.cpp_make_variable(s['output_branch']))

            variables += '{0}.Branch("{1}", &{2});\n'.format(
                self.cpp_make_variable(tree),
                s['output_branch'],
                self.cpp_make_variable(s['output_branch'])
            )

            variables += 'TTreeReaderValue<{0}> {1}({2}, "{3}");\n'.format(
                s['datatype'],
                self.cpp_make_variable(s['input_branch'], suffix='_src'),
                self.cpp_make_variable(s['input_tree']),
                s['input_branch']
            )
            variables += '\n'

        return variables

    def cpp_loops(self, tree):
        loops = ''

        input_settings = self.output_directive[tree]
        loops += 'while ({0}.Next()) {{\n'.format(
            self.cpp_make_variable(input_settings[0]['input_tree']),
            input_settings[0]['input_tree'],
            self.input_file
        )
        loops += 'if ({}) {{\n'.format(self.cpp_selections(tree))

        for s in input_settings:

            loops += '{0} = *{1};\n'.format(
                self.cpp_make_variable(s['output_branch']),
                self.cpp_make_variable(s['input_branch'], suffix='_src')
            )

        loops += '{}.Fill();'.format(self.cpp_make_variable(tree))
        loops += '}\n'
        loops += '}\n'

        return loops

    def cpp_selections(self, tree):
        selections = ''

        for s in self.output_directive[tree]:
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

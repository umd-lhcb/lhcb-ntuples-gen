#!/usr/bin/env python
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jul 01, 2019 at 02:43 AM -0400

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
    def cpp_main(body):
        return '''
int main(int, char** argv) {{
  {}
  return 0;
}}
'''.format(body)


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

        loops = self.cpp_tree_handler('Good/stuff', (('P_X', 'Double_t'),
                                                     ('P_Y', 'Int_t')))
        main = self.cpp_main(self.cpp_tfiles(loops))
        filecontent += main

        with open(cpp_file, 'w') as f:
            f.write(filecontent)

    def cpp_tfiles(self, loops):
        return '''
TFile *{0} = new TFile(argv[1], "read");
TFile *{1} = new TFile(argv[2], "recreate");

{2}

delete {0};
delete {1};
'''.format(self.input_file, self.output_file, loops)

    def cpp_tree_handler(self, input_tree, branches):
        reader = self.cpp_tree_variable(input_tree)
        variables = '\n'.join(['TTreeReaderValue<{}> {}({}, "{}");'.format(
            t, b, reader, input_tree) for b, t in branches])

        return '''
TTreeReader {0}("{1}", {2});
{3}

while ({0}.Next()) {{
  {4}
}}
'''.format(reader, input_tree, self.input_file,
           variables, 'loops')

    def cpp_branch_handler(self, output_tree, branch, selection=None):
        if not selection:
            return '''
'''
        else:
            return '''
'''

    @staticmethod
    def cpp_tree_variable(tree):
        return re.sub('/', '_', tree)


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    if args.generator == 'PostProcess':
        generator = PostProcess(args.datatype, args.headers)

    generator.parse_conf(args.input)
    generator.write(args.output)

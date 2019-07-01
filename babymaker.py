#!/usr/bin/env python
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sun Jun 30, 2019 at 09:54 PM -0400

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
                        help='''
choose a C++ code generator.''')

    parser.add_argument('-i', '--input',
                        nargs='?',
                        help='''
path to input YAML file.''')

    parser.add_argument('-o', '--output',
                        nargs='?',
                        help='''
path to output C++ file.''')

    parser.add_argument('-d', '--datatype',
                        nargs='?',
                        help='''
path to ntuple datatype YAML file.''')

    return parser.parse_args()


##########################
# C++ generator template #
##########################

class CppWriter(metaclass=abc.ABCMeta):
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
    def read_ntuple_structure(yaml_ntuple):
        '''
        Read ntuple data structure.
        '''
        with open(yaml_ntuple) as f:
            return yaml.safe_load(f)

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

class PostProcess(CppWriter):
    input_file = 'input_file'
    output_file = 'output_file'

    def __init__(self,
                 include=['TFile.h', 'TTreeReader.h'],
                 drop=[],
                 keep=['*'],
                 rename=[],
                 selection={}
                 ):
        self.include = include
        self.keep = keep
        self.drop = drop
        self.rename = rename
        self.selection = selection

    def parse_conf(self, yaml_conf):
        pass

    def write(self, cpp_file):
        filecontent = self.cpp_gen_date()
        filecontent += ('\n').join([self.cpp_header(h) for h in self.include])
        filecontent += '\n'

        main = self.cpp_main(self.cpp_tfiles(''))
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
        branch_names = [
            'TTreeReaderValue<{}> {};\n'.format(branches[b]['type'], b) for b in
            branches.keys()]
        branch_loops = ''
        return '''
TTreeReader {0}("{1}", {2});
{3}

while ({0}.Next()) {
  {4}
}
'''.format(self.cpp_tree_variable(input_tree), input_tree, self.input_file,
           branch_names, branch_loops)

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

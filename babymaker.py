#!/usr/bin/env python
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sun Jun 30, 2019 at 05:24 PM -0400

import abc
import yaml

from datetime import datetime


################################
# Comand line arguments parser #
################################


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
        return '// Generated on: {}'.format(
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
    def __init__(self,
                 include=['TFile.h', 'TTreeReader.h'],
                 tree_keep=['*'],
                 tree_drop=[],
                 tree_rename=[],
                 branch_drop=[],
                 branch_keep=['*'],
                 branch_rename=[]
                 ):
        self.include = include

    def parse_conf(self, yaml_conf):
        pass

    def write(self, cpp_file):
        filecontent = ('\n').join([self.cpp_header(h) for h in self.include])
        filecontent += '\n'

        main = self.cpp_main(self.cpp_tfiles(''))
        filecontent += main

        with open(cpp_file, 'w') as f:
            f.write(filecontent)

    @staticmethod
    def cpp_tfiles(loops):
        return '''
TFile *input_file = new TFile(argv[1]);
TFile *output_file = new TFile(argv[2]);

{}

delete input_file;
delete input_file;
'''.format(loops)


########
# Main #
########

if __name__ == '__main__':
    generator = PostProcess()
    generator.write('test.cpp')

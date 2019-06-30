#!/usr/bin/env python
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sun Jun 30, 2019 at 01:29 PM -0400

import abc
import yaml


################################
# Comand line arguments parser #
################################


##########################
# C++ generator template #
##########################

class CppWriter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse_conf(yaml_conf):
        '''
        Parse configuration file for the writer.
        '''

    @abc.abstractmethod
    def write(cpp_file):
        '''
        Write generated C++ file to 'cpp_file'.
        '''

    def read_ntuple_structure(yaml_ntuple):
        '''
        Read ntuple data structure.
        '''
        with open(yaml_ntuple) as f:
            return yaml.safe_load(f)

    @staticmethod
    def cpp_gen_date(strpformat):
        return 0

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

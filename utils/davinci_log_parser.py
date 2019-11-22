#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Nov 20, 2019 at 02:43 AM -0500

import re
import sys

from collections import OrderedDict as odict
from abc import ABC, abstractmethod


##############
# Data store #
##############
# Store info (total num. of input, num. of events after each cut, etc.) for each
# selection.

class Selection(object):
    def __init__(self, selection):
        self.selection = selection

        self.headers = None
        self.result = dict()

    def parse_headers(self, headers_line):
        self.headers = self.split_entries(headers_line)

    def parse_counter(self, counter_line):
        entries = self.split_entries(counter_line)
        counter_name = entries[0]
        counter_vals = {k: v for k, v in zip(self.headers[1:], entries[1:])}
        self.result[counter_name] = counter_vals

    @staticmethod
    def split_entries(line, splitter='|'):
        entries = line.split(splitter)
        return [i for i in map(lambda x: x.strip(), entries) if i != '']


#################
# State machine #
#################
# For parsing.

class State(ABC):
    @abstractmethod
    def run(self, data):
        '''
        Action on current data.
        '''

    @abstractmethod
    def next(self, data):
        '''
        Determine next state
        '''


class StateMachine(ABC):
    def __init__(self, filename, init_state):
        self.filename = filename
        self.init_state = init_state
        self.current_state = init_state

    def run_all(self):
        with open(self.filename) as f:
            for line in f:
                data = self.data(line)
                self.current_state = self.current_state.next(data)
                self.current_state.run(data)

    @abstractmethod
    def data(self, raw_data):
        '''
        Pack data for each state to consume.
        '''


##########
# Parser #
##########

class DaVinciLogParser(StateMachine):
    def __init__(self, *args):
        super().__init__(*args)

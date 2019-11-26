#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Nov 25, 2019 at 10:48 PM -0500

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

# NOTE: This should be used as a metaclass only.
class State(type):
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kw)
        return cls.instance

    def run(self, data):
        '''
        Action on current data.
        '''
        raise NotImplementedError

    def next(self, data):
        '''
        Determine next state
        '''
        raise NotImplementedError


class StateMachine(ABC):
    def __init__(self, filename, init_state):
        self.filename = filename
        self.current_state = init_state

    def run_all(self):
        with open(self.filename) as f:
            for line in f:
                data = self.data(line)
                # We create states on the fly, because we want 'state.next' to
                # be able to return arbitrary name, not just some already
                # defined state.
                #
                # Note that 'state' should be a singleton to avoid recreating.
                # As long as the 'state' uses State (defined above) as its
                # metaclass, averting should be fine.
                self.current_state = globals()[self.current_state.next(data)]()

    @abstractmethod
    def data(self, raw_data):
        '''
        Pack data for each state to consume.
        '''


##########
# Parser #
##########

class DaVinciLogInit(metaclass=State):
    def next(self, data):
        line, parsed = data
        total_num = self.find_total_num_of_event(line)

        if total_num:
            parsed['Total'] = total_num
            return 'DaVinciSelInit'
        else:
            return 'DaVinciLogInit'

    def find_total_num_of_event(self, line):
        result = re.match(r'DaVinciInitAlg    SUCCESS (\d+) events processed',
                          line)
        if result:
            return result.group(1)


class DaVinciSelInit(metaclass=State):
    def next(self, data):
        return 'DaVinciSelInit'


class DaVinciLogParser(StateMachine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parsed = {}

    def data(self, line):
        return (line, self.parsed)


if __name__ == '__main__':
    filename = sys.argv[1]
    parser = DaVinciLogParser(filename, DaVinciLogInit())
    parser.run_all()
    print(parser.parsed)

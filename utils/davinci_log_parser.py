#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Nov 22, 2019 at 03:21 AM -0500

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
                self.current_state.run(data)

    @abstractmethod
    def data(self, raw_data):
        '''
        Pack data for each state to consume.
        '''


##########
# Parser #
##########

class DaVinciLogInit(metaclass=State):
    def run(self, data):
        data

    def next(self, data):
        return 'somenextstate'


class DaVinciLogParser(StateMachine):
    def __init__(self, *args):
        super().__init__(*args)

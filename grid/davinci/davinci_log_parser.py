#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Nov 19, 2019 at 05:28 PM -0500

import re
import sys


###########
# Parsing #
###########

READ_HEADER = -1
TERMINATE = 0


class Selection(object):
    def __init__(self, selection):
        self.selection = selection

        self.counter = READ_HEADER
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


class DaVinciLogParser(object):
    def __init__(self, file):
        self.file = file
        self.result = dict()

    def parse(self):
        pass

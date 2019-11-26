#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Nov 26, 2019 at 03:28 AM -0500

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
    def __init__(self, selection, headers_to_keep=['#', 'sum']):
        self.selection = selection
        self.headers_to_keep = headers_to_keep

        self.headers = None
        self.result = odict()

    def parse_headers(self, headers_line):
        self.headers = self.split_entries(headers_line)

    def parse_counter(self, counter_line):
        entries = self.split_entries(counter_line)
        counter_name = self.regularize_name(entries[0])
        counter_vals = {k: v for k, v in zip(self.headers[1:], entries[1:])}
        counter_vals = {self.regularize_counter(k): self.int_or_float(v)
                        for k, v in counter_vals.items()
                        if k in self.headers_to_keep}
        self.result[counter_name] = counter_vals

    @staticmethod
    def regularize_name(name):
        if name.startswith('*'):
            return name[1:]
        elif name.startswith('"') and not name.endswith('"'):
            return name+'"'
        elif name.endswith(' "'):
            return name[:-2]+'"'
        else:
            return name

    @staticmethod
    def regularize_counter(key):
        return 'tot' if key == '#' else key

    @staticmethod
    def int_or_float(n):
        try:
            return int(n)
        except ValueError:
            return float(n)

    @staticmethod
    def split_entries(line, splitter='|'):
        entries = line.split(splitter)
        return [i for i in map(lambda x: x.strip(), entries) if i != '']


#################
# State machine #
#################
# For parsing.

# NOTE: This should be used as a metaclass only.
class StateSingleton(type):
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kw)
        return cls.instance

    def next(self, data):
        '''
        Determine next state after performing action on current data.
        '''
        raise NotImplementedError


class State(ABC):
    @abstractmethod
    def next(self, data):
        '''
        Determine next state after performing action on current data.
        '''


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
                state, args = self.current_state.next(data)
                self.current_state = globals()[state](*args)

    @abstractmethod
    def data(self, raw_data):
        '''
        Pack data for each state to consume.
        '''


##########
# Parser #
##########

class DaVinciLogInit(metaclass=StateSingleton):
    def next(self, data):
        line, parsed = data
        total_num = self.find_total_num_of_event(line)
        if total_num:
            parsed['Total'] = total_num
            return ('DaVinciSelInit', ())
        else:
            return ('DaVinciLogInit', ())

    def find_total_num_of_event(self, line):
        result = re.match(r'DaVinciInitAlg    SUCCESS (\d+) events processed',
                          line)
        if result:
            return int(result.group(1))


class DaVinciSelInit(metaclass=StateSingleton):
    def next(self, data):
        line, _ = data
        try:
            name, counter = self.find_selection_name_and_counter(line)
            return ('DaVinciSelHeaders', (name, counter))
        except TypeError:
            return ('DaVinciSelInit', ())

    def find_selection_name_and_counter(self, line):
        result = re.match(r'([\w\.]+)\s*SUCCESS Number of counters : (\d+)',
                          line)
        if result:
            return (result.group(1), int(result.group(2)))


class DaVinciSelHeaders(State):
    def __init__(self, name, counter):
        self.name = name
        self.counter = counter

    def next(self, data):
        line, _ = data
        selection = Selection(self.name)
        selection.parse_headers(line)
        return ('DaVinciSelCounter', (selection, self.counter))


class DaVinciSelCounter(State):
    def __init__(self, selection, counter):
        self.selection = selection
        self.counter = counter

    def next(self, data):
        line, parsed = data
        if self.counter > 0:
            self.counter -= 1
            self.selection.parse_counter(line)
            return ('DaVinciSelCounter', (self.selection, self.counter))
        else:
            parsed[self.selection.selection] = self.selection.result
            return ('DaVinciSelInit', ())


class DaVinciLogParser(StateMachine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parsed = odict()

    def data(self, line):
        return (line, self.parsed)


##########
# Output #
##########

def yaml_gen(data, indent='', indent_increment=' '*4):
    result = ''
    for key, items in data.items():
        result += '{}{}:'.format(indent, key)
        if type(items) in [dict, odict]:
            result += '\n'
            result += yaml_gen(items, indent=indent+indent_increment)
        else:
            result += ' {}\n'.format(items)
    return result


def update_dict(orig, new):
    for key, items in new.items():
        if type(items) in [dict, odict]:
            try:
                update_dict(orig[key], items)
            except KeyError:
                orig[key] = items
        else:
            try:
                orig[key] += items
            except KeyError:
                orig[key] = items


if __name__ == '__main__':
    output = sys.argv[1]
    result = odict()

    for log_filename in sys.argv[2:]:
        parser = DaVinciLogParser(log_filename, DaVinciLogInit())
        parser.run_all()
        update_dict(result, parser.parsed)

    with open(output, 'w') as f:
        f.write(yaml_gen(result))

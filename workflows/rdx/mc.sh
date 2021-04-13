#!/usr/bin/env bash
#Author: Yipeng Sun
#License: GPLv2
#Last Change: Tue Apr 13, 2021 at 02:48 AM +0200

INPUT_NTP=$1

# Hlt1 emulation
run2-rdx-hlt1.py ${INPUT_NTP} emu_hlt1_b0.root -t TupleB0/DecayTree -B b0
run2-rdx-hlt1.py ${INPUT_NTP} emu_hlt1_b.root -t TupleBminus/DecayTree -B b

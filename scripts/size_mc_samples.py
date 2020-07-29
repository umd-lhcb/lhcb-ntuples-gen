#!/usr/bin/env python3

###### Script to count 
import os, sys, subprocess
import glob
import string
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("-i", "--input", help="MC ID of sample", default="14543010")
args = parser.parse_args()

class bcolors:
    BOLD = '\033[1m'
    ENDC = '\033[0m'

output = subprocess.check_output(['lb-run','lhcbdirac', 'dirac-bookkeeping-decays-path', args.input])

nrun1 = 0
nrun2 = 0
lines = output.decode().replace('\n','').replace(',', '').replace('(', '').replace("'", '').split(')')
for line in lines:
    splits = line.split(' ')
    if(len(splits) > 2):
        nevents = int(splits[-2])
        sample = splits[0]
        print(f'{nevents:12,d}' + '   ' + sample)
        if('2015' in sample or '2016' in sample or '2017' in sample or '2018' in sample): nrun2 += nevents
        else: nrun1 += nevents


print('\n Total number of events for MC ID '+args.input+' in Run 1 is '+bcolors.BOLD+f'{nrun1:,d}'+bcolors.ENDC+' and in Run 2 is '+bcolors.BOLD+f'{nrun2:,d}'+bcolors.ENDC+'\n')




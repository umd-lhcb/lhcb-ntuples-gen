#!/usr/bin/env python3
# Author: Alex Fernez

# create soft links from all annexed files in ../ntuples that are physically located on glacier to their glacier location so that tuples don't have to be
# stored multiple times on glacier
# this script is just for ntuples in lhcb-ntuples-gen, but of course it can easily be used for other repos
# by default, don't update existing links unless flag below is changed

import os
import os.path as op
import socket

update_existing_links = False

def create_glacier_links(ntuples, storage): # glacier_links will be a folder inside ntuples with same directory structure as ntuples
    annexed_ntuples = {} # dict from abs path of an annexed tuple inside ntuples to the abs path of the tuple inside this repo's .git/annex/objects
    print(f'Finding locations of all annexed root files in {ntuples}...\n')
    for root,_,files in os.walk(ntuples):
        if 'glacier_links' in root: continue # don't look at the already created links, of course
        for f in files:
            if f[-5:]=='.root': # I explictly only care about root files
                tuple_path = op.abspath(op.join(root,f))
                if op.islink(tuple_path): annexed_ntuples[tuple_path] = op.realpath(tuple_path)
    storage_ntuples = {} # dict from annex keys to abs path of file in glacier lhcb-ntuples-gen annex/objects
    print(f'Finding locations of all annexed root files stored on glacier at {storage} (note: if this step takes more than a few seconds, likely some files at this location dont have correct access, and someone needs to sudo -R chmod +rx)...\n')
    for root,_,files in os.walk(storage):
        for f in files: # note: annex storage will name file containing actual object with '.root' in the name too, but it will be a directory, so it won't show up in files
            if f[-5:]=='.root': # I explictly only care about root files
                tuple_path = op.abspath(op.join(root,f))
                annexKey = tuple_path.split('/')[-1]
                storage_ntuples[annexKey] = tuple_path
    print(f'Going through list of annexed root files, and if link not already created (or user wants to update all), creating link...\n')
    for ntp in annexed_ntuples:
        link = ntp.replace('/ntuples/', '/ntuples/glacier_links/')
        if update_existing_links or (not op.islink(link)):
            annexKey = annexed_ntuples[ntp].split("/")[-1]
            if not annexKey in storage_ntuples:
                print(f'Could not find {annexKey} for {ntp} in {storage}, maybe not copied correctly (eg. maybe only copied to julian, or otherwise never transferred to glacier)? Skipping')
            else:
                os.system(f'mkdir -p {"/".join(link.split("/")[:-1])}')
                os.system(f'ln -s {storage_ntuples[annexKey]} {link}')


if socket.gethostbyname(socket.gethostname()) == '10.229.60.85': # glacier IP
    annex_path_glacier = '/home/git/repositories/lhcb-ntuples-gen.git/annex/objects'
    create_glacier_links('../ntuples', annex_path_glacier)
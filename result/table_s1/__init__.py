# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_weinberg}.
#*************************************************************************
import os
import json
import pickle
from ipdb import set_trace
from os.path import dirname, join, exists
import sbie_weinberg

__all__ = []


def get_config():
    return config


def get_workdir():
    return join(dirname(__file__))


def get_savedir():
    savedir = join(dirname(__file__), 'dataset')
    if not exists(savedir):
        os.makedirs(savedir)

    return savedir

def load_table(cid):
    if cid == 'd':
        with open(config['tables'][cid], 'r') as f:
            dict_data = json.load(f)

        return dict_data

    elif cid == 'e':
        with open(config['tables'][cid], 'rb') as f:
            dict_data = pickle.load(f, encoding='utf-8')

        return dict_data

    elif cid == 'h':
        with open(config['tables'][cid], 'r') as f:
            dict_data = json.load(f)

        return dict_data

    elif cid == 'i':
        with open(config['tables'][cid], 'rb') as f:
            dict_data = pickle.load(f, encoding='utf-8')

        return dict_data

    else:
        assert False

config = {
    'parameters': {
        },
    'tables': {
        'a': join(get_savedir(), 'Table-S1A-Fumia-processed.csv'),
        'b': join(get_savedir(), 'Table-S1B-Fumia-regulation-network.csv'),
        # for normal cell
        'c': join(get_savedir(), 'Table-S1C-Input-combinations.json'),
        'd': join(get_savedir(), 'Table-S1D-Scanning-results.json'),
        'e': join(get_savedir(), 'Table-S1E-Clustering.p'),
        'f': join(get_savedir(), 'Table-S1F-Scanning-results-with-class.json'),
        # for APC-mutated cell
        'g': join(get_savedir(), 'Table-S1G-Input-combinations-APC.json'),
        'h': join(get_savedir(), 'Table-S1H-Scanning-results-APC.json'),
        'i': join(get_savedir(), 'Table-S1I-Clustering-APC.p'),
        'j': join(get_savedir(), 'Table-S1J-Scanning-results-with-class-APC.json'),
        }
    }
